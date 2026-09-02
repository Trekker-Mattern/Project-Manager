scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $scriptDir
python3 "$scriptDir/main.py"

