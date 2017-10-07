import gamefiles
import pandas as pd
import codecs, sys, os


################################
# SESSION INIT / ERRORS HANDLING / HELP DISPLAY
################################
def init_session():
    pd.set_option('display.max_rows', 2800) #default PowerShell buffer size is 3K
    pd.set_option('display.max_columns', 50)
    pd.set_option('display.width', 1000)
    global error_prefix
    global input_prefix
    global legal_nonexit_calls
    global legal_exit_calls
    error_prefix = '\n[Error] '
    input_prefix = '\n[Editor] > '
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
    ]
    legal_exit_calls = [
        'exit',
        'quit',
    ]
    return


def raise_error(error_type, content='', fatal=False):
    print(error_prefix, end = "") #PREFIX
    if error_type == 'illegal_call':
        print('Unrecognized function: "'+content+'"')
    if error_type == 'unknown_subcall': #FuncAttr
        print('Unrecognized parameter for called function')
    if error_type == 'too_many_arguments':
        print('Function recieved too many arguments')
    if error_type == 'data_not_loaded':
        print('Can not execute this function. Data not found')
    if error_type == 'data_not_selected':
        print('Can not execute this function. No data was selected')
    if error_type == 'unknown_attribute': #DataAttr
        print('Unknown attribute "'+content+'". Use legal column names')
    if error_type == 'filestream_error':
        print('Selected file does not exist or the permission was denied')

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
        print(i, "Copy data from selected scope to AllData")
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
        print(i, "In selected provinces set [attribute] with [value]")
        print(i, "SET [attribute] [value]")
    if funcname in [None, 'replace']:
        print('-'*32)
        print("REPLACE")
        print(i, "In selected provinces, where [attribute] is [oldvalue], set [attribute] to [newvalue]")
        print(i, "SET [attribute] [oldvalue] [newvalue]")
    if funcname in [None, 'inprov']:
        print('-'*32)
        print("INPROV")
        print(i, "In province with id [provID] set [attribute] as [value]")
        print(i, "INPROV [provID] [attribute] [value]")
    if funcname in [None, 'print']:
        print('-'*32)
        print("PRINT")
        print(i, "Show selected data on screen. Use ['all'] to show all data")
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
            ################
            BUFSIZE = 4096
            BOMLEN = len(codecs.BOM_UTF8)
            with open(location, "r+b") as fp:
                chunk = fp.read(BUFSIZE)
                if chunk.startswith(codecs.BOM_UTF8):
                    i = 0
                    chunk = chunk[BOMLEN:]
                    while chunk:
                        fp.seek(i)
                        fp.write(chunk)
                        i += len(chunk)
                        fp.seek(BOMLEN, os.SEEK_CUR)
                        chunk = fp.read(BUFSIZE)
                    fp.seek(-BOMLEN, os.SEEK_CUR)
                    fp.truncate()
            #with open(location, "r") as fp:
            #    return fp.read()
            ################
            if depth < 3:
                load(ltype, location, depth+1)
            else:
                raise
    if ltype == 'game':
        try:
            return gamefiles.load(location)
        except (FileNotFoundError, PermissionError):
            raise_error('filestream_error')

################################
def save(ltype, location):
    if ltype == 'sheet':
        try:
            return pd.to_csv(location)
        except:
            print("ERROR:Script:Save (Sheet)")
    if ltype == 'game':
        try:
            return gamefiles.save(location)
        except:
            print("ERROR:Script:Save (Game)")


################################
# INPUT ANALYSIS
################################
def interactive():
    '''Analysis of input. Calls relevant functions.'''
    cont = True
    prefixes = { #PrefixName : RequiredWordsCount (include prefix itself)
        'where'     : 3,
        'wherenot'  : 3,
        'onlyprint' : 1,
    }
    data = None
    selected = None
    while cont:
        call = input(input_prefix).split()

        if len(call) == 0:
            continue

        funcname = call[0]

        if funcname in legal_exit_calls:
            cont = False
            break

        if funcname not in legal_nonexit_calls:
            raise_error('illegal_call', funcname)

        ################################
        # INTERACTIVE FUNCTIONS
        ################################

        if funcname == 'load':
            try:
                subcall = call[1]
                directory = call[2]
            except:
                show_usage('load')
                continue
            if subcall not in ['sheet', 'game']:
                raise_error('unknown_subcall')
                continue
            data = load(subcall, directory, 0)


        if funcname == 'save':
            try:
                subcall = call[1]
                directory = call[2]
            except:
                show_usage('save')
                continue
            if subcall not in ['sheet', 'game']:
                raise_error('unknown_subcall')
                continue
            data = save(subcall, directory)


        if funcname == 'apply':
            try:
                subcall = call[1]
                raise_error('too_many_arguments')
                continue
            except:
                pass
            if data == None: #Data is not loaded
                raise_error('data_not_loaded', 'apply')
            data.update(selected)


        if funcname == 'select':
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
                    continue #TODO: Explain: When using unknown attr pandas says theres key error
            try:
                selected = data.loc[data[attribute].isin(values)]
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute', attribute)


        if funcname == 'subselect':
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
                    continue #TODO: Explain: Same as above
            try:
                selected = selected.loc[data[attribute].isin(values)]
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute', attribute)


        if funcname == 'append':
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
                    continue #TODO: Explain: Same as above
            try:
                newselect = data.loc[data[attribute].isin(values)]
                newselect.update(selected)
                selected = newselect
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute', attribute)


        if funcname == 'deselect':
            try:
                attribute = call[1]
                values = call[2:]
            except:
                show_usage(funcname)
                continue
            try:
                data = data[~data[attribute].isin(values)] # ~ negation
            except (AttributeError, TypeError):
                raise_error('data_not_loaded')
            except KeyError:
                raise_error('unknown_attribute', attribute)


        if funcname == 'sort':
            try:
                scope = call[1]
                attrlist = call[2:]
            except:
                show_usage(funcname)
                continue
            if scope == 'all':
                data.sort_values(attrlist, inplace = True)
            elif scope == 'selection':
                selected.sort_values(attrlist, inplace = True)
            else: raise_error('unknown_subcall')


        if funcname == 'set':
            try:
                attribute = call[1]
                value = call[2]
            except:
                show_usage(funcname)
                continue
            #data[attribute] = value #TODO


        if funcname == 'replace':
            try:
                oldvalue = call[1]
                newvalue = call[2]
            except:
                show_usage(funcname)
                continue
            data.replace(oldvalue, newvalue, inplace = True)
            #TODO: No info about which column should be affected


        if funcname == 'inprov':
            try:
                provid = call[1]
                attribute = call[2]
                value = call[3]
            except:
                show_usage(funcname)
                continue
            data.set_value(provid, attribute, value) #TODO: Is it in-place?


        if funcname == 'print':
            mode = None
            try:
                mode = call[1]
            except: pass #Argument is optional
            if mode == None:
                print(selected)
            elif mode == 'all':
                print(data)
            else:
                raise_error('unknown_subcall')


        if funcname == 'clear':
            os.system('cls')

        if funcname == 'help':
            funcname = None
            try:
                funcname = call[1].lower()
            except: pass
            show_usage(funcname)



################################
# MAIN
################################

def main():
    print('EU4 Province Editor  |  Jakub21  |  October 2017')
    init_session()
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
