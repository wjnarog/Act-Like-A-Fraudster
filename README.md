# <ins>Act-Like-A-Fraudster<ins>
### 2024 - 2025 CU Boulder Software Engineering Capstone - Sponsored by Alliant National.<br>
Act Like a Fraudster is a cutting-edge platform designed to expose and combat title fraud in real estate transactions. By simulating modern fraud tactics—like phishing emails and deep fake videos—it educates users on how scammers exploit public property data. With a robust tech stack including web scraping, and AI, this tool equips buyers, lenders, and title professionals with the knowledge and resources needed to prevent costly fraud and protect their investments.



## Team:
* [Daniel Evarone](https://github.com/danielevarone) - Test Engineer
* [Diego Marrero Zilenziger](https://github.com/MariegoZ) - Project Manager
* [Isaac Kou](https://github.com/isko9924) - Security Engineer
* [Shuchi Shah](https://github.com/Shuchi18) - Security Engineer
* [Walker Narog](https://github.com/wjnarog) - Security Engineer
* [Zachary Cook](https://github.com/zaco6003) - Database Engineer
<br><br>

# <ins>Repository Structure<ins>
`Documentation/`: Contains folders holding any necessary documentation for the project.<br>
`Documentation/Status Reports`: Status reports required for project Status.<br>
`Documentation/Requirements.pdf`: A pdf outline of the project's requirements.<br>
`Documentation/Project Plan.pdf`: A pdf of our project plan.<br>
`Documentation/Gantt Chart`: Folder with a spreadsheet and pdf of our Gantt chart.<br>
`Documentation/Timesheets`: Folder containing the team member's weekly timesheets.<br>
`webScrapingResearch/`: Folder containing any research into webscraping tools.<br>
`README.md`: Project description and overview.<br><br>

# Documentation of the Website and the Backend
## Getting a Local Copy Up and Running
### Files needed:
* Files We Provide You:
- `flask_server.py`
- `server.js`
- scrapers
  - `adams.py`
  - `boulder.py`
  - `denver.py`
  - `douglas.py`
  - `elpaso.py`
  - `homes.py`
  - `redfin.py`
- public
  - `about.html`
  - `about.html`
  - `address.html`
  - `copyright.html`
  - `county.html`
  - `emailgen.html`
  - `index.html`
  - `nextsteps.html`
  - `normalize.css`
  - `style.css`
- ai
  - `emailgen.py`
* Files We Also Provide, but You Can Generate
- `package-lock.json`
- `package.json`
- node_modules
  - Check inside the github repository
* Files you will need to make on your own
  - public
	- `API_KEY.js`
  - ai
	- `API_KEY.py`

## How to set up API_KEY.js
Follow the guide from here: https://developers.google.com/maps/documentation/embed/quickstart#create-project

Steps 1-3 on the quickstart will get you an API KEY
1. Go to /public
2. Create a file named API_KEY.js
3. Inside the file on line one type
`let api_data = {"API_KEY": "YOUR_API_KEY_HERE"}`<br>
With YOUR_API_KEY_HERE replaced with the API key you generated

## How to Set Up Azure API Key:
Create a file in /ai called `API_KEY.py`

Azure API key is found from the Azure homepage: Azure > rcualfml > Launch Studio > Endpoints > Azure OpenAI Services > malfgpt-4o-mini > Key

In the file, insert
	api_key = “”

Save the file

## How to set up Flask Server:
### Create a python virtual environment
In your main directory <br>
Windows: <br>
- python3 -m venv venv <br>
- source venv/bin/activate <br>


Linux/Mac<br>
- python -m venv venv <br>
- source venv/bin/activate <br>

 You know it works if you have (venv) in front of your prompt<br>
 ### Install required packages
 run: <br>
`sudo apt update` <br>
`pip install flask` <br>
`pip install flask-cors` <br>
`pip install selenium` <br>
`pip install bs4` <br>
`pip install azure.ai.inference` <br>

## Running the Website
Open two terminals <br>
Navigate to /Webpage in both terminals<br>
In the first one, run <br>
	`node server.js`<br>
And verify that the output is something like<br>
	`node.js server running at http://localhost:3000`<br>
<br>
In the second one, run<br> 
Windows → `python3 flask_server.py`<br>
Mac/Linux → `python flask_server.py`<br>
And verify that the output is something like:<br>
	`WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.`
 `* Running on http://127.0.0.1:5000`<br>
`Press CTRL+C to quit`<br>
`127.0.0.1 - - [21/Apr/2025 14:45:45] "GET / HTTP/1.1" 200 -`<br>
`127.0.0.1 - - [21/Apr/2025 14:45:58] "OPTIONS /query_redfin HTTP/1.1" 200 -`<br>


# Documentation to run DeepLiveCam
## Model Structure:
- The "Deep-Live-Cam" folder is a subdirectory within our main repository. It originates from its own github repository that was forked
and embedded into our main project repo.
- A description of the original repository exists within the submodule folder in the "README" file.
- Submodules have specific commands in order to initialize and effect changes, please refer to "https://git-scm.com/book/en/v2/Git-Tools-Submodules".
- The original repository can be found here: https://github.com/hacksider/Deep-Live-Cam.git

## Model Setup:
- The "README" file maintains a reference to a prepackaged version of the model accessible for a monthly fee as well as installation  
instruction for a free version under the "Installation (Manual)" section.
- We highly recommend following all the suggested steps since compatibility issues may arise otherwise. One such example would be to use python
3.10 as opposed to newer versions to maintain functionality with onnxruntime version requirements. 
- There are two main methods of operating the model: via CPU or GPU. Enabling GPU will improve model performance but the instructions are
limited to those developed by NVIDIA.
- Remember to download the specified models and store them in the appropriate folder in addition to meeting the requirements
listed in the "requirements.txt" file.
- Upon completion of installation instructions, it is recommended to restart the machine, especially if CUDA was installed to enable the GPU.
- The model is not perfect and still in active development so it may require some platform/environment specific troubleshooting.
- From experience, installing ffmpeg, visual studio, and NVIDIA's CUDA can be points of confusion but they are addressed in the example.
- The following link is to a video that, although not the most professional, provides a step-by-step guide to installing
and running Deep-Live-Cam for Windows 11: https://youtu.be/f5DA7LYCoPQ?si=FnNvqV9nuUMxMrRn&t=123

## Using the Model:
As mentioned earlier, the model can be run in two modes. Commands for each are available in the "README" file instructions.
Once the program is running, a GUI will appear after ten or so seconds. 

### Key components include:
- Keep fps: maintain framerate of target video
- Face Enhancer: improves output video quality
- Select a face: image that will be overlayed on the target
- Select a target: image or video that will be manipulated 
- Start: will begin the process of overlaying one image onto another image or video
- Live: will overlay image onto live feed from selected source (laptop camera, OBS virtual camera, etc.)

If creating a static video (not using video feed for real-time alteration), the user will be prompted to select a directory within which to store 
the output.

* We did not test the paid version of the model; it may be the case that performance is much better since it claims to improve quality
and user experience.
