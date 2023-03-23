import sys
import json
import ast
import os
if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
#print(__file__)
#print(os.path.basename(__file__))


"""
import psutil
for proc in psutil.process_iter():
  ps_name = proc.name()
  if ps_name == 'python3':
    cmdline = proc.cmdline()
    print(cmdline)
"""

"""
print()
for key, value in os.environ.items():
    print('{}: {}'.format(key, value))
print()
"""

py_name=os.path.basename(__file__)
print("os.path.basename(__file__) : ",py_name, style="bold CYAN")

absFilePath = os.path.abspath(__file__)
print("os.path.abspath(__file__)  : " , absFilePath , style="bold CYAN")

realFilePath = os.path.realpath(__file__)
print("os.path.abspath(__file__)  : " + realFilePath , style="bold CYAN")

normpath=os.path.normpath(__file__)
print("os.path.normpath(__file__) : " + normpath , style="bold CYAN")

subfolder = os.path.dirname(normpath)
print("os.path.dirname(normpath) : " + subfolder , style="bold CYAN")

filename = os.path.basename(normpath)
print("os.path.basename(normpath) : " + filename , style="bold CYAN")

mainFile = os.path.abspath(sys.modules['__main__'].__file__)
print("os.path.abspath(sys.modules\['__main__'].__file__) : " + mainFile ,style="bold CYAN")
mainfolder = os.path.dirname(mainFile)
print("os.path.dirname(mainFile) : " + mainfolder , style="bold CYAN")

def jsondic(full,dic,update=False):
    #print("full : ",os.path.exists(full),full,style="reset")
    #print("dic0 : ",dic,style="reset")
    path=os.path.split(full)[0]
    #print("path : ",path,style="reset")
    if not os.path.exists(path):
        os.makedirs(path)
    #with open(f"./RandomLoop/chars-{time.strftime('_%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as file:
    if os.path.exists(full):
        #print("dic1 : ",dic,style="reset")
        with open(full, 'r', encoding='utf-8') as file:
        
            text=""
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
                if not line.startswith("#"):
                    #print("line" , line)
                    text+=line+"\n"
            #print("text" , text)
            text=ast.literal_eval(text)
            #print("text" , text)
            text = json.dumps(text)
            #print("text" , text)
            tmp=json.loads(text)
            #print("type(tmp) : ",type(tmp),style="reset")
            #print("tmp : ",tmp,style="reset")
            if update:
                if type(dic) is dict:
                    dic.update(tmp)
                    #print("dic2 : ",dic,style="reset")
                elif type(dic) is list:
                    dic+=tmp
                    #print("dic3 : ",dic,style="reset")
                else:
                    print("type(dic) : ",type(dic),style="reset")
            else:
                dic=tmp
                #print("dic4 : ",dic,style="reset")
            #print("dic5 : ",dic,style="reset")
    else:
        with open(full, 'w', encoding='utf-8') as file:
            json.dump(dic, file, sort_keys=False, indent=4)
    #print("dic6 : ",dic,style="reset")
    return path
        