import os
from anytree import Node, RenderTree
from collections import deque
import networkx as nx
from random import randint
from pyvis.network import Network
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import re
import pyvis._version
import networkx as nx

root = './ekart-cl-ui'
Savefolder = './'

def createColorDict(contentList, interestedFolder):
    colorDict = {}
    flag=0
    denom=1/54
    for c in contentList:
    
        if os.path.isdir(root+interestedFolder+'/'+c):
            flag+=denom
            compColor = randint(1,255)/255

            colorDict[root+interestedFolder+'/'+c] = flag
    return colorDict

def routeDict(fileName, importDict):
    # Example code snippet
    with open(fileName, 'r') as file:
        code = file.read()
    # print('File: ',code)
    # Define a regular expression pattern to match ProtectedRoute tags
    pattern = r'<\w*Route(?:.|\n)*?\n+?\s+?/>?\n+'

    # Find all matches of ProtectedRoute tags and extract the render attribute content
    matches = re.findall(pattern, code)
    # print(list(importDict['import'].items()))
    # print('Link!', importDict['link'])
    # Initialize an empty dictionary to store component-link pairs
    component_link_dict = {}
    # print(importDict['import'].items())
    # Iterate through the matches and extract component and link information
    for imp in importDict['import'].items():
        for match in matches:
            # print('Each match', match)
            # Extract the component and link using regular expressions
            if imp[1][0] in match:
                # print(imp[1][0])

                component_match = re.findall(r'render(?:.|\n)+?\/>', match)
                link_match1 = re.findall(r"path?.*?\{?.*?\}\n+", match)
                
                print('Link? ', link_match1)
                
                if component_match and link_match1:
                    link_match = link_match1[0].split("/")
                    # print(link_match)
                    if len(link_match)>1:
                        link = importDict['link']+'/'+'/'.join(('/'.join(link_match[1:])).split('`')[:-1])
                    else:
                        link = importDict['link']
                    # print('Component? ', component_match, imp[0])
                    # print('Path? ', link_match1)
                    component_link_dict[imp[0]] = link
                break
            
    # Print the resulting dictionary
    # print(component_link_dict)  
    return(component_link_dict)  
def createAbsFilePath(base,fileName):
    absFilePath1 = fileName.split('/')
    if absFilePath1[-1]=='index':
        absFilePath = absFilePath1[:-1]
        # print(absFilePath)
    else:
        absFilePath = absFilePath1
    if ("." or "..") in fileName:
        count = 0
        for relpath in absFilePath:
            if relpath == "..":
                count+=1
        baseSplit = base.split('/')
        basePath = '/'.join(baseSplit[:len(baseSplit)-count])
        finalAbsPath = basePath+'/'+'/'.join(absFilePath[count:])
    else:
        finalAbsPath = root+'src/'+'/'.join(absFilePath)
    return finalAbsPath


