'''
--------------------------------
EU4 Province Editor
Jakub21, October 2017
Published and Developed on GitHub
github.com/Jakub21/EU4-Province-Editor
--------------------------------
Shell-styled province editor.
Generates files readable for game
--------------------------------
Explaination of usage symbols
<keyword>   - Only use words listed next to keyword or function will not be launched
[value]     - Any value is allowed OR allowed values depend on loaded data
(value)     - Just like above but multiple words are allowed
?           - Prefix indicating that argument is optional
Alldata     - Main data scope. 'load' and 'append' functions are only that affect it.
                When 'save', 'select' or 'append' is used - Data is loaded from this scope.
Selection   - Current selection. Every function that modifies data operates here.
                Function 'apply' moves data from Selection to AllData
--------------------------------
Usage of Interactive Functions
    load <mode> [location]
        <mode>  'sheet'     - load from CSV
                'game'      - load from directory with game-like files
        [location] - Location of file/directory. Must be subdir of location of script
    save <mode> [location]
        <mode>  'sheet'     - save to CSV
                'game'      - generate game-readable files
        [location] - Location of files. Subdirectory of location of script
    apply
        Update Alldata with changes from Selection
    select [attribute] (value)
        [attribute] - Name of column that will be searched for values
        (value)     - Provinces with those values will create selection
    subselect [attribute] (value)
        [attribute] - Name of column that will be searched for values
        (value)     - Provinces with values OTHER than this will be removed from selection
    append
        [attribute] - Name of column that will be searched for values
        (value)     - Provinces with those values will be added to selection
        Append provinces to selection
    sort <scope> (attribute)
        <scope> 'all'       - Alldata will be sorted
                'selection' - Selection will be sorted
        (attribute) Column names data should be sorted by
        Sort data
    set [attribute] [value]
        [attribute] - Column to change
        [value] - Value that should be put in column
        Selection is affected
    inprov [id] [attribute] [value]
        [id]        - ID of province to change value in
        [attribute] - Column name
        [value]     - Value to set
    print ?<mode> ?[attribute] ?[value]
        <mode>  'all'       - Print all loaded data
                'selection' - Print whole selection         (FUNCTION'S DEFAULT)
                'all_where' - Print provinces from Alldata when condition is true
                'sel_where' - Print provinces from Selection when condition is true
        [attribute] - Column to look for values in
        [value]     - Value to look for
        'attribute' and 'value' argument are only required when mode is 'all_where' or 'sel_where'
    clear
        Clear screen. No data is affected.
    help
        Show this message
    exit
        Leave program
--------------------------------
Selection info
Creating new selection or reducing previous one discards changes that were not applied
'''



import gamefiles
import pandas as pd
import codecs, sys, os
from platform import system as psys


################################
# SESSION INIT / ERRORS HANDLING / HELP DISPLAY
################################
def apply_settings():
    # Data from global variable
    if settings['preceding_blank_line']:
        settings['error_prefix'] = '\n' + settings['error_prefix']
        settings['input_prefix'] = '\n' + settings['input_prefix']
    pd.set_option('display.max_rows', settings['pandas_max_rows'])
    pd.set_option('display.max_columns', settings['pandas_max_cols'])
    pd.set_option('display.width', settings['pandas_disp_width'])
    pass

def init_session():
    global settings
    settings = {
        'pandas_max_rows'       : 500,
        'pandas_max_cols'       : 50,
        'pandas_disp_width'     : 250,
        'preceding_blank_line'  : False, #Blank line before every input and error message
        'history_subdir'        : '/history/',
        'error_prefix'          : '(Error) ',
        'input_prefix'          : '[Editor] > ',
        'program_header'        : 'EU4 Province Editor v0.1',
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
            'id', 'filename', 'capital', 'tax', 'owner', 'modifiers'
        ],
    }
    ################################
    apply_settings()
    gamefiles.init(settings)
    return


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
        'nolocalisation_error'  : 'Could not load localisation'
    }
    print(messages[error_type])
    if fatal:
        print("Program Terminated")
        exit(1)

################################
# FILES MANIPULATION
################################
def load(ltype, location, depth):
    encodings = ['utf-8', 'utf-8-sig']
    if ltype == 'sheet':
        for encoding in encodings:
            try:
                data = pd.read_csv(location, encoding = encoding)
                for q in ['id', 'ProvID']:
                    try:
                        data.set_index(q, inplace=True)
                        break
                    except: pass
                return data
            except (FileNotFoundError, PermissionError):
                raise_error('filestream_error')
                break # No encoding will open this file if this happens
            except UnicodeDecodeError:
                pass # Intended
    if ltype == 'game':
        #try:
            return gamefiles.load(location)
        #except (FileNotFoundError, PermissionError):
        #    raise_error('filestream_error')

def save(ltype, data, location):
    if ltype == 'sheet':
        data.to_csv(location, encoding = 'utf-8-sig')
    if ltype == 'game':
        try:
            return gamefiles.save(data, location)
        except:
            print("ERROR: Unhandled error occured in Main when tried to call 'gamefiles.save()'")
            raise


