# EU4 Province Editor
**Province History Editor for Europa Universalis IV**

Written by Jakub21

October 2017

Published and Developed on GitHub


***Requirements***

- Python 3
- Pandas v0.20

***TODOs***

- Loader for game files
- Solve problems that cause display of Pandas' warning message during usage of functions:
    'sort', 'inprov', 'replace'
- Allow user to change which (and how many) columns and rows should be displayed



# Changelog

***Version 0.1***

**Initial' Repair II**

- Using unknown attribute in 'print' function with mode 'only' is longer considered fatal error
- Solved problems with loading CSV sheets encoded with UTF-8 BOM
- Default encoding when saving CSV sheets is now UTF-8 BOM (Spreadsheet programs default)
- Changed usage / help messages


**Initial' Repair I**

- Functions 'inprov' and 'set' now work but Pandas error is displayed
- Removed BOM converter because it did not work. Error is raised instead
- Optimized argument parsing in interactive functions (less code)
- Full Help Message has info about valid exit calls
- Function 'clear' is now cross-platform
- Added more options for 'print'


**Initial Commit**

- Initial version of program.
- Lacks basic features and contains bany bugs.
- Files can not be loaded from GameFiles
