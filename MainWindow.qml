import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml.StateMachine as DSM
import MyWindow

pragma ComponentBehavior: Bound // pragma: 希腊语,"行为、事情"; 常翻译为编译指示、杂注

Window{
    id:root

    width:150
    height:150
    color:"transparent"
    visible:true
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    title:"Biu~"

    // onXChanged:updatePos()
    // onYChanged:updatePos()

    // function updatePos(){
    //     if(!fsmContainer.special_style){
            
    //     }
    // }

    DragWindow{
        dragWindow:root
    }

    readonly property list<string> gifPath:["graphs/dynamic_graphs/3-ri'chang-bye.gif", //退出动画放在0 以免反复修改
                                            "graphs/dynamic_graphs/1-zhuzhunian-fighting.gif"
                                           ]
    property int choice:1

    Item{ // 把DSM放在Window里面无法正常监听信号, 因此加了一个容器
          // 需要有默认属性default property才能往里面加子对象
        visible:false
        width:0
        height:0
        id:dsmContainer

        signal leftClicked()
        // onLeftClicked:console.log("leftClicked")

        property int special_style:0
        signal exit()

        // signal up()
        // signal down()
        // signal left()
        // signal right()

        DSM.StateMachine{
            id:dsm
            initialState:s0
            running:true
            DSM.State{
                id:s0 // 播放
                DSM.SignalTransition{
                    targetState:quit_0
                    signal:dsmContainer.exit
                }
                onEntered:root.choice=1
            }
            DSM.State{
                id:quit_0
                onEntered:{
                    root.choice=0; //把退出动画放在0 以免频繁修改
                    // animatedImage.loops=1 // 我使用pacman安装的qt包版本是6.11.1低于6.12 不支持这个property
                    quitTimer.start()
                } 
                // DSM.SignalTransition{
                //     targetState:quit_1
                //     signal: animatedImage.currentFrameChanged
                //     guard: animatedImage.currentFrame === animatedImage.frameCount - 1
                // }
                Timer{
                    id:quitTimer
                    interval:3500
                    repeat:false
                    onTriggered:Qt.quit()
                }
            }
            // DSM.State{
            //     id:quit_1
            //     onEntered:Qt.exit()
            // }
        }
    }
    
    MouseArea{
        anchors.fill:parent
        id:mouseListener
        enabled:true
        acceptedButtons:Qt.AllButtons
        onClicked:(mouse)=>{
            if(mouse.button==Qt.RightButton) menu.popup()
            
            // else if (mouse.button==Qt.LeftButton){
            //     fsmContainer.leftClicked()
            //     // console.log("clicked")
            // }
            
        }
    }

    Menu{
        id:menu
        MenuItem{text:"退出";onTriggered:dsmContainer.exit()}
    }
    
    // MousePos{
    //     id:mp
    // }

    // Item{
    //     anchors.fill:parent 
    //     height:100
    //     Text{
    //         id:mousePosDisp
    //         text:`鼠标位置: (${Math.round(mp.mousePos.x)},${Math.round(mp.mousePos.y)})`
    //     }
    // }


    ColumnLayout{
        anchors.fill:parent

        // Item{
        //     Layout.fillHeight: true
        //     Layout.fillWidth: true            
        // }
        // Text{
        //     id:graphName
        //     text:"我会暖床求包养"
        //     Layout.alignment:Qt.AlignHCenter
        // }

        // Image{
        //     id:welcome_0

        //     // source:"file:///C:/Users/Lee/Desktop/Qt notes/src_code/1-4-display_image/graphs/static_graphs/0-welcomeImg.gif"
        //     source:"../graphs/static_graphs/0-welcome.gif"

        //     Layout.alignment: Qt.AlignHCenter
        //     Layout.maximumWidth: parent.width
        //     Layout.maximumHeight: parent.height
        //     fillMode:Image.PreserveAspectFit

        //     smooth: true
        //     asynchronous: true
        // }

        AnimatedImage{
            id:animatedImage

            Layout.alignment: Qt.AlignHCenter
            Layout.maximumWidth: parent.width
            Layout.maximumHeight: parent.height
            fillMode:Image.PreserveAspectFit

            // source:"graphs/dynamic_graphs/1-zhuzhunian-fighting.gif"
            source: root.gifPath[root.choice]
            
            // playing: s0.active
            playing:true
        }
    }
}
