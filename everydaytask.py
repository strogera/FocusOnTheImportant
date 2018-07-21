from appJar import gui
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
        #writing the changes on the file is not entirely needed since its done on exit either way
        #it may be useful but if its a permormance problem later on i can remove it
        with app.labelFrame("Today's Goals"):
            with open(".TodayLogFile", "w+") as curFile:
                curFile.write("#Deleting this file you wont be able to track your todays goals. \n#Its recommended that you don't edit it manually either, so there is no data loss. \n#The program will read the first 3 non-comment lines.\n")
                for textAreaName in dic:
                    if "Task" in textAreaName:
                        #write to file
                        if todaysCheckBoxes[textAreaName]:
                            curFile.write('1')
                        else:
                            curFile.write('0')
                        curFile.write(dic[textAreaName]+"\n")
                        #update the memory copy of the checkboxes
                        todaysCheckBoxesContent[textAreaName]=dic[textAreaName]
                        #hide the entry
                        app.hideEntry(textAreaName)
                        #add the updated checkbox
                        app.addNamedCheckBox(dic[textAreaName],textAreaName, count, 0)
                        #update its ticked state
                        if todaysCheckBoxes[textAreaName]:
                            app.setCheckBox(textAreaName, ticked=True, callFunction=False)
                        else:
                            app.setCheckBox(textAreaName, ticked=False, callFunction=False)
                        #on click use the checkBoxTicked function 
                        app.setCheckBoxChangeFunction(textAreaName, checkBoxTicked)
                        #set the correct colour
                        setCheckBoxColour(textAreaName)
                        count+=1
            app.hideButton("Done")
            app.showButton("Edit")
    elif btn=="Edit":
        #then the user wants to edit the contents of the checkboxes
        #and needs to see the entries
        dic=app.getAllCheckBoxes()
        count=1
        with app.labelFrame("Today's Goals"):
            for checkBoxName in dic:
                if "Task" in checkBoxName:
                    #show the entry and edit its content with the content of the
                    #checkbox respectively
                    app.showEntry(checkBoxName)
                    app.setEntry(checkBoxName, todaysCheckBoxesContent[checkBoxName])
                    #I need to remove the checkboxes and make them again when needed
                    #because the appJar library doesn't provide
                    #a way to set a namedCheckBox's content
                    app.removeCheckBox(checkBoxName)
                    count+=1
            app.hideButton("Edit")
            app.showButton("Done")

def addEntriesElements(listOfEntries):
    #adds as much entries elements as there are in the given list with the name provided
    #ex: ["Task1", "Task2"]
    #adds two Entries elements with the respective names
    count=0
    for entry in listOfEntries:
        app.addEntry(entry, count, 0)
        count+=1

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
                while  line[0]=='#':
                    line=todaysFile.readline()
                if line[0]=='1':
                    todaysCheckBoxes[checkBox]=True
                todaysCheckBoxesContent[checkBox]=line[1:-1]
                app.addNamedCheckBox(todaysCheckBoxesContent[checkBox],checkBox, count, 0)
                app.setCheckBox(checkBox, ticked=todaysCheckBoxes[checkBox])
                app.setCheckBoxChangeFunction(checkBox, checkBoxTicked)
                setCheckBoxColour(checkBox)

            else:
                todaysCheckBoxesContent[checkBox]=""
                app.addNamedCheckBox("", checkBox, count, 0)
                app.setCheckBoxChangeFunction(checkBox, checkBoxTicked)
            count+=1

def saveChanges():
    #save any changes localy so they are available when the program is opened again
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
            #local copy of the contents in order to manage them, present them and keep them up to date
            todaysCheckBoxes={"Task1":False, "Task2":False, "Task3":False}
            todaysCheckBoxesContent={"Task1":"", "Task2":"", "Task3":""}
            tasks=["Task1", "Task2", "Task3"]
            with app.labelFrame("Today's Goals"):
                app.setSticky("ew")
                try:
                    #if the program has stored data show them
                    addCheckBoxesElementsFromFile(tasks, ".TodayLogFile")
                    addEntriesElements(tasks)
                    hideEntriesElements(tasks)
                    app.addButton("Done", editButton, len(tasks), 0)
                    app.addButton("Edit", editButton, len(tasks), 0)
                    app.hideButton("Done")
                except IOError:
                    #else make them
                    addEntriesElements(tasks) 
                    app.addButton("Done", editButton, len(tasks), 0)
                    app.addButton("Edit", editButton, len(tasks), 0)
                    app.hideButton("Edit")
        with app.tab("Tomorrow"):
            with app.labelFrame("Tomorrow's Goals"):
                app.addEntry("asdf")
        with app.tab("Long Term"):
            with app.labelFrame("Long Term Goals"):
                app.addEntry("Goals")
        with app.tab("Archieved Goals"):
            app.addEntry("afdf")
    app.setStopFunction(saveChanges)      

