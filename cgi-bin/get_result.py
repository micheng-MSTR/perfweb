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
from shutil import copy
import sys
# import replace_index
reload(sys)
sys.setdefaultencoding('gbk')
# Original directory organized as {date}/{start page}/{run mode}
id_dict = {'Warm Start':'0','Cold Start 60s':'1','Cold Start 30s':'2','默认页':'1','空白页':'2','百度':'3'}
global index


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
    with open('data/' + date + '/list.txt','r') as f:
        num = len(f.readlines())
    return num

def get_browsers_list():
    list = []
    with open('data/' + date + '/list.txt','r') as f:
        for each in f.readlines():
            br = each.split(' ')[0]
            list.append(br.decode('gbk').encode('utf-8'))
            # list = [each.split(' ')[0] for each in f.readlines()]
    print(list)
    return list

def get_versions():
    versions = []
    with open('data/' + date + '/list.txt','r') as f:
        lines = f.readlines()
    for each in lines:
        versions.append(each.split(' ')[1])
    return versions


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
        response += generate_block(dir[each] + '/Warm', 'Warm')
        response += generate_block(dir[each] + '/60s', 'Cold')
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
    response += '<head><title>启动性能对比测试</title>\
    <link rel="icon" href="../images/logo.png"><link rel="stylesheet" href="../style.css"><meta charset="UTF-8">\
    <script src="../js/resultPage.js"></script></head>\
    <body onload="switchPanel(\'tag_1\'); drawCharts();">\
    <div id="banner" ><div id="title_container"><span id="title" onclick="location.href=\'index.html\'" >浏览器启动性能横向对比测试</span></div></div>\
    <div id="main"><div id="back" ><a class="page_link" href="../index.html"><<返回首页</a></div>\
    <div id="versions1" style="display:none"><span id="versions_box_corner"></span>\
    <span style="font-weight:bolder">详细版本号:</span>\
    <a href="#" id="close" onclick="hideTooltip(\'versions1\')">关闭<image id="close_btn" src="../images/closebtn.gif"></a><br>'
    string = ''
    versions = get_versions()

    i = 0
    for each in browsers_list:
        string = string + '<div class="browser_span">'+each+'</div><span> '+versions[i]+'</span><br>'
        i += 1
    response += string
    response += '</div>\
    <h1>'+title +' 测试结果</h1>\
    <a id="version_link1" onclick="showTooltip(\'versions1\')">点击查看详细版本号</a>'
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

    data = read_files(dir, mode.split(' ')[0])
    response += generate_table(data, mode)

    # strings = mode.split()
    # if len(strings)>2:
    #     mode = strings[0]+strings[2]
    # else:
    #     mode = strings[0]
    #writeChart('.\images\\'+title+mode+'.jpg',targetFile)
    response += generate_canvas(mode)
    response += '</div>'
    return response

def generate_table(data, mode):
    response = ""
    response += '<div class="table_block">\
    <table>\
    <tr id="chartLabel'+str(index)+'">'


    for each in browsers_list:
        response += '<th>'+each+'</th>'
    response += '</tr>'
    # Write 5 rows of time data
    # print(sorted(data.keys()))
    for rowNo in range(5):
        response += '<tr>'
        for each in sorted(data.keys(),key=str.lower):
            response += '<td>'+str(data[each][rowNo])+'</td>'
        response += '</tr>'
    average = []
    for each in sorted(data.keys(),key=str.lower):
        li = data[each]
        average.append(round(sum(li)/len(li),2))
    #print(average)

    response += '<tr id="chartData'+str(index)+'">'

    for each in average:
        response += '<th>'+str(each)+'</th>'
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
    date = form_data.getvalue('date')
    # date = '20141231'
    # os.chdir('..')
    browsers_list = get_browsers_list()
    response_html = ""
    response_html += generate_head(date)

    response_html += generate_main()

    # for each in dir.keys():
    #     data = read_files(dir[each] + '/Warm', "Warm")
    #     print(data)

    response_html += generate_foot()
    print('Content-type: text/html\n\n')
    print(response_html)
    # print(dir)

