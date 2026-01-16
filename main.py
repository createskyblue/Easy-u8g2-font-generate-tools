import os
import re
import glob
import json

#确保win10终端颜色正常显示
if os.name == "nt":
    os.system("")

#字符转unicode函数
def to_unicode(string):
    ret = ""
    for v in string:
        ret = ret + hex(ord(v)).upper().replace('0X', '$')
    return ret

def removeComments(List):
    """去除C/C++注释"""
    s = '\n'.join(List) + '\n' #为最后一行的'//'提供闭区间
    i, n = 1, len(s)
    ans = ''
    while i < n:
        if s[i - 1] + s[i] == '//':
            i = s.find('\n', i) + 1
        elif s[i - 1] + s[i] == '/*':
            i = s.find('*/', i + 1) + 3
        else:
            ans += s[i - 1]
            i += 1
    return ans.split('\n')

def extractChinese(text):
    """提取中文字符（包括汉字、中文标点符号）"""
    # 匹配中文字符（包括汉字、中文标点）
    chinese_pattern = re.compile(
        r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f'
        r'\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\u3000-\u303f\uff00-\uffef]+'
    )
    return chinese_pattern.findall(text)

def processFile(filePath):
    """处理单个文件：读取、去注释、提取中文"""
    try:
        # 尝试不同编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
        content = None
        
        for encoding in encodings:
            try:
                with open(filePath, 'r', encoding=encoding) as f:
                    content = f.readlines()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  [警告] 无法解码文件: {filePath}")
            return []
        
        # 去除注释
        noComment = removeComments(content)
        noCommentText = '\n'.join(noComment)
        
        # 提取中文
        chineseChars = extractChinese(noCommentText)
        
        return chineseChars
        
    except Exception as e:
        print(f"  [错误] 处理文件 {filePath} 时出错: {e}")
        return []

def getFileList(inputStr):
    """根据输入获取文件列表"""
    files = []
    
    for item in inputStr:
        item = item.strip()
        if not item:
            continue
            
        # 检查是否是文件路径
        if os.path.isfile(item):
            # 检查扩展名
            ext = os.path.splitext(item)[1].lower()
            if ext in ['.c', '.cpp', '.h', '.hpp']:
                files.append(os.path.abspath(item))
        elif os.path.isdir(item):
            # 如果是目录，递归查找符合条件的文件
            for ext in ['*.c', '*.cpp', '*.h', '*.hpp']:
                files.extend(glob.glob(os.path.join(item, '**', ext), recursive=True))
        else:
            # 尝试使用glob模式匹配
            matched = glob.glob(item, recursive=True)
            for f in matched:
                ext = os.path.splitext(f)[1].lower()
                if ext in ['.c', '.cpp', '.h', '.hpp']:
                    files.append(os.path.abspath(f))
    
    return list(set(files))  # 去重

def loadConfig(configPath):
    """加载JSON配置文件"""
    try:
        with open(configPath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except UnicodeDecodeError:
        with open(configPath, 'r', encoding='gbk') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f'\033[1;31m[错误] 读取配置文件失败: {e}\033[0m')
        exit(1)

def validateConfig(config):
    """验证配置文件"""
    required_keys = ['font_name', 'font_path', 'font_dpi', 'font_size_px', 'font_spacing_percent', 'file_paths']
    for key in required_keys:
        if key not in config:
            print(f'\033[1;31m[错误] 配置文件缺少必需参数: {key}\033[0m')
            exit(1)
    
    # 验证字体文件是否存在
    if not os.path.isfile(config['font_path']):
        print(f'\033[1;31m[错误] 字体文件不存在: {config["font_path"]}\033[0m')
        exit(1)

#启动信息   
print('\033[1;31;43m',"{:=^40}".format("U8g2字库生成器 V3.0"),'\033[0m')
print('\033[1;30;33m',"Email: createskyblue@outlook.com\n",'\033[0m')
print('\033[1;36m',"支持从JSON配置文件自动提取中文并生成字库\n",'\033[0m')

#获取配置文件路径
if len(os.sys.argv) > 1:
    configPath = os.sys.argv[1]
else:
    configPath = input('\033[1;30;33m[ASK] JSON配置文件路径 >\033[0m')

