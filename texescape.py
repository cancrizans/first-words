import re


    
conv = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
}
regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    

def escape(text):
    try:
        return regex.sub(lambda match: conv[match.group()], text)
    except TypeError:
        print("Not a string error:",text)
        return "Null"
