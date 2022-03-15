. venv_modmanager/Scripts/activate
pyinstaller HH_Tools/HHModManager/HHModManager.spec --distpath .

. venv_editor/Scripts/activate
pyinstaller HH_Tools/HerosHourEditor/HerosHourEditor.spec --distpath .

. venv_animation/Scripts/activate
pyinstaller HH_Tools/AnimationTool/AnimationTool.spec --distpath .





exit
