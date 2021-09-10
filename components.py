def increment_string(stri):
    strings = ""
    num = ""
    inc = 0
    
    for i in range(len(stri)):
        if (stri[i].isdigit()):
            num = num + stri[i]
        else:
            strings += stri[i]
    if(num == ""):
       print("No num found in: ", stri)
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
    
def states_test_14(states):
    #Hard Coded for N = 14
    st = []
    st.append("S")
    st.append("B0")
    st.append("B'0")
    st.append("F0")
    # 1s
    st.append("B1")
    st.append("F1")
    st.append("F'1")
    # 2s
    st.append("B2")
    st.append("F2")
    st.append("F'2")
    # 3's
    st.append("B3")
    # Rs
    st.append("R3")
    st.append("R'3")
    st.append("R2")
    st.append("R'2")
    st.append("R'0")

    passes = []
    missing = st.copy()
    failures = []
    
    for i in range(len(states)):
        if states[i] in st:
            passes.append(states[i])  
            missing.remove(states[i])  
        elif not(states[i] in st):
            failures.append(states[i])

    print("Number Passed: ", len(passes), "Out of: ", len(st))
    for p in passes:
        print("Passed: ", p)
        
    print("Number Failed: ", len(failures), "Out of: ", len(st))
    for p in failures:
        print("Failed: ", p)

    print("Number Missing: ", len(missing), "Out of: ", len(st))
    for p in missing:
        print("Missing: ", p)    

def states_test_27(states):
    #Hard Coded for N = 27
    st = []
    st.append("S")
    st.append("B0")
    st.append("B'0")
    st.append("F0")
    # 1s
    st.append("B1")
    st.append("F1")
    st.append("F'1")
    # 2s
    st.append("B2")
    st.append("F2")
    st.append("F'2")
    # 3's
    st.append("B3")
    st.append("F3")
    st.append("F'3")
    # 4's
    st.append("B4")
    # Rs
    st.append("R4")
    st.append("R'4")
    st.append("R3")
    st.append("R'3")
    st.append("R1")
    st.append("R'1")
    

    passes = []
    missing = st.copy()
    failures = []
    
    for i in range(len(states)):
        if states[i] in st:
            passes.append(states[i])  
            missing.remove(states[i])  
        elif not(states[i] in st):
            failures.append(states[i])

    print("Number Passed: ", len(passes), "Out of: ", len(st))
    for p in passes:
        print("Passed: ", p)
        
    print("Number Failed: ", len(failures), "Out of: ", len(st))
    for p in failures:
        print("Failed: ", p)

    print("Number Missing: ", len(missing), "Out of: ", len(st))
    for p in missing:
        print("Missing: ", p)
              
def affinities_test(aff_dict):
    pass
