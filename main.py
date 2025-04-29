import os
import argparse

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input",help = "需要生成的文本")
parser.add_argument("-n", "--font_name", help = "输出字体名称")
parser.add_argument("-p", "--font_path", help = "字体路径")
parser.add_argument("-d", "--dpi", help = "字体分辨率")
parser.add_argument("-s", "--size", help = "字体大小")
parser.add_argument("-sp", "--space", help = "字体间距",default=0)
parser.add_argument("-b", "--bdf", action='store_true', help = "生成bdf文件")
parser.add_argument("-c", "--c_file", action='store_true', help = "生成C文件")
parser.add_argument("-ia", "--ignore_ascii", action='store_true', help = "是否忽略ASCII输入")
parser.add_argument("-fa", "--font_ascii", action='store_true', help = "是否包含ASCII")

#确保win10终端颜色正常显示
if os.name == "nt":
    os.system("")

#字符转unicode函数
def to_unicode(string):
    ret = ""
    for v in string:
        ret = ret + hex(ord(v)).upper().replace('0X', '$')
    return ret

# 启动信息   
print('\033[1;31;43m',"{:=^40}".format("U8g2字库生成器 V1.0"),'\033[0m')
print('\033[1;30;33m',"Email: createskyblue@outlook.com\n",'\033[0m')


# 输入是否过滤ascii
del_ASCII_flag  = False
# map字符映射文件是否包含ASCII
add_ASCII_flag = False
# 生成bdf文件
bdfFlag = False
# 生成C文件
cFileFlag = False
fontSPSize = 0

args = parser.parse_args()
if (args.input != None):
    inputText = args.input
    print('\033[1;30;33m',"[INFO] 读取命令行参数,待生成文本 >\033[0m",inputText)
if (args.font_name != None):
    targetFontName = args.font_name
    print('\033[1;30;33m',"[INFO] 读取命令行参数,字体名称 >\033[0m",targetFontName)
if (args.font_path != None):
    ttfFontPath = args.font_path
    print('\033[1;30;33m',"[INFO] 读取命令行参数,字体路径 >\033[0m",ttfFontPath)
if (args.dpi != None):
    fontSizeDPI = eval(args.dpi)
    print('\033[1;30;33m',"[INFO] 读取命令行参数,字体分辨率 >\033[0m",fontSizeDPI)
if (args.size != None):
    fontSizePx = eval(args.size)
    print('\033[1;30;33m',"[INFO] 读取命令行参数,字体大小 >\033[0m",fontSizePx)
if (args.space != None):
    fontSPSize = eval(args.space)
    print('\033[1;30;33m',"[INFO] 读取命令行参数,字体间距 >\033[0m",fontSPSize)
if (args.bdf != None):
    bdfFlag = args.bdf
    print('\033[1;30;33m',"[INFO] 读取命令行参数,是否生成bdf文件 >\033[0m",bdfFlag)
if (args.c_file != None):
    cFileFlag = args.c_file
    print('\033[1;30;33m',"[INFO] 读取命令行参数,是否生成C文件 >\033[0m",cFileFlag)
if (args.ignore_ascii != None):
    del_ASCII_flag = args.ignore_ascii
    print('\033[1;30;33m',"[INFO] 读取命令行参数,是否过滤ASCII >\033[0m",del_ASCII_flag)
if (args.font_ascii != None):
    add_ASCII_flag = args.font_ascii
    print('\033[1;30;33m',"[INFO] 读取命令行参数,是否包含ASCII >\033[0m",add_ASCII_flag)    

#如果命令行参数不完整，则提示用户手动输入
if (args.input == None):
    #获取字符输入 电子科技大学中山学院
    inputText = input('\033[1;31;43m[ASK] 请输入需要生成字库的文本（自动去重）：\033[0m')
    # inputText = " 电子科技大学中山学院"
if (args.font_name == None):
    #获取生成目标字体名称
    targetFontName = input("\033[1;30;33m[ASK] 生成字库命名 >\033[0m")
    # targetFontName = "testFont"
if (args.font_path == None):
    #获取字体文件
    ttfFontPath = input("\033[1;30;33m[ASK] 输入ttf格式字体路径 >\033[0m")
    # ttfFontPath = "font/Alibaba-PuHuiTi-Medium.ttf"
