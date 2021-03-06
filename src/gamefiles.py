from src.meta import err_msg
from pandas import DataFrame, isnull
from os import listdir
import yaml


################################
def _init(_const):
    global const
    const = _const
    global numbers
    numbers = ''.join(map(lambda x: str(x), range(10)))


################################
# Load file and remove comments
def getfile(fpath):
    ################
    def rem_cmnt(text):
        ndata = ''
        for line in text.split('\n'):
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
    ################
    try:
        enc = const['histload_prim_enc']
        text = open(fpath, encoding=enc).read()
    except UnicodeDecodeError:
        enc = const['histload_secn_enc']
        text = open(fpath, encoding=enc).read()
    except FileNotFoundError:
        err_msg('FileNotFound', data=fdir)
        return
    text = rem_cmnt(text)
    return text


################################
def getscope(data, rcr_depth=0):
    key_index   = 0
    eqs_index   = 1
    val_index   = 2
    index       = 0     # Base index correction
    rcr_index   = 0     # InDepth index correction
    ssc_cuthead = 1     # How many words remove from subscope head
    depth       = 0
    total_index = 0
    key         = const['none']
    value       = ''
    inquotes    = False
    quoted      = ''
    obr         = '{'
    cbr         = '}'
    eqs         = '='
    quo         = '"'
    sep         = ' ' # For quoted text
    ################
    result = {}
    subscope = []
    ################
    if rcr_depth > 0:
        index = rcr_index
    ################
    for word in data:
        last = False
        fromsub = False
        ################
        if word == obr:
            depth += 1
        elif word == cbr:
            depth -= 1
        ################
        if depth == 0:
            if word != cbr:
                subscope = []
        else:
            subscope.append(word)
            continue
        ################
        if word.count(quo) == 1:
            inquotes = not inquotes
            if inquotes:
                quoted = ''
            else:
                last = True
        ################
        if inquotes:
            quoted += word + sep
        ################
        if last:
            quoted += word
            value = quoted
        ################
        if index == key_index:
            key = word
        elif index == eqs_index:
            if word != eqs:
                return total_index
        elif index == val_index:
            if not last:
                value = word
            if inquotes:
                continue
            ################
            if value == cbr:
                index = (index+1)%3
                subscope = subscope[ssc_cuthead:]
                value = getscope(subscope, rcr_depth+1)
                fromsub = True
            try:
                result[key].append(value)
            except KeyError:
                result[key] = [value]
        ################
        if not fromsub:
            index = (index+1)%3
        total_index += 1
    return result


################################
def get_regioning(attrdir, filepaths):
    ################
    def regfile_analysis(text, mem_depth):
        par_depth = 0
        depth = 0 # Starting
        master = const['none']
        members = []
        result = {}
        for word in text.split():
            depth += word.count('{')
            depth -= word.count('}')
            if word in const['skip_at_region_load']:
                continue
            if depth == par_depth:
                if master != const['none']:
                    result[master] = members
                master = word
                members = []
            if depth == mem_depth:
                members.append(word)
        return result
    ################
    def _find(search_key, scope):
        for key in scope:
            value = scope[key]
            if search_key in value:
                return key
    ################
    def _shorten(name, rtype):
        suffixes = const['regioning_names_suffiexes']
        suffix = suffixes[rtype]
        try:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        except AttributeError:
            name = const['none']
        return name
    ################
    segions = regfile_analysis(getfile(attrdir + filepaths['segion']), 1)
    regions = regfile_analysis(getfile(attrdir + filepaths['region']), 2)
    areas   = regfile_analysis(getfile(attrdir + filepaths['area']),   1)
    if (type(segions)=={}) or (type(regions)=={}) or (type(areas)=={}):
        err_msg('WrongRegionFile')
        return
    ################
    result = {}
    for area in areas:
        region = _find(area, regions)
        segion = _find(region, segions)
        areaprovs = areas[area]
        ################
        # When names are shortened the keys to search for should stay the same
        aname = area
        rname = region
        sname = segion
        ################
        if const['shorten_region_names']:
            aname = _shorten(aname, 'area')
            rname = _shorten(rname, 'region')
            sname = _shorten(sname, 'segion')
        ################
        # Assigning
        for province in areaprovs:
            result[province] = [aname, rname, sname]
    return result


################################
def get_locl(filepath):
    try:
        with open(filepath, 'r', encoding=const['locl_enc']) as f:
            content = f.read()
    except (FileNotFoundError, PermissionError):
        err_msg('AttrFileNotFound', data=filepath)
        return
    ################
    newcontent = ''
    prev = ''
    for c in content:
        if (prev == ':') and (c in numbers):
            c = ''
        newcontent += c
        prev = c
    content = newcontent
    ################
    try:
        full_locl = yaml.load(content)
    except yaml.YAMLError as e:
        err_msg('YAMLError: '+str(e), self_contents=True)
        return
    for lang in const['lcl_languages']:
        try:
            locl = full_locl[lang]
        except KeyError:
            pass
    if locl == {}:
        return
    return locl


