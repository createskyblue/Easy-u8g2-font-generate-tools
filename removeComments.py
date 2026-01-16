import os
#确保win10终端颜色正常显示
if os.name == "nt":
    os.system("")


def removeComments(List):
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


with open('D:\Documents\Github\hc32f460kcta_Acq_PAD\project\source\menu.c',encoding='utf-8') as lines:  #一次性读入txt文件，并把内容放在变量lines中
    C_File=lines.readlines()  #返回的是一个列表，该列表每一个元素是txt文件的每一行 


ans = removeComments(C_File)
print(ans)