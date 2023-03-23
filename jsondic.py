import sys
import json
import ast
import os
if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
	
	
def jsondic(full,dic,update=False):

    path=os.path.split(full)[0]
    if not os.path.exists(path):
        os.makedirs(path)
        
    #with open(f"./RandomLoop/chars-{time.strftime('_%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as file:
    if os.path.exists(full):
        with open(full, 'r', encoding='utf-8') as file:
            text=""
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
                if not line.startswith("#"):
                    text+=line+"\n"

            text=ast.literal_eval(text)
            text = json.dumps(text)
            tmp=json.loads(text)

            if update:
                if type(dic) is dict:
                    dic.update(tmp)
                elif type(dic) is list:
                    dic+=tmp
                else:
                    print("type(dic) : ",type(dic),style="reset")
            else:
                dic=tmp

    else:
        with open(full, 'w', encoding='utf-8') as file:
            json.dump(dic, file, sort_keys=False, indent=4)

    return path
        