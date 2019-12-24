import sys
import re

asks = list()
rep = list()
nq = 0
ns = 0




def implication(stn):
    index = stn.find("=>")
    stn = stn.replace("&", '')
    negate_sub = stn[:index-1]
    neg=negate_sub.split()
    new_neg = []
    for x in range(len(neg)):
        if neg[x][0]=='~':
            new_neg.append(neg[x][1:])
        else:
            new_neg.append('~'+neg[x])
    stn = stn.replace("=>","|")
    half = stn.find("|")
    stn = ' | '.join(new_neg) +' '+ stn[half:]
    #print(stn)
    return stn


def checkline(rep):
    if "|" in rep:
        return False
    const_list = re.search(r'\((.*?)\)', rep).group(1)
    const = const_list.split(",")
    #print(const)
    for val in const:
        if val[0].isupper():
            continue
        else:
            return False
    return True


def resolve(ask,rem,sp,sn,sc):

    if ask[0] != '~':
        second = ask.partition("(")[0]
        try:
            value = sn[second]
        except KeyError:
            return False

        for line in value:
            try:
                dup = rem
                ask_temp = ask

                if line in sc:
                    ret1, l1 = delete(dup, line[1:])
                    ret2 = 1
                    l2 = ""
                else:
                    ret1, l1 = delete(dup, ask_temp)
                    ret2, l2 = delete(line, "~" + ask_temp)
                if ret1 == 0 or ret2 == 0:
                    continue
                else:
                    if l1 == '' and l2 != '':
                        dup = l2
                    elif l2 == '' and l1 != '':
                        dup = l1
                    elif l1 == '' and l2 == '':
                        dup = ''
                    else:
                        dup = l2 + " | " + l1

                    if dup == '':
                        return True
                    else:
                        if "|" in dup:
                            data = dup.split("|")
                            for i in data:
                                i = i.replace(" ","")
                                if resolve(i,dup,sp,sn,sc):
                                    return True
                                else:
                                    break
                        else:
                            if resolve(dup,dup,sp,sn,sc):
                                return True
                            else:
                                continue
            except RuntimeError as re:
                if re.args[0] == 'maximum recursion depth exceeded':
                    return False

        return False

    else:
        second = ask.partition("(")[0]
        try:
            value = sp[second[1:]]
        except KeyError:
            return False
        for line in value:
            try:
                dup = rem
                ask_temp = ask
                if line in sc:
                    print1, l1 = delete(dup, "~" + line)
                    print2 = 1
                    l2 = ""
                else:
                    print1, l1 = delete(dup, ask_temp)
                    print2, l2 = delete(line, ask_temp[1:])
                if print1 == 0 or print2 == 0:
                    continue
                else:
                    if l1 == '' and l2 != '':
                        dup = l2
                    elif l2 == '' and l1 != '':
                        dup = l1
                    elif l1 == '' and l2 == '':
                        dup = ''
                    else:
                        dup = l2 + " | " + l1

                    if dup == '':
                        return True
                    else:
                        if "|" in dup:
                            data = dup.split("|")
                            for i in data:
                                i = i.replace(" ", "")
                                if resolve(i, dup, sp, sn, sc):
                                    return True
                                else:
                                    break
                        else:
                            if resolve(dup, dup, sp, sn, sc):
                                return True
                            else:
                                continue
            except RuntimeError as re:
                if re.args[0] == 'maximum recursion depth exceeded':
                    return False
        return False


def delete(k,ask):
    __int, newq, st = change(k, ask)
    if __int == 1:
        if newq in st:
            sm = st.replace(newq, "")
        else:
            start = st.find(ask.partition("(")[0])
            end = st.find(')', start)
            to_del = st[start:end + 1]
            sm = st.replace(to_del, "")
        if " |  | " in sm:
            st2 = sm.replace(" |  | ", " | ")
            return 1,st2
        elif sm[:3] == " | ":
            st2 = sm[3:]
            return 1,st2
        elif sm[-3:] == " | ":
            st2 = sm[:-3]
            return 1,st2
        else:
            return 1, sm
    else:
        return 0,st


def change(line,ask):
    predicate = ask.partition("(")[0]


    constant = re.search(r'\((.*?)\)', ask).group(1)
    cons_list = constant.split(",")
    count = 0

    data = line.split("|")
    flag = 0
    for i in data:
        m = i.partition("(")[0]
        m = m.replace(' ', '')
        if m == predicate:
            __vars = re.search(r'\((.*?)\)',i).group(1)
            var_list = __vars.split(",")
            for j in var_list:
                if j[0].isupper() and cons_list[count][0].islower():

                    matching = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, cons_list[count])))
                    a = matching.sub(j, ask)
                    ask = a
                    flag = 1
                    count += 1
                elif j[0].islower() and cons_list[count][0].isupper():

                    matching = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, j)))
                    a = matching.sub(cons_list[count], line)
                    line = a
                    flag = 1
                    count +=1
                elif j[0].isupper() and cons_list[count][0].isupper():
                    if j == cons_list[count]:
                        ask = ask
                        line = line
                        flag = 1
                    else:
                        flag = 0
                        break
                    count +=1
                elif j[0].islower() and cons_list[count][0].islower():

                    if not (j == cons_list[count]):


                        matching = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, j)))
                        a = matching.sub(cons_list[count], line)
                        line = a
                        ask = ask
                        flag = 1
                    else:
                        line = line
                        ask = ask
                        flag = 1
                    count += 1
            if flag == 1:
                break
    if flag == 0:
        return 0, ask, line
    else:
        return 1, ask, line





def main():
    output_file = "output.txt"
    fo = open(output_file, 'w')

    fin = "input.txt"
    output_file = "output.txt"
    global asks
    global rep
    global nq
    global ns

    try:
        input_file = open(fin, 'r')
        lines = input_file.readlines()
        for index, line in enumerate(lines):
            if index == 0:
                nq = int(lines[index].strip("\n"))
                for i in range(1, nq + 1):
                    asks.append(lines[i].strip("\n"))
                ns = int(lines[nq + 1].strip("\n"))
                for i in range(nq + 2, nq + ns + 2):
                    rep.append(lines[i].strip("\n"))
                break
        input_file.close()
        ask_list = asks
        lines = rep
        #return asks, rep


    except IOError:
        fo = open(output_file, 'w')
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()

    sn = dict()
    sp = dict()

    for item in rep:
        if (item.find('=>') != -1):
            item = implication(item)

        data = item.split('|')
        for i in data:
            i = i.replace(' ', '')
            if i[0] == '~':
                b = i[1:]
                b = b.partition("(")[0]
                try:
                    sn[b].append(item)
                except KeyError:
                    sn[b] = [item]
            else:
                i = i.partition("(")[0]
                try:
                    sp[i].append(item)
                except KeyError:
                    sp[i] = [item]
    #print(sp)
    #print(sn)



    sc = []


    for a in lines:
        if(a.find('=>')!=-1):
            a = implication(a)
        if checkline(a):
            sc.append(a)
    #print(sc)

    for ask in ask_list:
        if ask[0] == '~':
            new_ask = ask[1:]
            if resolve(new_ask, new_ask, sp, sn, sc):
                fo.write("TRUE" + "\n")
            else:
                fo.write("FALSE" + "\n")

        else:
            new_ask = "~"+ ask
            if resolve(new_ask, new_ask, sp, sn, sc):
                fo.write("TRUE" + "\n")
            else:
                fo.write("FALSE" + "\n")
    fo.close()


if __name__ == '__main__':
    main()