# programming-integration-project-221: URA Web

This Github repository is for the Programming Integration Project, Semester 221, done by Group 4.

# Summary
We are tasked with implementing a website for the URA team of HCMUT. The website allows searching and hearing the pronunciations of words in Bahnaric via either API calls or local assets. The development started in September after the formation of the groups. Many technologies were considered, and we went with using Flask as the backend service; HTML-CSS-JS (with Bootstrap 5) for the frontend; and SQLite for the database. 

# Member list
* Dinh Le Nhat Anh - 2052370.
* Truong Tan Hao Hiep - 2011211.
* Nguyen Nho Gia Phuc - 2052214.
* Nguyen Viet Thang - 2052719.

We initially had five members, but one changed his group. The report explains further about this occasion. The event did not affect us very much, however.

# Instruction Manual
## Development environment
The current iteration of the project is not deployment-ready. Therefore, after cloning this project, follow the next steps.
### Create a directory and change into it
`cd /programming-integration-project-221`
### Create a new virtual environment in that directory and activate it
At the command prompt (Terminal for MacOS, cmd or Powershell on Windows), not the Python prompt, create a new virtual environment. **Do this only once**. Make sure you are not in an already-activated environment. After enviroment creation, activate it.

On MacOS: `python3 -m venv venv`, then `source venv/bin/activate`

On Windows: `python -m venv venv`, then `venv\Scripts\activate` (try adding .bat to activate if the command does not run)

After activation, you should see at least a `(venv)` at the far left side of your command prompt, indicating the activation of the virtual environment. Some text editors highlight this to another color. For example, on my Windows PC, I would see `(venv) PS D:\Developer\programming-integration-project-221>`

## Install the dependencies
Install the dependencies in the requirements.txt file in the **currently active** Python3 virtual environment. When it is not active, all the dependencies will not be available to you. This is ideal, because you would want to create different virtual environments for different Python project and need not to worry about updated libraries in the future breaking your (past) code.

Do that by running `pip install -r requirements.txt`

## Launch the project
Execute `python main.py` and the development server at localhost:5000 will be availble. Ctrl + Click to open it up in your web browser.

## Troubleshooting
If you are on Windows and using VSCode as a code editor, it has Powershell as its default command prompt. It would have issues with the assets file, due to problems in the path. Switching to WSL command prompt and cloning like usual should resolve this problem, as the paths are fixed automatically. 

Anyway, you could download a zip file of this repository and worry not about the issue!