################################
# INPUT ANALYSIS
################################
def interactive():
    '''Analysis of input. Calls relevant functions.'''
    data = None #VarName Declaration
    selection = None
    while True:
        call = input(settings['input_prefix']).split()
        if len(call) == 0:
            continue #Empty input
        funcname = call[0]
        if funcname in settings['legal_exit_calls']:
            break
        if funcname not in settings['legal_nonexit_calls']:
            raise_error('illegal_call')

        ################################
        # SUB-CALLS AND ARGUMENTS PARSING
        ################################

        if funcname in ['load', 'save']: #Filestream
            try:
                subcall = call[1]
                directory = call[2]
            except:
                show_usage(funcname)
                continue

        if funcname in ['apply']: #No arguments needed
            try:
                subcall = call[1]
                raise_error('too_many_arguments')
                continue
            except:
                pass

        if funcname in ['select', 'subselect', 'append', 'deselect', 'set']: #Attribute and Value
            try:
                attribute = call[1]
                values = call[2:]
            except:
                show_usage(funcname)
                continue
            if type(values) != list:
                try:
                    values = [values]
                except KeyError:
                    continue
                    #TODO: Explain: When using unknown attr pandas says there's error
                    #NOTE: Copy of this is in interactive > print > mode : where/only


        ################################
        # INTERACTIVE FUNCTIONS
        ################################

        if funcname == 'load':
            if subcall not in ['sheet', 'game']:
                raise_error('unknown_subcall')
                continue
            data = load(subcall, directory, 0)


        if funcname == 'save':
            if subcall not in ['sheet', 'game']:
                raise_error('unknown_subcall')
                continue
            data = save(subcall, data, directory)


        if funcname == 'apply':
            data.update(selection) #No possible errors found so far


        if funcname in ['select', 'subselect']:
            try:
                if funcname == 'select':
                    selection = data.loc[data[attribute].isin(values)]
                if funcname == 'subselect':
                    selection = selection.loc[data[attribute].isin(values)]
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute')


        if funcname == 'append':
            try:
                newsel = data.loc[data[attribute].isin(values)]
                selection = pd.concat([selection, newsel])
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute')


        if funcname == 'deselect':
            print("(SCRIPT) Function is not done yet and has no effect.")
            pass #TODO


        if funcname == 'sort':
            try:
                scope = call[1]
                attrlist = call[2:]
            except:
                raise_error('too_less_arguments')
                continue
            if attrlist == ['location']: #TEMP - Only works with CSV used for tests
                attrlist = ['segion', 'region', 'area']
            if scope == 'all':
                try:
                    data.sort_values(attrlist, inplace = True)
                except AttributeError:
                    raise_error('data_not_loaded')
            elif scope == 'selection':
                try:
                    selection.sort_values(attrlist, inplace = True)
                except AttributeError:
                    raise_error('data_not_selected')
            else: raise_error('unknown_subcall')


        if funcname == 'set':
            selection.loc[:, attribute] = [values][0]


        if funcname == 'replace': #Separate argument parser
            try:
                oldvalue = call[1]
                newvalue = call[2]
            except:
                show_usage(funcname)
                continue
            selection.replace(oldvalue, newvalue, inplace = True)
            #TODO: Pandas Function takes no arg specifying which column should be affected


        if funcname == 'inprov': #Separate argument parser
            try:
                provid = int(call[1])
                attribute = call[2]
                values = call[3]
            except:
                show_usage(funcname)
                continue
            selection.loc[provid, attribute] = [values][0]
            #NOTE: Pandas message about indexing and copying is displayed


        if funcname == 'print': #Separate argument parser
            mode = None
            printwhere_has_args = False
            try:
                mode = call[1]
                try:
                    attribute = call[2]
                    values = call[3]
                    printwhere_has_args = True
                except: pass #Only required if mode is 'where' or 'only'
            except: pass #Argument is optional
            if mode == None:
                print(selection)
            elif mode == 'all':
                print(data)
            elif mode in ['where', 'only']:
                if not printwhere_has_args:
                    raise_error('too_less_arguments')
                try:
                    if type(values) != list:
                        try:
                            values = [values]
                        except KeyError:
                            continue #NOTE
                    if mode == 'where':
                        psel = data.loc[data[attribute].isin(values)]
                    if mode == 'only':
                        psel = selection.loc[data[attribute].isin(values)]
                    print(psel)
                except (AttributeError, TypeError):
                    raise_error('data_not_loaded')
                    continue
                except KeyError:
                    raise_error('unknown_attribute')
                    continue
            else:
                raise_error('unknown_subcall')


        if funcname == 'clear':
            if psys() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            print(settings['program_header'])


        if funcname == 'help':
            print(__doc__)



################################
# MAIN
################################

def main():
    init_session()
    print(settings['program_header'])
    interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n"+ "-"*32 + "\nProgram manually terminated\n"+ "-"*32+"\n\n")
    except Exception as e: #Any Unhandled Error
        print("\n"+ "-"*32 + "\nUnhandled error occured: "
        + str(type(e).__name__) + "\n" + "-"*32+"\n\n")
        raise
