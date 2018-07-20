from appJar import gui
import sys


def setCheckBoxColour(cb):
    if todaysCheckBoxes[cb]:
        app.setCheckBoxFg(cb, "#808080")
        app.setCheckBoxActiveFg(cb, "#808080")
    else:
        app.setCheckBoxFg(cb, "#000000")
        app.setCheckBoxActiveFg(cb, "#000000")


def checkBoxTicked(cb):
    if todaysCheckBoxes[cb]:
        todaysCheckBoxes[cb]=False
    else:
        todaysCheckBoxes[cb]=True
    setCheckBoxColour(cb)

def editButton(btn):
    if btn=="Done":
        count=0
        dic=app.getAllEntries()
        with app.labelFrame("Today's Goals"):
            with open(".TodayLogFile", "w+") as curFile:
                curFile.write("#Deleting this file you wont be able to track your todays goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
                for textAreaName in dic:
                    if "Task" in textAreaName:
                        if todaysCheckBoxes[textAreaName]:
                            curFile.write('1')
                        else:
                            curFile.write('0')
                        curFile.write(dic[textAreaName]+"\n")
                        todaysCheckBoxesContent[textAreaName]=dic[textAreaName]
                        app.hideEntry(textAreaName)
                        app.addNamedCheckBox(dic[textAreaName],textAreaName, count, 0)
                        if todaysCheckBoxes[textAreaName]:
                            app.setCheckBox(textAreaName, ticked=True, callFunction=False)
                        else:
                            app.setCheckBox(textAreaName, ticked=False, callFunction=False)
                        app.setCheckBoxChangeFunction(textAreaName, checkBoxTicked)
                        setCheckBoxColour(textAreaName)
                        count+=1
            app.hideButton("Done")
            app.showButton("Edit")
    elif btn=="Edit":
        dic=app.getAllCheckBoxes()
        count=1
        with app.labelFrame("Today's Goals"):
            for textBoxName in dic:
                if "Task" in textBoxName:
                    todaysCheckBoxes[textBoxName]=app.getCheckBox(textBoxName)
                    app.showEntry(textBoxName)
                    app.setEntry(textBoxName, todaysCheckBoxesContent[textBoxName])
                    app.removeCheckBox(textBoxName)
                    count+=1
            app.hideButton("Edit")
            app.showButton("Done")

def editView():
    app.setSticky("ew")
    app.addEntry("Task1", 0, 0)
    app.addEntry("Task2", 1, 0)
    app.addEntry("Task3", 2, 0)
    app.addButton("Done", editButton, 3, 0)
    app.addButton("Edit", editButton, 3, 0)
    app.hideButton("Edit")

def hideEditView():
    app.hideEntry("Task1")
    app.hideEntry("Task2")
    app.hideEntry("Task3")
    app.hideButton("Done")
    app.showButton("Edit")

def showView():
    with open(".TodayLogFile", "r") as todaysFile:
        line=todaysFile.readline()
        if line:
            while  line[0]=='#':
                line=todaysFile.readline()
                if not line:
                   editView() 
                   return
        if line[0]=='1':
            todaysCheckBoxes["Task1"]=True
        todaysCheckBoxesContent["Task1"]=line[1:-1]
        app.addNamedCheckBox(todaysCheckBoxesContent["Task1"],"Task1", 0, 0)
        app.setCheckBox("Task1", ticked=todaysCheckBoxes["Task1"])
        app.setCheckBoxChangeFunction("Task1", checkBoxTicked)
        setCheckBoxColour("Task1")
        line=todaysFile.readline()
        if line:
            if line[0]=='1':
                todaysCheckBoxes["Task2"]=True
            todaysCheckBoxesContent["Task2"]=line[1:-1]
            app.addNamedCheckBox(todaysCheckBoxesContent["Task2"],"Task2", 1, 0)
            app.setCheckBox("Task2", ticked=todaysCheckBoxes["Task2"])
            app.setCheckBoxChangeFunction("Task2", checkBoxTicked)
            setCheckBoxColour("Task2")
        else:
            todaysCheckBoxesContent["Task2"]=""
            app.addNamedCheckBox("", "Task2", 1, 0)
            app.setCheckBoxChangeFunction("Task2", checkBoxTicked)

        line=todaysFile.readline()
        if line:
            if line[0]=='1':
                todaysCheckBoxes["Task3"]=True
            todaysCheckBoxesContent["Task3"]=line[1:-1]
            app.addNamedCheckBox(todaysCheckBoxesContent["Task3"],"Task3", 2, 0)
            app.setCheckBox("Task3", ticked=todaysCheckBoxes["Task3"])
            app.setCheckBoxChangeFunction("Task3", checkBoxTicked)
            setCheckBoxColour("Task3")
        else:
            todaysCheckBoxesContent["Task3"]=""
            app.addNamedCheckBox("", "Task3", 2, 0)
        app.setCheckBoxChangeFunction("Task3", checkBoxTicked)
        print todaysCheckBoxesContent
        editView()
        hideEditView()

def saveChanges():
    with open(".TodayLogFile", "w+") as curFile:
        curFile.write("#Deleting this file you wont be able to track your todays goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
        for task in todaysCheckBoxes:
            if todaysCheckBoxes[task]:
                curFile.write('1')
            else:
                curFile.write('0')
            curFile.write(todaysCheckBoxesContent[task]+"\n")
    return True

with gui("tba") as app:
    app.setBg("lightblue")
    app.setSize(600, 300)
    with app.tabbedFrame("pages"):
        with app.tab("Today"):
            todaysCheckBoxes={"Task1":False, "Task2":False, "Task3":False}
            todaysCheckBoxesContent={"Task1":"", "Task2":"", "Task3":""}
            with app.labelFrame("Today's Goals"):
                try:
                    showView()
                except IOError:
                    editView() 
                
                


        with app.tab("Long Term"):
            with app.labelFrame("Long Term Goals"):
                app.addEntry("Goals")
        with app.tab("Archieved Goals"):
            app.addEntry("afdf")
    app.setStopFunction(saveChanges)      

