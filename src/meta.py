from platform import system as psys
from os import getcwd
################################
# SETTINGS AND CONSTANT VARIABLES
def get_const():
    global const
    const = {
        # Pandas Display
        'pandas_max_rows'       : 500,
        'pandas_max_cols'       : 50,
        'pandas_disp_width'     : 250,
        # Directories and Files
        'dir_sep'               : '/',
        'history_subdir'        : 'provinces',
        'sprd_enc'              : 'utf-8-sig',
        'locl_enc'              : 'utf-8-sig',
        'all_encodings'         : ['utf-8', 'utf-8-sig'],
        # Appearance
        'preceding_blank_line'  : False,
        'error_prefix'          : '(Error) ',
        'input_prefix'          : '[Editor] > ',
        'program_header'        : 'EU4 Province Editor v0.1',
        'drop_from_print'       : [
            'filename',
            'discovered',
            'modifiers',
        ],
        # Value Related
        'shorten_region_names'  : True,
        'multival_sep'          : '&',
        'default_name'          : 'NoNameFound',
        'default_area'          : 'NoArea',
        'default_region'        : 'NoRegion',
        'default_segion'        : 'NoSegion',
        # DataFrames / SpreadSheets
        'index_column'          : 'id',
        'auto_sort_by'          : ['segion', 'region', 'area', 'tax'],
        'column_order'          : [
            'id', 'name', 'capital',
            'area', 'region', 'segion',
            'cores', 'claims',
            'owner', 'cntrl',
            'culture', 'religion', 'hre',
            'tax', 'prod', 'manp',
            'trade_goods',
            'city', 'cost', 'fort',
            'discovered', 'modifiers',
            'filename',
        ],
        # Callables
        'legal_nonexit_calls'   : [
            'load', 'save',
            'apply',
            'select', 'subselect', 'append',
            'sort',
            'set', 'inprov',
            'print', 'clear', 'help',
        ],
        'legal_exit_calls'      : [
            'exit', 'quit', 'leave'
        ],
        # Game Files
        'lcl_languages'         : [
            'l_english', 'l_spanish', 'l_french', 'l_german',
        ],
        'historyfile_keys'      : {
            'capital'       : 'capital',
            'cores'         : 'add_core',
            'claims'        : 'add_claim',
            'owner'         : 'owner',
            'cntrl'         : 'controller',
            'culture'       : 'culture',
            'religion'      : 'religion',
            'hre'           : 'hre',
            'tax'           : 'base_tax',
            'prod'          : 'base_production',
            'manp'          : 'base_manpower',
            'trade_goods'   : 'trade_goods',
            'city'          : 'is_city',
            'ntv_size'      : 'native_size',
            'ntv_ferc'      : 'native_ferocity',
            'ntv_hstl'      : 'native_hostileness',
            'cost'          : 'extra_cost',
            'fort'          : 'fort_15th',
            'discovered'    : 'discovered_by',
            'modifiers'     : ['add_permanent_province_modifier', 'name'],
        },
    }
    ################################
    # Variables
    const['cwd'] = getcwd()
    if psys() == 'Windows':
        const['terminal_clear'] = 'cls'
    else:
        const['terminal_clear'] = 'clear'
    ################################
    # Checking
    if const['index_column'] not in const['column_order']:
        raise_error('Column "'+const['index_column']+'" is not in "column_order" list. Its presence there is necessary.',
            self_contents = True, fatal = True)
    ################################
    return const



################################
# ERRORS HANDLING
################################
def raise_error(error_type, fatal=False, data=['None'], self_contents = False):
    if type(data) != list:
        data = [data]
    try:
        directory = const['dir_sep'].join(data[0].split(const['dir_sep'])[-3:])
    except:
        pass
    print(const['error_prefix'], end = "")
    messages = {
        'illegal_call'          : 'Unrecognized function "'+data[0]+'"',
        'unknown_subcall'       : 'Unrecognized parameter "'+data[0]+'"',
        'too_many_arguments'    : 'Function recieved too many arguments',
        'too_less_arguments'    : 'Function recieved not enough arguments. Usage: '+' '.join(data),
        'data_not_loaded'       : 'No data was loaded',
        'data_not_selected'     : 'No data was selected',
        'unknown_attribute'     : 'Unrecognized column name "'+data[0]+'"',
        'filestream_error'      : 'File "'+ directory +'" does not exist or the permission was denied',
        'nolocalisation_error'  : 'Localisation could not be loaded. Check files and language tags',
        'hparser_equal_sign'    : 'Syntax error in file ' +directory,
        'unknown_fstr_error'    : 'Unknown error occured when file "'+directory+'" was loaded',     # unused
        'encoding_bom_error'    : 'Loaded file uses encoding with BOM and can not be loaded',       # unused
    }
    if self_contents:
        print(error_type)
    else:
        print(messages[error_type])
    if fatal:
        print("Program Terminated")
        exit(1)
