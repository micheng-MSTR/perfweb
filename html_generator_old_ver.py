__author__ = 'Administrator'
# -*- coding:utf-8 -*-

from os import listdir
import os
from shutil import copy
import sys
reload(sys)
sys.setdefaultencoding('gbk')
# Original directory organized as {date}/{machine}/{run mode}

idDict = {'Warm Start':'0','Cold Start 60s':'1','Cold Start 30s':'2'}

def generateAllDirs(root_dir):
    dirs = {}
    for date in os.listdir(root_dir):
        curDir = os.path.join(root_dir,date)
        for machine in listdir(curDir):
            dirs[date+'-'+machine] = os.path.join(curDir,machine)
            print(machine)
    return dirs

def getDir(specifiedDir):
    dir = {}
    date = specifiedDir[specifiedDir.rfind('\\')+1:]
    #print(listdir(specifiedDir))
    for machine in listdir(specifiedDir):
#        print('元数据 '+machine)

        # print('utf-8 编码后'+machine.encode("utf-8"))
        dir[date+'-'+machine.decode("gbk")] = os.path.join(specifiedDir, machine)
        uni = u'what'
#        print('gbk 解码后 ')
#        print('utf-8 编码后 '+machine.decode("gbk").encode("utf-8"))
    return dir

def getBarNumber():
    with open(target_dir+'\\'+browsersListFile) as f:
        num = len(f.readlines())
    return num

def getBrowsersList():
    with open(target_dir+browsersListFile,'r') as f:
        list = [each.split(' ')[0] for each in f.readlines()]
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
        data[br] = [round(float(s)/1000,2) for s in tmp]
        data[br].remove(max(data[br]))
        data[br].remove(min(data[br]))
    #print(data)
    return data

def generateWebPage(title, machine, target_dir):
    #copyResources(title, machine, target_dir)
    with open(target_dir+title+'.html','w') as webPage:
        writeHead(title, webPage)
        warmDir,cold60Dir,cold30Dir = machine+'\\60s',machine+'\\60s',machine+'\\30s'
        writeBlock('Warm Start', warmDir, webPage)
        writeBlock('Cold Start 60s', cold60Dir, webPage)
        writeBlock('Cold Start 30s', cold30Dir, webPage)
        writeFoot(webPage)

def generateIndexPage(titleList):
    return None

def writeHead(utitle, targetFile):
    title = utitle.encode('utf-8')
    targetFile.write('<head><title>')
    targetFile.write('启动性能对比测试')
    targetFile.write('</title><link rel="icon" href="images/logo.png"><link rel="stylesheet" href="style.css"><meta charset="UTF-8">')
    targetFile.write('<script src="js/resultPage.js"></script></head>')
    targetFile.write('<body onload="hideTooltip();drawCharts();">')
    targetFile.write('<div id="banner"><p id="title" onclick="location.href=\'index.html\'" onmouseover="this.style.cursor=\'hand\'">浏览器启动性能横向对比测试</p></div>')
    targetFile.write('<div id="main"><div id="back" ><a class="page_link" href="index.html"><<返回首页</a></div>')
    targetFile.write('<div id="versions" style="display:none"><span id="versions_box_corner"></span><span style="font-weight:bolder">详细版本号:</span><a href="#" id="close" onclick="hideTooltip()">关闭<image id="close_btn" src="./images/closebtn.gif"></a><br>')
    string = ''
    versions = getVersions()

    i=0
    for each in browsersList:
        string = string + '<div class="browser_span">'+each+'</div><span> '+versions[i]+'</span><br>'
        i=i+1
    targetFile.write(string+'</div>')
    targetFile.write('<h1>'+title +'</h1>')
    targetFile.write('<a id="version_link" href="#" onclick="showTooltip()">点击查看详细版本号</a>')


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
    targetFile.write('<tr id="chartLabel'+idDict[mode]+'">')

    for each in browsersList:
        targetFile.write('<th>'+each+'</th>')
    targetFile.write('</tr>')
    # Write 5 rows of time data
    for rowNo in range(5):
        targetFile.write('<tr>')
        for each in sorted(data.keys()):
            targetFile.write('<td>'+str(data[each][rowNo])+'</td>')
        targetFile.write('</tr>')
    average = []
    for each in sorted(data.keys()):
        li = data[each]
        average.append(round(sum(li)/len(li),2))
    #print(average)
    targetFile.write('<tr id="chartData'+idDict[mode]+'">')
    for each in average:
        targetFile.write('<th>'+str(each)+'</th>')
    targetFile.write('</tr>')
    targetFile.write('</table>')
    targetFile.write('</div>')

def writeChart(image, targetFile):
    targetFile.write('<img src="'+image+'">')

def writeCanvas(mode, targetFile):
    if(getBarNumber()>10):
        height="320"
    else:
        height="280"
    targetFile.write('<div class="chart_block"><canvas id="canvas'+idDict[mode]+'" height='+height+' width="'+str(getBarNumber()*70+40)+'"></canvas></div>')

root_dir = 'D:\Work\Performance Test\webpage result'
target_dir = 'E:\Learning\JavaScript\PerformanceWeb\\'
browsersListFile = 'list.txt'


browsersList = getBrowsersList()

# run all results
dirs = generateAllDirs(root_dir)
for each in dirs.keys():
    generateWebPage(each, dirs[each], target_dir)

browsersListFile = 'list2.txt'
browsersList = getBrowsersList()

txtDir = 'D:\Work\Performance Test\\result\\20141126'
dir = getDir(txtDir)
for each in dir.keys():
    generateWebPage(each, dir[each], target_dir)


txtDir = 'D:\Work\Performance Test\\result\\20141127'
dir = getDir(txtDir)
for each in dir.keys():
    generateWebPage(each, dir[each], target_dir)

# run results under specific directory
browsersListFile = 'list3.txt'
browsersList = getBrowsersList()

txtDir = 'D:\Work\Performance Test\\result\\20141203'
dir = getDir(txtDir)
for each in dir.keys():
    generateWebPage(each, dir[each], target_dir)


