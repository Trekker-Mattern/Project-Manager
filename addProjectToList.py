from main import addProject, openTMDLFile, writeListToFile 
import sys

def main():
    projectList = openTMDLFile() 

    if not sys.argv[2] == "":
       addProjectUsingArgs(sys.argv[2], sys.argv[3], sys.argv[4], projectList)
       return

    addProject(projectList)


def addProjectUsingArgs(projName : str, projPath: str, projIDE: str, projectList: list[str]):
    projectList.append(projName + "," + projPath + "," + projIDE + "\n") 
    writeListToFile(projectList)
    return
