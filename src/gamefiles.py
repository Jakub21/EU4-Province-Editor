from src.meta import raise_error
from pandas import DataFrame
from os import getcwd, listdir
import yaml

################################################################
# LOAD GAME
################################################################

################################
# INITIALISE SESSION
def init(_settings):
    global settings
    settings = _settings
    global cwd
    cwd = getcwd()

################################
# LOAD FILE AND REMOVE COMMENTS
def getfile(fdir):
    try:
        data = open(fdir).read().split('\n')
    except FileNotFoundError:
        raise_error('filestream_error', False, fdir)
        return None
    ndata = ''
    for line in data:
        nline = ''
        for c in line:
            if c in '#\r\n':
                break
            if c == '\t':
                c = ' '
            if c in '{=}':
                c = ' ' + c + ' '
            nline += c
        ndata += nline + ' '
    return ndata

################################
# LOAD REGION DATA
def getregions(wordlist, memdepth):
    pardepth = 0
    depth = 0
    master = 'none'
    members = []
    result = {}
    for word in wordlist:
        depth += word.count("{")
        depth -= word.count("}")
        if word in "{=}colorareas":
            continue
        if depth == pardepth:
            result[master] = members
            master = word
            members = []
        if depth == memdepth:
            members.append(word)
    return result

################################
# CONVERT REGIONING DATA TO DICTIONARY (ProvID as key)
def merge_regions(segions, regions, areas):
    ################
    def _find(search_key, scope):
        for key in scope:
            value = scope[key]
            if search_key in value: # 'value' is list
                return key
    ################
    result = {}
    for area in areas:
        region = _find(area, regions)
        segion = _find(region, segions)
        provlist = areas[area]
        area_name = area
        region_name = region
        segion_name = segion
        if settings['shorten_region_names']:
            try:
                if area_name.endswith('_area'):
                    area_name = area_name[:-5]
            except AttributeError: #None
                area_name = 'none'
            try:
                if region_name.endswith('_region'):
                    region_name = region_name[:-7]
            except AttributeError: #None
                area_name = 'none'
            try:
                if segion_name.endswith('_superregion'):
                    segion_name = segion_name[:-12]
            except AttributeError: #None
                area_name = 'none'
        for province in provlist:
            result[province] = [area_name, region_name, segion_name]
    return result


################################
# RECURSIVE WORDLIST ANALYSIS (used in LOAD)
def getscope(data, r_depth = 0):
    key_index = 1
    val_index = 0
    eqs_index = 2
    depth = 0
    index = 1
    total_index = 0
    key = 'none'
    inquotes = False
    quoted = ''
    value = ''
    result = {}
    subscope = []
    for word in data:
        #print(r_depth, index, depth, word, sep = '\t')
        last = False
        if word == '{':
            depth += 1
        if word == '}':
            depth -= 1
        if depth > 0:
            subscope.append(word)
            continue
        else:
            if word != '}':
                subscope = []
        if word.count('"') == 1:
            inquotes = not inquotes
            if not inquotes:
                last = True
            else:
                quoted = ''
        if inquotes:
            quoted += word + ' '
        if last:
            quoted += word
            value = quoted
        if index == key_index:
            key = word
        if index == val_index:
            if not last:
                value = word
            if inquotes:
                continue
            if value == '}':
                subscope = subscope[1:]
                try: # NEXT RECURSION DEPTH
                    result[key].append(getscope(subscope, r_depth+1))
                except KeyError:
                    result[key] = [getscope(subscope, r_depth+1)]
                except TypeError: # Move exception level up
                    return None
            else:
                try:
                    result[key].append(value)
                except KeyError:
                    result[key] = [value]
        if index == eqs_index:
            if word != '=':
                return None
        index = (index+1)%3
        total_index += 1
    return result

################################
# RECURSIVE VALUE RETRIEVER (used in LOAD)
def getvalue(keys, data):
    if len(keys) == 1:
        return data[keys[0]]
    else:
        q = []
        for sub in data[keys[0]]:
            q += getvalue(keys[1:], sub)
        return q

