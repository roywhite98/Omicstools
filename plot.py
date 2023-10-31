'''
Descripttion: 
version: 
Author: Roy White
Date: 2021-07-13 10:22:17
LastEditors: Roy White
LastEditTime: 2021-07-29 10:05:20
'''
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
''' upset plot '''

def upsetplot():
    
    from upsetplot import from_memberships
    example = from_memberships(
    [[],
        ['cat2'],
        ['cat1'],
        ['cat1', 'cat2'],
        ['cat0'],
        ['cat0', 'cat2'],
        ['cat0', 'cat1'],
        ['cat0', 'cat1', 'cat2'],
        ],
        data=[56, 283, 1279, 5882, 24, 90, 429, 1957]
    )
    path = ''
    
    # from upsetplot import generate_counts
    # example = generate_counts()

    from upsetplot import plot
    plot(example, show_counts='%d')
    plt.show()

# plt.savefig(path)

def barplot(x, y, title):
    plt.bar(x, y)
    plt.title(title)
    plt.show()

def multibarplot(list1, list2, x_axis):
    # lang:Chinese
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # show minus correctllist2
    plt.rcParams['axes.unicode_minus'] = False

    # x_axis = ['碳酸饮料', '绿茶', '矿泉水', '果汁', '其他']
    # list1 = [6, 7, 6, 1, 2]
    # list2 = [9, 4, 4, 5, 6]
 
    bar_width = 0.3 # 条形宽度
    index_list1 = np.arange(len(x_axis)) # 男生条形图的横坐标
    index_list2 = index_list1 + bar_width # 女生条形图的横坐标
    
    # 使用两次 bar 函数画出两组条形图
    plt.bar(index_list1, height=list1, width=bar_width, color='b', label='list1')
    plt.bar(index_list2, height=list2, width=bar_width, color='r', label='list2')
    
    plt.legend() # 显示图例
    plt.xticks(index_list1 + bar_width/2, x_axis) # 让横坐标轴刻度显示 x_axis 里的饮用水， index_list1 + bar_width/2 为横坐标轴刻度的位置
    plt.ylabel('纵坐标') # 纵坐标轴标题
    plt.title('一个标题') # 图形标题
    plt.xticks(rotation=45) # 转横坐标轴标签

    plt.show()


def venn(list1, list2, list3=[]):
    from matplotlib_venn import venn3, venn3_circles
    from matplotlib_venn import venn2, venn2_circles
    ## 首先是两个list的韦恩图
    if list3:
        venn3([set(list1), set(list2),set(list3)],set_labels = ('list1', 'list2',"list3"))
    else:
        venn2([set(list1), set(list2)], set_labels = ('list1', 'list2'))
    plt.show()


if __name__=='__main__':
    data1 = (2.4,10,3.35,24.5,20.5,10.5,19.5,29.5,6,21.75,14.875,15,19.5,25,10.5,19.75,11.75,18.16666667)
    data2 = (17.5,10.5,9.75,17.875,16,21.5,11.4,12,21,12,13.5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x1 = np.array(["SS282","SS284","SS314","SS329","SS339","SS366","SS369","SS393","SS398","SS399","SS408","SS410","SS412","SS417","SS421","SS425","SS429","SS474"])
    x2 = np.array(["SS295","SS306","SS363","SS365","SS405","SS414","SS432","SS433","SS442","SS468","SS469"])
    
    plt.bar(x1,data1,label="粳稻")
    # plt.xlabel("品种代号")
    # plt.ylabel("株高(cm)")
    plt.bar(x2,data2,color='g',label="籼稻")
    plt.title("正常土壤处理下水稻株高",fontsize=20)
    plt.xlabel("品种代号", fontsize=16)
    plt.ylabel("株高(cm)", fontsize=16)
    plt.xticks(rotation=45)
    plt.legend()

    plt.show()
