import random
import xlrd
from openpyxl import Workbook
import time

def del_null(string):
    return string != ''

def int2(string):
    return int(string)

filedata = xlrd.open_workbook('夜游排班表.xlsx')
Staff_list = filedata.sheet_by_name('人员表')
relational = filedata.sheet_by_name('关系表')

# 获取人员表里面的上班人员数据：
part_timer = []
full_timer = []
Headwaiter = []
ship1 = []

for i in range(9,18):
    part_timer = part_timer + Staff_list.row_values(i, 1, 11)
for i in range(3, 9):
    full_timer = full_timer + Staff_list.row_values(i, 1, 11)
for i in range(0, 3):
    Headwaiter = Headwaiter + Staff_list.row_values(i, 1, 11)
for i in range(18, 22):
    ship1 = ship1 + Staff_list.row_values(i, 1, 11)

part_timer = list(filter(del_null, part_timer))
full_timer = list(filter(del_null, full_timer))
Headwaiter = list(filter(del_null, Headwaiter))
ship1 = list(map(int2, filter(del_null, ship1)))

# 获取关系表里面的关系数据:
temp1 = list(map(int2, filter(del_null, relational.col_values(0, 1))))
temp2 = list(filter(del_null, relational.col_values(1, 1)))
temp3 = list(map(int2, filter(del_null, relational.col_values(2, 1))))
temp4 = list(filter(del_null, relational.col_values(4, 1)))
temp5 = []

for i in range(1, relational.nrows):
    temp5.append(list(filter(del_null, relational.row_values(i, 5))))

dict1 = dict(map(lambda x, y:[x, y], temp1, temp2)) # 船对应的领班
dict2 = dict(map(lambda x, y:[x, y], temp1, temp3)) # 船对应的人数
dict3 = dict(map(lambda x, y:[x, y], temp4, temp5)) # 领班对应的服务员
ship2 = []
table = dict.fromkeys(ship1)
log = []

for k, v in table.items():
    table[k] = []
people_counting = 0

for i in ship1:
    people_counting += dict2[i]
part_timer_counting = people_counting - len(full_timer) - len(Headwaiter) # 今天需要几个兼职
if part_timer_counting < 0:
    y = 0
else:
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
            if j in part_timer:
                table[i].append(j)
                part_timer.remove(j)
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
        if j in part_timer:
            table[i].append(j)
            part_timer.remove(j)
            dict2[i] -= 1

for i in ship1:
    while (dict2[i]-y)>0:
        if len(Headwaiter) != 0:
            x = random.randint(0, len(Headwaiter)-1)
            table[i].append(Headwaiter[x])
            Headwaiter.pop(x)
            dict2[i] -= 1
            for k in dict3[dict1[i]]:
                if k in full_timer:
                    table[i].append(k)
                    full_timer.remove(k)
                    dict2[i] -= 1
                if k in part_timer:
                    table[i].append(k)
                    part_timer.remove(k)
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
    while dict2[i] < 0:
        if len(part_timer) != 0:
            x = random.randint(0, len(part_timer)-1)
            table[i].append(part_timer[x])
            part_timer.pop(x)
        else:
            log.append('%s船缺一位服务员' % i)


wb = Workbook()
ws = wb.active
for k, v in table.items():
    v.insert(0, "巴%s" % str(k))
    ws.append(v)
for i in log:
    ws.append([i,])

wb.save(filename="%s排班表.xlsx" % time.strftime('%Y-%m-%d', time.localtime(time.time())))

