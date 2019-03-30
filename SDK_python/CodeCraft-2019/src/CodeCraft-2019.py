# -*- coding: utf-8 -*-
import copy
import logging
import sys
#import time
import numpy as np

def main():
    # cocurence_num = 230  ##并发量
    # step = 8
    # a = 1
    # b = 1
    # c = 20

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    roadData, road_rows = loadData(road_path)
    carData, car_rows = loadData(car_path)
    crossData, cross_rows = loadData(cross_path)

    if crossData[0][0] == 11: #图1
        cocurence_num = 80  ##并发量
        step = 1
        a = 1
        b = 1
        c = 20
    else:
        cocurence_num = 230  ##并发量
        step = 8
        a = 1
        b = 1
        c = 20


    dict = {}
    for i in range(cross_rows):
        dict[crossData[i][0]] = i + 1

    cross_class= [[] for i in range(cross_rows)]
    for i in range(car_rows):
        cross_class[dict[carData[i][1]]-1].append(carData[i])

    for i in range(cross_rows):
        #cross_one_class = cross_class[i]
        cross_class[i] = sorted(cross_class[i], key=lambda s: (s[4], -s[3]))
        #cross_class[i] = sorted(cross_class[i], key=lambda s: s[4])

    answer_temp = []
    maxLen = max(list(map(len, cross_class)))

    for i in range(maxLen):
        for j in range(cross_rows): ##节点类
            if len(cross_class[j]) != 0:
                temp = cross_class[j].pop(0)
                answer_temp.append(temp)
                for i in range(len(cross_class[j])): ##每类pop一个出来后，后面的数据的出发时间加1
                    if cross_class[j][i][4] == temp[-1]:
                        cross_class[j][i][4] = cross_class[j][i][4] + 1
                cross_class[j] = sorted(cross_class[j], key=lambda s: (s[4], -s[3]))
            else:
                continue

    carData = answer_temp


    #初始化邻接矩阵
    matrix = initMatrix(roadData, cross_rows, a, b, c, dict)
    answer = []
    for i in range(car_rows):
        car_start_index = dict[carData[i][1]] - 1  #车的出发节点下标
        car_end_index = dict[carData[i][2]] - 1   #车的结束节点下表
        arc = copy.deepcopy(matrix)
        arc_new = convertMatrix(arc, car_start_index)
        Patharc_1 = Dijkstra(arc_new, cross_rows)
        Patharc_1_temp = []

        #使Patharc_1的位置归位到原来的位置
        for jjj in range(len(Patharc_1)):
            if Patharc_1[jjj] == car_start_index:
                Patharc_1[jjj] = 0
            elif Patharc_1[jjj] == 0:
                Patharc_1[jjj] = car_start_index

        if car_end_index == 0: #如果末端为0,实际也添加对应节点,但映射用car_start_index去映射
            Patharc_1_temp.append(car_end_index)
            car_end_index = car_start_index  #但映射用car_start_index去映射
        else:
            Patharc_1_temp.append(car_end_index)
        m = Patharc_1[car_end_index] #取出下一个映射点

        appear = False ##边界出现,出现过则置为True,如10089中,[33->1], 1,0,33(出现两次,该数实际为0,要手动添加0,但还是用33去映射),8,,16,24,25,33 注意33只可能出现两次，所以用appear指示
        while m != car_start_index: #没有回溯回car_start_index就一直遍历
            Patharc_1_temp.append(m)
            m = Patharc_1[m]
            if car_start_index == m and (not appear): ##10089中，如果第一次遇到33了，实际上是遇到0了，把0手动添加进去，但映射还是用33
                appear = True  ##第一次遇到33
                if m != 0: ##33
                    if m == car_start_index: ##33
                        if Patharc_1_temp[-1] == 0:
                            m = Patharc_1[m]
                        else: #否则就是遍历完成然后直接退出
                            break
                    else:
                        Patharc_1_temp.append(0)
        Patharc_1_temp.append(car_start_index)
        Patharc_1_temp.reverse()
        route = []
        temp = []
        cross_temp1 = []
        cross_temp2 = []
        for i1 in range(len(Patharc_1_temp) - 1):
            temp.extend([Patharc_1_temp[i1] + 1, Patharc_1_temp[i1 + 1] + 1])
            for j1 in range(cross_rows):
                if dict[crossData[j1][0]] == temp[0]:
                    cross_temp1.extend(crossData[j1][1:5])
                elif dict[crossData[j1][0]] == temp[1]:
                    cross_temp2.extend(crossData[j1][1:5])
            ok = False
            for i2 in range(4):
                if cross_temp1[i2] == -1:
                    continue
                if ok:
                    break
                for j2 in range(4):
                    if cross_temp1[i2] != -1:
                        if cross_temp1[i2] == cross_temp2[j2]:
                            route.append(cross_temp1[i2])
                            ok = True
                            break
            cross_temp1.clear()
            cross_temp2.clear()
            temp.clear()
        answer.append([carData[i][0], carData[i][4]] + route)
        #route.clear()

    #answer = sorted(answer, key=lambda s: s[0]) ##使用时间那一套算法要排序

    cocurency(answer, car_rows, cocurence_num, step)
    outputData(answer_path, answer, car_rows)