################################
# MAIN GAMEFILES LOAD PROCEDURE
def load(histdir, attrdir):
    ################
    def getvalue(keys, data):
        if len(keys) == 1:
            return data[keys[0]]
        else:
            q = []
            for sub in data[keys[0]]:
                q += getvalue(keys[1:], sub)
            if q == 'nan':
                q = ''
            return q
    ################
    def getid(filename):
        result = ''
        for c in filename:
            if c not in numbers:
                break
            result += c
        return result
    ################
    sep = const['dir_sep']
    filenames = const['fnames']
    ################
    regioning = get_regioning(attrdir, const['fnames'])
    localisation = get_locl(attrdir+const['fnames']['provloc'])
    if localisation == None:
        err_msg('LocalisationNotFound')
        return DataFrame
    ################
    provkeys = const['province_attr_keys']
    rows = []
    ################
    try:
        filelist = listdir(histdir)
    except FileNotFoundError:
        err_msg('DirectoryNotFound')
        return DataFrame
    for filename in filelist:
        filedir = histdir + filename
        data = getscope(getfile(filedir).split())
        if type(data) == int:
            err_msg('WrongHistorySyntax', data=filedir)
            return DataFrame
        ################
        province = {}
        provid = getid(filename)
        if provid == '':
            continue
        province[provkeys['id']] = int(provid)
        province[provkeys['fn']] = filename
        province[provkeys['gr']] = ''
        ################################
        try:
            province[provkeys['nm']] = localisation[const['locl_key_prefix']+provid]
        except KeyError: province[provkeys['nm']] = const['default_name']
        try:
            province[provkeys['ar']] = regioning[provid][0]
        except KeyError: province[provkeys['ar']] = const['default_area']
        try:
            province[provkeys['rg']] = regioning[provid][1]
        except KeyError: province[provkeys['rg']] = const['default_region']
        try:
            province[provkeys['sg']] = regioning[provid][2]
        except KeyError: province[provkeys['sg']] = const['default_segion']
        ################################
        for datakey in const['historyfile_keys']:
            provkey = const['historyfile_keys'][datakey]
            if type(provkey) == list:   keys = provkey
            else:                       keys = [provkey]
            try:                        value = getvalue(keys, data)
            except KeyError:            value = []
            province[datakey] = value
        ################
        row = []
        for key in const['column_order']:
            value = province[key]
            if type(value) == list:
                row.append(const['multival_sep'].join(value))
            else:
                row.append(value)
        rows.append(row)
    ################
    df = DataFrame(rows, columns=const['column_order'])
    df.set_index(const['index_column'], inplace=True)
    return df


################################
# MAIN GAMEFILES SAVE PROCEDURE
def save(data, histdir):
    ################
    def _saveline(key, value, maxdepth, depth):
        i = const['indent']
        result = ''
        if depth == maxdepth:
            result += i*depth + key[0] + ' = ' + value + '\n'
        else:
            result += i*depth + key[0] + ' = {\n'
            result += _saveline(key[1:], value, maxdepth, depth+1)
            try:
                result += i*(depth+1) + const['additional_save_info'][key[0]] + '\n'
            except KeyError: pass # Optional
            result += i*depth + '}\n'
        return result
    ################
    try:
        idlist = data.index.values
    except AttributeError:
        err_msg('DataNotLoaded')
        return
    data = data.values.tolist()
    columns = const['column_order']
    columns.remove(const['index_column'])
    sep = const['dir_sep']
    prov_index = 0
    total_provs = len(data)
    ################
    for row in data:
        if const['show_save_toggle']:
            if prov_index % const['show_save_freq'] == 0:
                percentage = str(round((prov_index/total_provs)*100))
                print(const['show_save_msg']+percentage+'%')
        provid = idlist[prov_index]
        text = '#Province no.'+ str(provid) + '\n'*2
        filename = ''
        for i in range(len(columns)):
            cname = columns[i]
            value = row[i]
            if (type(value)==float) and not(isnull(value)):
                value = int(value)
            value = str(value)
            ################
            if cname == 'filename':
                filename = value
            if cname not in const['historyfile_keys'].keys():
                continue
            ################
            key = const['historyfile_keys'][cname]
            if (type(key)==str):
                key = [key]
            ################
            if const['multival_sep'] in value:
                value = value.split(const['multival_sep'])
            else:
                value = [value]
            ################
            for element in value:
                if (element.lower() in const['value_empty']) or (element == ''):
                    continue
                text += _saveline(key, element, len(key)-1, 0)
        filedir = histdir + filename
        open(filedir, 'w', encoding=const['histsave_enc']).write(text)
        prov_index += 1
    if const['show_save_toggle']:
        print('Done.')
    return True
