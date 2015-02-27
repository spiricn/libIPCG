import re

def nameToDefine(name):
    res = ''
    
    for word in re.findall('[A-Z][a-z]*', name):
        res += word.upper() + '_'

    return res[:-1]
