'''
--------------------------------
EU4 Province Editor
Jakub21, October 2017
Published and Developed on GitHub
--------------------------------
Version 0.1.0 - Not released
--------------------------------
Repository site
Visit for updates and usage info
github.com/Jakub21/EU4-Province-Editor
--------------------------------
Province Editor is a shell-styled program that allows easy edition of province history.
User can change attributes in areas or regions with out need to look for files in long list.
Program can generate spreadsheets with provinces' data or files ready to copy to mod.
--------------------------------
'''


################################
import src.gamefiles as gamefiles
from src.meta import raise_error, get_const
import pandas as pd
from os import system, makedirs, path



################################
# DATA MANIPULATION
################################
def _load(filetype, location):
    encodings = ['utf-8', 'utf-8-sig']
    if filetype == 'sheet':
        try:
            for encoding in encodings:
                alldata = pd.read_csv(location, encoding = encoding)
                alldata.set_index('id', inplace = True)
                return alldata
        except (FileNotFoundError, PermissionError):
            raise_error('filestream_error', data=location)
            return None
        except UnicodeDecodeError:
            pass
    elif filetype == 'game':
        return gamefiles.load(location)
    else:
        raise_error('unknown_subcall')
        return None


################################
def _save(filetype, location):
    #if not path.exists(location):
    #    makedirs(location)
    if filetype == 'sheet':
        alldata.to_csv(location, encoding = 'utf-8-sig')
    elif filetype == 'game':
        history_path = location+const['def_dir_sep']+const['history_subdir']
        if not path.exists(history_path):
            makedirs(history_path)
        gamefiles.save(alldata, location)


################################
def _apply():
    alldata.update(selection)


################################
def _select(_from, attribute, values):
    global selection
    _apply()
    try:
        if _from == 'all':
            selection = alldata.loc[alldata[attribute].isin(values)]
        if _from == 'selection':
            selection = selection.loc[selection[attribute].isin(values)]
    except (AttributeError, TypeError):
        raise_error('data_not_loaded')
        return None
    except KeyError:
        raise_error('unknown_attribute', data=attribute)
        return None


################################
def _append(attribute, values):
    global selection
    try:
        new_selection = alldata.loc[alldata[attribute].isin(values)]
        selection = pd.concat([selection, new_selection])
    except (AttributeError, TypeError):
        raise_error('data_not_loaded')
        return None
    except KeyError:
        raise_error('unknown_attribute', data=attribute)
        return None


################################
def _sort(scope_name, sort_by):
    if scope_name == 'all':
        try:
            alldata.sort_values(sort_by, inplace=True)
        except AttributeError:
            raise_error('data_not_loaded')
            return None
    elif scope_name == 'selection':
        try:
            selection.sort_values(sort_by, inplace=True)
        except AttributeError:
            raise_error('data_not_selected', False)
            return None
    else:
        raise_error('unknown_subcall', data=scope_name)
        return None


################################
def _set(attribute, value):
    # TODO: Pandas warning message may be displayed (Not tested)
    for i in range(value.count(None)):
        value.remove(None)
    value = ' '.join(value)
    try:
        selection.loc[:, attribute] = value
    except AttributeError:
        raise_error('data_not_selected')
        return None


################################
def _inprov(provid, attribute, value):
    # TODO: Pandas warning message may be displayed (Not tested)
    for i in range(value.count(None)):
        value.remove(None)
    value = ' '.join(value)
    try:
        selection.loc[provid, attribute] = value
    except AttributeError:
        raise_error('data_not_selected')
        return None


################################
def _print(scope_name='selection', mode='full', attribute='', values=[]):
    # TODO: Test function to find possible errors
    # TODO: Selective print of rows
    drop_list = const['drop_from_print']
    print_selection = None
    if scope_name == 'all':
        try:
            print_selection = alldata.drop(drop_list, axis=1)
        except AttributeError:
            raise_error('data_not_loaded')
            return None
    elif scope_name == 'selection':
        try:
            print_selection = selection.drop(drop_list, axis=1)
        except AttributeError:
            raise_error('data_not_selected')
            return None
    else:
        raise_error('unknown_subcall')
        return None
    print(print_selection)


################################
def _clear():
    system(const['terminal_clear'])
    print(const['program_header'])


################################
def _help():
    print(__doc__)



################################
# MAIN SCRIPT
################################
def init():
    global const
    const = get_const() # src.meta
    if const['preceding_blank_line']:
        const['error_prefix'] = '\n' + const['error_prefix']
        const['input_prefix'] = '\n' + const['input_prefix']
    pd.set_option('display.max_rows', const['pandas_max_rows'])
    pd.set_option('display.max_columns', const['pandas_max_cols'])
    pd.set_option('display.width', const['pandas_disp_width'])
    global alldata
    alldata = None
    global selection
    selection = None
    gamefiles.init(const)


################################
def loop():
    # TODO: IndexError in this function is temporarily considered fatal
    global alldata
    cmnd = input(const['input_prefix']).split()
    if len(cmnd) == 0:
        return True
    funcname = cmnd[0]
    try:
        args = cmnd[1:]# + [None, ]*(4-len(cmnd))
    except IndexError:
        pass
    if funcname in const['legal_exit_calls']:
        return False
    if funcname not in const['legal_nonexit_calls']:
        raise_error('illegal_call', data=funcname)
    ################################
    try:
        if funcname == 'load':
            alldata = _load(args[0], args[1])
        if funcname == 'save':
            _save(args[0], args[1])
        if funcname == 'apply':
            _apply()
        if funcname == 'select':
            _select('all', args[0], args[1:])
        if funcname == 'subselect':
            _select('selection', args[0], args[1:])
        if funcname == 'append':
            _append(args[0], args[1:])
        if funcname == 'sort':
            _sort(args[0], args[1:])
        if funcname == 'set':
            _set(args[0], args[1:])
        if funcname == 'inprov':
            _inprov(int(args[0]), args[1], args[2:])
        if funcname == 'clear':
            _clear()
        if funcname == 'help':
            _help()
        if funcname == 'print':
            try:
                _print(args[0], args[1], args[2], args[3:])
            except IndexError:
                try:
                    _print(args[0])
                except IndexError:
                    _print()

    except IndexError:
        raise_error('too_less_arguments')
        raise # TODO
    return True


################################
def main():
    init()
    print(const['program_header'])
    while loop(): pass


################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n"+ "-"*32 + "\nProgram manually terminated\n"+ "-"*32+"\n\n")
    except Exception as e: #Any Unhandled Error
        print("\n"+ "-"*32 + "\nUnhandled error occured: "
        + str(type(e).__name__) + "\n" + "-"*32+"\n\n")
        raise
