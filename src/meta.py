from platform import system as psys
from os import getcwd
################################
# SETTINGS AND CONSTANT VARIABLES
def get_const():
    global const
    const = {
        # General
        'auto_sort'             : True,
        'auto_apply'            : True,
        'autoprint_atselect'    : False,
        'autoprint_atsort'      : False,
        'autoprint_atchange'    : False,
        # Pandas Display
        'pandas_max_rows'       : 1000,
        'pandas_max_cols'       : 50,
        'pandas_disp_width'     : 250,
        'pandas_hide_warnings'  : True,
        # Directories
        'dir_sep'               : '/',
        'data_subdir'           : 'data',
        'attr_subdir'           : 'attributes',
        'fnames'                : {
            'segion'        : 'superregion.txt',
            'region'        : 'region.txt',
            'area'          : 'area.txt',
            'provloc'       : 'localisation.yml',
        },
        # Encodings
        'histload_prim_enc'     : 'utf-8',          # Try to load history...
        'histload_secn_enc'     : 'ansi',           # ... and use this if 1st coulndt do it
        'histsave_enc'          : 'ansi',           # Always save history in this encoding
        'sprd_enc'              : 'utf-8-sig',      # Spreadsheets
        'locl_enc'              : 'utf-8-sig',      # Localisation
        'all_encodings'         : ['ansi', 'utf-8', 'utf-8-sig'],
        # Appearance
        'preceding_blank_line'  : False,
        'show_save_toggle'      : True,
        'show_save_freq'        : 350,              # Message every _ provinces saved
        'empty_marker'          : '',
        'show_save_msg'         : 'Progress: ',
        'error_prefix'          : '(Error) ',
        'input_prefix'          : '[Editor] > ',
        'program_header'        : 'EU4 Province Editor v0.1',
        'drop_from_print'       : [
            'filename',
            'discovered',
            #'modifiers',
        ],
        # Value Related
        'shorten_region_names'  : True,
        'multival_sep'          : '&',
        'default_name'          : 'NoNameFound',
        'default_area'          : 'NoArea',
        'default_region'        : 'NoRegion',
        'default_segion'        : 'NoSegion',
        'value_empty'           : ['xxx', 'nan', 'no', '0', 'none'], # lowercase
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
            'filename', 'group',
        ],
        # User's functions
        'legal_nonexit_calls'   : [
            'load', 'save',
            'apply', 'operate_on',
            'select', 'subselect', 'append',
            'sort',
            'set', 'inprov',
            'print', 'clear', 'help',
        ],
        'legal_exit_calls'      : [
            'exit', 'quit', 'leave'
        ],
        # Localisation
        'locl_key_prefix'   : 'PROV',
        'lcl_languages'         : [
            'l_english', 'l_spanish', 'l_french', 'l_german',
        ],
        # Region files
        'none'                  : 'none',
        'skip_at_region_load'   : '{=}colorareas',
        'regioning_names_suffiexes' : {
            'area'          : '_area',
            'region'        : '_region',
            'segion'        : '_superregion',
        },
        # Province Files
        'indent'                : ' '*4,
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
        'province_attr_keys'    : {
            'id'            : 'id',
            'nm'            : 'name',
            'fn'            : 'filename',
            'gr'            : 'group',
            'ar'            : 'area',
            'rg'            : 'region',
            'sg'            : 'segion',
        },
        'additional_save_info'  : {
            # Lines added to every scope with specified name
            'add_permanent_province_modifier'   : 'duration = -1',
        },
    } # Endof Const
    ################################
    # Dependends
    cwd = getcwd() + const['dir_sep']
    bck = '\\'
    if bck in cwd:
        cwd = const['dir_sep'].join(cwd.split(bck))
    const['cwd'] = cwd
    if psys() == 'Windows':
        const['terminal_clear'] = 'cls'
    else:
        const['terminal_clear'] = 'clear'
    ################################
    return const



################################
# ERRORS HANDLING
################################
def err_msg(error_type, fatal=False, data=['None'], self_contents=False):
    if type(data) != list:
        data = [data]
    try:
        directory = const['dir_sep'].join(data[0].split(const['dir_sep'])[-3:])
    except:
        pass
    print(const['error_prefix'], end = '')
    messages = {
        'IllegalCall'           : 'Unrecognized function "'+data[0]+'"',
        'UnknownSubcall'        : 'Unrecognized parameter "'+data[0]+'"',
        'TooLessArguments'      : 'Function received not enough arguments',
        'InvalidArgumentType'   : 'Received argument of invalid type.',
        'DataNotLoaded'         : 'No data was loaded',
        'DataNotSelected'       : 'No data was selected',
        'UnknownColumn'         : 'Unrecognized column name "'+data[0]+'"',
        'FileNotFound'          : 'File "'+ directory +'" does not exist or the permission was denied',
        'DirectoryNotFound'     : 'Selected directory does not exist.',
        'LocalisationNotFound'  : 'Localisation could not be loaded. Check files and language tags',
        'AttrFileNotFound'      : 'Required Attribute file ('+directory+') was not found or permission was denied.',
        'WrongHistorySyntax'    : 'Syntax error in file ' + directory,
        'WrongRegionFile'       : 'File with regioning data is empty or contains syntax error',
    }
    if self_contents:
        print(error_type)
    else:
        print(messages[error_type])
    if fatal:
        print('Program Terminated')
        exit(1)
