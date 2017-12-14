################################
import src.gamefiles as gamefiles
from src.meta import err_msg, get_const
from warnings import filterwarnings
import pandas as pd
from numpy import nan
from os import makedirs, path


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
                data = pd.read_csv(location, encoding=encoding)
                data.set_index(const['index_column'], inplace=True)
                data.replace(nan, const['empty_marker'], inplace=True)
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
if __name__ == '__main__':
    add_key = 'modifiers'
    init()
    print('Script updates single column with data from other set')
    print('Type: "sheet", "game"')
    t_old = input('Type of old data\t')
    p_old = input('Path of old data\t')
    t_new = input('Type of new data\t')
    p_new = input('Path of new data\t')
    t_rsl = input('Type of result\t\t')
    p_rsl = input('Path of result\t\t')
    old = _load(t_old, p_old)
    new = _load(t_new, p_new).loc[:, add_key]
    old.update(new)
    global alldata
    alldata = old
    _save(t_rsl, p_rsl)
    print('Done.')
