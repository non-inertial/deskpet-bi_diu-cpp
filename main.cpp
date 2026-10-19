#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QDebug>
#include <QDir>
// #include <QCoreApplication>
#include <QIcon>

#include <QTemporaryFile>
#include <QFile>
#include <QUuid>
#include <windows.h>


int main(int argc, char *argv[]){
    // qDebug()<<"exists:"<<QFile::exists(":/MyWindow/graphs/cursor/2-mouse_ico_fixed.cur"); // 注意! 构建之后会放到模块文件夹下, 而非原始目录
                                                                                          // 所以是:/MyWindow/graphs··· 而非 :/graphs···
    // qDebug()<<"check_1";
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;

    /*
        // 该部分已经重写. 如果使用QTemporaryFile, 它会对临时文件持续占用 导致系统无法读取、更换光标.
            // QTemporaryFile *curPath=QTemporaryFile::createNativeFile(":MyWindow/graphs/cursor/2-mouse_ico_fixed.cur"); //这样给出的curPath后缀是形如.SsqdtX的随机字符形式,将无法被系统识别
            QTemporaryFile *curPath=new QTemporaryFile(QDir::tempPath()+"/cursor_XXXXXX.cur");
            if(!curPath->open()){
                qDebug()<<"咦? 光标加载失败了biu~ 原因是创建临时文件失败";
            }
            else{
                QFile res(":/MyWindow/graphs/cursor/2-mouse_ico_fixed.cur");
                if(!res.open(QIODevice::ReadOnly)){
                    qDebug()<<"咦? 光标加载失败了biu~ 原因是打开资源失败";
                }
                else{
                    curPath->write(res.readAll());
                    // curPath->close(); // 本意是关闭文件, 否则Windows API打不开它
                                        // 但是这里的close()并不会结束QTemporaryFile对文件的占用(不会释放文件句柄(file handle)), 因此接下来如果调用LoadImage仍会返回32报错, 表示文件被占用. 因此需要手动维护临时文件
                    qDebug() << "curPath fileName:" << curPath->fileName();
                    qDebug()<<"check_2";
                    // QString curPath = QDir(QCoreApplication::applicationDirPath()).filePath("graphs/cursor/2-mouse_ico_fixed.cur");

                    qDebug()<<"check_3";

                    HCURSOR CustomCursor = nullptr;
                    CustomCursor = (HCURSOR) LoadImage(
                                                    nullptr,
                                                    (LPCWSTR)curPath->fileName().utf16(),
                                                    IMAGE_CURSOR,
                                                    0,0,
                                                    LR_LOADFROMFILE | LR_DEFAULTSIZE
                                                    );
                    qDebug()<<"check_4";
                    if(!CustomCursor){
                        DWORD err = GetLastError();
                        qDebug() << "咦? 光标加载失败了biu~ 原因是调用系统API失败 错误代码:"<<err;
                    }
                    else{
                        SetSystemCursor(CustomCursor, 32512); // 32512是系统默认光标、标准箭头
                    }
                }
            }
    */
    /*
        // 这里一开始使用了固定的文件名. 但存在问题: 由于设置了系统光标 (此处本来想使用process explorer查看究竟是什么在锁着文件, 但未能成功) , 所以系统可能仍以某种方式接管了文件, 会导致删除失败 (命令行会失败, 但用windows文件资源管理器进入目录则可以删除)
            // 接下来使用AI了解具体原因.
                QString curFile=QDir::tempPath()+"/my_cursor.cur";
                if(QFile::exists(curFile)&&!QFile::remove(curFile)){// 清除上次运行的临时文件(两次运行时使用相同的地址)
                    qDebug()<<"咦? 光标加载失败了biu~ 原因是清理上次运行临时文件失败";
                }
                else{

                }
    */
    QString curFile=QDir::tempPath() + "/cursor_" + QUuid::createUuid().toString(QUuid::WithoutBraces) + ".cur"; // 使用UUID, 即使上次运行临时文件未能成功移除, 也不会影响本次运行.
    if(QFile::copy(":/MyWindow/graphs/cursor/2-mouse_ico_fixed.cur",curFile)){
        HCURSOR CustomCursor = nullptr;
        CustomCursor = (HCURSOR) LoadImage(
                                        nullptr,
                                        (LPCWSTR)curFile.utf16(),
                                        IMAGE_CURSOR,
                                        0,0,
                                        LR_LOADFROMFILE | LR_DEFAULTSIZE
                                        );  
        if(!CustomCursor){
            DWORD err = GetLastError();
            qDebug() << "咦? 光标加载失败了biu~ 原因是调用系统API失败 错误代码:"<<err;
        }
        else{
            SetSystemCursor(CustomCursor, 32512); // 32512是系统默认光标、标准箭头
            QFile::remove(curFile);
        }          
    }

    QTemporaryFile *iconPath=QTemporaryFile::createNativeFile(":MyWindow/graphs/icon/0-icon.ico");
    // QString iconPath = QDir(QCoreApplication::applicationDirPath()).filePath("graphs/icon/0-icon.ico");
    if(!iconPath){
        qDebug()<<"咦? 图标加载失败了biu~ ";
    }
    else{
        iconPath->close();
        QIcon appIcon(iconPath->fileName());
        if (!appIcon.isNull()) {
            app.setWindowIcon(appIcon);
        }
        else{
            qDebug() << "咦? 图标加载失败了biu~ " << iconPath;
        }        
    }


    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
        
    engine.loadFromModule("MyWindow", "MainWindow");

    int run_result=app.exec();

    // 无需手动消除 CustomCursor, 全局替换系统会自动管理
    SystemParametersInfo(SPI_SETCURSORS, 0, nullptr, 0);

    return run_result;
}
