from appJar import gui
import time
import sys


def setCheckBoxColour(cb):
    #changes the colour of the checkbox to gray when ticked and black otherwise
    if todaysCheckBoxes[cb]:
        app.setCheckBoxFg(cb, "#808080")
        app.setCheckBoxActiveFg(cb, "#808080")
    else:
        app.setCheckBoxFg(cb, "#000000")
        app.setCheckBoxActiveFg(cb, "#000000")


def checkBoxTicked(cb):
    #when a check box is ticked we need to update the global stored values of the checkboxes
    if todaysCheckBoxes[cb]:
        todaysCheckBoxes[cb]=False
    else:
        todaysCheckBoxes[cb]=True
    setCheckBoxColour(cb)

def editButton(btn):
    #the main functionlity of this button is to switch between the checkboxes and the entries 
    #and connect them so that the entries edit the contents of the checkboxes
    if btn=="Done":
        #then user is done editing the entries and he needs to see the updated checkboxes
        count=0
        dic=app.getAllEntries()
        dicKeySorted=sorted(app.getAllEntries().keys())
        #writing the changes on the file is not entirely needed since its done on exit either way
        #it may be useful but if its a permormance problem later on i can remove it
        with app.labelFrame("Today's Goals"):
            with open(".TodayLogFile", "w+") as curFile:
                curFile.write("#Deleting this file you wont be able to track your todays goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
                for textAreaName in dicKeySorted:
                    if textAreaName.startswith("Task"):
                        #write to file
                        if todaysCheckBoxes[textAreaName]:
                            curFile.write('1')
                        else:
                            curFile.write('0')
                        curFile.write(dic[textAreaName]+"\n")
                        #update the memory copy of the checkboxes
                        oldContent=todaysCheckBoxesContent[textAreaName]
                        todaysCheckBoxesContent[textAreaName]=dic[textAreaName]
                        #hide the entry
                        app.hideEntry(textAreaName)
                        #add the updated checkbox
                        app.addNamedCheckBox(dic[textAreaName],textAreaName, count, 0, colspan=2)
                        #update its ticked state
                        if todaysCheckBoxes[textAreaName] and oldContent!='' and oldContent==todaysCheckBoxesContent[textAreaName]:
                                app.setCheckBox(textAreaName, ticked=True, callFunction=False)
                                todaysCheckBoxes[textAreaName]=True
                                setCheckBoxColour(textAreaName)
                        else:
                            #if a checkbox's state is false or its content was edited was edited untick
                            app.setCheckBox(textAreaName, ticked=False, callFunction=False)
                            todaysCheckBoxes[textAreaName]=False
                            setCheckBoxColour(textAreaName)
                        #on click use the checkBoxTicked function 
                        app.setCheckBoxChangeFunction(textAreaName, checkBoxTicked)
                        #set the correct colour
                        setCheckBoxColour(textAreaName)
                        count+=1
            app.hideButton("Done")
            app.showButton("Edit")
            app.hideButton("Cancel")
            app.showButton("Archieve")
    elif btn=="Edit":
        #then the user wants to edit the contents of the checkboxes
        #and needs to see the entries
        dic=app.getAllCheckBoxes()
        dicKeySorted=sorted(app.getAllCheckBoxes().keys())
        count=1
        with app.labelFrame("Today's Goals"):
            for checkBoxName in dicKeySorted:
                if checkBoxName.startswith("Task"):
                    #show the entry and edit its content with the content of the
                    #checkbox respectively
                    app.showEntry(checkBoxName)
                    app.setEntry(checkBoxName, todaysCheckBoxesContent[checkBoxName])
                    #I need to remove the checkboxes and make them again when needed
                    #because the appJar library doesn't provide
                    #a way to set a namedCheckBox's content
                   # app.setCheckBox(checkBoxName, ticked=False)
                   # todaysCheckBoxes[checkBoxName]=False
                    app.removeCheckBox(checkBoxName)
                    count+=1
            app.hideButton("Edit")
            app.showButton("Done")
            app.hideButton("Archieve")
            app.showButton("Cancel")

def archieveButton(btn):
    pass

def addEntriesElements(listOfEntries):
    #adds as much entries elements as there are in the given list with the name provided
    #ex: ["Task1", "Task2"]
    #adds two Entries elements with the respective names
    count=0
    for entry in listOfEntries:
        app.addEntry(entry, count, 0, colspan=2)
        count+=1

def setEntriesElements(listOfEntries, dicOfContent):
    #set the entries elements with the provided content in the dictionary
    for entry in listOfEntries:
        app.setEntry(entry, dicOfContent[entry])


def hideEntriesElements(listOfEntries):
    #hides all the entry elements found in the given list
    for entry in listOfEntries:
        app.hideEntry(entry)

def addCheckBoxesElementsFromFile(listOfCheckBoxes, inputFile):
    #adds as much checkboxes as there are in the given list with the name provided
    #and with the content found in the local file
    with open(inputFile, "r") as todaysFile:
        count=0
        for checkBox in listOfCheckBoxes:
            line=todaysFile.readline()
            if line:
                #ignore comment lines
                while line and line[0]=='#':
                    line=todaysFile.readline()
                if line[0]=='1':
                    todaysCheckBoxes[checkBox]=True
                todaysCheckBoxesContent[checkBox]=line[1:-1]
                app.addNamedCheckBox(todaysCheckBoxesContent[checkBox],checkBox, count, 0, colspan=2)
                app.setCheckBox(checkBox, ticked=todaysCheckBoxes[checkBox])
                app.setCheckBoxChangeFunction(checkBox, checkBoxTicked)
                setCheckBoxColour(checkBox)

            else:
                todaysCheckBoxesContent[checkBox]=""
                app.addNamedCheckBox("", checkBox, count, 0, colspan=2)
                app.setCheckBoxChangeFunction(checkBox, checkBoxTicked)
            count+=1

def addEntriesElementsFromFile(listOfEntries, inputFile):
    count=0
    with open(inputFile, "r") as tomorrowsFile:
        for entry in listOfEntries:
            app.addEntry(entry)
            line=tomorrowsFile.readline()
            if line:    
                #ignore comment lines
                while line[0]=='#':
                    line=tomorrowsFile.readline()
                app.setEntry(entry, line[:-1])
                if line=='\n':
                    count+=1
    return count



def saveChanges():
    #save any changes localy so they are available when the program is opened again
    entriesDic=app.getAllEntries()
    entriesDicKeysSorted=sorted(app.getAllEntries().keys())
    with open(".TodayLogFile", "w+") as todaysFile:
        todaysFile.write("#Deleting this file you wont be able to track your todays goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
        for task in todaysCheckBoxes:
            if todaysCheckBoxes[task]:
                todaysFile.write('1')
            else:
                todaysFile.write('0')
            todaysFile.write(todaysCheckBoxesContent[task]+"\n")
    for entries in entriesDic:
        if entries.startswith("Tomorrow"):
            tomorrowTasksContent[entries]=entriesDic[entries]
    with open(".TomorrowsLogFile", "w+") as tomorrowsFile:
        tomorrowsFile.write("#Deleting this file you wont be able to track your tomorrow's goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
        for entries in entriesDicKeysSorted:
            if entries.startswith("Tomorrow"):
                tomorrowsFile.write(entriesDic[entries]+"\n")
    with open(".lastOpened", "w+") as lastOpenedFile:
        t=time.localtime();
        lastOpenedFile.write(str(t.tm_year)+"\n"+str(t.tm_mon)+"\n"+str(t.tm_mday)+"\n"+str(t.tm_hour)+"\n")
    return True

def transferTomorrowsGoalsToTodays():
    #transfers the Goals set at Tomorrow's Goals tab to Today's
    dic=app.getAllEntries()
    dicKeySorted=sorted(app.getAllEntries().keys())
    count=1
    with app.labelFrame("Today's Goals"):
        for name in dicKeySorted:
            if name.startswith("Task"):
                #show the entry and edit its content with the content of the
                #tomorrow's respectively
                ##if dic["Tomorrow"+name]: #uncomment to replace only those Tomorrow's goals that are set and not empty ones
                app.setEntry(name, dic["Tomorrow"+name])
                app.setEntry("Tomorrow"+name, '')
                #I need to remove the checkboxes and make them again when needed
                #because the appJar library doesn't provide
                #a way to set a namedCheckBox's content
                app.setCheckBox(name, ticked=False)
                todaysCheckBoxes[name]=False
                #
                app.removeCheckBox(name)
                app.showEntry(name)
                count+=1
        app.hideButton("Edit")
        app.showButton("Done")


def tomorrowsGoalsPrompt():
    with app.subWindow("TomorrowsGoalsTransfer", modal=True):
        if app.yesNoBox("Today's Goals", "You have past goals set in the tomorrow's goals tab\nDo you want to transfer them in today's?", parent="TomorrowsGoalsTransfer"):
            #TODO archive current today's
            transferTomorrowsGoalsToTodays()


with gui("tba", sticky="nesw") as app:
    app.setBg("lightblue")
    app.setSize(600, 300)
    with app.tabbedFrame("pages"):
        with app.tab("Today"):
            #local copy of the contents in order to manage them, present them and keep them up to date
            todaysCheckBoxes={"Task1":False, "Task2":False, "Task3":False}
            todaysCheckBoxesContent={"Task1":"", "Task2":"", "Task3":""}
            tasks=["Task1", "Task2", "Task3"]
            with app.labelFrame("Today's Goals"):
                app.setSticky("nsew")
                app.setStretch("both")
                try:
                    #if the program has stored data show them
                    addCheckBoxesElementsFromFile(tasks, ".TodayLogFile")
                    addEntriesElements(tasks)
                    setEntriesElements(tasks, todaysCheckBoxesContent)
                    hideEntriesElements(tasks)
                    app.setSticky("ew")
                    app.addButton("Done", editButton, len(tasks), 0)
                    app.addButton("Edit", editButton, len(tasks), 0)
                    app.hideButton("Done")
                    app.addButton("Archieve", archieveButton, len(tasks), 1)
                    app.addButton("Cancel", editButton, len(tasks), 1)
                    app.hideButton("Cancel")
                    app.setSticky("nsew")
                except IOError:
                    #else make them
                    addEntriesElements(tasks) 
                    app.setSticky("ew")
                    app.addButton("Done", editButton, len(tasks), 0)
                    app.addButton("Edit", editButton, len(tasks), 0)
                    app.hideButton("Edit")
                    app.addButton("Archieve", archieveButton, len(tasks), 1)
                    app.addButton("Cancel", editButton, len(tasks), 1)
                    app.hideButton("Archieve")
                    app.setSticky("nsew")
        with app.tab("Tomorrow"):
            dayStartsAt=4; #0 for 00:00, 0-23 
            tomorrowTasks=["TomorrowTask1", "TomorrowTask2", "TomorrowTask3"]
            tomorrowTasksContent={"TomorrowTask1":'', "TomorrowTask2":'', "TomorrowTask3":''}
            countEmptyLinesInTomorrowsFile=-1
            with app.labelFrame("Tomorrow's Goals"):
                app.setSticky("ew")
                try:
                    #if the program has stored data show them
                    countEmptyLinesInTomorrowsFile=addEntriesElementsFromFile(tomorrowTasks, ".TomorrowsLogFile")
                except IOError:
                    #else make them
                    addEntriesElements(tomorrowTasks) 
        with app.tab("Long Term"):
            with app.labelFrame("Long Term Goals"):
                app.addEntry("Goals")
        with app.tab("Archieved Goals"):
            app.addEntry("afdf")


        if countEmptyLinesInTomorrowsFile!=-1 and countEmptyLinesInTomorrowsFile!=len(tomorrowTasks):
            #if there are at least something in .TomorrowsLogFile
            #ask the user to replace everything in the today's tab if the day has changed 
            #from the last time the program was opened
            try:
                with open(".lastOpened", "r") as lastOpenedFile:
                    lt=time.localtime()
                    line=lastOpenedFile.readline()
                    if line:
                        year=int(line[:-1])
                    line=lastOpenedFile.readline()
                    if line:
                        month=int(line[:-1])
                    line=lastOpenedFile.readline()
                    if line:
                        day=int(line[:-1])
                    if line:
                        hour=int(line[:-1])
                    if lt.tm_year>year:
                        #prompt
                        app.setTabbedFrameSelectedTab("pages","Tomorrow")
                        app.show()
                        tomorrowsGoalsPrompt()
                        app.setTabbedFrameSelectedTab("pages","Today")
                    elif lt.tm_year==year:
                        if lt.tm_mon>month:
                            #prompt
                            app.setTabbedFrameSelectedTab("pages","Tomorrow")
                            app.show()
                            tomorrowsGoalsPrompt()
                            app.setTabbedFrameSelectedTab("pages","Today")
                        elif lt.tm_mon==month:
                            if lt.tm_mday>day+1:
                                #prompt
                                app.setTabbedFrameSelectedTab("pages","Tomorrow")
                                app.show()
                                tomorrowsGoalsPrompt()
                                app.setTabbedFrameSelectedTab("pages","Today")
                            elif lt.tm_mday==day+1:
                                if ((lt.tm_hour+hour)-24)>=dayStartsAt:
                                    #prompt
                                    app.setTabbedFrameSelectedTab("pages","Tomorrow")
                                    app.show()
                                    tomorrowsGoalsPrompt()
                                    app.setTabbedFrameSelectedTab("pages","Today")
                            elif lt.tm_mday==day:
                                if lt.tm_hour-dayStartsAt<=0:
                                    #prompt
                                    app.setTabbedFrameSelectedTab("pages","Tomorrow")
                                    app.show()
                                    tomorrowsGoalsPrompt()
                                    app.setTabbedFrameSelectedTab("pages","Today")

            except IOError:
                pass

    app.setStopFunction(saveChanges)      

