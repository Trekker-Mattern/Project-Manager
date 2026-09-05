import subprocess
import sys
from pathlib import Path
import FuzzyFinder
import platform

listOfValidIDEs = ["Neovim", "VSCode", "Intellij"]
scriptDir = Path(__file__).parent
current_os = platform.system()

def main():

    
    projectList = openTMDLFile()
    print(len(sys.argv))
    if not len(sys.argv) == 1:
        openProjectByName(projectList, sys.argv[1]) 
        print("Closing down")
        return

    menu(projectList)

def openTMDLFile():
    print("Opening ProjectList.TMDL")
    print(f"Expecting projectlist.TMDL to be at {scriptDir}/projectlist.TMDL")

    try:
        file = open(f"{scriptDir}/projectlist.TMDL", 'r')
        print("Opened Successfully!")
    except FileNotFoundError:
        print("Couldnt Find File...")
        print("Creating file...")
        print(FileNotFoundError)
        file = open(f"{scriptDir}/projectlist.TMDL", 'x')
        print("File created!")
        file.close()
        file = open(f"{scriptDir}/projectlist.TMDL", 'r')

    projectList = file.readlines()
    file.close()
    return projectList



#Open The IDE
def openNeovim(path: str):
    print("Opening Neovim")
    if current_os == "Windows":
        bat = Path(__file__).parent.resolve() / "openNeovim.bat"
        _ = subprocess.call(['cmd', '/c', str(bat), str(path)])
    elif current_os == "Linux":
        script = Path(__file__).parent.resolve() / "openNeovim.sh"
        _ = subprocess.call(['bash',  str(script), str(path)])
    else:
        print("Error when attempting to open IDE.")
        print("No valid operating system found")

def openVSCode(path: str):
    print("Opening Windows")

    if current_os == "Windows":
        bat = Path(__file__).parent / "openVSCode.bat"
        _ = subprocess.call(['cmd', '/c', str(bat), str(path)])
    elif current_os == "Linux":
        script = Path(__file__).parent / "openVSCode.sh"
        _ = subprocess.call(['bash', str(script), str(path)])


def validateIDE(IDEStr: str):
    if IDEStr in listOfValidIDEs:
        return True
    return False


def openIDE(path: str, IDE: str):
    print("Opening IDE")
    print(IDE)
    match IDE:
        case "Neovim":
            openNeovim(path)
            return
        case "VSCode":
            openVSCode(path)
            return
        case _:
            print("No proper IDE found")
            pass


def addProject(projectList: list[str]):
    """Add Project To the File and the List"""

    projName = input("What is the name of the project you would like to add?    ").strip()
    projPath = input("What is the PATH of the project?    ").strip()
    projIDE = input("Which IDE would you like to use for this project?    ").strip()

    if "," in projName or "," in projPath or "," in projIDE:
        print("invalid input")
        return
    if not validateIDE(projIDE):
        print("invalid IDE")
        return

    projectList.append(f"{projName},{projPath},{projIDE}")
    writeListToFile(projectList)

   

def removeProject(projectList: list[str]):
    """Remove Project from file and list"""

    project = input("Which project would you like to remove?")
    project = project.strip().lower()
    pname: list[str] = list(map(lambda p: p.strip().split(",")[0], projectList))

    if project in pname:
        _ = projectList.pop(pname.index(project))
        print(f"Project \'{project}\' Removed Successfully")
        writeListToFile(projectList)
        return

    print(f"Project \'{project}\' was unable to be removed")
    return

def writeListToFile(projectList: list[str]):
    """Opens 'ScriptDir/projectlist.TMDL' and writes all values from projectList into it"""
    file = open(f"{scriptDir}/projectlist.TMDL", 'w')
    for project in projectList:
         _ = file.write(project + "\n")
    file.close()
   


def menu(projectList: list[str]):
    userInput = ""
    while not userInput == "quit":
        userInput = input("1:Open Project, 2:Add Project, 3:Remove Project:   ")
        userInput = userInput.strip().lower()
        if userInput == "quit": quit()
        try:
            userInputInt = int(userInput)
            match userInputInt:
                case 2:
                    addProject(projectList)
                case 3:
                    removeProject(projectList)
                case _:
                    openProject(projectList)
                    return

        except Exception:
            match userInput:
                case "add project":
                    addProject(projectList)
                case "remove project":
                    removeProject(projectList)
                case "open project":
                    openProject(projectList)
                    return
                case _:
                    openProjectByName(projectList, userInput)
                    return

# Open Project based on the project list and a string
# Project to open is a default empty string
def openProject(projectList: list[str], projectToOpen: str = "") -> None:

    """
    Open a project based on project list and a string
    projectToOpen is a parameter with the default str of ""
    if a string is passed in the program will attempt to open the project using that string first
    then it checks for exact equality based on a user prompt
    then it opens the closest using the fuzzy finder
    """

    if not projectToOpen == "":
        openProjectByName(projectList, projectToOpen)
        return

    print("These are your saved projects:")
    for p in projectList:
        print(p.split(",")[0])

    projectNameList: list[str]= []

    requestedProject = input("Which project would you like to open?    ")
    requestedProject = requestedProject.strip().lower()

    print(f"Opening {requestedProject}")
    for project in projectList:

        projectName, projectPath, projectIDE = project.strip().split(",")

        print(f"checking {projectName} vs {requestedProject}, {projectName == requestedProject}")

        if projectName.lower() == requestedProject.lower():
            print("Found Suitable Project")
            openIDE(projectPath, projectIDE)
        else:
            projectNameList.append(projectName)

    #final guess and opening of project
    matchingProj: tuple[float, str] = FuzzyFinder.assessCloseness(projectNameList, requestedProject)
    fullMatchingProject = projectList[projectNameList.index(matchingProj[1])]

    _, path, projectIDE = fullMatchingProject.strip().split(",")
    print(f"OPENING {path}, WITH IDE {projectIDE}")
    openIDE(path.strip(), projectIDE.strip())
    return

# TODO: do a,b,c = str.split()
def openProjectByName(projectList: list[str], matchedStr: str):
    """For use in bypassing the inputs in the terminal"""

    projectNameList: list[str] = []

    if matchedStr == "": return

    for p in projectList:

        pName, pPath, pIDE = p.strip().split(',')
        pName = pName.lower()

        if pName == matchedStr.lower():
            openIDE(pPath , pIDE)
            return

        projectNameList.append(pName)


    matchingProj: tuple[float, str] = FuzzyFinder.assessCloseness(projectNameList, matchedStr.lower())
    fullMatchingProject =  projectList[projectNameList.index(matchingProj[1].lower())]

    _, path, projectIDE = fullMatchingProject.strip().split(",")
    openIDE(path.strip(), projectIDE.strip())
    return

main()
