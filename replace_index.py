# -*- coding: utf-8 -*-
__author__ = 'Administrator'


from shutil import copy

def updateIndexPage(filePath, date, tag):
    indexPage = filePath+'index.html'
    with open(indexPage,'r') as page:
        text = page.read()
        latestIndex = text.find('"latest"')
        insertIndex = text.find('<ul>')
        newLink = date+'.html'
        newTitle = date+' '+tag+'测试结果'
        replaceString = text.replace(text[insertIndex:latestIndex+8],'<ul><li><a class="latest" href="'+newLink+'">'+newTitle+'</a></li><li><a class="page_link"')

    copy(indexPage, filePath+'index.bak')

    with open(indexPage,'w') as page:
        page.write(replaceString)

        # print(insertIndex)

# copy test


# indexPage = 'E:\Learning\JavaScript\PerformanceWeb\index.html'
# updateIndexPage(indexPage,'test.html','testlink')
