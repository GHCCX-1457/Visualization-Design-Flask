
from flask import Flask, render_template
import jieba,webbrowser
from gevent import pywsgi

app = Flask(__name__)

from pyecharts.charts import Bar, Line, WordCloud, Pie, Map, Radar, Scatter, Timeline, Polar, Funnel, Boxplot
from pyecharts import options as opts
import pandas as pd
data=pd.read_excel('分省年度数据.xlsx',sheet_name=[0,1,2,3])


webbrowser.open('127.0.0.1:5000')
webbrowser.open('127.0.0.1:5000/page2')
webbrowser.open('127.0.0.1:5000/page1')


def pie_picture1() ->Timeline:

    tl = Timeline()
    for i in range(2011, 2022):
        water_2021 = data[0][data[0]['年份'] == i]
        c = (
            Pie()
                .add(
                "",
                [
                    list(z)
                    for z in zip(
                    water_2021['地区'],
                    water_2021['人均水资源量(立方米)'],
                )
                ],
                center=["40%", "50%"],
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}年".format(i)),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        tl.add(c, '{}年'.format(i))
    return tl


def line_picture1() ->Line:
    so2=data[2]
    c = (
        Line()
        .add_xaxis([str(i)+'年' for i in range(2011,2022)])
        .add_yaxis("河南省", list(reversed(so2[so2['地区']=='河南省']['二氧化硫排放量(万吨)'].tolist())))
        .add_yaxis("吉林省", list(reversed(so2[so2['地区']=='吉林省']['二氧化硫排放量(万吨)'].tolist())))
        .add_yaxis("陕西省", list(reversed(so2[so2['地区']=='陕西省']['二氧化硫排放量(万吨)'].tolist())))
        .add_yaxis("福建省", list(reversed(so2[so2['地区']=='福建省']['二氧化硫排放量(万吨)'].tolist())))
        .add_yaxis("四川省", list(reversed(so2[so2['地区']=='四川省']['二氧化硫排放量(万吨)'].tolist())))
        .set_series_opts(title_TextStyle = opts.TextStyleOpts(color='white'))
        .set_global_opts(
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="slider")]
    )
    )
    return c

def map_picture1() -> Timeline:
    def switch(tmp):
        for i in range(len(tmp)):
            tmp[i] = float(tmp[i][:-1])
        return tmp

    tl = Timeline()
    for i in range(2011, 2022):
        forest_2021 = data[1][data[1]['年份'] == i]
        c = (
            Map()
                .add("森林覆盖率", [list(z) for z in zip(forest_2021['地区'].tolist(), switch(forest_2021['森林覆盖率'].tolist()))],
                     "china")
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}年".format(i)),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True)
            )
        )
        tl.add(c, '{}年'.format(i))
    return tl

def radar_picture1() -> Timeline:
    def fun(index,i):
        dic={0:'人均水资源量(立方米)',1:'森林覆盖率',2:'二氧化硫排放量(万吨)',3:'城市绿化率'}
        tmp=data[index][data[index]['年份']==i]
        temp=[float(tmp[tmp['地区']==province][dic[index]].values
                    if index!=1 and index!=3 else tmp[tmp['地区']==province][dic[index]].values[0][:-1]) for province in provinces]
        temp.append(i-2010)
        values=[]
        values.append(temp)
        return values

    provinces=['河南省','吉林省','陕西省','福建省','四川省','青海省']


    c_schema2 = [
        {"name": "河南省", "max": 150},
        {"name": "吉林省", "max": 150},
        {"name": "陕西省", "max": 150},
        {"name": "福建省", "max": 150},
        {"name": "四川省", "max": 150},
        {"name": "青海省", "max": 150},
    ]

    tl=Timeline()
    for i in range(2011,2022):
        values=[]
        for j in range(4):
            values.append(fun(j,i))
        c = (
            Radar()
                .add_schema(schema=c_schema2, shape="circle")
                .add("森林覆盖率", values[1], color="blue")
                .add("二氧化硫排放量(万吨)", values[2], color="green")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="{}年".format(i)))
        )
        tl.add(c,'{}年'.format(i))
    return tl

