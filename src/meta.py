from platform import system as psys
################################
# SETTINGS AND CONSTANT VARIABLES
def get_const():
    global const
    const = {
        'pandas_max_rows'       : 500,
        'pandas_max_cols'       : 50,
        'pandas_disp_width'     : 250,
        'preceding_blank_line'  : False, # Blank line before every input and error message
        'shorten_region_names'  : True,
        'def_dir_sep'           : '/',
        'multival_sep'          : '&',
        'history_subdir'        : 'provinces', # With out directory separators
        'error_prefix'          : '(Error) ',
        'input_prefix'          : '[Editor] > ',
        'program_header'        : 'EU4 Province Editor v0.1',
        'default_name'          : 'NoNameFound',
        'default_area'          : 'NoArea',
        'default_region'        : 'NoRegion',
        'default_segion'        : 'NoSegion',
        'lcl_languages'         : [
                # Language tags used in localisation files
                'l_english', 'l_spanish', 'l_french', 'l_german',
        ],
        'legal_nonexit_calls'   : [
                # If user calls func that isnt listed here an error is raised
                'load', 'save',
                'apply',
                'select', 'subselect', 'append',
                'sort',
                'set', 'inprov',
                'print', 'clear',
                'help',
            ],
        'legal_exit_calls'      : [
                'exit', 'quit', 'leave'
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
        #OTHER LEGAL KEYS BESIDES THOSE FROM HISTORY
            # area, region, segion, id, filename, name
        'column_order'          : [
            #Keep 'ID' at 1st position
            'id', 'name', 'area', 'region', 'segion', 'filename',
            'capital',
            'cores',
            'claims',
            'owner',
            'cntrl',
            'culture',
            'religion',
            'hre',
            'tax',
            'prod',
            'manp',
            'trade_goods',
            'city',
            'cost',
            'fort',
            'discovered',
            'modifiers',
        ],
        'drop_from_print'       : [
            # Those will not be displayed when using _print()
            'filename',
            'discovered',
            'modifiers',
        ],
    }
    ################################
    # Platform-Related differences
    if psys() == 'Windows':
        const['dir_sep'] = '\\'
        const['terminal_clear'] = 'cls'
    else:
        const['dir_sep'] = '/'
        const['terminal_clear'] = 'clear'
    ################################
    if 'id' not in const['column_order']:
        raise_error('Column "id" is not in "column_order" list. Its presence there is necessary.',
            self_contents = True, fatal = True)
    return const



################################
# ERRORS HANDLING
################################
def raise_error(error_type, fatal=False, data=['None'], self_contents = False):
    if type(data) != list:
        data = [data]
    try:
        directory = const['def_dir_sep'].join(data[0].split(const['def_dir_sep'])[-3:])
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
