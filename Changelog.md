# Changelog

### 18: Modifiers loading
**Last on Master branch**
- Added `XXX` (No country) to list of emptiness markers
- Default value of `pandas_max_rows` setting changed from 500 to 1000
- Repaired program crashes that occurred when `save` received not enough arguments
- Province modifiers are now loaded correctly
- When loading from sheet, `NaN` is no longer displayed in empty cells
- When setting value to an `empty_marker`, there will be nothing displayed in the cell
- Data can be shown on screen after changes. Disabled by default.
- Added tool that copies modifiers info from one data set to other



### 17: Hidden warnings
- Pandas warnings are now hidden (warnings can be re-enabled in `meta.py`)
- Another update of encodings. Probably a final one (tested in-game)
- Basic directories info moved from `script.py` to a readme file



### 16: Errors handling
- A new column `group` was added. Column is empty when data is generated. User can assign any value here. This allows to "save" lists of provinces so they can be re-selected later. Groups data is saved to sheets but not to game files.
- It is now possible to check basic info about data with `print info` (will be developed later)
- When selecting provinces, if a column that does not exist was used, an error is raised
- Program no longer crashes when argument `id` of function `inprov` is not a number.
- When trying to change value in column that does not exist an error is raised
- It is now possible to select all provinces with `select all` command
- When trying to sort by column that does not exist an error is raised
- Function `raise_error` was renamed to `err_msg`
- Selective print of rows was added
- Changed IDs of errors



### 15: Game-files loader fix
- Fixed typos in changelog
- Fixed game files load procedure
- Fixed encoding problems
- Added progress info in game files save procedure
- When user choses directory that does not exist, a no-directory error is raised instead of file-stream-error



### 14: Standardize Directory Tree
- Standardization of directories in program. Always use separator `/`
- When saving files required directories are created by program (Now properly)
- Regions data and localisation will always be loaded from `project/attributes`
- Provinces data will always be loaded from `project/data`  
    (Command `load game my_folder` will load files from `project/data/my_folder`  
    and `load sheet my_sheet.csv` will load file `project/data/my_sheet.csv`)  
- Added function `operate_on`. Switches main data to selection (Drop everything outside of it).
- Changes in `gamefiles.py`. File is not a bit easier to read
- It is no longer necessary for `ID` Column to be listed at 1st position in `column_order` list



### 13: Auto Sort
- Data is now automatically sorted (by location) after it's loaded
- Settings in `const` were grouped for easier access
- Console working directory is only checked at launch



### 12: Auto Apply
- When changing selection changes are saved automatically
- If province is not assigned to a area/region/s-region a default value is inserted
- If province lacks localisation a default value is inserted
- Removed usage from ReadMe but it will be uploaded in separate file soon
- When creating spreadsheet a directory with sheet name is no longer disallowing creation of actual sheet (this also disabled auto-creation of directories when creating game files which will be repaired in next commit)



### 11: License
- Added license (MIT)



### 10: Script Rewritten
- Rewritten script (callable functions are now functions)
- Fixed typo in `meta.py` (controller)
- When printing Data, unnecessary columns are dropped (changeable in `const`)
- Function `replace` was removed due to lack of possibility to select column to operate in
- Added ordinals to Changelog
- When saving data, directories that don't exist are automatically created
- Variable `settings` was renamed to `const`



### 9: Separate Changelog
- Moved Changelog to separate file



### 8: Merge Game-Files-Parser
- Merged Branch



### 7: Game Files Parser IV
- Program can now save game-like history files
- Corrected usage of `type()` (It was used as method)
- Changed which attributes are loaded by default  
(It probably affected `print` but it will be repaired after branch's merged)



### 6: Game Files Parser III
Branch-Related
- Province ID is now set as index automatically (if 'id' is not in columns list fatal error is raised)
- Every error found in procedure of Loading Game Files was repaired.

Other Changes
- Corrections in ReadMe
- Detailed error info



### 5: Game Files Parser II
Branch-Related
- Parser for region files is now ready for use
- Solved problems with YAML parser (Numbers that followed colons and encoding)
- Values that consist of multiple words are now loaded correctly
- Region names are shortened (can be disabled in settings)

Other Changes
- Handling Platform-Related differences moved to settings
- Error messages and settings were moved to separate file
- Source files were moved to subdirectory

Creation of file `src/meta.py`:

There was situation where `gamefiles.py` was forced to import and then call function (`script.raise_error()`) from `script.py`. This probably should not happen so the function was moved to `meta.py`. Then the settings were moved here as well. It was 2nd source file so `src` subdirectory was created.



### 4: Game Files Parser I
Branch-Related
- Recursive parser for history files
- Using yaml package to load localisation
- Parser for region files (Data is not ready for use until merge_regions() is done)

Other Changes
- Shortened error messages handling
- Changes in init_session (global settings)
- Help messages moved to script's docstr



### 3: Initial' Repair II
- Using unknown attribute in `print` function with mode `only` is longer considered fatal error
- Solved problems with loading CSV sheets encoded with UTF-8 BOM
- Default encoding when saving CSV sheets is now UTF-8 BOM (Spreadsheet programs default)
- Changed usage / help messages



### 2: Initial' Repair I
- Functions `inprov` and `set` now work but Pandas error is displayed
- Removed BOM converter because it did not work. Error is raised instead
- Optimized argument parsing in interactive functions (less code)
- Full Help Message has info about valid exit calls
- Function `clear` is now cross-platform
- Added more options for `print`



### 1: Initial Commit
- Initial version of program.
- Lacks basic features and contains many bugs.
- Files can not be loaded from Game-files
