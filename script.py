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
from src.meta import err_msg, get_const
from warnings import filterwarnings
import pandas as pd
from os import system, makedirs, path


################################
# DATA MANIPULATION
################################
def _load(filetype, location):
    sep = const['dir_sep']
    data_directory = const['cwd'] + const['data_subdir'] + sep
    attr_directory = const['cwd'] + const['attr_subdir'] + sep
    location = data_directory + location
    encodings = const['all_encodings']
    if filetype == 'sheet':
        for encoding in encodings:
            try:
                data = pd.read_csv(location, encoding = encoding)
                data.set_index(const['index_column'], inplace=True)
            except (FileNotFoundError, PermissionError):
                err_msg('FileNotFound', data=location)
                return
            except UnicodeDecodeError:
                pass
    elif filetype == 'game':
        data = gamefiles.load(location+sep, attr_directory)
        if data.empty:
            print('ScriptLoad:', 'GameLoader returned empty DF')
            return
    else:
        err_msg('UnknownSubcall')
        return
    data.sort_values(const['auto_sort_by'], inplace=True)
    return data


################################
def _mkdir(directory):
    if not path.exists(directory):
        makedirs(directory)
################################
def _save(filetype, location):
    sep = const['dir_sep']
    data_directory = const['cwd'] + const['data_subdir'] + sep
    location = data_directory + location # No Separator
    sheet_dir = sep.join(location.split(sep)[:-1]) # No filename
    if filetype == 'sheet':
        _mkdir(sheet_dir)
        alldata.to_csv(location, encoding=const['sprd_enc'])
    elif filetype == 'game':
        _mkdir(location)
        gamefiles.save(alldata, location+sep)


################################
def _apply():
    try:
        alldata.update(selection)
    except AttributeError:
        err_msg('DataNotLoaded')


################################
def _operate_on():
    global alldata
    alldata = selection


################################
def _select(_from, attribute, values):
    global selection
    _apply()
    if attribute == 'all':
        selection = alldata
        return
    if attribute not in const['column_order']:
        err_msg('UnknownColumn', data=attribute)
        return
    try:
        if _from == 'all':
            selection = alldata.loc[alldata[attribute].isin(values)]
        if _from == 'selection':
            selection = selection.loc[selection[attribute].isin(values)]
    except (AttributeError, TypeError):
        return # Message is displayed by _apply()
    except KeyError:
        err_msg('UnknownColumn', data=attribute)
        return


################################
def _append(attribute, values):
    global selection
    if attribute not in const['column_order']:
        err_msg('UnknownColumn', data=attribute)
        return
    try:
        new_selection = alldata.loc[alldata[attribute].isin(values)]
        selection = pd.concat([selection, new_selection])
    except (AttributeError, TypeError):
        err_msg('DataNotLoaded')
        return
    except KeyError:
        err_msg('UnknownColumn', data=attribute)
        return


################################
def _sort(scope_name, sort_by):
    for c in sort_by:
        if c not in const['column_order']:
            err_msg('UnknownColumn', data=c)
            return
    if scope_name == 'all':
        try:
            alldata.sort_values(sort_by, inplace=True)
        except AttributeError:
            err_msg('DataNotLoaded')
            return
    elif scope_name == 'selection':
        try:
            selection.sort_values(sort_by, inplace=True)
        except AttributeError:
            err_msg('DataNotSelected', False)
            return
    else:
        err_msg('UnknownSubcall', data=scope_name)
        return


################################
def _set(attribute, value):
    # TODO: Pandas warning message may be displayed (Not tested)
    if attribute not in const['column_order']:
        err_msg('UnknownColumn', data=attribute)
        return
    for i in range(value.count(None)):
        value.remove(None)
    value = ' '.join(value)
    try:
        selection.loc[:, attribute] = value
    except AttributeError:
        err_msg('DataNotSelected')
        return


################################
def _inprov(provid, attribute, value):
    # TODO: Pandas warning message may be displayed (Not tested)
    try:
        provid = int(provid)
    except ValueError:
        err_msg('InvalidArgumentType')
        return
    if attribute not in const['column_order']:
        err_msg('UnknownColumn', data=attribute)
        return
    for i in range(value.count(None)):
        value.remove(None)
    value = ' '.join(value)
    try:
        selection.loc[provid, attribute] = value
    except AttributeError:
        err_msg('DataNotSelected')
        return


################################
def _print(dtype='selection', mode='full', attribute='', values=[]):
    # TODO: Test function to find possible errors
    drop_list = const['drop_from_print']
    psel = None
    ################ Drop columns listed in const['drop_from_print']
    if dtype == 'all':
        try:
            psel = alldata.drop(drop_list, axis=1)
        except AttributeError:
            err_msg('DataNotLoaded')
            return
    elif dtype == 'selection':
        try:
            psel = selection.drop(drop_list, axis=1)
        except AttributeError:
            err_msg('DataNotSelected')
            return
    elif dtype == 'info':
        try:
            c = [x for x in const['column_order'] if x not in const['drop_from_print']]
            h = const['drop_from_print']
            print('\nColumns:\n' + ', '.join(c))
            print('\nHidden columns:\n'+ ', '.join(h))
            print('\nTotal provinces:\t', len(alldata.index))
            print('Selected provinces:\t', len(selection.index))
        except:
            pass
        print()
        return
    else:
        err_msg('UnknownSubcall', dtype)
        return
    ################ Selecting rows
    if mode == 'full':
        pass
    elif mode == 'where':
        if (attribute == '') or (values == []):
            err_msg('TooLessArguments')
            return
        try:
            psel = psel.loc[psel[attribute].isin(values)]
        except (AttributeError, TypeError):
            if dtype == 'all':
                err_msg('DataNotLoaded')
                return
            elif dtype == 'selection':
                err_msg('DataNotSelected')
                return
    else:
        err_msg('UnknownSubcall', mode)
    ################ Print
    print(psel)


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
    if const['pandas_hide_warnings']:
        filterwarnings('ignore')
    global alldata
    alldata = None
    global selection
    selection = None
    gamefiles._init(const)


################################
def loop():
    # TODO: IndexError in this function is temporarily considered fatal
    global alldata
    cmnd = input(const['input_prefix']).split()
    if len(cmnd) == 0:
        return True
    funcname = cmnd[0]
    try:
        args = cmnd[1:]
    except IndexError:
        pass
    if funcname in const['legal_exit_calls']:
        return False
    if funcname not in const['legal_nonexit_calls']:
        err_msg('IllegalCall', data=funcname)
    ################################
    try:
        if funcname == 'load':
            alldata = _load(args[0], args[1])
        if funcname == 'save':
            _save(args[0], args[1])
        if funcname == 'apply':
            _apply()
        if funcname == 'operate_on':
            _operate_on()
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
            _inprov(args[0], args[1], args[2:])
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
        err_msg('TooLessArguments')
        raise # TODO
    return True


################################
def main():
    init()
    print(const['program_header'])
    while loop(): pass


################################
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n'+ '-'*32 + '\nProgram manually terminated\n'+ '-'*32+'\n\n')
    except Exception as e: #Any Unhandled Error
        print('\n'+ '-'*32 + '\nUnhandled error occured: '
        + str(type(e).__name__) + '\n' + '-'*32+'\n\n')
        raise
