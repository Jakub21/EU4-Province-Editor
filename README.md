# EU4 Province Editor

Province History Editor for Europa Universalis IV  
Written by Jakub21  
October 2017  
Published and Developed on GitHub  




## Requirements

- Python 3 (Program tested and built on version 3.6.2)
- Pandas package (v0.20)
- PyYAML package (v3.12)




## Usage

### Basics
- Download repository and unrar it anywhere
- Open console / terminal in location where program is located
- Launch file `script.py` using Python 3
- After everything is loaded user can input commands

### Commands
**Explaination of symbols and names used below**

- `<word>`    - Keyword; Only use listed words or function will not be launched
- `[word]`    - Any single word. In this case any word is allowed or allowed words depend on loaded data
- `(word)`    - Any word or list of words. Allowed words - Same as above
- `?`         - Prefix used to indicate that argument is optional

- `AllData`   - Main data scope.

    - Affected by : `load`, `append`
    - Loaded by   : `save`, `select`, `append`

- `Selection` - Current selection.

    - Affected by : Any data-manipulation function
    - NOTE        : Use `apply` if you want data from selection to be saved

**Commands**
- `load` `<mode>` `[location]`
    - `<mode>`      - allowed words: `game`, `sheet`
    - `[location]`  - location of file / folder to load
- `save` `<mode>` `[location]`
    - `<mode>`      - allowed words: `game`, `sheet`
    - `[location]`  - location where file / folder should be saved
- `select` `[attribute]` `(value)`
    - `[attribute]` - column to search for value(s) in
    - `(value)`     - rows with these will be selected
- `subselect` `[attribute]` `(value)`
    - `[attribute]` - column to search for value(s) in
    - `(value)`     - rows with OTHER than these will be removed from selection
- `sort` `<scope>` `(attribute)`
    - `<scope>`     - allowed words: `selection`, `all`
    - `(attribute)` - column to sort by  
        (NOTE: Keyword `location` can be used. The result is the same when using `segion region area`)
- `set` `[attribute]` `[value]`
    - `[attribute]` - column to change value in
    - `[value]`     - value to insert
- `inprov` `[id]` `[attribute]` `[value]`
    - `[id]`        - id of province to affect
    - `[attribute]` - column name to affect
    - `[value]`     - value to insert
- `print` `?<mode>` `?[attribute]` `?[value]`
    - `?<mode>`     - allowed words:
        - `only`    (selective print of Selection)
        - `where`   (selective print of AllData)
        - `all`     (this one takes no more args)
    - `?[attribute]`- column name to search values in
    - `?[value]`    - values to search for (only those will be displayed)
- `append`
- `apply`
- `clear`
- `help`
- `exit`




## TODOs

- Solve problems that cause display of Pandas' warning message during usage of functions:
    `sort`, `inprov`, `replace`
- Allow user to change which (and how many) columns and rows should be displayed (currently in `meta.py > init_settings() > settings{}`)
- Extend usage info
- Keep docstr in script.py updated




## Changelog for version 0.1

### Game Files Parser IV
**Last on Game-Files-Parser branch**
- Program can now save game-like history files
- Corrected usage of `type()` (It was used as method)
- Changed which attributes are loaded by default  
(It probably affected `print` but it will be repaired after branch's merged)

### Game Files Parser III

Branch-Related
- Province ID is now set as index automaticly (if 'id' is not in columns list fatal error is raised)
- Every error found in procedure of Loading Game Files was repaired.

Other Changes
- Corrections in ReadMe
- Detailed error info



### Game Files Parser II

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

There was situation where `gamefiles.py` was forced to import and then call funtion (`script.raise_error()`) from `script.py`. This probably should not happen so the function was moved to `meta.py`. Then the settings were moved here as well. It was 2nd source file so `src` subdirectory was created.



### Game Files Parser I

Branch-Related
- Recursive parser for history files
- Using yaml package to load localisation
- Parser for region files (Data is not ready for use until merge_regions() is done)

Other Changes
- Shortened error messages handling
- Changes in init_session (global settings)
- Help messages moved to script's docstr



### Initial' Repair II
**Last on Master branch**

- Using unknown attribute in `print` function with mode `only` is longer considered fatal error
- Solved problems with loading CSV sheets encoded with UTF-8 BOM
- Default encoding when saving CSV sheets is now UTF-8 BOM (Spreadsheet programs default)
- Changed usage / help messages



### Initial' Repair I

- Functions `inprov` and `set` now work but Pandas error is displayed
- Removed BOM converter because it did not work. Error is raised instead
- Optimized argument parsing in interactive functions (less code)
- Full Help Message has info about valid exit calls
- Function `clear` is now cross-platform
- Added more options for `print`



### Initial Commit

- Initial version of program.
- Lacks basic features and contains many bugs.
- Files can not be loaded from GameFiles
