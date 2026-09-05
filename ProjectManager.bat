set "getdir=%~dp0"
if "%1" == "-a" || "%1"=="-add" (
	if "%2" == "" || "%3"=="" || "%4"=="" && !(%2 == "" && %3=="" && %4=="") echo "-a command requires a NAME as Arg2, a PATH as Arg3, and IDE as Arg4" && exit /b 1
	python3 "%getdir%addProjectToList.py" %2 %3 %4
) else (
	python3 "%getdir%main.py" %*
)