def parseFileForImports(root,base,f, interestedFolder, interestedFolderB):
    connectedFiles = {}
    with  open(base+'/'+f, "r") as fcontent:
        flag=0
        while 1:
            fileLine_temp = ''
            finalRelPath = ''
            importComp = []
            fileName = ''
            flag+=1
            line=fcontent.readline()
            if not line:
                break
            else:   
                if 'React.lazy' in line or 'lazy' in line or 'import ' in line or ('index' in f and ('export' in line and 'from' in line)):
                    if ';\n' not in line: # we first make it one long line like regular imports
                        while 1: # When the import spills over to multiple lines
                            fileLine_temp = fileLine_temp + line.split('\n')[0]
                            if(';\n' in line):
                                break                        
                            line = fcontent.readline()
                    else:
                        fileLine_temp = line.split('\n')[0]
                if 'React.lazy' in fileLine_temp or 'lazy(' in fileLine_temp:
                    importComp = fileLine_temp.split('const ')[1].split('=')[0].replace(" ","").split(',')
                    fileName = ''.join(fileLine_temp.split('import')[-1].split("('")).split("')")[0]
                if 'import ' in line and 'from' in fileLine_temp:
                    fileName = fileLine_temp.split('from')[-1].split(';')[0].strip().strip("'")
                    importComp = ''.join(''.join(fileLine_temp.split('import')[1].split('from')[0].split('{ ')).split(' }')).replace(" ","").split(',')
                if 'index' in f and len(connectedFiles)==0 and ('export' in line and 'from' in line):
                    fileName = fileLine_temp.split('from')[-1].split(';')[0].strip().strip("'")
                    # print(fileLine_temp.split('export')[1].split('from')[0].split('{ ')).split(' }')
                    importComp = ''.join(''.join(fileLine_temp.split('export')[1].split('from')[0].split('{ ')).split(' }')).replace(" ","").split(',')
                finalRelPath = os.path.relpath(createAbsFilePath(base,fileName), root+interestedFolder)
                finalRelPathB = os.path.relpath(createAbsFilePath(base,fileName), root+interestedFolderB)
                if (".." not in finalRelPath or ".." not in finalRelPathB) and 'style' not in finalRelPath and 'Style' not in finalRelPath and 'Loader' not in finalRelPath:
                    # print(finalRelPath)
                    connectedFiles[finalRelPath] = importComp
            
    return connectedFiles
    # connectedFiles = {}
    # with  open(base+'/'+f, "r") as fcontent:
    #     flag=0
    #     while 1:
    #         fileLine_temp = ''
    #         finalRelPath = ''
    #         importComp = []
    #         fileName = ''
    #         flag+=1
    #         line=fcontent.readline()
    #         if not line:
    #             break
    #         else:   
    #             if 'React.lazy' in line or 'import ' in line or ('index' in f and ('export' in line and 'from' in line)):
    #                 if ';\n' not in line: # we first make it one long line like regular imports
    #                     while 1: # When the import spills over to multiple lines
    #                         fileLine_temp = fileLine_temp + line.split('\n')[0]
    #                         if(';\n' in line):
    #                             break                        
    #                         line = fcontent.readline()
    #                 else:
    #                     fileLine_temp = line.split('\n')[0]
    #             if 'React.lazy' in fileLine_temp:
    #                 importComp = fileLine_temp.split('const ')[1].split('=')[0].replace(" ","").split(',')
    #                 fileName = ''.join(fileLine_temp.split('import')[-1].split("('")).split("')")[0]
    #             if 'import ' in line and 'from' in fileLine_temp:
    #                 fileName = fileLine_temp.split('from')[-1].split(';')[0].strip().strip("'")
    #                 importComp = ''.join(''.join(fileLine_temp.split('import')[1].split('from')[0].split('{ ')).split(' }')).replace(" ","").split(',')
    #             if 'index' in f and len(connectedFiles)==0 and ('export' in line and 'from' in line):
    #                 fileName = fileLine_temp.split('from')[-1].split(';')[0].strip().strip("'")
    #                 # print(fileLine_temp.split('export')[1].split('from')[0].split('{ ')).split(' }')
    #                 importComp = ''.join(''.join(fileLine_temp.split('export')[1].split('from')[0].split('{ ')).split(' }')).replace(" ","").split(',')
    #             finalRelPath = os.path.relpath(createAbsFilePath(base,fileName), root+interestedFolder)
    #             finalRelPathB = os.path.relpath(createAbsFilePath(base,fileName), root+interestedFolderB)
    #             if (".." not in finalRelPath or ".." not in finalRelPathB) and 'style' not in finalRelPath and 'Style' not in finalRelPath and 'Loader' not in finalRelPath:
    #                 connectedFiles[finalRelPath] = importComp
            
    # return connectedFiles

def getMainRoute(root, appName, interestedFolder, interestedFolderB, JustAppName):
    importDictFiles ={}
    for base, dirs, files in os.walk(root+appName):
            for ind,f in enumerate(files):
                if ('AuthWrapper' in f or 'RootComponent' in f) and (f.endswith(('.tsx')) or f.endswith(('.ts')) or f.endswith('.js')) :
                    print(f)
                    finalRelFilePath = os.path.relpath(base,  root+interestedFolder)
                    group = os.path.relpath(base,  root+appName)
                    fname = finalRelFilePath+'/'+f.split('.')[0]
                    connectedFiles = parseFileForImports(root,base, f, interestedFolder, interestedFolderB)
                    importDictFiles = {'import': connectedFiles, 'label':f.split('.')[0]}
                    importDictFiles['link']='http://10.24.1.71/'+JustAppName
                    routeDict1=routeDict(base+'/'+f, importDictFiles)
                    return routeDict1

