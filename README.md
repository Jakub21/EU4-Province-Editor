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


### Loading files

**Directory of Game Files**

When loading game files directory:
```
script_location/
    selected_directory/
        provinces/
            *province files with original names
        localisation.yml (File with province names in any language)
        area.txt
        region.txt
        superregion.txt
    script.py
```
Selected directory must be sub- of where script is located and console is working. Can be located in deeper folder eg. `script_location/folder/another_one/selected_directory/`
but in this case command looks like:
`load game folder/another_one/selected_directory`  
Note that program doesn't copy regioning and localisation files automaticly




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

- Solve problems that cause display of Pandas' warning message during usage of functions: `sort`, `inprov`
- Extend usage info