################################
# GET PROVINCE ID FROM FILENAME
def getid(filename):
    numbers = '0123456789'
    result = ''
    for c in filename:
        if c not in numbers:
            break
        result += c
    return result

################################
# REMOVE NUMBERS AFTER COLONS
def prepare_yaml(data):
    numbers = ''.join(map(lambda x: str(x), range(10)))
    result = ''
    prev = ''
    for c in data:
        if (prev == ':') and (c in numbers):
            c = ''
        result += c
        prev = c
    return result

################################
# MAIN GAME FILE LOAD PROCEDURE
def load(location):
    sep = settings['dir_sep']
    histdir = cwd + sep + location + sep + settings['history_subdir'] + sep
    datadir = cwd + sep + location + sep
    ################################
    segions = getregions(getfile(datadir + 'superregion.txt').split()   , 1)
    regions = getregions(getfile(datadir + 'region.txt').split()        , 2)
    areas   = getregions(getfile(datadir + 'area.txt').split()          , 1)
    if (type(segions) == None) or (type(regions) == None) or (type(areas) == None):
        return None
    regioning = merge_regions(segions, regions, areas)
    ################################
    localisation = {}
    with open(datadir + 'localisation.yml', 'r', encoding = 'utf-8-sig') as stream:
        content = prepare_yaml(stream.read())
        try:
            rlcl = yaml.load(content) # Whole Yaml file loaded to dict
        except yaml.YAMLError as e:
            print(e)
            return
    for lang in settings['lcl_languages']:
        try:
            localisation = rlcl[lang]
            break
        except KeyError:
            pass
    if localisation == {}:
        raise_error('nolocalisation_error', False)
        return
    ################################
    rows = []
    for filename in listdir(histdir):
        fdir = histdir + filename
        data = getscope(getfile(fdir).split())
        if type(data) == None:
            raise_error('hparser_equal_sign', False, [fdir])
            return
        province = {}
        provid = getid(filename)
        if provid == '':
            continue
        province['id']          = int(provid)
        province['filename']    = filename
        province['name']        = localisation['PROV'+provid]
        province['area']        = regioning[provid][0]
        province['region']      = regioning[provid][1]
        province['segion']      = regioning[provid][2]
        for datakey in settings['historyfile_keys']:
            provkey = settings['historyfile_keys'][datakey]
            if type(provkey) == list:
                keys = provkey
            else:
                keys = [provkey]
            try:
                value = getvalue(keys, data)
            except KeyError:
                value = []
            province[datakey] = value
        ################################
        row = []
        for key in settings['column_order']:
            value = province[key]
            #print(value)
            if type(value) == list:
                row.append(settings['multival_sep'].join(value))
            else:
                row.append(value)
        rows.append(row)
    ################################
    df = DataFrame(rows, columns = settings['column_order'])
    df.set_index('id', inplace = True)
    return df




################################################################
# SAVE GAME
################################################################

def save(data, location):
    idlist = data.index.values
    data = data.values.tolist()
    columns = settings['column_order'][1:] # 1st is ID and it is not in values so it should be excluded
    prov_index = 0
    for row in data:
        provid = idlist[prov_index]
        text = '#Province no.' + str(provid) + '\n\n'
        filename = 'None'
        for i in range(len(columns)):
            cname = columns[i]
            value = row[i]
            if cname == 'filename':
                filename = value
            try:
                key = settings['historyfile_keys'][cname]
            except KeyError:
                continue # Element should not be saved (eg. Filename or ID)
            if settings['multival_sep'] in value:
                value = value.split(settings['multival_sep'])
            else:
                value = [value]
            for element in value:
                if element == '':
                    continue
                if type(key) == str:
                    text += key + ' = ' + element + '\n'
                else:
                    if len(key) < 2:
                        print('Error (SaveGame:CreateHistoryFile)')
                    #NOTE: There should be proper converter for this.
                    text += key[0] + ' = {\n'
                    text += '    ' + key[1] + ' = ' + element + '\n'
                    text += '    ' + 'duration = -1\n' #TODO
                    text += '}\n'
        prov_index += 1
        sep = settings['def_dir_sep']
        open(cwd+sep+ location+sep+ filename, 'w').write(text)
