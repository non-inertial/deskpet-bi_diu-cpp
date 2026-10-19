# 比丢桌宠 (cpp版)
这是一个QtQuick为前端，c++为后端的项目。可以使用cmake从源码构建，也提供了用enigma virtual box打包的exe文件。  

## 功能:
· 运行时替换光标样式
· 运行时召唤一只比丢

## 注意事项:
· 运行使用enigma virtual box打包的exe文件时，如果直接退出将导致光标样式无法恢复。如果出现了这种情况，再次运行程序右键比丢退出即可恢复。
    
## 从源码构建:
### &emsp;所需工具
        我们接下来仅介绍一种可行的方案。以下是所需工具和安装方法  
            ·**vscode CMake Tools 插件**  
&emsp;&emsp;&emsp;&emsp;-在vscode扩展中安装  
&emsp;&emsp;&emsp;·**msys2**  
&emsp;&emsp;&emsp;&emsp;-前往msys2.org下载  
&emsp;&emsp;&emsp;·**C语言工具链安装**  
&emsp;&emsp;&emsp;&emsp;-在msys2的安装路径中(如C:\msys64)找到ucrt64.exe(推荐), 运行后输入
            ```bash
                pacman -S mingw-w64-ucrt-x86_64-toolchain
            ```
        -如果你的电脑打开了 "智能应用管理策略" 将可能导致vscode中直接运行.c文件时报错"launch:program '输入程序名称，例如···'"等错误：特征是ctrl+shift+B编译正常，但无法直接运行。如果出现上述错误可以优先尝试关闭这个功能以修复。  
    ·**Qt库获取**  
        -再次运行ucrt64.exe(请保证与C语言的安装环境相同)，输入
```bash
    pacman -S mingw-w64-ucrt-x86_64-qt6-base
```
    即可完成安装  
·vscode **Qt Extension Pack** 插件
