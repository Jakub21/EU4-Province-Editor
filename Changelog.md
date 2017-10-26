# Changelog

### Separate Changelog

**Last on Master branch**
- Moved Changelog to separate file



### Game Files Parser IV

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
