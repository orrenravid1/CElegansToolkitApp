import asyncio
import platform
import time
from multiprocessing import Process, Pipe, set_start_method
import socketio
from aiohttp import web
import json
from compneurovis.neuronutils.swc_utils import load_swc_multi
import os
import random
import numpy as np


# ─── Helper functions for NEURON logic ─────────────────────────────────────

def load_swc_model(swc_path):
    """Import an SWC file into NEURON and return the list of sections."""
    from neuron import h
    swc_files = [f for f in os.listdir(swc_path) if f.endswith('.swc')]
    secs = []
    for i,swcf in enumerate(swc_files):
        print(f"Loading cell {swcf}")
        cell_name = swcf.split('.')[0]
        trees = load_swc_multi(os.path.join(swc_path, swcf), cell_name)
        seclists = trees.values()
        for seclist in seclists:
            for sec in seclist:
                secs.append(sec)
    for sec in secs:
        if not "soma" in sec.name():
            sec.nseg = 5
        sec.insert('hh')
    return secs

def send_ready(conn):
    """Tell parent that worker is ready."""
    conn.send({"type": "ready", "info": "SWC model loaded and NEURON ready."})

def handle_stop(conn):
    """Cleanly acknowledge a stop command."""
    conn.send({"type": "status", "status": "stopping"})

def handle_get_morphology(conn, sections):
    """Extract 3D points and diameters from each section and send them."""
    try:
        morphology = []
        from neuron import h
        for sec in sections:
            pts = []
            for i in range(int(sec.n3d())):
                pts.append({
                    "id":   i,
                    "x":    sec.x3d(i),
                    "y":    sec.y3d(i),
                    "z":    sec.z3d(i),
                    "d":    sec.diam3d(i)
                })
            morphology.append({
                "name": sec.name(),
                "pts":  pts
            })
            
            print(len(morphology))
        conn.send({"type": "morphology", "data": json.dumps(morphology)})
    except Exception as e:
        conn.send({"type": "error", "message": str(e)})

def handle_simulation(conn, sections, cmd):
    """Run a brief NEURON simulation and send back a sample voltage."""
    try:
        from neuron import h
        h.load_file('stdrun.hoc')
        
        somas = [sec for sec in sections if 'soma' in sec.name().lower()]
        # WARNING: Need to store iclamps outside of this method i.e. via self otherwise they will
        # be garbage collected
        iclamps = []
        tvecs = []
        ivecs = []

        duration = 10000
        amp = 0.2
        period = 30
        for soma in somas:
            phase = random.random()*2*np.pi*period
            icl = h.IClamp(soma(0.5))
            icl.delay = 2
            icl.amp = amp
            icl.dur = duration
            t_vec = h.Vector(np.arange(0, duration, 0.1))
            i_vec = h.Vector(amp * (np.sin(np.pi * t_vec / period + phase)))
            i_vec.play(icl._ref_amp, t_vec, 1)
            tvecs.append(t_vec)
            ivecs.append(i_vec)
            iclamps.append(icl)

        h.finitialize(-65)
        h.dt = 0.25
        t = 0
        last_sent_t = 0
        thresh = 5
        while t < duration:
            print("t =", t)
            time.sleep(0.001)
            h.fadvance()
            t = h.t
            conn.send({
                "type":    "simulation",
                "command": cmd,
                # TODO: Do voltages per segment when we create morphology per segment
                "voltages": [sec.v for sec in sections],
                "sections": [sec.name() for sec in sections]
            })
            ##last_sent_t = t

        # after sending all voltages, send a final status
        conn.send({"type": "status", "status": "simulation_complete"})
    except Exception as e:
        conn.send({"type": "error", "message": str(e)})

# ─── The worker subprocess loop ────────────────────────────────────────────

def neuron_worker(conn):
    # Get the absolute path of the current script file
    script_path = os.path.abspath(__file__)
    # Get the directory of the script file
    script_directory = os.path.dirname(script_path)

    sections = load_swc_model(os.path.join(script_directory, "celegans_swc"))
    send_ready(conn)

    try:
        while True:
            if conn.poll(0.1):
                cmd_dict = conn.recv()
                cmd = cmd_dict.get("command")
                if cmd == "stop":
                    handle_stop(conn)
                    break
                elif cmd == "get_morphology":
                    handle_get_morphology(conn, sections)
                else:
                    handle_simulation(conn, sections, cmd)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

# --- Socket.IO + aiohttp setup ---

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

# Shared state
app["pipe"]        = None
app["process"]     = None
app["ready"]       = False
app["ready_info"]  = None
app["client_sids"] = set()

@sio.event
async def connect(sid, environ):
    app["client_sids"].add(sid)
    if app["ready"]:
        await sio.emit("neuron_result", {"type":"ready", "info": app["ready_info"]}, to=sid)
    print(f"[Server] Client connected: {sid}")

@sio.event
async def disconnect(sid):
    app["client_sids"].discard(sid)
    print(f"[Server] Client disconnected: {sid}")

@sio.event
async def neuron_command(sid, data):
    parent_conn = app["pipe"]
    cmd = data.get("command")
    parent_conn.send(data)

    if cmd == "simulation":
        # Stream every simulation message until we see a non-“simulation” type
        while True:
            # small sleep to avoid busy-spin
            await asyncio.sleep(0.05)
            if parent_conn.poll():
                resp = parent_conn.recv()
                await sio.emit("neuron_result", resp, to=sid)
                if resp.get("type") not in ("simulation",):
                    break
    else:
        # one-shot commands (get_morphology, stop, ready, etc.)
        for _ in range(50):
            await asyncio.sleep(0.1)
            if parent_conn.poll():
                resp = parent_conn.recv()
                await sio.emit("neuron_result", resp, to=sid)
                return
        await sio.emit("neuron_result", {"type":"error","message":"timeout waiting for worker"}, to=sid)

async def on_startup(app):
    if platform.system() == "Windows":
        try: set_start_method("spawn")
        except RuntimeError: pass

    parent_conn, child_conn = Pipe()
    app["pipe"]    = parent_conn
    p = Process(target=neuron_worker, args=(child_conn,), daemon=False)
    p.start()
    app["process"] = p

    # Wait for the initial ready handshake
    start = time.monotonic()
    while time.monotonic() - start < 5:
        if parent_conn.poll(0.1):
            msg = parent_conn.recv()
            if msg.get("type") == "ready":
                app["ready"]      = True
                app["ready_info"] = msg["info"]
                print(f"[Server] Worker ready: {msg['info']}")
                break
    else:
        app["ready_info"] = "Worker failed to signal ready"
        print("[Server] " + app["ready_info"])

async def on_shutdown(app):
    for sid in list(app["client_sids"]):
        try: await sio.disconnect(sid)
        except: pass

    parent_conn = app["pipe"]
    proc        = app["process"]
    if proc and proc.is_alive():
        try: parent_conn.send({"command": "stop"})
        except: pass
        proc.join(2)
        if proc.is_alive():
            proc.terminate()

    try: parent_conn.close()
    except: pass

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    port = 5001
    print(f"Starting NEURON API server on http://localhost:{port}")
    web.run_app(app, port=port, shutdown_timeout=1)
