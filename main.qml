import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3


Window {
    id: window
    visible: true
    width: 640
    height: 480
    title: qsTr("Focus On The Important")

    TabBar {
        id: goalsTabBar
        currentIndex: swipeView.currentIndex
        width: window.width
        TabButton {
            text: qsTr("Today")
        }
        TabButton {
            text: qsTr("Tomorrow")
        }
        TabButton {
            text: qsTr("Long Term")
        }
        TabButton {
            text: qsTr("Archieved")
        }
    }

    SwipeView {
        id: swipeView
        width: window.width
        height: window.height
        anchors.top: goalsTabBar.bottom
        currentIndex: goalsTabBar.currentIndex

        GroupBox {
            id: today
            title: "Today's Goals"
            Layout.fillWidth: true
            GridLayout {
                id: gridLayout
                rows: 3
                flow: GridLayout.TopToBottom
                width: parent.width
                Label { text: "Goal 1" }
                Label { text: "Goal 2" }
                Label { text: "Goal 3" }

                TextField { }
                TextField { }
                TextField { }

               // TextArea {
                 //   text: "This widget spans over three rows in the GridLayout.\n"
                   //       + "All items in the GridLayout are implicitly positioned from top to bottom."
                    Layout.rowSpan: 3
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                //}
            }
        }
        Item {
            Label { text: "Line 2" }
        }
        Item {
            Label { text: "Line 3" }
        }



    }


}