def loadData(filename):
    with open(filename,  mode='r', encoding='gbk', buffering=1) as f:
        lines = f.readlines()[1:]
        rows = len(lines)
        data = []
        for line in lines:
            line = line.strip("\n").strip("(").strip(")").split(',')
            line = list(map(int, line))
            data.append(line)
    return data, rows

def outputData(filename, answer, carrows):
    with open(filename, mode='w', encoding='gbk') as f:
        for i in range(carrows):
            str = "".join('%s' % id + "," for id in answer[i])
            str = '(' + str[:-1] + ')'+ "\n"
            f.write(str)

def initMatrix(roadData, cross_rows, a, b, c, dict): #初始化邻接矩阵
    # a = 1  # 道路的长度
    # b = 1  # 限制速度
    # c = 20  # 车道数目
    index = []
    matrix = (np.ones([cross_rows, cross_rows]) - np.eye(cross_rows)) * 65535
    for road in roadData:
        #index.extend(road[4:6])  #起点和终点
        index.append(dict[road[4]])
        index.append(dict[road[5]])
        if len(index) == 2:
            matrix[index[0]-1][index[1]-1] = a * road[1] - b *road[2] - c * road[3]
            if matrix[index[0]-1][index[1]-1] <= 0:
                matrix[index[0] - 1][index[1] - 1] = 1
            if road[6] == 1:
                matrix[index[1]-1][index[0]-1] = a * road[1] - b *road[2] - c * road[3]
                if matrix[index[1] - 1][index[0] - 1] <= 0:
                    matrix[index[1] - 1][index[0] - 1] = 1
            index.clear()
    return matrix

def Dijkstra(arc, cross_rows):
    Patharc_temp = [0 for i in range(cross_rows)]
    ShortPathTable_temp = [0 for i in range(cross_rows)]
    k = 0
    final = [0 for i in range(cross_rows)]
    for v in range(cross_rows):
        final[v] = 0
        ShortPathTable_temp[v] = arc[0, v]
        Patharc_temp[v] = 0
    ShortPathTable_temp[0] = 0
    final[0] = 1
    for v in range(1, cross_rows):
        min = 65535
        for w in range(cross_rows):
            if ((final[w]==0) and  (ShortPathTable_temp[w]<min)):
                k = w
                min = ShortPathTable_temp[w]
        final[k] = 1
        for w in range(cross_rows):
            if ((final[w]==0) and ((min + arc[k, w])< ShortPathTable_temp[w])):
                ShortPathTable_temp[w] = min + arc[k, w]
                Patharc_temp[w] = k
    return Patharc_temp

def convertMatrix(orignal_matrix, car_start_index):#转化邻接矩阵使其适合dij算法
    matrix_temp = copy.deepcopy(orignal_matrix)
    matrix_temp[[0, car_start_index], :] = matrix_temp[[car_start_index, 0], :]
    matrix_temp[:, [0, car_start_index]] = matrix_temp[:, [car_start_index, 0]]
    return matrix_temp

def cocurency(answer, car_rows, cocurence_num, step): ##设置一个时刻发的车数
    num = 0
    number_at_once = 0
    for iii in range(car_rows):
        number_at_once = number_at_once + 1
        if number_at_once != cocurence_num:
            answer[iii][1] = answer[iii][1] + num
        elif number_at_once == cocurence_num:
            answer[iii][1] = answer[iii][1] + num
            number_at_once = 0
            num = num + step


# to read input file
# process
# to write output file


if __name__ == "__main__":
    #starttime = time.clock()
    main()
    #endtime = (time.clock() - starttime)
    #print(endtime)