if (args.dpi == None):
    #获取字体DPI解析度
    fontSizeDPI = eval(input("\033[1;30;33m[ASK] 输入生成字库字体DPI >\033[0m"))
if (args.size == None):
    #获取字体px大小
    fontSizePx = eval(input("\033[1;30;33m[ASK] 输入生成字库字体大小(px) >\033[0m"))

if (args.input == None or args.font_name == None or args.font_path == None or args.dpi == None or args.size == None):
    #获取字体间距大小%
    fontSPSize = eval(input("\033[1;30;33m[ASK] 输入生成字库字体间距大小(%) >\033[0m"))

    #获取是否生成bdf文件
    bdfFlag = input("\033[1;30;33m[ASK] 是否生成bdf文件? (Y/n) >\033[0m")
    if (bdfFlag == "y" or bdfFlag == "Y" or bdfFlag == ""):
        args.bdf = True

    #获取是否生成C文件
    cFileFlag = input("\033[1;30;33m[ASK] 是否生成C文件? (Y/n) >\033[0m")
    if (cFileFlag == "y" or cFileFlag == "Y" or cFileFlag == ""):
        args.c_file = True

    del_ASCII_flag_input = input("\033[1;30;33m[ASK] 是否过滤ASCII? (Y/n) >\033[0m")
    if (del_ASCII_flag_input == "y" or del_ASCII_flag_input == "Y" or del_ASCII_flag_input == ""):
        del_ASCII_flag = True

    add_ASCII_flag_input = input("\033[1;30;33m[ASK] MAP字符映射文件是否包含ASCII? (Y/n) >\033[0m")
    if (add_ASCII_flag_input == "y" or add_ASCII_flag_input == "Y" or add_ASCII_flag_input == ""):
        add_ASCII_flag = True

tftFontName = os.path.basename(ttfFontPath)
tftFontNameReal = tftFontName.split('.')[0]

#换算成单位pt
fontSizePt = fontSizePx/(fontSizeDPI/72)

#创建原子字典，对目标字去重
atomText = set(inputText)
print("原子字库：",atomText)

#原子字典转unicode格式
unicodeText = []
for c in atomText:
    #选择过滤ASCII结果
    if (del_ASCII_flag and ord(c) < 255):
        continue
    #unicode转换
    unicodeText.append(to_unicode(c))
#对转换结果进行排序
unicodeText.sort()
print("转unicode原子字库：",unicodeText)

#生成map字符映射表
mapFileDatas = ""
#选择性加入ASCII到map字符映射表
if (add_ASCII_flag):
    mapFileDatas += "32-128"
#合并unicode字典到映射表
for u in unicodeText:
    if (len(mapFileDatas) > 0):
        mapFileDatas += ", " #分隔符：这里必须要有空格
    mapFileDatas += u
print("字符map映射表：",mapFileDatas)

#覆盖创建map文件
mapPath = "map/{}.map".format(targetFontName)
mapFile_f = open(mapPath,"w")
mapFile_f.write(mapFileDatas)
mapFile_f.close()

#生成bdf字库
if (bdfFlag):
    #生成bdf文件
    exeExtension = ".exe" if os.name == "nt" else ""
    bdfPath = "bdf/{0}_{1}.bdf".format(tftFontNameReal,fontSizePx)
    targetFontName = "{0}_{1}".format(targetFontName,fontSizePx)
    c_codePath = "code/{0}.c".format(targetFontName)
    otf2bdfCMD = "otf2bdf"+exeExtension+" -v -r {3} -p {0} -o {1} {2}".format(fontSizePt,bdfPath,ttfFontPath,fontSizeDPI)
    print(">",otf2bdfCMD)
    os.system(otf2bdfCMD)

if (cFileFlag):
    #生成u8g2目标C语言字库文件
    bdfconvCMD = "bdfconv"+exeExtension+" -v -b 0 -f 1 {0} -M {1} -n {2} -o {3} -p {4} -d {0}".format(bdfPath,mapPath,targetFontName,c_codePath,fontSPSize)
    print(">",bdfconvCMD)
    os.system(bdfconvCMD)
#完成信息
print('\033[1;37;42m',"[操作完成]",'\033[0m')
