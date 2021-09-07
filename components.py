def increment_string(stri):
    strings = ""
    num = ""
    inc = 0
    
    for i in range(len(stri)):
        if (stri[i].isdigit()):
            num = num+ stri[i]
        else:
            strings += stri[i]
    if(num.isEmpty()):
       strings += "1"
       return strings
    else:            
        inc = int(num) + 1
        fin = strings + str(inc)
        return fin

def make_prime(stri):
    strings = ""
    num = ""

    for i in range(len(stri)):
        if (stri[i].isdigit()):
            num = num+ stri[i]
        else:
            strings += stri[i]
    strings = strings + "'"
    if(num == ""):
        return strings
    fin = strings + num
    return fin
    