def scatter_picture1() ->Scatter:
    forest_2021 = data[1][data[1]['年份'] == 2021]
    so2_2021 = data[2][data[2]['年份'] == 2021]

    forest_rate = forest_2021['森林覆盖率'].tolist()
    for i in range(len(forest_rate)):
        forest_rate[i] = float(forest_rate[i][:-1])

    value = list(zip(forest_rate, so2_2021['二氧化硫排放量(万吨)'].tolist()))
    value.sort(key=lambda x: x[0])
    x = [value[i][0] for i in range(len(value))]
    y = [value[i][1] for i in range(len(value))]

    c = (
        Scatter()
            .add_xaxis(x)
            .add_yaxis("二氧化硫排放量(万吨)", y)
            .set_global_opts(
        )
    )

    return c

def rose_picture1() -> Timeline:
    provinces=['河南省','吉林省','陕西省','福建省','四川省','青海省']
    tl=Timeline()
    tl.add_schema(play_interval=1000,
                  label_opts=opts.series_options.LabelOpts(
                      is_show=False, color='rgba(255,255,255,.6)', interval=0, font_size=5))
    for i in range(2011,2022):
        green=data[3][data[3]['年份']==i]
        so2=data[2][data[2]['年份']==i]
        value1=[float(green[green['地区']==province]['城市绿化率'].tolist()[0][:-1]) for province in provinces]
        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(provinces, value1)],
                radius=["30%", "75%"],
                rosetype="radius",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="{}年".format(i)))
        )

        tl.add(c,"{}年".format(i))

    return tl


def word_cloud() ->WordCloud:
    fs = open('生态新闻.txt')
    passage = fs.read()
    fs.close()
    words = jieba.lcut(passage)
    stopwords = set()
    content = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]
    stopwords.update(content)

    ls = []
    counts = {}

    for word in words:
        if word not in stopwords and word != '\u3000':
            if len(word) == 1:
                continue
            else:
                ls.append(word)
                counts[word] = counts.get(word, 0) + 1

    data = []
    for i in counts.items():
        tup = ()
        tup += (i[0],)
        tup += (str(i[1]),)
        data.append(tup)

    c = (
        WordCloud()
            .add(series_name="生态新闻报道词云", data_pair=data, word_size_range=[6, 66], shape='star')
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )

    )

    return c

def line_picture2() ->Line:
    water_2021 = data[0][data[0]['年份'] == 2021]
    provinces = ['河南省', '吉林省', '陕西省', '福建省', '江苏省', '广东省']
    values = [float(water_2021[water_2021['地区'] == province]['人均水资源量(立方米)'].values[0]) for province in provinces]

    c = (
        Line()
            .add_xaxis(provinces)
            .add_yaxis("人均水资源量(立方米)", values, is_step=True,
                       itemstyle_opts=opts.ItemStyleOpts(color="#2f89cf"))
            .set_global_opts(legend_opts=opts.LegendOpts(textstyle_opts=
            opts.TextStyleOpts(color='rgba(255,255,255,.6)'),
            border_width=0),xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
            linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')),
            axislabel_opts =opts.LabelOpts(color='rgba(255,255,255,.6)'),
            axisline_opts=opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)'))),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
            linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')),
            axislabel_opts=opts.LabelOpts(color='rgba(255,255,255,.6)'),
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(
            color='rgba(255,255,255,.1)')))
                             )
    )
    return c


def bar_picture2() ->Bar:
    provinces = ['河南省', '吉林省', '陕西省', '福建省', '四川省', '青海省']
    forest_2021 = data[1][data[1]['年份'] == 2021]
    values = [float(forest_2021[forest_2021['地区'] == province]['森林覆盖率'].values[0][:-1]) for province in provinces]

    c = (
        Bar()
            .add_xaxis(provinces)
            .add_yaxis("森林覆盖率", values,itemstyle_opts=opts.ItemStyleOpts(color="#2f89cf"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                             )
            .set_global_opts(
            legend_opts=opts.LegendOpts(textstyle_opts=
                opts.TextStyleOpts(color='rgba(255,255,255,.6)'),border_width=0),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
                linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')),
            axislabel_opts =opts.LabelOpts(color='rgba(255,255,255,.6)'),
            axisline_opts=opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)'))),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
                linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')),
            axislabel_opts=opts.LabelOpts(color='rgba(255,255,255,.6)'),
            axisline_opts = opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')),
            )

    )
    )
    return c

