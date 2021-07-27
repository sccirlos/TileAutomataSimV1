def increment_string(stri):
    strings = ""
    num = ""
    inc = 0
    
    for i in range(len(stri)):
        if (stri[i].isdigit()):
            num = num+ stri[i]
        else:
            strings += stri[i]
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
    
strg = "A'10"   
increment_string(strg)
stri = "B5"
make_prime(stri)