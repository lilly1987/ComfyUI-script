import os, sys
import glob
import json
from urllib import request, parse
import random
import time
#from LinkedList import LinkedList 
import time
import copy  
import os


print(__name__)
print(os.path.splitext(os.path.basename(__file__))[0])
if __name__ == os.path.splitext(os.path.basename(__file__))[0] or __name__ =='__main__':
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console

from PromptClass import *
from jsondic import jsondic

#print(f"PromptClass : " , PromptClass.__dict__)
#----------------------------
chars={
    #"my" : {
    #    "positive" : "__my__",
    #    #"negative" : "__no2d__",
    #},
}
#----------------------
loradic={
}
#----------------------
ckptnmsmy=[
]
#----------------------
styles={
    "arknightsChibiLora_v1" : "chibi, full body, "
}
#---------------------------------
itemnames=PromptClass.positivenames+["negative"]

settup={
}
for p in itemnames:
    settup[p]=eval(f"PromptClass.{p}")

#---------------------------------
ckptcnt=0
colormy="bright_yellow"
# [{colormy}] [/{colormy}]
while True:
    try:
        if os.path.exists("./RandomLoop/__deletejson__.txt"):
            for filename in glob.glob("./RandomLoop/*.json"):
                os.remove(filename)

        def jsonget(name,item,update=False):
            tmp=""
            if os.path.exists(f"./RandomLoop/{name}.json"):
                tmp=jsondic(f"./RandomLoop/{name}.json",item,update)
            #elif os.path.exists(f"./RandomLoop/sample/{name}.json"):
            #    return jsondic(f"./RandomLoop/sample/{name}.json",item,update)
            elif os.path.exists(f"./RandomLoop/default/{name}.json"):
                tmp=jsondic(f"./RandomLoop/default/{name}.json",item,update)
            return tmp
                
        settupjsonpath=jsonget("settup",settup,True)
        ckptsjsonpath=jsonget("ckpts",ckptnmsmy,True)
        charsjsonpath=jsonget("chars",chars,True)
        lorasjsonpath=jsonget("loras",loradic,True)
        
        for p in itemnames:
            if p in settup :
                exec(f"PromptClass.{p}=settup[p]")
        
        keys = [list(chars.keys())]
        if "mychar" in settup :
            if type(settup["mychar"]) is list:
                keys += [settup["mychar"]]
            else:
                keys += [[settup["mychar"]]]

        if len(ckptnmsmy)>0:
            ckptnms2=[ckptnms,ckptnmsmy]
        else:
            ckptnms2=[ckptnms]
            
        #random.shuffle(keys)
        c=random.choice(random.choice(keys))
        #c="Tomoyo"
        cc=chars[c]
        for j in range(settup["charLoop"] if "charLoop" in settup else 2):
        
            console.rule(f" {c} char Loop ")
            
            if ckptcnt <=0 :
                PromptClass.ckptnm=random.choice(random.choice(ckptnms2))
                #PromptClass.ckptnm="VIC-BACLA-MIX-V1-fp16"
                print()
                print(f"[{colormy}]PromptClass.ckptnm : [/{colormy}]{PromptClass.ckptnm}")
                ckptcnt=6
            ckptcnt-=1
            
            print()
            print(f"[{colormy}]ckptcnt : [/{colormy}]{ckptcnt}")
            
            m=PromptClass(cc)
                    
            if random.choice([True, False]) and len(loradic)>0:#, False
                loradnm=random.choice(list(loradic.keys()))
                m.lora_add(loradnm)
                m.caddin("NSFW_add",loradic[loradnm])
                
            if random.choice([True, False]) and len(styles)>0:#, False
                loradnm=random.choice(list(styles.keys()))
                m.lora_add(loradnm)
                m.caddin("style_add",styles[loradnm])

            if random.choice([True, False]) and len(loranms)>0:
                loradnm=random.choice(loranms)
                m.lora_add(loradnm)

            """
            if random.choice([True, False]):
            #if True:
                nm=m.lora_add("breastsOutExposed_24")
                m.caddin("NSFW_add",loradic["breastsOutExposed_24"])
                
            if random.choice([True, False]):
            #if True:
                nm=m.lora_add("conceptCowgirl_v10")
                m.caddin("NSFW_add","__Cowgirl1__,")
            
            if random.choice([True, False]):
            #if True:
                nm=m.lora_add("hunged_girl")
                m.caddin("NSFW_add","__hunged_girl1__,")
            """
            
            def lora_set():
                if m.LoraLoader==m.LoraLoaderT :
                    m.lora_set("strength_model",random.uniform(settup[strength_model_min],settup[strength_model_max]))
                    m.lora_set("strength_clip" ,random.uniform(settup[strength_clip_min],settup[strength_clip_max]))                
                if m.LoraLoader==m.LoraLoaderR :
                    m.lora_set("strength_model_min",random.uniform(settup[strength_model_min],settup[strength_model_max]))
                    m.lora_set("strength_clip_min" ,random.uniform(settup[strength_clip_min],settup[strength_clip_max]))    
                    
            m.pset("EmptyLatentImage","height",settup["height"])
            m.pset("EmptyLatentImage","width",settup["width"])

            r=m.promptGet()
            print()
            print(f"[{colormy}]promptSet : [/{colormy}]",r)

            queue_prompt(r,1)
    except Exception:
        console.print_exception()
        quit()
