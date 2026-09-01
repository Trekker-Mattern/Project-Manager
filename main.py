import subprocess
import sys
from pathlib import Path
import FuzzyFinder

listOfValidIDEs = ["Neovim", "VSCode", "Intellij"]
scriptDir = Path(__file__).parent


def main():


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
 
    projectList = file.readlines()
    file.close()

    print(len(sys.argv))
    if not len(sys.argv) == 1:
        openProjectByName(projectList, sys.argv[1]) 
        return

    menu(projectList)

#Open The IDE
def openNeovim(path: str):
    bat = Path(__file__).parent / "openNeovim.bat"
    _ = subprocess.call(['cmd', '/c', str(bat), str(path)])


def openVSCode(path: str):
    bat = Path(__file__).parent / "openVSCode.bat"
    _ = subprocess.call(['cmd', '/c', str(bat), str(path)])


def validateIDE(IDEStr: str):
    if IDEStr in listOfValidIDEs:
        return True
    return False


def openIDE(path: str, IDE: str):
    print("Opening IDE")
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
        return True

    print(f"Project \'{project}\' was unable to be removed")
    return False

def writeListToFile(projectList: list[str]):
    file = open(f"{scriptDir}projectlist.TMDL", 'w')
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
                    openProjectThroughSubstring(projectList, userInput)

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


    openProjectThroughSubstring(projectList, projectToOpen)

    print("These are your saved projects:")
    for p in projectList:
        print(p.split(",")[0])

    projectNameList: list[str]= []

    requestedProject = input("Which project would you like to open?    ")
    requestedProject = requestedProject.strip().lower()

    print(f"Opening {requestedProject}")
    for project in projectList:

        projectName, projectPath, projectIDE = project.split(",")

        print(f"checking {projectName} vs {requestedProject}, {projectName == requestedProject}")

        if projectName == requestedProject:
            print("Found Suitable Project")
            openIDE(projectPath, projectIDE)
        else:
            projectNameList.append(projectName)

        matchingProj: tuple[float, str] = FuzzyFinder.assessCloseness(projectNameList, requestedProject)
        fullMatchingProject = projectList[projectNameList.index(matchingProj[1])]

        path = fullMatchingProject.split(",")[1]
        projectIDE = fullMatchingProject.split(",")[2]

        openIDE(path, projectIDE)
        return

def openProjectThroughSubstring(projectList: list[str], projectToOpen: str = ""):
    """
    Uses Trekkers FuzzyFinder algorithm to get the "closest" string
    Input: projectList, projectToOpen(could be empty string as default)
    Return: No return but should Successfully open an IDE 
    """

    possibleVals: dict[str, str] = {}

    if projectToOpen == "":
        return

    #check each value in the list to see if it is a substring
    #if so, add to the dict with the <full-path:value> and <key:name>
    for p in projectList:
        pSplit = p.split(",")[0]
        if projectToOpen in pSplit:
            possibleVals[p.split(",")[0].lower()] = p

    if len(possibleVals) == 0:
        return
    if len(possibleVals) == 1:
        pvals: list[str] = list(possibleVals.values())
        pPath, pIDE = (pvals[0].split(","))
        openIDE(pPath.strip(), pIDE.strip())
        return

    matchingProj: tuple[float, str] = FuzzyFinder.assessCloseness(list(possibleVals.keys()), projectToOpen)
    fullMatchingProject = possibleVals[matchingProj[1]]

    path, projectIDE = fullMatchingProject.split(",")

    openIDE(path, projectIDE)
    return


# TODO: do a,b,c = str.split()
def openProjectByName(projectList: list[str], matchedStr: str):
    """For use in bypassing the inputs in the terminal"""

    projectNameList: list[str] = []

    if matchedStr == "": return

    for p in projectList:

        if p.split(",")[0].lower() == matchedStr.lower():
            openIDE(p.split(',')[1].strip(), p.split(',')[2].strip())
            return

        projectNameList.append(p.split(',')[0].lower())


    matchingProj: tuple[float, str] = FuzzyFinder.assessCloseness(projectNameList, matchedStr.lower())
    fullMatchingProject =  projectList[projectNameList.index(matchingProj[1].lower())]

    path, projectIDE = fullMatchingProject.split(",")
    openIDE(path.strip(), projectIDE.strip())
    return

main()
