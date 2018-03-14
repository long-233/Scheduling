import random

dict1 = {31:'领班A', 25:'领班B', 20:'领班D'} # 船对应的领班
dict2 = {31:5, 25:5, 20:6, } #船对应的人数
dict3 = {'领班A':['全职B', '全职E'], '领班B':['全职D'], '领班C':[], '领班D':[]} # 领班带的服务员
part_timer = ['兼职A', '兼职B', '兼职C', '兼职D', '兼职E', '兼职F']
full_timer = ['全职A', '全职B', '全职C', '全职D', '全职E']
Headwaiter = ['领班A', '领班B', '领班C', '领班D']
ship1 = (31, 25, 20)
ship2 = []
table = dict.fromkeys(ship1)
tag = ''
for k, v in table.items():
    table[k] = []
people_counting = 0

for i in ship1:
    people_counting += dict2[i]
part_timer_counting = people_counting - len(full_timer) - len(Headwaiter) # 今天需要几个兼职
y = part_timer_counting // len(ship1)    # 每艘船最少派几个兼职

for i in ship1:
    if dict1.get(i) in Headwaiter:
        table[i].append(dict1[i])
        Headwaiter.remove(dict1[i])
        dict2[i] -= 1
        for j in dict3[dict1[i]]:
            if j in full_timer:
                table[i].append(j)
                full_timer.remove(j)
                dict2[i] -= 1

    else:
        ship2.append(i)
        continue

for i in ship2:
    x = random.randint(0, len(Headwaiter) - 1)
    table[i].append(Headwaiter[x])
    Headwaiter.pop(x)
    dict2[i] -= 1
    for j in dict3[dict1[i]]:
        if j in full_timer:
            table[i].append(j)
            full_timer.remove(j)
            dict2[i] -= 1

for i in ship1:
    for j in range(dict2[i]-y):
        if len(Headwaiter) != 0:
            x = random.randint(0, len(Headwaiter)-1)
            table[i].append(Headwaiter[x])
            Headwaiter.pop(x)
            for k in dict3[dict1[i]]:
                if k in full_timer:
                    table[i].append(k)
                    full_timer.remove(k)
                    dict2[i] -= 1
        elif len(full_timer) != 0:
            x = random.randint(0, len(full_timer)-1)
            table[i].append(full_timer[x])
            full_timer.pop(x)
            dict2[i] -= 1
        else:
            x = random.randint(0, len(part_timer)-1)
            table[i].append(part_timer[x])
            part_timer.pop(x)
            dict2[i] -= 1

for i in ship1:
    for j in range(dict2[i]):
        if len(part_timer) != 0:
            x = random.randint(0, len(part_timer)-1)
            table[i].append(part_timer[x])
            part_timer.pop(x)
        else:
            tag = tag + '%s船缺一位服务员\n' % i



for k, v in table.items():
    print('%s船：%s' % (k, v))
print(tag)