def createDict(root, appName, colorDict, interestedFolder, interestedFolderB):
    importDictFiles = {}
    nodeColorDict = {}
    nodeGroup = {}
    dictNodes = []
    flag = 0
    appNameTemp = appName.split('/')
    appNameInd = appNameTemp.index('apps')
    JustAppName = appNameTemp[appNameInd+1]
    mainRoute = getMainRoute(root,appName, interestedFolder, interestedFolderB, JustAppName)
    print('MAIN ROUTE',mainRoute)
    if flag>-1:
        for base, dirs, files in os.walk(root+appName):
            dirs.sort()
            for ind,f in enumerate(sorted(files)):
                if (f.endswith(('.tsx')) or f.endswith(('.ts')) or f.endswith('.js')) and ('test' not in f ) or f=='index.js':
                    finalRelFilePath = os.path.relpath(base,  root+interestedFolder)
                    group = os.path.relpath(base,  root+appName)
                    fname = finalRelFilePath+'/'+f.split('.')[0]
                    connectedFiles = parseFileForImports(root,base, f, interestedFolder, interestedFolderB)
                    print('Next file', fname)
                    if 'index' in f:
                        fname=finalRelFilePath
                    if connectedFiles.__len__:
                        dictNodes.append(fname)
                    parentComp = finalRelFilePath.split('/')[0]
                    if fname in importDictFiles:

                        importDictFiles[fname].update({'import': connectedFiles, 'label':f.split('.')[0], group: base})
                    else:
                        importDictFiles[fname] = {'import': connectedFiles, 'label':f.split('.')[0], group: base}
                    # if('AuthWrapper' in f):
                    #     importDictFiles[fname]['link']='http://10.24.1.71/hub-ops'
                    if('Routes' in f or 'AuthWrapper' in f):
                        # print(f)
                        if fname in mainRoute:
                            importDictFiles[fname]['link']=mainRoute[fname]
                        routeDict1=routeDict(base+'/'+f, importDictFiles[fname])
                        # print('Current imports', routeDict1)
                        # print(routeDict1.items())
                        for k in routeDict1.items():
                            print(k)
                            if k[0] in importDictFiles.keys():
                                print(k[0])
                                importDictFiles[k[0]]['link']=k[1]
                                print(importDictFiles[k[0]])
                            else:
                                importDictFiles[k[0]]={'link': k[1]}
                    for k in colorDict.keys():
                        if '/'+ group+'/' in k +'/':
                            nodeColorDict[fname] = colorDict[k]
                            break
                        else:
                            nodeColorDict[fname] = 0
                    nodeGroup[fname] = {'group': group}
                    flag+=1
    return importDictFiles, dictNodes, nodeGroup, nodeColorDict
def createGraph(dictNodes, importDictFiles, nodeGroup, filename):
    G = nx.DiGraph()
    flag=0
    for (ind, node )in enumerate(dictNodes):
        G.add_node(node, label=importDictFiles[node]['label'], title=node, group=nodeGroup[node]['group'])
        if 'link' in importDictFiles[node]:
            G.nodes[node]['title'] = '<a href="{}" target="_blank">{}</a>'.format(importDictFiles[node]['link'], node)
        connectedNodes = list(importDictFiles[node]['import'].keys())
        for othernode in importDictFiles[node]['import']:
            G.add_edge(othernode,node,title=','.join(importDictFiles[node]['import'][othernode]), value=len(importDictFiles[node]['import'][othernode]))
        G.nodes[node]['size']=G.in_degree(node)+20
    nt = Network(directed=True, height="90vh", neighborhood_highlight=True)
    nt.from_nx(G)
    nt.save_graph(filename+'.html')
    return G

def createFile(appNameInp,intFolder):
    appName='src/apps/'+appNameInp
    interestedFolder = appName+'/'+intFolder
    interestedFolderB=interestedFolder
    # interestedFolderB= appName #+'/widgets'
    contentList = os.listdir(root+interestedFolder)
    colorDict = createColorDict(contentList, interestedFolder)
    [importDictFiles, dictNodes, nodeGroup, nodeColorDict] = createDict(root,interestedFolder, colorDict,interestedFolder, interestedFolderB)
    createGraph(dictNodes, importDictFiles,nodeGroup, f'{Savefolder}polls/templates/polls/nx_{appNameInp}')

if __name__ == '__main__':
    rootFolderInp = input('are you interested in visualizing web apps?(y/n)')
    if(rootFolderInp=='y'):
        root=root+'-apps/'
    else:
        root=root+'-native-apps/'
    appNameInp=input('What is the app you are interested in?')
    appName= 'src/apps/' + appNameInp
    intFolder=input('Interactions within which folder?')
    interestedFolder = appName+'/'+intFolder
    interestedFolderInp=input('Any other interactions you want to visualize?(y/n)')
    interestedFolderB = interestedFolder
    if(interestedFolderInp=='y'):
        interestedFolderB=input('What is the interaction folder name?')
    contentList = os.listdir(root+interestedFolder)
    colorDict = createColorDict(contentList, interestedFolder)
    [importDictFiles, dictNodes, nodeGroup, nodeColorDict] = createDict(root,interestedFolder, colorDict, interestedFolder, interestedFolderB)
    createGraph(dictNodes, importDictFiles, nodeGroup, './nx_'+appNameInp)
