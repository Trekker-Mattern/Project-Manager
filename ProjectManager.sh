#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ $1 == -add ]]; then
	NAME="${2:?Error: Project name parameter is required using the add flag}"
	PTH="${3:?Error: Project path is required using the add flag}"
	python3 "$SCRIPT_DIR/addProjectToList.py" "$@"
	exit
fi

python3 "$SCRIPT_DIR/main.py" "$@"

