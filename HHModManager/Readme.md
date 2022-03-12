For use the python source, you will need:
* python
* tkinter
* pyinstaller

Use pip from python for install all of them.


For compile the python to a software:

pyinstaller --onefile "sources/HHModManager.py"  --noconsole --distpath .

Or if HHModManager.spec exist:
pyinstaller HHModManager.spec --distpath .

For compile to a easy zip:
git archive --output=HHModManager.zip HEAD
This command will compile everything except on the gitignore AND gitattributes.
