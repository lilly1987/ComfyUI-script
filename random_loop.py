import os, glob, sys
import json
from urllib import request, parse
import random
import time
#from LinkedList import LinkedList 
import time
from PromptClass import *

dress="{__character_dress__|__dress_my__|},__acc_my__,"
shoulder="{off shoulder, bare shoulders, Strapless,|__shoulder__,}"
quality="{masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,|__quality_my__,}"
dress="{__character_dress__|__dress_my__|},__acc_my__,"
NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:__1.00_1.49__), __NSFW_my__,"
char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, __breasts__,"
negative="__no2d__"
positive=quality + char + dress + shoulder + NSFW

chars={ 
    "SaegusaMayumi" : {
        "prompt" : "{mayumi,__breasts__,|__mayumi__},",
        #"dress" : [ "mahouka_uniformm, green_jacket, see-through lace white long sleeveless dress, shoulder, black high heels, black_pantyhose,","__SaegusaMayumidress__" ,dress],
        "dress" : "{__SaegusaMayumidress__|__character_dress__|__dress_my__|}, __acc_my__," ,
        "lora" : ["SaegusaMayumiTheIrregularAt_mayumi"],
    },
    "Tomoyo" : {
        "prompt" : "(daidouji_tomoyo:1.2), (tomoyo:1.2), black long hair, blunt bangs, small breasts, cardcaptor sakura \(style\),",
        #"dress" : "{__character_dress__},"+shoulder ,
        "lora" : ["daidoujiTomoyo_v01.safetensors","tomoyo_V1Epoch6.safetensors","sakuraKinomoto_sakuraV1Epoch6.safetensors","cardcaptorSakura_sakuraEpoch6.safetensors"],
    },
    "diana" : {
        "prompt" : "diana cavendish, long wavy hair, multicolored two-tone streaked hair, light green hair, light blonde hair, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : "dianaCavendishLittle_v11ClothesFix.safetensors",
        "dress":"{__diana_cavendish_dress__|__character_dress__|__dress_my__|}, __acc_my__,"
    },
    "schnee" : {
        "prompt" : "weiss schnee, white long hair, bangs, hair between eye, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : ["weissSchneeRWBY_weissSchneeV10.safetensors","weissSchneeLORA_weissSchnee.safetensors"],
        #"dress": "{__character_dress__|__diana_cavendish_dress__},"
    },
    "my" : {
        "positive" : "__my__",
        "negative" : "__no2d__",
        #"strength_model" : [0.5,1.0]
    },

}

myckpts=["AOM3A1-fp16","libmix_v20-fp16"]

#wildcardsOn=False
#random.shuffle(ckptnms)

for ckptnm in random.sample(ckptnms,2):#+myckpts
#for ckptnm in ckptnms:

    print(f"ckptnm : {ckptnm}")
    PromptClass.ckptnm=ckptnm
    #continue
    
    
    #for c  in chars:
    c="SaegusaMayumi"
    #for j in range(10 - len(chars)):
    for j in range(1):
        for j in range(4):
            
            m=PromptClass()            
            chars[c]["loraList"]=["amazonPositionSexAct_v10"]
            m.prompt_set(chars[c])
            #m.pset("CheckpointLoaderSimple","ckpt_name",ckptnm)
            
            print(m.prompts)
            queue_prompt(m.prompts)
    #c="SaegusaMayumi"
    #for j in range(1):
    #for c  in chars:
    #    for j in range(2):
    #        
    #        m=myprompt()            
    #        m.prompt_set(chars[c])
    #        #m.pset("CheckpointLoaderSimple","ckpt_name",ckptnm)
    #        print(m.prompts)
    #        queue_prompt(m.prompts)