from tkinter import Label
import PySimpleGUI as sg
import os
import re
import pydot

layout = [  [sg.Input(), sg.FolderBrowse("Choose Project Folder",size=(20))],
            [sg.Input(), sg.FolderBrowse("Choose Image Path",size=(20))], 
            [sg.Button("Start",size=(61),enable_events=True)],
            [sg.Text("Status:"),sg.Text("",key='-TEXT-',enable_events=True)]
         ] 

window = sg.Window('Diagram Creator',icon="Left.ico").Layout(layout)

event, values = window.read()

while True:
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    if event == 'Start':
        if not values[0] or not values[1]:
            window['-TEXT-'].update("Please choose project folder and image path!")
        else:
            window['-TEXT-'].update("Processing...")

            #1
            def list_files(filepath, filetype):
                paths = []
                for root, dirs, files in os.walk(filepath):
                    for file in files:
                        if file.lower().endswith(filetype.lower()):
                            paths.append(os.path.join(root, file))
                return(paths)

            #2
            xamlList = list_files(values[0],'.xaml')

            #3
            mainGraph = pydot.Dot(graph_type='digraph',strict = True)
            subgraphs = []

            #4
            for xamlFile in xamlList:
                if xamlFile != "Main" and xamlFile != "RetryCurrentTransaction" and xamlFile != "SetTransactionStatus" and  xamlFile != "Test": 
                    with open(xamlFile,"r") as xF:
                        xamlContent = re.findall("(?<= DisplayName=\\\")(.*?)(?=\\\")", str(xF.readlines()))
                    
                    resultDict = {}
                    index = 0
                    for match in xamlContent:
                        resultDict[index] = re.sub("(?=&)(.*?)(;)","",match)
                        index += 1

                    index = 1
                    subgraph = pydot.Subgraph()
                    for k,v in resultDict.items():
                        try:
                            edge = pydot.Edge(resultDict[index], resultDict[index+1])
                            subgraph.add_edge(edge)
                            index += 1
                        except:
                            pass
                    subgraphs.append(subgraph)

            #5
            for subg in subgraphs:
                mainGraph.add_subgraph(subg)

            #6
            mainGraph.write_png(os.path.join(values[1],"graph.png"))

            #7
            window['-TEXT-'].update("Finished.")

window.close()