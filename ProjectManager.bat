set "getdir=%~dp0"
if "%1" == "-a" (
	if "%2" == "" echo -a command requires a NAME as Arg2 and a PATH as Arg3 && exit /b 1
	python3 "%getdir%addProjectToList.py" %2 %3
) else (
	python3 "%getdir%main.py" %*
)


