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

def make_not_prime(stri):
    strings = ""
    num = ""

    for i in range(len(stri)):
        if (stri[i].isdigit()):
            num = num + stri[i]
        else:
            if not(stri[i] == "'"):
                strings += stri[i]
    if(num == ""):
        return strings
    fin = strings + num
    return fin

def check_is_prime(label):
    if "'" in label:
        return True
    else: return False

def split_prime_label(label):
    if "'" in label:
        split_label = label.split("'")

        split_label[1] = int(split_label[1])
        print(split_label)
        return split_label

def split_nonprime_label(label):
    if "'" in label:
        pass
    else:
        split_label = []
        split_label.append(label[0])
        split_label.append(label[1:])

        if len(split_label) > 1:
            split_label[1] = int(split_label[1])
        print(split_label)
        return split_label

def split_label_pnp(label):
    split_label = []
    if label == "S":
        pass

    elif "'" in label:
        split_label = label.split("'")
        split_label[1] = int(split_label[1])
    else:
        split_label.append(label[0])
        split_num = label[1:]
        split_label.append(int(split_num))
    return split_label

def transition_to_forward(label):
    new_label = "F" + label[1:]
    return new_label

def transition_to_backward(label):
    if not("B'" in label):
        new_label = "B" + label[1:]
        return new_label


def check_nums_same(labelA, labelB):
    split_labelA = split_label_pnp(labelA)
    split_labelB = split_label_pnp(labelB)
    if split_labelA[1] == split_labelB[1]:
        return True
    else:
        return False

def check_A_greater(labelA, labelB):
    split_labelA = split_label_pnp(labelA)
    split_labelB = split_label_pnp(labelB)
    if split_labelA[1] > split_labelB[1]:
        return True
    else:
        return False

def check_A_less(labelA, labelB):
    split_labelA = split_label_pnp(labelA)
    split_labelB = split_label_pnp(labelB)
    if split_labelA[1] < split_labelB[1]:
        return True
    else:
        return False
