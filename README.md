# CElegansToolkitApp
A repository to host the executable application of the C elegans toolkit

<img width="572" height="571" alt="CompZoologyCover" src="https://github.com/user-attachments/assets/088dfc16-6e1e-4916-a0a1-f240b8d11cf8" />

## About

The C. elegans Toolkit consists of 3 parts:

1. The Anatomy and Data Viewer  
2. The Simulation Tool  
3. An LLM UI (in my local version, fine tuned for C. elegans-related queries)

---

## Installation Instructions

You can either download or clone this repository. The app can be run in `build/NeuronUnity.exe` with a few caveats:

- The app is currently compiled and accessible only for Windows.
- It is also currently in a proof of concept state. Bugs are to be expected.
- Check the [General Information](#general-information) section below before beginning.  
- The LLM UI will not be functional out of the box. See more info in the [LLM UI Section](#3-llm-ui).  
- The live network simulation viewer will not be functional out of the box. See more info in the [Simulation Tool section](#2-simulation-tool).

---

## General Information

1. At any point, to **Quit**, you currently need to press `Alt-F4`. This version of the toolkit was developed for a public demo stand and thus exiting the app was not made easily accessible.  
2. The **Login Screen** currently acts as a placeholder. Any input entered, including empty, will be fine to enter the demo. You can simply click the **Login** button.

### General Controls
<img width="2559" height="1439" alt="image" src="https://github.com/user-attachments/assets/a41a0754-3f6c-4796-a3dd-a226af9ce47e" />

In both the Anatomy View and the Simulation View, the following controls are always valid:

a. **Chat**  
- You can always click this to open a chat panel and interface with an LLM.  
- In the future this model would be able to engage with the platform and help you with specific tasks related to the toolkit.  
- Currently, it has no access to the platform objects and is just there as a proof-of-concept. See more in the [LLM UI Section](#3-llm-ui).

b. **Menu**  
- You can use it to switch between the anatomy and simulation tools in the toolkit.  
- You can also use it to return to the login screen.

Any **Open Panel** can either be closed by **clicking the panel button again** or pressing the **Red Button**.

Controls:

| Action          | Control                     | Description                                                |
| --------------- | --------------------------- | ---------------------------------------------------------- |
| Move            | WASD                        | Move the camera around forwards, backwards, left, or right |
| Accelerate      | Shift (while pressing WASD) | Accelerate in the movement direction                       |
| Rotate          | Right Mouse Drag            | Look around with the camera                                |
| Select/Deselect | Left Click                  | Select/Deselect buttons and sliders                        |

---

## 1. Anatomy and Data Viewer
<img width="2558" height="1438" alt="image" src="https://github.com/user-attachments/assets/27a9b582-fd74-4aba-b41d-d26bd657dca6" />


The Anatomy and Data Viewer was developed to demonstrate the value of embedding and viewing known data in context of the anatomy of the organism (in this case C. elegans).

### Controls

a. **Visibility Panel**  
- Sliders to vary the opacity of various layers of the anatomy.  
- A toggle to hide all unselected neurons.

b. **System Selection Panel**  
- A panel to select certain neural systems.

c. **Reset View**  
- Resets the camera view to the starting view.

d. **Info Panel**  
- Presents info for the currently selected neuron.  
- Presents info for the currently selected neural system.

Extra Controls:

| Action                 | Control      | Description                                |
| ---------------------- | ------------ | ------------------------------------------ |
| Select/Deselect Neuron | Left Click   | Select/Deselect a neuron in the connectome |
| Zoom                   | Scroll Wheel | Zoom the camera in and out                 |

### Usage

- Move around and pick a region of the connectome you are interested in.  
- Click on a neuron to see information on it (**NOTE:** Descriptions leveraged AI for placeholder but relevant text).  
- Use the **System Selection Panel** to select a neural system to look at. Select individual neurons in the neural system to learn about them.  
- Use the **Visibility Panel** to show/hide various parts of the anatomy to see them in context with the neural system. Hide all other neurons to see the system alone.

---

### Developer Information

The Anatomy and Data Viewer is broken down into 4 pieces:

1. 3D Anatomy  
2. 3D Connectome Navigation  
3. Single Neuron Data Selection  
4. Neural System Data Selection  

#### 1. 3D Anatomy

- The 3D anatomy is taken from the Blender model found [here](http://caltech.wormbase.org/virtualworm/).  
- The model was then updated to store various groups of the anatomy to display as layers.

##### Future Goals

- Extend the selection capabilities to the anatomy itself so that any component can be selected. This will also improve the extensiveness of the data that can be represented.  
- Visualize the relationships between certain anatomical parts and the connectome to better see how they relate.

#### 2. 3D Connectome Navigation

- The connectome uses **SWC** files generated from the detailed NeuroML model of the connectome in the [c302 repository](https://github.com/openworm/c302).  
- The models are ball-and-stick where individual sections from the SWC file are represented as individual components. Each is 1-1 with the morphology found in the [Network Activity Viewer](#2-neuron-simulation-and-live-network-activity-viewer) in the [Simulation Tool](2-simulation-tool).

##### Future Goals

- Allow for more granular selection of neurons down to the section so that more granular data can be investigated.  
- Create a mode for a reduced point neuron connectome view so that a simplified view for different connectome data sets can be used.  
- Create a search functionality for finding neurons and systems.

#### 3. Single Neuron Data Selection

- The single neuron data currently uses AI generated placeholder data based on WormAtlas's data.  
- Under the hood, however, are many of OpenWorm's, WormBook's, and WormAtlas's datasets:  
  - OpenWorm via [owmeta](https://github.com/openworm/owmeta) are datasets on ion channels, neurotransmitters, receptors.  
  - Other sources from OpenWorm have connectome data.  
  - Textual corpora on various classes of neuron from WormBook and WormAtlas.  
  - Genomic data taken from WormBase.

##### Future Goals

- Allow for exposing many of the aforementioned data sources:  
  - Create tabs for different kinds of data.  
  - Create links so that you can learn about different ion channels, receptors, etc. if they are present in a certain neuron.  
- Allow for viewing/editing model parameters of different neurons in formats like NeuroML.

#### 4. Neural System Data Selection

- The neural system data currently uses AI generated placeholder data based on WormAtlas's data.  
- It also currently has hardcoded neural systems defined as collections of the single neurons. However, the data schema is shared and built hierarchically.

##### Future Goals

- Allow for arbitrary definition of neural systems and color coding by allowing multiselect of neurons and grouping them.  
- Create a way to search through all the neurons that are part of a neural system.  
- Allow for selecting anatomy parts as well as neurons as part of the system (e.g. muscles for the motor system).

---

## 2. Simulation Tool
<img width="2558" height="1439" alt="image" src="https://github.com/user-attachments/assets/8dbd4120-95b9-4dfd-93ea-e6ad04b7b3d7" />


The Simulation Tool demonstrates a closed loop simulation environment with the biomechanical model of C. elegans in a simulated environment and a biophysical model of its nervous system.

### Controls

a. **Control Sliders**  
- Sliders to vary predefined simulation parameters.  
- Changes will influence the simulation in real time.

b. **Nervous System Viewer**  
- A panel to view the live simulated compartmental model of the nervous system in 3D.
- **NOTE**: This panel requires a substantial amount of extra setup in order to work. Setup is described in [Section 2](#local-setup-for-use-in-the-platform) of the developer information below.
- **Right Click**: Rotates the 3D model of the nervous system.  
- **Scroll Wheel**: Grows and shrinks the panel.  
- **Left Click (Inside Panel Sphere)**: Closes the panel.  

c. **Analysis Panel**  
- Click on each of the toggles to open up certain plots.  
- Plots can be moved by dragging the panel.  
- Plots can be closed by clicking the toggle again.

Extra Controls:

| Action       | Control      | Description                  |
| ------------ | ------------ | ---------------------------- |
| Move Up/Down | Scroll Wheel | Moves the camera up and down |

### Usage

- Follow the worm as it navigates around salt particles and feeds on bacterial lawns.  
- Use the **Control Sliders** to modulate the systems described in the **Anatomy Viewer**:  
  - The top two sliders manipulate the balance of excitation and inhibition in the motor system.  
  - The middle two sliders manipulate the food seeking behavior.  
  - The bottom two sliders manipulate the neurons responsible for salt sensitivity.  
- Use the **Analysis Panel** to view the systems described in the Anatomy Viewer as you modulate them:  
  - Manipulate the control sliders for each system and watch the corresponding plots change in tandem with the worm's behavior.  
- Use the **Nervous System Viewer** to view the time evolution of voltage in the nervous system in real time.

---

### Developer Information

The Simulation Tool consists of 4 aspects:

1. C. elegans biomechanical simulation  
2. NEURON simulation and live network activity viewer  
3. Control sliders  
4. Live plotting tools  

### 1. C. elegans Biomechanical Simulation

#### Body Plan

- The C. elegans muscles and body are implemented in close similarity to how it is described in [this paper](https://www.mdpi.com/2227-7390/11/11/2442).  
  - The body is segmented into 25 rigid capsules of varying size and mass.  
  - Each segment is connected to the next via 4 springs each representing DL, DR, VL, VR respectively.

#### Motion

- While the C. elegans biomechanical simulation can be driven by arbitrary stimuli, including the NEURON simulation running in the backend, for the purposes of the proof of concept it was implemented in the following ways:  
  - Sinusoidal pulse generator to create the general motion of the body.  
  - A mass following biased Brownian motion attached to the head, which was made to detect and follow or avoid the stimuli present in the scene: the **food** (bacteria) and the **salt**.  
- The reasons for forgoing the NEURON simulation approach is simply that "solving" the C. elegans motor system in a way that maps from a biophysical simulation with morphologically detailed compartmental neuron models to muscle activity to create the correct body motion is still an open problem. A recent approach can be seen in [this paper](https://www.nature.com/articles/s43588-024-00738-w).

#### Future Goals

1. There is technically a softbody simulation version hiding in the codebase. I would like to see if that adds any value to simulation fidelity over an arbitrarily segmented body.  
   - There are limitations to the collision fidelity of the capsules, namely that they pretty much cannot be wider than they are tall and so the lower bound on their dimensions height-wise is effectively a sphere.  
   - A softbody simulation would allow for vertex-scale collision detection, useful for both improved physics simulations and collision sensors for feedback to the network.  
2. The environment does not currently incorporate any notions of buoyancy or fluids and viscosity. This would be a crucial component for mimicking the environment C. elegans maneuvers in normally and would likely improve the body's ability to move through it when following a sinusoidal pattern.

### 2. NEURON Simulation and Live Network Activity Viewer

#### How It Works

The simulation communicates with Python live via a Socket.IO server-client structure:

1. The simulation spawns a Python process running the script found in  
   `build\NeuronUnity_Data\StreamingAssets\Scripts\Python\celeganssocketio.py`.  
2. That script spawns a [Socket.IO](https://socket.io/) server running on a local port.  
3. That server is running NEURON internally and is able to load data and run NEURON code on demand.  
4. On the Unity app side, a parallel Socket.IO client is running connected to the same local port.  
5. The Unity app client then communicates bidirectionally with the server, with the server providing data on the network morphology and activity.  
6. The Unity app then visualizes this data with native geometry and materials.

#### Local Setup for Use in the Platform

Unfortunately, the current setup depends on your global Python installation. This means that you will need to install packages directly to your global Python environment and a virtual environment (venv) solution is not possible. This is the most challenging step and can also be ignored for many users not interested in this part of the platform.

However, if you want to have this piece functional, you will need to:

1. Ensure you have Python 3.11+.  
2. Install NEURON to your global Python installation.  
3. Download this repository: <https://github.com/orrenravid1/CompartmentalNeuronGUI> and follow the installation instructions there.  
4. Install all remaining requirements from the `requirements.txt` file in this repository via the pip command:  
   `pip install -r requirements.txt` in the root of this repository.

#### Future Goals

1. Obviously, the requirements to get this part working are the most demanding and not particularly user friendly. Other architectures and solutions will need to be investigated to make this easily accessible and usable.  
2. A fully fledged API will need to be developed for supporting the bidirectional communication between the app and Python or potentially other apps. This will require:  
   - Rearchitecting things such that the server lives in the app side.  
   - A well-defined data schema will need to be made to fit the needs of researchers looking to use the tool.  
   - Data coming from many aspects of the app including the biophysical simulation and user controls will need to be sent as part of the schema.  
   - A more generic API for data sending should also be considered that allows for other models outside of morphologically accurate biophysical neuron models.  
3. Currently, the network data has no notion of clock-synchronization with the platform and, as such, the physics simulation in the app and the network simulation run at different timescales and out of sync. This would need to be a strong consideration when considering real architecture.  
4. The short term desired goal is to get a NEURON simulation of the C. elegans motor system to correctly drive the biophysical model of C. elegans.

### 3. Control Sliders

Control sliders were provided to demonstrate what user control would look like when controlling aspects of the simulation. In this case, sliders are provided demonstrating the fundamental ideas presented first in the data and anatomy viewer.

#### Currently

This was an entirely proof-of-concept work. Nothing about this section is customizable. For demo purposes, controls were implemented the following way:

- Sliders mapped to parameters of the components described in the [Motion](#1-c-elegans-biomechanical-simulation) section of part 1.1. They manipulated aspects of the sinusoidal pulse generator and the biased-Brownian-motion-driven mass.

#### Future Goals

1. Obviously the sliders will need to map to arbitrary components of the simulation.  
2. Beyond that, controls will need to be much more flexible than sliders, allowing for various forms of interaction depending on the research question of interest.  
3. My particular objectives would be to map sliders to parameters in the biophysical simulation as described in the future goals of the [NEURON simulation](#2-neuron-simulation-and-live-network-activity-viewer) section.  
   - I am interested in questions relating to neurotransmission and neuromodulation and thus my interest would be in manipulating those models live to see both the network activity and consequent behavioral results.

### 4. Live Plotting Tools

The live plotting tools were presented, similarly to the control sliders, as a proof-of-concept of how live plotting and analysis of various aspects of the simulation might work. In this case, the plots were selected similarly to the sliders for demonstrating fundamental ideas presented first in the data and anatomy viewer.

#### Future Goals

1. Plots will need to be able to map to arbitrary data.  
2. Users will need to be able to customize plots.  
3. Various plot types should be available for different plotting needs.  
4. Users will need to be able to export plots or the underlying data for use in other tools like Matplotlib or Excel.  
5. Data should be recordable so that it can be reviewed, replayed, and analyzed later.

---

## 3. LLM UI
<img width="490" height="500" alt="image" src="https://github.com/user-attachments/assets/899f39b8-e122-41e6-aedb-525b755d0578" />

The LLM UI is there as a demonstration of the incorporation of LLM tooling into the platform. If you would like to avoid setup and are not interested in dealing with any of the LLM-based features of the toolkit, you can skip this.

### Usage

- Click in the **text field** and type to enter text.  
- Press **Enter** to start a new line.  
- **Arrow keys** let you navigate text.  
- Click the **Send** button to send the query.

### Local Setup for Use in the Platform

1. For public users, there is no built-in access to an LLM. To get it working you will need to supply your own [OpenAI API Key](https://platform.openai.com/api-keys) (more information in the [Developer Quickstart section](https://platform.openai.com/docs/quickstart) of the OpenAI developer site).  
2. Once you have your OpenAI API Key, make a folder in the directory:  
   `build/NeuronUnity_Data/StreamingAssets/` called `ApiKeys` and in it make a new file called `openaiapikey.txt`. There simply paste your API key directly.  
   - If this worked, then in the toolkit, when you query the Chat, the bubble should show as **"(thinking...)"**  
   - If it failed, then you will see a `NullReferenceException` in the bubble.

### Developer Information

#### For the ALIFE Demo

For the ALIFE Demo I fine tuned a GPT model with additional C. elegans data:  
<https://github.com/orrenravid1/CElegansResources/blob/main/vectorstore.ipynb>  

This GPT model was then associated with my specific API key, which when used allowed me to leverage my custom tuned LLM. You can do similar by looking at what I did in the above.

### Future Goals

1. Make the custom trained C. elegans GPT model accessible without an API key.  
2. Make the LLM able to interface with the toolkit so that it can:  
   - Select elements  
   - Modify and interact with them  
   - Give you specific help relating to aspects of the toolkit  
