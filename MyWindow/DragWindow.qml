import QtQuick
import QtQuick.Controls

// 参考 https://doc.qt.io/qtforpython-6/examples/example_quickcontrols_filesystemexplorer.html#example-quickcontrols-filesystemexplorer 的 DragWindowHandler.qml

pragma ComponentBehavior: Bound // pragma: 希腊语,"行为、事情"; 常翻译为编译指示、杂注

DragHandler{ // 这是一个内置类型
    required property Window dragWindow

    target:null
    onActiveChanged:{
        if(active)dragWindow.startSystemMove()
    }
}