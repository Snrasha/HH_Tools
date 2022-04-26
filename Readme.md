# Description
<p>
Hero's hour unofficial tools editor.
</p>

See this link for the modding guide of Hero's Hour.
https://docs.google.com/document/d/1h64ac7rNAW0_0Kfj-KsMecsdMdQGZlJ2cmIU0PMVWFY/edit#heading=h.rrar1dgps27e

## Hero's Hour Editor

This editor has the Hero, Faction tab, Unit Tab and Mod Tab.

### Usage

Double click on the HerosHourEditor.exe. Warning, this software will probably be seens like a **virus** the first time.</br>

On open, you will have different tabs. Click on these tabs for switching of editor or press the number on your keyboard.

### Shortcut

* **1,2,3,4** will open the tab wanted.
* **D** will open the file dialog for edit a file.
* **V** will "save as" your work.


### Hero Tab
 * **Name**: Hero name. Need to be unique amongs every mods and vanilla heroes;
 * **Unit**: The unit which the Hero spawn at the start or linked to skills;
 * **Class**: For neutral heroes only. Look at the guide for know what insert;
 * **Skills**: Setup the 18 skills like in the game. You do not need to fill every slots, they will be randomized on game.
 * **Neutral and Replacement Checkbox**: The first disable or enable the "class". If checked, the saved file will not contain Class. For replacement, will just check if the data end with the correct suffix.

 For the skills tree, click on the skill slot than you want fill, then double click on the skill on the skill list. A simple click on a skill slot or a skill from skill list will display the description.

 Do not hesitate to use the search bar because it check also the description of each skill.

### Faction Tab
  * **Faction Name/Lore fields**: Text to fill;
  * **Buildings**: DWELLING NAMES + FACTION UNITS ALTERNATES;
  * **Others**: See modding guide;
  * **Town names**: Look the description popup.

### Unit Tab
Description to add. If someone wish to do it.

## Animation Tool
Each button are linked to a hotkey

* Unit:
Create the animation used like the game. The attack animation use 100ms like in battle compared.
* Hero:
Simple animation but each rotation has a more loop.
* Scaling: Rescale the global size of the gif.
* Set Scale to 24x24: If your unit is on a canvas of 16x16, place it on a 24x24.
* Double Background: Duplicate the gif with a transparent and gray background for see the difference.

## HH Mod Manager
For Itch, Gog or Steam, you can easily install your mod with this tool.

### Compilation (For developpment only)

Each tool has a .spec, this is from PyInstaller which made a executable from source code.</br>
Without spec, you need to launch the command:</br>
* pyinstaller --onefile "sources/HHModManager.py"  --noconsole --distpath .</br>
Then modify a bit the spec for be what you want.</br>

The issue with PyInstaller is than it build and compile every module and also optional module which are not used for your app. Which compile it to a 100Mo executable and not 10 Mo.
For resolve the issue, you need to create a virtual env, like that:
* python -m venv venv_modmanager
* python -m venv venv_editor
* python -m venv venv_animation

When this is made, you can activate it, where you will got a clean python without anything installed. You will need to uninstall PyInstaller on your global path, so use: pip uninstall PyInstaller.

Then you can active them with:
* . venv_modmanager/Scripts/activate
* . venv_editor/Scripts/activate
* . venv_animation/Scripts/activate

And for each, you install manually:
* pip install Pyinstaller

Then you can launch for each one:
* pyinstaller HH_Tools/HHModManager/HHModManager.spec --distpath .
* pyinstaller HH_Tools/HerosHourEditor/HerosHourEditor.spec --distpath .
* pyinstaller HH_Tools/AnimationTool/AnimationTool.spec --distpath .

Then you can launch each executable and see what module is lacking for each.
On this case, you will need to install PIL for the animation and editor tool, so go on their virtual environment and install it:
* pip install pillow


For made the three executable more easily, i have made a .bat containing these 6 lines.