# 检查配置文件是否存在
if not os.path.isfile(configPath):
    print('\033[1;31m',"[错误] 配置文件不存在！",'\033[0m')
    print("请确保配置文件存在，或运行: python main.py <配置文件路径>")
    exit(1)

# 加载配置文件
config = loadConfig(configPath)

# 验证配置
validateConfig(config)

print(f'\033[1;33m加载配置文件: {configPath}\033[0m')
print(f"  字体名称: {config['font_name']}")
print(f"  字体路径: {config['font_path']}")
print(f"  字体DPI: {config['font_dpi']}")
print(f"  字体大小: {config['font_size_px']}px")
print(f"  字体间距: {config['font_spacing_percent']}%")
print(f"  过滤ASCII: {config.get('filter_ascii', True)}")
print(f"  MAP包含ASCII: {config.get('map_include_ascii', False)}")

# 获取文件列表
fileList = getFileList(config['file_paths'])

if not fileList:
    print('\033[1;31m',"[错误] 未找到任何符合条件的文件！",'\033[0m')
    exit(1)

print(f'\033[1;32m找到 {len(fileList)} 个文件：\033[0m')
for f in fileList:
    print(f"  - {f}")

# 处理所有文件，提取中文
allChineseChars = []
print('\033[1;33m正在处理文件...\033[0m')
for filePath in fileList:
    print(f"  处理: {os.path.basename(filePath)}")
    chars = processFile(filePath)
    allChineseChars.extend(chars)

if not allChineseChars:
    print('\033[1;31m',"[警告] 未找到任何中文字符！",'\033[0m')
    exit(1)

# 合并并去重
inputText = ''.join(allChineseChars)
print(f'\033[1;32m提取到的中文字符（共 {len(set(inputText))} 个唯一字符）:\033[0m')
print(f"  {set(inputText)}")

# 获取配置参数
targetFontName = config['font_name']
ttfFontPath = config['font_path']
fontSizeDPI = config['font_dpi']
fontSizePx = config['font_size_px']
fontSPSize = config['font_spacing_percent']
del_ASCII_flag = config.get('filter_ascii', True)
add_ASCII_flag = config.get('map_include_ascii', False)

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

#确保输出目录存在
outputDir = config.get('output_dir', '')
if outputDir:
    os.makedirs(os.path.join(outputDir, "map"), exist_ok=True)
    os.makedirs(os.path.join(outputDir, "bdf"), exist_ok=True)
    os.makedirs(os.path.join(outputDir, "code"), exist_ok=True)
    mapPath = os.path.join(outputDir, "map", "{}.map".format(targetFontName))
    bdfPath = os.path.join(outputDir, "bdf", "{0}_{1}.bdf".format(tftFontNameReal, fontSizePx))
    c_codePath = os.path.join(outputDir, "code", "{0}.c".format(targetFontName))
else:
    os.makedirs("map", exist_ok=True)
    os.makedirs("bdf", exist_ok=True)
    os.makedirs("code", exist_ok=True)
    mapPath = "map/{}.map".format(targetFontName)
    bdfPath = "bdf/{0}_{1}.bdf".format(tftFontNameReal,fontSizePx)
    c_codePath = "code/{0}.c".format(targetFontName)

#覆盖创建map文件
mapFile_f = open(mapPath,"w", encoding='utf-8')
mapFile_f.write(mapFileDatas)
mapFile_f.close()

#生成bdf字库
targetFontName = "{0}_{1}".format(targetFontName,fontSizePx)
otf2bdfCMD = "otf2bdf.exe -v -r {3} -p {0} -o {1} {2}".format(fontSizePt,bdfPath,ttfFontPath,fontSizeDPI)
print(">",otf2bdfCMD)
os.system(otf2bdfCMD)
#生成u8g2目标C语言字库文件
bdfconvCMD = "bdfconv.exe -v -b 0 -f 1 {0} -M {1} -n {2} -o {3} -p {4} -d {0}".format(bdfPath,mapPath,targetFontName,c_codePath,fontSPSize)
print(">",bdfconvCMD)
os.system(bdfconvCMD)
#完成信息
print('\033[1;37;42m',"[操作完成]",'\033[0m')
print(f"生成的文件：")
print(f"  - {mapPath}")
print(f"  - {bdfPath}")
print(f"  - {c_codePath}")
