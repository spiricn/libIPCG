import re

def nameToDefine(context, name):
    res = ''
    
    for word in re.findall('[A-Z][a-z]*', name):
        res += word.upper() + '_'

    return res[:-1]
