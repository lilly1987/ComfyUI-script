import sys
import json
import os
if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
print(__file__)
print(os.path.basename(__file__))


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
print(py_name, style="bold CYAN")

absFilePath = os.path.abspath(__file__)
print("abspath   : " + absFilePath , style="bold CYAN")

realFilePath = os.path.realpath(__file__)
print("realpath  : " + realFilePath , style="bold CYAN")

normpath=os.path.normpath(__file__)
print("normpath  : " + normpath , style="bold CYAN")

subfolder = os.path.dirname(normpath)
print("subfolder : " + subfolder , style="bold CYAN")

filename = os.path.basename(normpath)
print("filename  : " + filename , style="bold CYAN")
        
mainFile = os.path.abspath(sys.modules['__main__'].__file__)
print("mainFile  : " + mainFile ,style="bold CYAN")

mainfolder = os.path.dirname(mainFile)
print("mainfolder : " + mainfolder , style="bold CYAN")

def jsondic(full,dic):
    
    path=os.path.split(full)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    #with open(f"./RandomLoop/chars-{time.strftime('_%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as file:
    if os.path.exists(full):
        with open(full, 'r', encoding='utf-8') as file:
            dic=json.load(file)
            #print(dic)
    else:
        with open(full, 'w', encoding='utf-8') as file:
            json.dump(dic, file, sort_keys=False, indent=4)
            
    return path
        