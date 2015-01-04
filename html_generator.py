__author__ = 'Administrator'
# -*- coding:utf-8 -*-

from os import listdir
import os
from shutil import copy
import sys
import replace_index
reload(sys)
sys.setdefaultencoding('gbk')
# Original directory organized as {date}/{machine}/{run mode}
idDict = {'Warm Start':'0','Cold Start 60s':'1','Cold Start 30s':'2','默认页':'1','空白页':'2','百度':'3'}
global index


def generateAllDirs(root_dir):
    dirs = {}
    for date in os.listdir(root_dir):
        curDir = os.path.join(root_dir,date)
        for machine in listdir(curDir):
            dirs[date+'-'+machine] = os.path.join(curDir,machine)
            print(machine)
    return dirs

def getDirs(specifiedDir):
    dir = {}
    date = specifiedDir[specifiedDir.rfind('\\')+1:]
    #print(listdir(specifiedDir))
    for startPage in listdir(specifiedDir):
#        print('元数据 '+machine)

        # print('utf-8 编码后'+machine.encode("utf-8"))
        dir[startPage.decode("gbk")] = os.path.join(specifiedDir, startPage)
        uni = u'what'
#        print('gbk 解码后 ')
#        print('utf-8 编码后 '+machine.decode("gbk").encode("utf-8"))
    return dir

def getBarNumber():
    with open(target_dir+'\\'+browsersListFile) as f:
        num = len(f.readlines())
    return num

def getBrowsersList():
    list = []
    with open(target_dir+browsersListFile,'r') as f:
        for each in f.readlines():
            br = each.split(' ')[0]
            list.append(br.decode('gbk').encode('utf-8'))
            # list = [each.split(' ')[0] for each in f.readlines()]
    print(list)
    return list

def getVersions():
    versions = []
    with open(target_dir+browsersListFile,'r') as f:
        lines = f.readlines()
    for each in lines:
        versions.append(each.split(' ')[1])
    return versions

def copyResources(title, sourceDir, targetDir):
    for root, dirs, files in os.walk(sourceDir):
        for name in files:
            if '.jpg' in name:
                copy(root+'\\'+name, targetDir+'images\\'+title+name)

def readFiles(dir, mode):
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

def generateWebPage(sourceDir, targetDir):
    global index
    index = 0
    date = sourceDir[sourceDir.rfind('\\')+1:]
    dir = getDirs(txtDir)
    #copyResources(title, machine, target_dir)
    with open(target_dir+date+'.html','w') as webPage:
        writeHead(date, webPage)
        webPage.write('<div id="nav_bar"><ul id="nav_list">')
        startPages = sorted(dir.keys(),reverse=True)
        for each in startPages:
            i = idDict[each.encode('utf-8')]
            if i=='1':
                className='selected'
                style = 'border-left: 1px solid #003D79'
            else:
                className='unselected'
                style=''
            webPage.write('<li id="tag_'+i+'" class="'+className+'" style="'+style+'" onclick="switchPanel(this.id)" onmouseover="highLight(this.id)" onmouseout="cancelHighLight(this.id)">'+each.encode('utf-8')+'</li>')
        webPage.write('</ul></div><div id="content">')
        for each in sorted(dir.keys(),reverse=True):
            print(each)
            webPage.write('<div class="content_data" id="start_page_'+idDict[each.encode('utf-8')]+'">')
            writePage(dir[each], webPage)
            webPage.write('</div>')
        webPage.write(('</div>'))
        writeFoot(webPage)
        return date

def writePage(page, targetFile):
    warmDir,cold60Dir,cold30Dir = page+'\\Warm',page+'\\60s',page+'\\30s'
    writeBlock('Warm Start', warmDir, targetFile)
    # writeBlock('Cold Start', cold60Dir, targetFile)
    writeBlock('Cold Start 60s', cold60Dir, targetFile)
    writeBlock('Cold Start 30s', cold30Dir, targetFile)


def generateIndexPage(titleList):
    return None

