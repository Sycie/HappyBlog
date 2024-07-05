# -*- coding: utf-8 -*-
import csv
from time import sleep

import pandas as pd
from pyecharts import charts, options
from pyecharts.charts import Geo
from geopy.geocoders import Nominatim

filename = 'dataset3'  # 使用的文件名
column = 'age_range'  # 玫瑰图统计的列名
position = 'province'  # 地理图统计的地点的列名（与 longitude 和 latitude 二选一）
latitude = ''  # 地理图统计的纬度的列名（必须和 longitude 一起使用）
longitude = ''  # 地理图统计的经度的列名（必须和 latitude 一起使用）

file = open(("data/" + filename + ".csv"), 'r', encoding="UTF-8-sig")  # 打开数据文件（sig 是防止文件首部出现 UTF-8 标识符）
data = pd.read_csv(file)  # 读取数据

# 玫瑰图
if column != '':
    item_data = data[column]  # 读取玫瑰图所选列名的数据
    item_counts = item_data.value_counts()  # 统计数据数量
    item_dict = dict(item_counts)  # 数据转为字典类型
    for key in item_dict:
        item_dict[key] = int(item_dict[key])  # 将数据从 numpy.int64 转换为 int。
    item_list = list(item_dict.items())  # 字典转为列表

    # 生成玫瑰图
    rose = charts.Pie()
    rose.set_global_opts(legend_opts=options.LegendOpts(is_show=False))
    rose.add(column, data_pair=item_list[0:19],
             rosetype='area', radius=['3%', '100%'], center=['30%', '70%'], is_clockwise=False,
             label_opts=options.LabelOpts(is_show=True, position='inside', font_size=8, formatter='{b}:{c}')
             ).set_colors(
        ['rgb({r},{g},0)'.format(r=255 - 15 * x if x < 10 else 0, g=100 + 10 * (x - 10) if x >= 10 else 0) for x in
         range(20)])
    rose.render(path=("pages/rose-" + filename + "-" + column + ".html"))

# 地理图（地点）
if position != '':
    position_data = data[position]
    position_counts = position_data.value_counts()
    position_dict = dict(position_counts)
    for key in position_dict:
        position_dict[key] = int(position_dict[key])
    position_list = list(position_dict.items())

    c = (
        Geo()
            .add_schema(maptype="china")
            .add(position, data_pair=position_list)
            .set_series_opts(label_opts=options.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=options.VisualMapOpts(min_=5700, max_=6050),
            title_opts=options.TitleOpts(title=(filename + '-' + position)),
        )
    )
    c.render(path=("pages/geo-" + filename + "-" + position + ".html"))

# 地理图（经纬度）
if latitude != '' and longitude != 'null':
    # coordinate_data = data[[latitude, longitude]]
    # coordinate_dict = dict(coordinate_data)
    # geolocator = Nominatim(user_agent="http", timeout=3)  # 定义坐标到地点转换器
    # coordinate_list = list(coordinate_dict.items())
    # # for i in range(0, 1000):
    # for i in range(0, len(coordinate_list)):
    #     address_coordinate = open("data/address-coordinate.csv", 'r', encoding="UTF-8-sig")
    #     address_coordinate_data = pd.read_csv(address_coordinate)
    #     coordinate_list[i] = list(coordinate_list[i])  # 将元组转换为列表
    #     coordinate_list[i][0] = list(coordinate_list[i][0])
    #     try:
    #         index = address_coordinate_data[
    #             address_coordinate_data.latitude == coordinate_list[i][0][0] and address_coordinate_data.longitude ==
    #             coordinate_list[i][0][1]].index.tolist()[0]
    #         print(index)
    #     except IndexError and ValueError:
    #         address_coordinate = open("data/address-coordinate.csv", 'w', encoding="UTF-8-sig")
    #         print(coordinate_list[i][0])
    #         print(type(coordinate_list[i][0]))
    #         location = geolocator.reverse(coordinate_list[i][0])  # 根据坐标获取地点
    #         address = location.address.split(",")[-3]  # 直接选取地点
    #         print(i, address, sep=": ")
    #         csv.writer(address_coordinate).writerow([coordinate_list[0][i][0], coordinate_list[0][i][1], address])
    #         address_coordinate.close()
    #
    #     sleep(3)  # 停止 3 秒

    coordinate_data = data[[latitude, longitude]]
    coordinate_counts = coordinate_data.value_counts()
    coordinate_dict = dict(coordinate_counts)
    geolocator = Nominatim(user_agent="http", timeout=30)  # 定义坐标到地点转换器
    for key in coordinate_dict:
        coordinate_dict[key] = int(coordinate_dict[key])
    coordinate_list = list(coordinate_dict.items())
    for i in range(0, 50):
        # for i in range(0, len(coordinate_list)):
        coordinate_list[i] = list(coordinate_list[i])  # 将元组转换为列表
        coordinate_list[i][0] = list(coordinate_list[i][0])
        location = geolocator.reverse(coordinate_list[i][0])  # 根据坐标获取地点
        coordinate_list[i][0] = location.address.split(",")[-3]  # 直接选取地点
        print(i, coordinate_list[i][0], sep=": ")
        sleep(3)  # 停止 3 秒

    coordinate_list = coordinate_list[0:50]

    c = (
        Geo()
            .add_schema(maptype="china")
            .add((longitude + ", " + latitude), data_pair=coordinate_list)
            .set_series_opts(label_opts=options.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=options.VisualMapOpts(max_=10, min_=1),
            title_opts=options.TitleOpts(title=(filename + '-' + longitude + "_" + latitude)),
        )
    )
    c.render(path=("pages/geo-" + filename + "-" + longitude + "_" + latitude + ".html"))
