# -*- coding: utf-8 -*-
__author__ = '程鸣'

"""
Copyright 2014 Shenma Co., Ltd.
Create time: 2015/1/4 14:32
"""
import cgi
from os import listdir
from os import path
import os
import sys
import MySQLdb
# import replace_index
reload(sys)
sys.setdefaultencoding('gbk')
# Original directory organized as {date}/{start page}/{run mode}
id_dict = {'Warm Start':'0','Cold Start 60s':'1','Cold Start 30s':'2','默认页':'1','空白页':'2','百度':'3'}
global index


def get_db_connection(host):
    connection = MySQLdb.connect(host=host, port=3306, user='root', passwd='root', db='perfweb', charset='utf8')
    return connection
#
def get_dirs(date_dir):
    dir = {}

    #print(listdir(specifiedDir))
    for start_page in listdir(date_dir):
        if path.isdir(path.join(date_dir, start_page)):
            dir[start_page.decode("gbk")] = path.join(date_dir, start_page)
        uni = u'what'
#        print('gbk 解码后 ')
#        print('utf-8 编码后 '+machine.decode("gbk").encode("utf-8"))
    return dir
#
def get_bar_number():
    return len(browsers_list)

def get_browsers_list(date):

    connection = get_db_connection('localhost')
    cursor = connection.cursor()
    cursor.execute("select browser from comparison where date='%s' group by browser order by id" % date)
    list = [row[0].encode('utf-8') for row in cursor.fetchall()]
    # with open('data/' + date + '/list.txt','r') as f:
    #     for each in f.readlines():
    #         br = each.split(' ')[0]
    #         list.append(br)
            # list.append(br.decode('gbk').encode('utf-8'))
    # print(list)
    return list

def get_versions(table):
    versions = []
    connection = get_db_connection('localhost')
    cursor = connection.cursor()
    if table == 'regular':
        cursor.execute("select version from regular where date<='%s' group by date order by version desc limit 0,5;" % date)
        versions = [('UC '+row[0]).encode('utf-8') for row in cursor.fetchall()]
        versions.reverse()
    else:
        with open('data/' + date + '/list.txt','r') as f:
            lines = f.readlines()
        for each in lines:
            versions.append(each.split(' ')[1])
    # print(versions)
    return versions


def get_data(startpage, mode):
    data = {}
    cursor = get_db_connection('localhost').cursor()
    for browser in browsers_list:
        if table == 'regular':
            version = browser.split(' ')[1]
            cursor.execute("select result, avg_result from regular where version='%s' and startpage='%s' and mode='%s';" % (version, startpage, mode))
        elif table == 'comparison':
            br = browser.decode('utf-8')
            cursor.execute("select result, avg_result from comparison where date='%s' and browser='%s' and startpage='%s' and mode='%s';" % (date, br, startpage, mode))
        result_string, avg_result = cursor.fetchone()
        result_list = result_string.split(',')
        data[browser] = [[value.encode("gbk") for value in result_list], avg_result]
    print(data)
    return data

def read_files(dir, mode):
    data = {}
    for each in listdir(dir):
        br = each[:each.find('_')]
        if '.log' not in each or mode not in each:
            continue;
        with open(dir+'/'+each,'r') as record:
            tmp = record.readlines()
        data[br] = []
        for str in tmp:
            time = round(float(str),2)
            if time > 50: # time is in unit ms
                time = round(time/1000,2)
            data[br].append(time)
        # data[br] = [round(float(s)/1000,2) for s in tmp]
        data[br].remove(max(data[br]))
        data[br].remove(min(data[br]))
    # print(data)
    return data
#
def generate_main():
    response = ""
    dir = get_dirs('data/' + date)
    #copyResources(title, machine, target_dir)
    response += '<div id="nav_bar"><ul id="nav_list">'
    start_pages = sorted(dir.keys(), reverse=True)  # reverse the keys so that they will be listed from 默认页 to 百度
    for each in start_pages:
        i = id_dict[each.encode('utf-8')]
        if i == '1':
            class_name = 'selected'
            style = 'border-left: 1px solid #003D79'
        else:
            class_name = 'unselected'
            style = ''
        response += '<li id="tag_'+i+'" class="'+class_name+'" style="'+style+'" onclick="switchPanel(this.id)" \
        onmouseover="highLight(this.id)" onmouseout="cancelHighLight(this.id)">'+each.encode('utf-8')+'</li>'
    response += '</ul></div><div id="content">'
    for each in sorted(dir.keys(), reverse=True):
        response += '<div class="content_data" id="start_page_'+id_dict[each.encode('utf-8')]+'">'
        response += generate_block(dir[each] + '\\Warm', 'Warm')
        response += generate_block(dir[each] + '\\60s', 'Cold')
        response += '</div>'
    response += '</div>'
    return response
#
# def writePage(page, targetFile):
#     warmDir,cold60Dir,cold30Dir = page+'\\Warm',page+'\\60s',page+'\\30s'
#     writeBlock('Warm Start', warmDir, targetFile)
#     # writeBlock('Cold Start', cold60Dir, targetFile)
#     writeBlock('Cold Start 60s', cold60Dir, targetFile)
#     writeBlock('Cold Start 30s', cold30Dir, targetFile)
#
#
# def generateIndexPage(titleList):
#     return None

