#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ $1=="-add" || $1=="-a"]]; then
	[[ $2 == "" && $3 == "" && $4=="" ]] {python3 "$SCRIPT_DIR/addProjectToList.py" exit}
	NAME="${2:?Error: Project name parameter is required using the add flag}"
	PTH="${3:?Error: Project path is required using the add flag}"
	IDE="${4:?Error: Project IDE is required when using the add flag}"
	python3 "$SCRIPT_DIR/addProjectToList.py" "$@"
	exit
fi

python3 "$SCRIPT_DIR/main.py" "$@"
exit

