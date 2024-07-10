def rid_pipes(top, bottom):
    """
    removes unneccesary pipes

    inputs:
        '|  |  |  |  |  |  |  |'    # bottom
        '   9           8     7'    # top

    returns:
        '   |           |     |'
    """
    out = ''
    for t,b in zip(top, bottom):
        if t == ' ': out += ' '
        else: out += b
    return out

def rid_underscores(top, bottom):
    """
    removes unnecessary underscores

    inputs:
        ' _4__  _ __  _6__  _7__'   # bottom
        '    |           |     |'   # top

    returns:
        '  4__         6__   7__'
    """
    out = bottom
    l = r = -1
    for i, ch in enumerate(bottom):
        if ch == '_':
            if l < 0: l = i
            r = i

        else:
            if l >= 0 and ('|' not in top[l:r+1]):
                out = out[:l] + ' '*(r-l+1) + out[r+1:]
            l = r = -1
    return out

b = '_4__  _ __  _6__  _7__'   # bottom
t = '   |           |     |'   # top

# print(rid_underscores(t, b))


def audit(rows: list[str]):
    rows[0] = rows[0].replace('?', ' ')
    for i in range(len(rows)-1):
        # change bottom based on top
        top = rows[i]
        bottom = rows[i+1]
        
        if i%2 == 1:
            # top contains pipes, bottom contains values
            bottom = bottom.replace('?', ' ')
            rows[i+1] = rid_underscores(top, bottom)
        else:
            # bottom contains pipes, top contains values:=
            rows[i+1] = rid_pipes(top, bottom)

    return rows
