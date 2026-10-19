# 比丢桌宠 (cpp版)

这是一个 QtQuick 为前端、C++ 为后端的项目。可以使用 CMake 从源码构建，也提供了用 Enigma Virtual Box 打包的 exe 文件。

## 功能

- 运行时替换光标样式
- 运行时召唤一只比丢

## 注意事项

- 运行使用 Enigma Virtual Box 打包的 exe 文件时，如果直接退出将导致光标样式无法恢复。如果出现了这种情况，再次运行程序，右键比丢退出即可恢复。

## 从源码构建

### 所需工具

我们接下来仅介绍一种可行的方案。以下是所需工具和安装方法：

- **vscode CMake Tools 插件**
  - 在 vscode 扩展中安装

- **msys2**
  - 前往 msys2.org 下载

- **C 语言工具链安装**
  - 在 msys2 的安装路径中（如 `C:\msys64`）找到 `ucrt64.exe`（推荐），运行后输入：

    ```bash
    pacman -S mingw-w64-ucrt-x86_64-toolchain
    ```

    即可完成安装。
  - 如果你的电脑打开了“智能应用管理策略”，将可能导致 vscode 中直接运行 `.c` 文件时报错 `launch: program '输入程序名称，例如···'` 等错误：特征是在 vscode 中 `Ctrl+Shift+B` 编译正常，但无法直接运行。如果出现上述错误，可以优先尝试关闭这个功能以修复。

- **Qt 库获取**
  - 再次运行 `ucrt64.exe`（请保证与 C 语言的安装环境相同），输入：

    ```bash
    pacman -S mingw-w64-ucrt-x86_64-qt6-base
    ```

    即可完成安装。

- **vscode Qt Extension Pack 插件**
  - 在 vscode 扩展中安装
  - （非必需）vscode 中 `Ctrl+Shift+P` 打开命令面板，查找 `Qt: Register Qt installation`，添加 qmake 的路径（如 `C:\msys64\ucrt64\bin\qmake.exe`）

### 构建

- 打开 `CMakeLists.txt`，`Ctrl+S` 保存将激活插件自动配置构建选项。
- 打开 `MainWindow.qml`，右上角将出现运行按钮，点击即可。
