import difflib as diff
import src.VisualizeHistogram as vh
import src.ReshapeTexts as rt

if __name__ == '__main__':
    # TODO: get texts from each file
    a = ['hoge', 'fuga', 'piyo']
    b = ['hoge', 'fuga', 'fugafuga', 'piyo']
    c = ['hoge', 'hogehoge', 'fugafuga', 'piyo']

    spacer = u'*'
    space = u'<sp>'

    diff_a_b = spacer.join(diff.Differ().compare(a, b)).split(spacer)
    # print('diff_a_b: ' + str(diff_a_b))
    a_b = []
    b_a = []
    for i in diff_a_b:
        if '?' in i:
            continue
        elif '+ ' in i:
            if space not in i:
                a_b.append(space)
                b_a.append(i.replace('+ ', ''))
        elif '- ' in i:
            if space not in i:
                a_b.append(i.replace('- ', ''))
                b_a.append(space)
        elif '  ' in i:
            if space not in i:
                a_b.append(i.replace('  ', ''))
                b_a.append(i.replace('  ', ''))
    # print('a: ' + str(a))
    # print('b: ' + str(b))
    # print('a_b: ' + str(a_b))
    # print('b_a: ' + str(b_a))

    diff_ab_c = spacer.join(diff.Differ().compare(a_b, c)).split(spacer)
    # print('diff_ab_c: ' + str(diff_ab_c))
    a_b_c = []
    c_a_b = []
    for i in diff_ab_c:
        if '?' in i:
            continue
        elif '+ ' in i:
            if space not in i:
                a_b_c.append(space)
                c_a_b.append(i.replace('+ ', ''))
        elif '- ' in i:
            if space not in i:
                a_b_c.append(i.replace('- ', ''))
                c_a_b.append(space)
        elif '  ' in i:
            if space not in i:
                a_b_c.append(i.replace('  ', ''))
                c_a_b.append(i.replace('  ', ''))
    # print('c: ' + str(c))
    # print('a_b_c: ' + str(a_b_c))
    # print('c_a_b: ' + str(c_a_b))

    diff_abc_ba = spacer.join(diff.Differ().compare(a_b_c, b_a)).split(spacer)
    # print('diff_abc_ba: ' + str(diff_abc_ba))
    b_a_c = []
    count_plus = 0
    count_minus = 0
    for i in diff_abc_ba:
        if '?' in i:
            continue
        elif '+ ' in i:
            count_plus += 1
            if space not in i:
                b_a_c.append(i.replace('+ ', ''))
        elif '- ' in i:
            count_minus += 1
            if space not in i:
                b_a_c.append(space)
        elif '  ' in i:
            # if count_plus > count_minus:
                # for i in range(abs(count_plus - count_minus)):
                #     <list>.append(space)
            if count_plus < count_minus:
                for j in range(abs(count_plus - count_minus)):
                    b_a_c.append(space)
            count_plus = 0
            count_minus = 0
            if space not in i:
                b_a_c.append(i.replace('  ', ''))
    # print('b_a_c: ' + str(b_a_c))

    # Priority: b & c > a > b, c
    ans = []
    for i in range(len(a_b_c)):
        if b_a_c[i] == c_a_b[i]:
            if space not in b_a_c[i]:
                ans.append(b_a_c[i])
        else:
            if space not in a_b_c[i]:
                ans.append(a_b_c[i])

    print('ans: ' + str(ans))

    fout = open('./arimura_ensemble.txt', mode='w', encoding="utf8")
    for i in ans:
        fout.write(i + '\n')
    fout.close()