def rose_picture2() -> Pie:
    provinces=['河南省','吉林省','陕西省','福建省','四川省','青海省',
               '湖北省','湖南省','江苏省','浙江省','广东省','江西省']
    green=data[3][data[3]['年份']==2021]
    value1=[float(green[green['地区']==province]['城市绿化率'].tolist()[0][:-1]) for province in provinces]
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(provinces, value1)],
            radius=["30%", "75%"],
            rosetype="radius",
        )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
    return c

def funnel_picture2() -> Funnel:
    provinces = ['河南', '吉林', '陕西', '福建', '四川', '青海']
    so2_2021 = data[2][data[2]['年份'] == 2021]
    values = [float(so2_2021[so2_2021['地区'] == province+'省']['二氧化硫排放量(万吨)'].values[0]) for province in provinces]
    c = (
        Funnel()
            .add("商品", [list(z) for z in zip(provinces, values)])
            .set_global_opts(legend_opts=opts.LegendOpts(textstyle_opts=
                opts.TextStyleOpts(color='rgba(255,255,255,.6)',font_size=10),
                border_width=0,pos_bottom=0))
    )
    return c

def boxplot_picture2() ->Boxplot:
    so2 = [data[2][data[2]['年份'] == i]['二氧化硫排放量(万吨)'].tolist() for i in range(2015, 2022)]
    c = Boxplot()
    c.add_xaxis([i for i in range(2015, 2022)])
    c.add_yaxis("二氧化硫排放量分布", c.prepare_data(so2),
    itemstyle_opts=opts.ItemStyleOpts(color="#2f89cf"))
    c.set_global_opts(
        legend_opts=opts.LegendOpts(textstyle_opts=
                opts.TextStyleOpts(color='rgba(255,255,255,.6)'),border_width=0),
    xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
                                 linestyle_opts=opts.LineStyleOpts(
                                     color='rgba(255,255,255,.1)')),
    axislabel_opts=opts.LabelOpts(color='rgba(255,255,255,.6)'),
    axisline_opts=opts.AxisLineOpts(
    linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)'))),
    yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True,
                                 linestyle_opts=opts.LineStyleOpts(
                                     color='rgba(255,255,255,.1)')),
    axislabel_opts=opts.LabelOpts(color='rgba(255,255,255,.6)'),
    axisline_opts=opts.AxisLineOpts(
    linestyle_opts=opts.LineStyleOpts(color='rgba(255,255,255,.1)')))
                      )

    return c




@app.route("/pieChart1")
def get_pie_chart1():
    c = pie_picture1()
    return c.dump_options_with_quotes()

@app.route('/lineChart1')
def get_line_chart1():
    c=line_picture1()
    return c.dump_options_with_quotes()

@app.route('/mapChart1')
def get_map_chart1():
    c=map_picture1()
    return c.dump_options_with_quotes()

@app.route('/radarChart1')
def get_radar_chart1():
    c=radar_picture1()
    return c.dump_options_with_quotes()

@app.route('/scatterChart1')
def get_scatter_chart1():
    c=scatter_picture1()
    return c.dump_options_with_quotes()

@app.route('/roseChart1')
def get_rose_chart1():
    c=rose_picture1()
    return c.dump_options_with_quotes()

@app.route('/wordCloud')
def get_wordCloud():
    c=word_cloud()
    return c.dump_options_with_quotes()


@app.route("/lineChart2")
def get_line_chart2():
    c = line_picture2()
    return c.dump_options_with_quotes()

@app.route('/barChart2')
def get_bar_chart2():
    c=bar_picture2()
    return c.dump_options_with_quotes()

@app.route('/roseChart2')
def get_rose_chart2():
    c=rose_picture2()
    return c.dump_options_with_quotes()

@app.route('/funnelChart2')
def get_funnel_chart2():
    c=funnel_picture2()
    return c.dump_options_with_quotes()

@app.route('/boxplotChart2')
def get_boxplot_chart2():
    c=boxplot_picture2()
    return c.dump_options_with_quotes()







@app.route("/page2")
def page1():
    return render_template("myhtml/page2.html")

@app.route("/page1")
def page2():
    return render_template("myhtml/page1.html")

@app.route('/')
def index():
    return render_template('myhtml/index.html')

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
