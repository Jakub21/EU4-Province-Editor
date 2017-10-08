import gamefiles
import pandas as pd
import codecs, sys, os
from platform import system as psys


################################
# SESSION INIT / ERRORS HANDLING / HELP DISPLAY
################################
def init_session():
    pd.set_option('display.max_rows', 2800)
    #default buffer size in programs:
        #PowerShell : 3000
        #CMD        : 9001
    pd.set_option('display.max_columns', 50)
    pd.set_option('display.width', 1000)
    global error_prefix
    global input_prefix
    global legal_nonexit_calls
    global legal_exit_calls
    global line_before_calls
    global legal_settingnames
    global program_header
    line_before_calls = False
    program_header = 'EU4 Province Editor version 0.1.0'
    error_prefix = '(Error) '
    input_prefix = '[Editor] > '
    if line_before_calls:
        error_prefix = '\n' + error_prefix
        input_prefix = '\n' + input_prefix
    legal_nonexit_calls = [
        'load',
        'save',
        'apply',
        'select',
        'subselect',
        'append',
        'deselect',
        'where',
        'wherenot',
        'sort',
        'set',
        'replace',
        'inprov', #set attr of single prov to value
        'print',
        'clear', #clear screen
        'help',
        #'settings', #
    ]
    legal_exit_calls = [
        'exit', 'quit', 'leave',
    ]
    return


def raise_error(error_type, fatal=False):
    print(error_prefix, end = "") #PREFIX
    if error_type == 'illegal_call':
        print('Unrecognized function')
    if error_type == 'unknown_subcall': #FuncAttr
        print('Unrecognized parameter for called function')
    if error_type == 'too_many_arguments':
        print('Function recieved too many arguments')
    if error_type == 'too_less_arguments':
        print('Function recieved not enough arguments')
    if error_type == 'data_not_loaded':
        print('Can not execute this function. Data not found')
    if error_type == 'data_not_selected':
        print('Can not execute this function. Selection not found')
    if error_type == 'unknown_attribute': #DataAttr
        print('Unknown province attribute. Use legal column names')
    if error_type == 'filestream_error':
        print('Selected file does not exist or the permission was denied')
    if error_type == 'encoding_bom_error':
        print('Loaded file uses encoding with BOM and can not be loaded')

    if fatal:
        print("Program Terminated")
        exit(1)


def show_usage(funcname): #TODO: Messages should be re-written
    i = " "*4
    if funcname == None:
        print('-'*32)
        print("EU4 Province Editor")
        print("Jakub21, October 2017")
        print("Visit github.com/Jakub21 for readme and updates")
    if funcname in [None, 'load']:
        print('-'*32)
        print("LOAD")
        print(i, "LOAD ['sheet'/'game'] [directory]")
        print(i, "Load data from external source (Called AllData from now on)")
    if funcname in [None, 'save']:
        print('-'*32)
        print("SAVE")
        print(i, "SAVE ['sheet'/'game'] [directory]")
        print(i, "Save AllData to file(s)")
    if funcname in [None, 'apply']:
        print('-'*32)
        print("APPLY")
        print(i, "Copy data from selection to AllData")
    if funcname in [None, 'select']:
        print('-'*32)
        print("SELECT")
        print(i, "Select provinces in which [attribute] is [value]. Uses AllData as source")
        print(i, "SELECT [attribute] [value]")
    if funcname in [None, 'subselect']:
        print('-'*32)
        print("SUBSELECT")
        print(i, "Same as 'select' but use current selection as source")
        print(i, "SUBSELECT [attribute] [value]")
    if funcname in [None, 'append']:
        print('-'*32)
        print("APPEND")
        print(i, "To current selection append provinces where [attribute] is [value]")
        print(i, "APPEND [attribute] [value]")
    if funcname in [None, 'deselect']:
        print('-'*32)
        print("DESELECT")
        print(i, "From current selection remove provinces where [attribute] is [value]")
        print(i, "DESELECT [attribute] [value]")
    if funcname in [None, 'where']:
        print('-'*32)
        print("WHERE")
        print(i, "Unused")
    if funcname in [None, 'wherenot']:
        print('-'*32)
        print("WHERENOT")
        print(i, "Unused")
    if funcname in [None, 'sort']:
        print('-'*32)
        print("SORT")
        print(i, "Sort [data] by [attributes]")
        print(i, "SORT ['all'/'selection'] [attributes(lists allowed)]")
    if funcname in [None, 'set']:
        print('-'*32)
        print("SET")
        print(i, "In selection set [attribute] with [value]")
        print(i, "SET [attribute] [value]")
    if funcname in [None, 'replace']:
        print('-'*32)
        print("REPLACE")
        print(i, "In selection, where [attribute] is [oldvalue], set [attribute] to [newvalue]")
        print(i, "SET [attribute] [oldvalue] [newvalue]")
    if funcname in [None, 'inprov']:
        print('-'*32)
        print("INPROV")
        print(i, "In province with id [provID] set [attribute] as [value]")
        print(i, "INPROV [provID] [attribute] [value]")
    if funcname in [None, 'print']:
        print('-'*32)
        print("PRINT")
        print(i, "Show selection on screen. Use ['all'] to show all data")
        print(i, "PRINT ?['all']")
    if funcname in [None, 'clear']:
        print('-'*32)
        print("CLEAR")
        print(i, "Clear terminal")
    if funcname in [None, 'help']:
        print('-'*32)
        print("HELP")
        print(i, "Display this message. Specify funcname to only show help for this function")
        print(i, "HELP ?[funcname]")
    if funcname == None:
        print('-'*32)
        print("EXIT")
        print(i, "Those will exit program: \""+ '", "'.join(legal_exit_calls)+'"')

