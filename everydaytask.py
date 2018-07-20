from appJar import gui

def editButton(btn):
    if btn=="Done":
        count=0
        dic=app.getAllEntries()
        with app.labelFrame("Today's Goals"):
            for textAreaName in dic:
                if "Task" in textAreaName:
                    app.hideEntry(textAreaName)
                    app.addNamedCheckBox(dic[textAreaName],textAreaName, count, 0)
                    count+=1
            app.hideButton("Done")
            app.showButton("Edit")
    elif btn=="Edit":
        dic=app.getAllCheckBoxes()
        count=1
        with app.labelFrame("Today's Goals"):
            for textBoxName in dic:
                app.removeCheckBox("Task"+str(count))
                app.showEntry("Task"+str(count))
                count+=1
            app.hideButton("Edit")
            app.showButton("Done")


with gui("tba") as app:
    app.setBg("lightblue")
    app.setSize(600, 300)
    with app.tabbedFrame("pages"):
        with app.tab("EveryDay"):
            with app.labelFrame("Today's Goals"):
                app.setSticky("ew")
                app.addEntry("Task1", 0, 0)
                app.addEntry("Task2", 1, 0)
                app.addEntry("Task3", 2, 0)
                app.addButton("Done", editButton, 3, 0)
                app.addButton("Edit", editButton, 3, 0)
                app.hideButton("Edit")
                #app.disableButton("Edit")
        with app.tab("Long Term"):
            with app.labelFrame("Long Term Goals"):
                app.addEntry("Goals")
        with app.tab("Archieved Goals"):
            app.addEntry("afdf")
            


