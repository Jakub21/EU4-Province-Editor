from os import getcwd
fdir = getcwd() + '\\' + 'data/gdansk.txt'
data = open(fdir).read().split('\n')

ndata = ''
for line in data:
    nline = ''
    for c in line:
        if c in '#\r\n':
            break
        if c in '{=}':
            c = ' ' + c + ' '
        nline += c
    ndata += nline + ' '
data = ndata.split()

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
                subscope = subscope[1:] # remove open bracket
                try:
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



def showlevel(data, i):
    for key in data:
        value = data[key]
        if type(value[0]) != dict:
            print(' '*(4*i), key, ' '*(30-len(key)), ', '.join(data[key]))
        else:
            for subdata in value:
                print(' '*(4*i), key)
                showlevel(subdata, i+1)



result = getscope(data)
showlevel(result, 0)
