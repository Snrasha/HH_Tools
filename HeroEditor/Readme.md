For compile the python to a software:

pyinstaller --onefile "sources/main.py" --distpath .

Or if main.spec exist:
pyinstaller main.spec --distpath .
