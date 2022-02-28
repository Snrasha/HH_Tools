For use the python source, you will need:
* python
* tkinter
* pyinstaller

Use pip from python for install all of them.


For compile the python to a software:

pyinstaller --onefile "sources/main.py" --distpath .

Or if main.spec exist:
pyinstaller main.spec --distpath .

For compile to a easy zip:
git archive --output=HeroEditor.zip HEAD
This command will compile everything except on the gitignore AND gitattributes.
