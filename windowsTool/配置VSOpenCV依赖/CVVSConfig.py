# -*- coding: utf-8 -*-
PrintInfo = '''
# ----------------------------------------------------------------------------------------------------------------
#                                     Opencv-Vs auto configure script
# ----------------------------------------------------------------------------------------------------------------
#
#                                  此脚本为 Visual Studio 配置 OpenCV3.1
#                                              on Windows.
#
#      你必须安装，Python3.* 和 python.exe 必须把相应路径下的bin文件添加到到环境变量 (例如 C:\Python34)。
# 使用请参考：http://my.phirobot.com/blog/2014-02-opencv_configuration_in_vs.html#opencv-x64-x86-debug-release
#
#                                          __author__ = 'luxux'
# ----------------------------------------------------------------------------------------------------------------
'''
import os
import re
from xml.dom import minidom

CvConfig = {
    "build": "",
    "include": "",
    "libraryWin32": "",
    "libraryX64": "",
    "link": ["opencv_world310"],
    "vs": ""
}

Win32 = r"'$(Platform)'=='Win32'"
X64 = r"'$(Platform)'=='X64'"

Debug = r"'$(Configuration)'=='Debug'"
Release = r"'$(Configuration)'=='Release'"


def get_lib():
    rootlib = CvConfig['libraryWin32'] or CvConfig['libraryX64']
    pathT = os.listdir(rootlib)  # 显示该路径下所有文件
    pathT.sort()
    # print(pathT)
    Dbuf = ""
    Rbuf = ""
    for i in pathT:
        Dm = re.search(r'd.lib', i)
        if Dm is not None:
            Dbuf = Dbuf + i + ';'
        else:
            Rm = re.search(r'.lib', i)
            if Rm is not None:
                Rbuf = Rbuf + i + ';'

    Debuglist = Dbuf + '%(AdditionalDependencies)'
    Releslist = Rbuf + '%(AdditionalDependencies)'
    return Debuglist, Releslist
# 写入xml文档的方法


def create_xml(filename, includepath, libx86path=None, libx64path=None, Dlist=None, Rlist=None):
    # 新建xml文档对象
    xml = minidom.Document()
    # 创建第一个节点，第一个节点就是根节点了
    Project = xml.createElement('Project')

    # 写入属性（xmlns:xsi是命名空间，同样还可以写入xsi:schemaLocation指定xsd文件）
    Project.setAttribute('ToolsVersion', "4.0")
    Project.setAttribute(
        'xmlns', "http://schemas.microsoft.com/developer/msbuild/2003")
    # 创建节点后，还需要添加到文档中才有效
    xml.appendChild(Project)

    # 一个节点加了文本之后，还可以继续追加其他东西
    ImportGroup = xml.createElement('ImportGroup')
    ImportGroup.setAttribute('Label', 'PropertySheets')
    Project.appendChild(ImportGroup)

    # 一个节点加了文本之后，还可以继续追加其他东西
    PropertyGroup = xml.createElement('PropertyGroup')
    PropertyGroup.setAttribute('Label', 'UserMacros')
    Project.appendChild(PropertyGroup)

    author = xml.createElement('PropertyGroup')
    Project.appendChild(author)
    # include Path
    author_IncludePath = xml.createElement('IncludePath')
    author_IncludePath_text = xml.createTextNode(includepath)
    author_IncludePath.appendChild(author_IncludePath_text)
    author.appendChild(author_IncludePath)
    # library Win32 | X86
    if libx86path is not None:
        author_LibraryPath = xml.createElement('LibraryPath')
        author_LibraryPath.setAttribute('Condition', Win32)
        author_LibraryPath_text = xml.createTextNode(libx86path)
        author_LibraryPath.appendChild(author_LibraryPath_text)
        author.appendChild(author_LibraryPath)
    else:
        pass
        # library X64
    if libx64path is not None:
        author_LibraryPath1 = xml.createElement('LibraryPath')
        author_LibraryPath1.setAttribute('Condition', X64)
        author_LibraryPath_text1 = xml.createTextNode(libx64path)
        author_LibraryPath1.appendChild(author_LibraryPath_text1)
        author.appendChild(author_LibraryPath1)
    else:
        pass
    Project.appendChild(author)

    ItemDefinitionGroup = xml.createElement('ItemDefinitionGroup')
    Project.appendChild(ItemDefinitionGroup)

    # Debug
    if Dlist is not None:
        Link = xml.createElement('Link')
        Link.setAttribute('Condition', Debug)
        ItemDefinitionGroup.appendChild(Link)

        AdditionalDependencies = xml.createElement('AdditionalDependencies')
        AdditionalDependencies_text = xml.createTextNode(Dlist)
        Link.appendChild(AdditionalDependencies)
        AdditionalDependencies.appendChild(AdditionalDependencies_text)
    else:
        pass
    # Release
    if Rlist is not None:
        Link1 = xml.createElement('Link')
        Link1.setAttribute('Condition', Release)
        ItemDefinitionGroup.appendChild(Link1)

        AdditionalDependencies = xml.createElement('AdditionalDependencies')
        AdditionalDependencies_text = xml.createTextNode(Rlist)
        Link1.appendChild(AdditionalDependencies)
        AdditionalDependencies.appendChild(AdditionalDependencies_text)
    else:
        pass
    Project.appendChild(ItemDefinitionGroup)

    ItemGroup = xml.createElement('ItemGroup')
    Project.appendChild(ItemGroup)
    # 写好之后，就需要保存文档了
    f = open(filename, 'wb')
    f.write(xml.toprettyxml(encoding='utf-8'))
    f.close()


