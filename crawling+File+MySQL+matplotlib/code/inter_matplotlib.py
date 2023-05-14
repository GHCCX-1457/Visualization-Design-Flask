import pyecharts
from numpy.ma.bench import xl
pyecharts.globals._WarningControl.ShowWarning = False
import warnings
import sys
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
plt.rcParams["font.sans-serif"]="SimHei"
plt.rcParams["axes.unicode_minus"]=False
import matplotlib.pyplot as plt
import pandas as pd
def mouse():
    data=pd.read_excel('分省年度数据.xlsx',sheet_name=[2])
    fig = plt.figure()#创建figure对象实例
    ax = fig.add_subplot(111)#1行1列1个图
    ax.set_xticks([i for i in range(2014,2020)])
    ax.set_title('鼠标点击交互图-福建省二氧化硫排放量')
    forest_2021 = data[2][data[2]['地区'] == '福建省']
    values = [float(forest_2021[forest_2021['年份'] == i]['二氧化硫排放量(万吨)'].values[0]) for i in range(2014,2020)]
    ax.plot(values)

    # 定义回调函数event是事件参数
    def onclick(event):
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              (event.button, event.x, event.y, event.xdata, event.ydata))
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()


def press():
    def on_press(event):
        print('press', event.key)
        sys.stdout.flush()
        if event.key == 'x':
            visible = xl.get_visible()
            xl.set_visible(not visible)
            fig.canvas.draw()

    data = pd.read_excel('分省年度数据.xlsx', sheet_name=[2])
    fig = plt.figure()  # 创建figure对象实例
    ax = fig.add_subplot(111)  # 1行1列1个图
    ax.set_xticks([i for i in range(2014, 2020)])
    ax.set_title('键盘敲击交互图-福建省二氧化硫排放量')
    forest_2021 = data[2][data[2]['地区'] == '福建省']
    values = [float(forest_2021[forest_2021['年份'] == i]['二氧化硫排放量(万吨)'].values[0]) for i in range(2014, 2020)]
    ax.plot(values)

    fig.canvas.mpl_connect('key_press_event', on_press)
    plt.show()

mouse()
press()