from platform import system as psys
################################
# SESSION INIT
def init_settings():
    global settings
    settings = {
        'pandas_max_rows'       : 500,
        'pandas_max_cols'       : 50,
        'pandas_disp_width'     : 250,
        'preceding_blank_line'  : False, # Blank line before every input and error message
        'shorten_region_names'  : True,
        'history_subdir'        : 'provinces', # With out directory separators
        'error_prefix'          : '(Error) ',
        'input_prefix'          : '[Editor] > ',
        'program_header'        : 'EU4 Province Editor v0.1',
        'lcl_languages'         : [
                # Language tags used in localisation files
                'l_english', 'l_spanish', 'l_french', 'l_german',
        ],
        'legal_nonexit_calls'   : [
                # If user calls func that isnt listed here an error is raised
                'load', 'save',
                'apply',
                'select', 'subselect', 'append', 'deselect',
                'sort',
                'set', 'replace', 'inprov',
                'print', 'clear',
                'help',
            ],
        'legal_exit_calls'      : [
                'exit', 'quit', 'leave'
            ],
        'historyfile_keys'      : {
            'cores'         : 'add_core',
            'claims'        : 'add_claim',
            'owner'         : 'owner', #conrtoller
            'culture'       : 'culture',
            'religion'      : 'religion',
            'hre'           : 'hre',
            'tax'           : 'base_tax',
            'prod'          : 'base_production',
            'manpwr'        : 'base_manpower',
            'trade_goods'   : 'trade_goods',
            'capital'       : 'capital',
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
            # area, region, segion, id, filename
        'column_order'          : [
            'id', 'filename', 'capital', 'tax', 'owner', 'cores', 'modifiers',
            'area', 'region', 'segion'
        ],
    }
    ################################
    # Platform-Related differences
    if psys() == 'Windows':
        settings['dir_sep'] = '\\'
        settings['term_clear'] = 'cls'
    else:
        settings['dir_sep'] = '/'
        settings['term_clear'] = 'clear'
    ################################
    return settings



################################
# ERRORS HANDLING
################################
def raise_error(error_type, fatal=False):
    print(settings['error_prefix'], end = "")
    messages = {
        'illegal_call'          : 'Unrecognized function',
        'unknown_subcall'       : 'Unrecognized parameter for called function',
        'too_many_arguments'    : 'Function recieved too many arguments',
        'too_less_arguments'    : 'Function recieved not enough arguments',
        'data_not_loaded'       : 'No data was loaded',
        'data_not_selected'     : 'No data was selected',
        'unknown_attribute'     : 'Unrecognized column name',
        'filestream_error'      : 'Selected file does not exist or the permission was denied',
        'unknown_fstr_error'    : 'Unknown error occured during file loading',
        'encoding_bom_error'    : 'Loaded file uses encoding with BOM and can not be loaded', # depracated
        'nolocalisation_error'  : 'Could not load localisation. Check files and language tags',
        'hparser_equal_sign'    : 'Syntax error in province-history file',
    }
    print(messages[error_type])
    if fatal:
        print("Program Terminated")
        exit(1)