def DetectionFiles(dir, suffix):
    # 文件和文件夹查找
    if os.path.exists(dir):
        for root, directory, files in os.walk(dir):
            for directoryname in directory:
                if directoryname == suffix:
                    print("prompt---->" + os.path.join(root, directoryname))
                    return suffix
            for filesname in files:
                if filesname == suffix:
                    print("prompt---->" + os.path.join(root, filesname))
                    return suffix
    else:
        return None


def getCvPath():
    include = None
    libx86 = None
    libx64 = None
    while True:
        vc = input(
            "Which Visual Studio you are using? (vs2010 or vs2013 or vs2015): ")
        print("\n\n")
        if vc == "vs2010":
            CvConfig["vs"] = "vc10"
            break
        elif vc == "vs2013":
            CvConfig["vs"] = "vc12"
            break
        elif vc == "vs2015":
            CvConfig["vs"] = "vc14"
            break
        else:
            print("Please type vs2010 or vs2013 or vs2015")

    while True:
        root_ = input(
            r"Where is your opencv root path?(e.g, C:\path\to\opencv3): ")
        print("\n\n")
        if os.path.exists(root_):
            if DetectionFiles(root_, "x86") is not None:
                root_x86 = input(r"Where is your opencv x86 path:")
                print("\n\n")
                CvConfig["libraryWin32"] = os.path.normpath(
                    "%s/%s/lib/" % (root_x86, CvConfig["vs"]))
            else:
                libx86 = None
            if DetectionFiles(root_, "x64") is not None:
                root_x64 = input(r"Where is your opencv x64 path:")
                print("\n\n")
                CvConfig["libraryX64"] = os.path.normpath(
                    "%s/%s/lib/" % (root_x64, CvConfig["vs"]))
            else:
                libx64 = None
            if DetectionFiles(root_, "include") is not None:
                CvConfig["include"] = input(
                    r"Where is your opencv include path:")
                print("\n\n")
                break
        else:
            break

    if os.path.exists(CvConfig["include"]):
        include = CvConfig["include"] + ';$(IncludePath)'
    else:
        print("Invalid path!!!!")
    if os.path.exists(CvConfig["libraryWin32"]):
        libx86 = CvConfig["libraryWin32"] + ';$(LibraryPath)'
    else:
        libx86 = None
    if os.path.exists(CvConfig["libraryX64"]):
        libx64 = CvConfig["libraryX64"] + ';$(LibraryPath)'
    else:
        libx64 = None

    return include, libx86, libx64

if __name__ == '__main__':
    print(PrintInfo)
    includepath, libx86path, libx64path = getCvPath()
    D_, R_ = get_lib()
    # 在当前目录下，创建1.xml
    print(includepath, libx86path, libx64path)
    create_xml('Vs.opencv.x64.x86.debug.release.props',
               includepath=includepath, libx86path=libx86path, libx64path=libx64path,
               Dlist=D_, Rlist=R_)
