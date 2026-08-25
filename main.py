import subprocess
from pathlib import Path

listOfValidIDEs = ["Neovim", "VSCode", "Intellij"]


def main():

    try:
        file = open("projectlist.TMDL", 'r')
    except FileNotFoundError:
        print(FileNotFoundError)
        open("projectlist.TMDL", 'x')
        file = open("projectlist.TMDL", 'r')

    projectList = file.readlines()
    file.close()
    menu(projectList)


def openNeovim(path: str):
    bat = Path(__file__).parent / "openNeovim.bat"
    _ = subprocess.call(['cmd', '/c', str(bat), str(path)])


def openVSCode(path: str):
    bat = Path(__file__).parent / "openVSCode.bat"
    _ = subprocess.call(['cmd', '/c', str(bat), str(path)])


def addProject(projectList: list[str]):
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

    file = open("projectlist.TMDL", 'w')
    for project in projectList:
        _ = file.write(project + "\n")
    file.close()


def validateIDE(IDEStr: str):
    if IDEStr in listOfValidIDEs:
        return True
    return False


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
                case _:
                    openProject(projectList)
                    return


def openProject(projectList: list[str]):
    print("These are your saved projects:")
    for p in projectList:
        print(p.split(",")[0])

    requestedProject = input("Which project would you like to open?    ")
    requestedProject = requestedProject.strip().lower()
    print(f"Opening {requestedProject}")
    for project in projectList:
        splitProject = project.split(",")

        projectName = splitProject[0].strip().lower()
        projectPath = splitProject[1]
        projectIDE = splitProject[2].strip()
        assert '\n' not in projectIDE
        print(f"checking {projectName} vs {requestedProject}, {projectName == requestedProject}")

        if projectName == requestedProject:
            print("Found Suitable Project")
            openIDE(projectPath, projectIDE)


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


def removeProject(projectList: list[str]):
    project = input("Which project would you like to remove?")
    project = project.strip().lower()
    pname: list[str] = list(map(lambda p: p.strip().split(",")[0], projectList))
    if project in pname:
        _ = projectList.pop(pname.index(project))
        print(f"Project \'{project}\' Removed Successfully")
        return True
    return False


main()