def writeHead(utitle, targetFile):
    title = utitle.encode('utf-8')
    targetFile.write('<head><title>')
    targetFile.write('启动性能对比测试')
    targetFile.write('</title><link rel="icon" href="images/logo.png"><link rel="stylesheet" href="style.css"><meta charset="UTF-8">')
    targetFile.write('<script src="js/resultPage.js"></script></head>')
    targetFile.write('<body onload="switchPanel(\'tag_1\'); drawCharts();">')
    targetFile.write('<div id="banner" ><div id="title_container"><span id="title" onclick="location.href=\'index.html\'" >浏览器启动性能横向对比测试</span></div></div>')
    targetFile.write('<div id="main"><div id="back" ><a class="page_link" href="index.html"><<返回首页</a></div>')
    targetFile.write('<div id="versions1" style="display:none"><span id="versions_box_corner"></span><span style="font-weight:bolder">详细版本号:</span><a href="#" id="close" onclick="hideTooltip(\'versions1\')">关闭<image id="close_btn" src="./images/closebtn.gif"></a><br>')
    string = ''
    versions = getVersions()

    i=0
    for each in browsersList:
        string = string + '<div class="browser_span">'+each+'</div><span> '+versions[i]+'</span><br>'
        i=i+1
    targetFile.write(string+'</div>')
    targetFile.write('<h1>'+title +' 测试结果</h1>')
    targetFile.write('<a id="version_link1" onclick="showTooltip(\'versions1\')">点击查看详细版本号</a>')


def writeFoot(targetFile):
    targetFile.write('<div id="footer"><a class="page_link" href="index.html"><<返回首页</a><a class="page_link" href="#">回到顶部</a></div></div>')
    targetFile.write('<script src="js/Chart.js/Chart.js"></script>')
    targetFile.write('<script src="js/drawChart.js"></script>')
    targetFile.write('</body>')


def writeBlock(mode, dir, targetFile):
    targetFile.write('<div class="data_block">')
    targetFile.write('<div class="subtitle"><h3>'+mode+' Results (单位：秒)</h3></div>')

    data = readFiles(dir, mode.split(' ')[0])
    writeTable(data, mode, targetFile)

    # strings = mode.split()
    # if len(strings)>2:
    #     mode = strings[0]+strings[2]
    # else:
    #     mode = strings[0]
    #writeChart('.\images\\'+title+mode+'.jpg',targetFile)
    writeCanvas(mode, targetFile)
    targetFile.write('</div>')

def writeTable(data, mode, targetFile):
    targetFile.write('<div class="table_block">')
    targetFile.write('<table>')
    targetFile.write('<tr id="chartLabel'+str(index)+'">')

    for each in browsersList:
        targetFile.write('<th>'+each+'</th>')
    targetFile.write('</tr>')
    # Write 5 rows of time data
    # print(sorted(data.keys()))
    for rowNo in range(5):
        targetFile.write('<tr>')
        for each in sorted(data.keys(),key=str.lower):
            targetFile.write('<td>'+str(data[each][rowNo])+'</td>')
        targetFile.write('</tr>')
    average = []
    for each in sorted(data.keys(),key=str.lower):
        li = data[each]
        average.append(round(sum(li)/len(li),2))
    #print(average)

    targetFile.write('<tr id="chartData'+str(index)+'">')

    for each in average:
        targetFile.write('<th>'+str(each)+'</th>')
    targetFile.write('</tr>')
    targetFile.write('</table>')
    targetFile.write('</div>')

def writeChart(image, targetFile):
    targetFile.write('<img src="'+image+'">')

def writeCanvas(mode, targetFile):
    global index
    if(getBarNumber()>10):
        height="320"
    else:
        height="280"
    targetFile.write('<div class="chart_block"><canvas id="canvas'+str(index)+'" height='+height+' width="'+str(getBarNumber()*70+40)+'"></canvas></div>')
    index += 1



target_dir = 'E:\Learning\JavaScript\PerformanceWeb\\'

# root_dir = 'D:\Work\Performance Test\webpage result'
# browsersListFile = 'list.txt'
# browsersList = getBrowsersList()

# run all results
# dirs = generateAllDirs(root_dir)
# for each in dirs.keys():
#     generateWebPage(each, dirs[each], target_dir)

browsersListFile = 'list2.txt'
browsersList = getBrowsersList()

txtDir = 'D:\Work\Performance Test\\result\\20141126'
dir = getDirs(txtDir)
date = generateWebPage(txtDir, target_dir)


# txtDir = 'D:\Work\Performance Test\\result\\20141127'
# dir = getDir(txtDir)
# for each in dir.keys():
#     generateWebPage(each, dir[each], target_dir)

# run results under specific directory
# browsersListFile = 'list3.txt'
# browsersList = getBrowsersList()
browsersListFile = 'list4.txt'
browsersList = getBrowsersList()

# txtDir = 'D:\Work\Performance Test\\result\\20141211'
# txtDir = 'D:\Work\Performance Test\\result\\20141216'
# date = generateWebPage(txtDir, target_dir)
# tag = 'M38'

# browsersListFile = 'list5.txt'
# browsersList = getBrowsersList()
# print(browsersList)
# for each in browsersList:
#     print(each)
# txtDir = 'D:\Work\Performance Test\\result\\20141218'
#
# date = generateWebPage(txtDir, target_dir)
# tag = '横向对比'
#


# replace_index.updateIndexPage(target_dir, date, tag)



