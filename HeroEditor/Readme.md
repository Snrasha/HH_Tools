For use the python source, you will need:
* python
* tkinter
* pyinstaller

Use pip from python for install all of them.


For compile the python to a software:

pyinstaller --onefile "sources/HeroEditor.py"  --noconsole --distpath .

Or if HeroEditor.spec exist:
pyinstaller HeroEditor.spec --distpath .

For compile to a easy zip:
git archive --output=HeroEditor.zip HEAD
This command will compile everything except on the gitignore AND gitattributes.
