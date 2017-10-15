from pandas import DataFrame#, read_csv, to_csv
import pandas as pd
from os import getcwd, listdir
from platform import system as psys
import yaml
import script

################################
# INITIALISE SESSION
def init(_settings):
    global settings
    settings = _settings

################################
# LOAD FILE AND REMOVE COMMENTS
################################
def getfile(fdir):
    data = open(fdir).read().split('\n')
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
        #print(depth, '"'+word+'"', ' '*(25-len(word)), master)
        if depth == pardepth:
            result[master] = members
            master = word
            members = []
        if depth == memdepth:
            members.append(word)

    #for key in result:
    #    value = result[key]
    #    print(key, ' '*(30-len(key)), value)
    return result

################################
# CONVERT REGIONING DATA TO DICTIONARY (ProvID as key)
def merge_regions(segions, regions, areas):
    #print(regions)
    pass

################################
# RECURSIVE WORDLIST ANALYSIS (used in LOAD)
def getscope(data):
    depth = 0
    index = 0
    key = ('none '*4).split()
    inquotes = False
    result = {}
    subscope = []
    for word in data:
        first = False
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
            if inquotes:
                first = True
        if index == 0:
            key = word
        if index == 2:
            value = word
            if value == '}':
                subscope = subscope[1:]
                try: # NEXT RECURSION DEPTH
                    result[key].append(getscope(subscope))
                except KeyError:
                    result[key] = [getscope(subscope)]
            else:
                try:
                    result[key].append(value)
                except KeyError:
                    result[key] = [value]
        index = (index+1)%3
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
# MAIN GAME FILE LOAD PROCEDURE
def load(location):
    cwd = getcwd()
    if psys() == 'Windows':
        sep = '\\'
    else:
        sep = '/'
    histdir = cwd + sep + location + sep + settings['history_subdir'] + sep
    datadir = cwd + sep + location + sep
    ################################
    segions = getregions(getfile(datadir + 'superregion.txt').split()   , 1)
    regions = getregions(getfile(datadir + 'region.txt').split()        , 2)
    areas   = getregions(getfile(datadir + 'area.txt').split()          , 1)
    regioning = merge_regions(segions, regions, areas)
    ################################
    localisation = {}
    with open(datadir + 'localisation.yml', 'r', encoding = 'utf-8-sig') as stream:
        try:
            localisation = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if localisation == {}:
        script.raise_error('nolocalisation_error')
    ################################
    rows = []
    for filename in listdir(histdir):
        provid = getid(filename)
        fdir = histdir + filename
        data = getscope(getfile(fdir).split())
        province = {}
        for datakey in settings['historyfile_keys']:
            provkey = settings['historyfile_keys'][datakey]
            if type(provkey) == list:
                keys = provkey
            else:
                keys = [provkey]
            try:
                value = getvalue(keys, data)
                #try:
                #    value = list(map(lambda x: int(x), value))
                #except ValueError:
                #    pass
            except KeyError:
                value = []
            #print(datakey, ' '*(12-len(datakey)), value)
            province[datakey] = value
        ################################
        row = []
        for key in settings['column_order']:
            if key == 'id':
                row.append(provid)
            elif key == 'filename':
                row.append(filename)
            else:
                row.append('&'.join(province[key]))
                print(province[key])
        #row = list(map(lambda x: str(x) (row)))
        rows.append(row)
    ################################
    #exit()
    df = DataFrame(rows, columns = settings['column_order'])
    return df






def save(arg1, arg2):
    print('Function is not available.')
