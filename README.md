# <ins>Act-Like-A-Fraudster<ins>
### 2024 - 2025 CU Boulder Software Engineering Capstone - Sponsored by Alliant National.<br>
...explanation of project...


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