################################
# FILES MANIPULATION
################################
def load(ltype, location, depth):
    encoding = 'utf-8'
    if ltype == 'sheet':
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
        except UnicodeDecodeError:
            raise_error('encoding_bom_error')
    if ltype == 'game':
        try:
            return gamefiles.load(location)
        except (FileNotFoundError, PermissionError):
            raise_error('filestream_error')

################################
def save(ltype, data, location):
    if ltype == 'sheet':
        #try:
        return data.to_csv(location)
        #except:
        #    print("ERROR:Script:Save (Sheet)")
    if ltype == 'game':
        try:
            return gamefiles.save(data, location)
        except:
            print("ERROR:Script:Save (Game)")


################################
# INPUT ANALYSIS
################################
def interactive():
    '''Analysis of input. Calls relevant functions.'''
    prefixes = { #PrefixName : RequiredWordsCount (include prefix itself)
        'where'     : 3,
        'wherenot'  : 3,
        'onlyprint' : 1,
    }
    data = None
    selection = None
    while True:
        call = input(input_prefix).split()

        if len(call) == 0:
            continue #Empty input

        funcname = call[0]

        if funcname in legal_exit_calls:
            break

        if funcname not in legal_nonexit_calls:
            raise_error('illegal_call', funcname)

        ################################
        # ARGUMENTS AND SUB-CALLS PARSING
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
            try:
                data.update(selection)
            except: #No possible errors found so far
                raise


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
                data.sort_values(attrlist, inplace = True)
            elif scope == 'selection':
                selection.sort_values(attrlist, inplace = True)
            else: raise_error('unknown_subcall')


        if funcname == 'set':
            selection.loc[:, attribute] = [values][0] #Somewhat works


        if funcname == 'replace': #Separate argument parser
            try:
                oldvalue = call[1]
                newvalue = call[2]
            except:
                show_usage(funcname)
                continue
            selection.replace(oldvalue, newvalue, inplace = True)
            #TODO: Pandas Function takes no arg
                #specifying which column should be affected


        if funcname == 'inprov': #Separate argument parser
            try:
                provid = int(call[1])
                attribute = call[2]
                values = call[3]
            except:
                show_usage(funcname)
                continue
            #data.set_value(provid, attribute, value) #TODO: Is it in-place?
            selection.loc[provid, attribute] = [values][0]


        if funcname == 'print': #Separate argument parser
            mode = None
            printwhere_has_args = False
            try:
                mode = call[1]
                try:
                    attribute = call[2]
                    values = call[3]
                    printwhere_has_args = True
                except: pass #Only required if mode is 'where'
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
                    raise_error('unknown_attribute', attribute)
                    continue
            else:
                raise_error('unknown_subcall')


        if funcname == 'clear':
            if psys() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')
            print(program_header)


        if funcname == 'help':
            funcname = None
            try:
                funcname = call[1].lower()
            except: pass #Argument is optional
            show_usage(funcname)



################################
# MAIN
################################

def main():
    init_session()
    print(program_header)
    interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n"+ "-"*32 + "\nProgram manually terminated\n\n")
    except Exception as e: #Any Unhandled Error
        print("\n"+ "-"*32 + "\nUnhandled error occured: "
        + str(type(e)) + "\n" + "-"*32+"\n\n")
        raise