def generate_head(utitle):
    title = utitle.encode('utf-8')
    response = ""
    if table == 'regular': js_function = 'drawLines();'
    else: js_function = 'drawCharts();'
    response += '<head><title>启动性能对比测试</title>\
    <link rel="icon" href="../images/logo.png"><link rel="stylesheet" href="../style.css"><meta charset="UTF-8">\
    <script src="../js/resultPage.js"></script></head>\
    <body onload="switchPanel(\'tag_1\'); %s">\
    <div id="banner" ><div id="title_container"><span id="title" onclick="location.href=\'../index.html\'" >浏览器启动性能横向对比测试</span></div></div>\
    <div id="main"><div id="back" ><a class="page_link" href="../index.html"><<返回首页</a></div>\
    <div id="versions1" style="display:none"><span id="versions_box_corner"></span>\
    <span style="font-weight:bolder">详细版本号:</span>\
    <a id="close" onclick="hideTooltip(\'versions1\')" style="cursor: pointer;">关闭<image id="close_btn" src="../images/closebtn.gif"></a><br>' % js_function
    if table != 'regular':
        string = ''
        versions = get_versions('comparison')

        i = 0
        for each in browsers_list:
            string = string + '<div class="browser_span">'+each+'</div><span> '+versions[i]+'</span><br>'
            i += 1
        response += string
    response += '</div>'
    response += '<h1>'+title +' 测试结果</h1>'
    if table != 'regular':
        response += '<a id="version_link1" onclick="showTooltip(\'versions1\')">点击查看详细版本号</a>'
    return response


def generate_foot():
    response = ""
    response += '<div id="footer"><a class="page_link" href="../index.html"><<返回首页</a><a class="page_link" href="#">回到顶部</a></div></div>\
    <script src="../js/Chart.js/Chart.js"></script>\
    <script src="../js/drawChart.js"></script>\
    </body>'
    return response


def generate_block(dir, mode):
    response = ""
    response += '<div class="data_block">\
    <div class="subtitle"><h3>'+mode+' Results (单位：秒)</h3></div>'
    startpage = dir.split('\\')[1].decode('gbk')
    data = get_data(startpage, mode)
        # data = read_files(dir, mode.split(' ')[0])
    # print(data)
    # print(mode)
    response += generate_table(data)

    # strings = mode.split()
    # if len(strings)>2:
    #     mode = strings[0]+strings[2]
    # else:
    #     mode = strings[0]
    #writeChart('.\images\\'+title+mode+'.jpg',targetFile)

    response += generate_canvas(mode)
    response += '</div>'
    return response


def generate_table(data):
    response = ""

    response += '<div class="table_block">\
    <table>\
    <tr id="chartLabel'+str(index)+'">'


    for each in browsers_list:
        if table == 'regular' and browsers_list.index(each) == len(browsers_list)-1 or table == 'comparison':
            response += '<th>'+each+'</th>'
        else:
            response += '<th class="old_lab">'+each+'</th>'
    response += '</tr>'
    # Write 5 rows of time data
    for rowNo in range(5):
        response += '<tr>'
        # key_string_list = [key.encode('utf-8') for key in data.keys()]
        for each in browsers_list:
            if table == 'regular' and browsers_list.index(each) == len(browsers_list)-1:
                # print(each)
                response += '<td style="font-weight:bolder;">' + data[each][0][rowNo] + '</td>'
            elif table == 'regular':
                response += '<td class="old_value">'+ data[each][0][rowNo] +'</td>'
            else:
                response += '<td>'+ data[each][0][rowNo] +'</td>'
        response += '</tr>'
    response += '<tr id="chartData'+str(index)+'">'

    # Write average result
    for each in browsers_list:
        if table == 'regular' and browsers_list.index(each) == len(browsers_list)-1 or table == 'comparison':
            response += '<th>' + str(data[each][1]) + '</th>'
        else:
            response += '<th class="old_lab">' + str(data[each][1]) + '</th>'

    response += '</tr></table></div>'
    return response


def generate_canvas(mode):
    global index
    response = ""
    if(get_bar_number()>10):
        height="320"
    else:
        height="280"
    response += '<div class="chart_block"><canvas id="canvas'+str(index)+'" height=' + height\
                + ' width="' + str(get_bar_number() * 70 + 40) + '"></canvas></div>'
    index += 1
    return response

if __name__ == "__main__":
    index = 0
    form_data = cgi.FieldStorage()
    debug = 0
    if not debug:
        date = form_data.getvalue('date')
        table = form_data.getvalue('tb')
    #for debugging
    else:
        date = '20141203'
        table = 'comparison'
        os.chdir('..')
    if table=='regular':
        browsers_list = get_versions('regular')
    else:
        browsers_list = get_browsers_list(date)
    response_html = ""
    response_html += generate_head(date)

    response_html += generate_main()


    response_html += generate_foot()
    print('Content-type: text/html\n\n')
    print(response_html)

    # print(dir)

