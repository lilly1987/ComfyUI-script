import os, glob, sys
import json
from urllib import request, parse
import random
import time
#from LinkedList import LinkedList 
import time
from PromptClass import *
import copy  

dress="{__character_dress__|__dress_my__|},__acc_my__,"
shoulder="{off shoulder, bare shoulders, Strapless,|__shoulder__,}"
quality="{masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,|__quality_my__,}"
dress="{__character_dress__|__dress_my__|},__acc_my__,"
NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:__1.00_1.49__), __NSFW_my__,"
pose="{standing,|}"
focus="{full body,|}"
acc="{__acc_my__|}"
char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, __breasts__,"
negative="__no2d__"
positive=quality + char + dress + shoulder + NSFW + acc + focus + pose

chars={ 
    "SaegusaMayumi" : {
        "char" : "{mayumi,__breasts__,|__mayumi__},",
        #"dress" : [ "mahouka_uniformm, green_jacket, see-through lace white long sleeveless dress, shoulder, black high heels, black_pantyhose,","__SaegusaMayumidress__" ,dress],
        "dress" : "{__SaegusaMayumidress__|__character_dress__|__dress_my__|}, __acc_my__," ,
        "lora" : ["SaegusaMayumiTheIrregularAt_mayumi"],
    },
    "Tomoyo" : {
        "char" : "(daidouji_tomoyo:1.2), (tomoyo:1.2), black long hair, blunt bangs, small breasts, cardcaptor sakura \(style\),",
        #"dress" : "{__character_dress__},"+shoulder ,
        "lora" : ["daidoujiTomoyo_v01.safetensors","tomoyo_V1Epoch6.safetensors","sakuraKinomoto_sakuraV1Epoch6.safetensors","cardcaptorSakura_sakuraEpoch6.safetensors"],
    },
    "diana" : {
        "char" : "diana cavendish, long wavy hair, multicolored two-tone streaked hair, light green hair, light blonde hair, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : "dianaCavendishLittle_v11ClothesFix.safetensors",
        "dress":"{__diana_cavendish_dress__|__character_dress__|__dress_my__|},",
        "acc":"__acc_my__,"
    },
    "schnee" : {
        "char" : "weiss schnee, white long hair, bangs, hair between eye, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : ["weissSchneeRWBY_weissSchneeV10.safetensors","weissSchneeLORA_weissSchnee.safetensors"],
        #"dress": "{__character_dress__|__diana_cavendish_dress__},"
    },
    "lillie" : {
        "char" : "character_pokemon_lillie, hat,",
        #"negative" : "__no2d__",
        "lora" : "pokemonLillieLilieSD15_v4"
    },
    "sailorMercury" : {
        "char" : "sailormercury, hat,",
       # "negative" : "__no2d__",
        "lora" : "sailorMercury_v10"
    },
    "lovedollLikenessMiyou" : {
        "char" : "photorealistic, __my__",
        "negative" : "__no3d__",
        "lora" : "lovedollLikenessMiyou_v10"
    },
    #"ShiningBladeIra_ira" : {
    #    #"char" : "photorealistic, __my__",
    #    #"negative" : "__no3d__",
    #    "lora" : "ShiningBladeIra_ira"
    #},
    "riceShowerUmamusume_v10" : {
        "char" : "(rice shower \(umamusume\)),",
       # "negative" : "__no2d__",
        "lora" : "riceShowerUmamusume_v10"
    },
    "solutionEpsilon_v10" : {
        "char" : "solution_epsilon,",
        #"negative" : "__no2d__",
        "lora" : "solutionEpsilon_v10"
    },
    "yorBriarSpyFamily_lykonV1" : {
        "char" : "__yor_briar_head__,",
        #"negative" : "__no2d__",
        "lora" : "yorBriarSpyFamily_lykonV1"
    },
    "keqingGenshinImpactLora_v10" : {
        "char" : "keqing \(genshin impact\),",
        #"negative" : "__no2d__",
        "lora" : "keqingGenshinImpactLora_v10"
    },
    "yamanakaInoNaruto_v1" : {
        "char" : "hair_over_one_eye, blonde_hair,",
        #"negative" : "__no2d__",
        "lora" : "yamanakaInoNaruto_v1"
    },
    "gwenFromLeagueOf_gwenLolV1" : {
        "char" : "gwen \(league of legends\), drill hair,",
        #"negative" : "__no2d__",
        "lora" : "gwenFromLeagueOf_gwenLolV1"
    },
    "barbara2in1Lora_v10" : {
        "char" : "{barbara \(genshin impact\)|barbara \(summertime sparkle\) \(genshin impact\)}, twintails, blonde hair,",
        #"negative" : "__no2d__",
        "lora" : "barbara2in1Lora_v10"
    },
    "ningguang_v10" : {
        "char" : "__ningguang_head__,",
        #"negative" : "__no2d__",
        "lora" : "ningguang_v10"
    },
    "kamisatoAyakaGenshin_ayakav10" : {
        "char" : "ayaka, genshin impact, kamisato ayaka, photorealistic,",
        "negative" : "__no3d__",
        "lora" : "kamisatoAyakaGenshin_ayakav10"
    },
    "primKuroinu_10" : {
        "char" : "kuroinu_prim,",
        #"negative" : "__no3d__",
        "lora" : "primKuroinu_10"
    },
    "tsubeHanaTheHypnosis_tsubeHana" : {
        "char" : "Tsube Hana, side braid, ",
        #"negative" : "__no3d__",
        "lora" : "tsubeHanaTheHypnosis_tsubeHana"
    },
    "Fashion Girl" : {
        "char" : "fashi-girl, red lips, makeup, realistic,",
        #"negative" : "__no3d__",
        "lora" : ["fashionGirl_v50","fashionGirl_v47"]
    },
    "liyuuLora_liyuuV1" : {
        "char" : "black hair, bangs, ",
        "negative" : "__no3d__",
        "lora" : "liyuuLora_liyuuV1"
    },
    "chineseCosplayerXiaorouseeu_v10" : {
        "char" : "black hair, bangs, ",
        "negative" : "__no3d__",
        "lora" : "liyuuLora_liyuuV1"
    },
    "IrisPokemon_v10" : {
        "char" : "irisa, irisb, irisc,",
        #"negative" : "__no3d__",
        "lora" : "IrisPokemon_v10"
    },
    "my" : {
        "positive" : "__my__",
        #"negative" : "__no2d__",
        #"strength_model" : [0.5,1.0]
    },

}

myckpts=["AOM3A1-fp16","libmix_v20-fp16"]

#wildcardsOn=False
#random.shuffle(ckptnms)

#======================
loradic={
    "femaleMasturbationBoob_v1" : "masturbation, fingering, female_masturbation, grabbing_own_breast,",
    "femaleMasturbation_v1" : "fingering, schlick, masturbation,",
    "amazonPositionSexAct_v10" : "sex,pussy,",
    "artistKidmo_v10" : "Artist_Kidmo,porn,sex,realism, blush,sweat,saliva, orgasm, lewd, hentai,",
    "artistYimao_v10" : "Artist_Yimao,sexy,porn, blush,sweat,saliva, orgasm, ahegao, bondage,",
    "artistHimitsu_v10" : "Artist_Himitsu, sexy,porn, blush,sweat,saliva, gag, ",
    "artistMeito_v10" : "Artist_Meito, sex,porn, blush,sweat,saliva, orgasm, ahegao, rape, speech bubble, ",
    "fromBelowPOV_v1" : "from_below,  foreshortening ,uncensored,pussy, no panties,",
    #"lrCumInStomach_lrCumInStomachV10" : "deepthroat, fellatio, x-ray, cum in stomach,",
}
def loradicRandom(m,c):
    loradnm=random.choice(list(loradic.keys()))
    m.lora_add(loradnm)
    caddin(c,"NSFW_add",loradic[loradnm])
#======================
keys = list(chars.keys())
ckptcnt=0
while True:
    
    random.shuffle(keys)
    for c in keys:
        c=random.choice(["SaegusaMayumi","Tomoyo","diana"])
        for j in range(2):
            cc=copy.deepcopy(chars[c])
            if ckptcnt ==0 :
                PromptClass.ckptnm=random.choice(ckptnms)
                #PromptClass.ckptnm="VIC-BACLA-MIX-V1-fp16"
                ckptcnt=6
            ckptcnt-=1
            m=PromptClass()            
            #chars[c]["loraList"]=["amazonPositionSexAct_v10"]
            
            loradicRandom(m,cc)
            
            #if random.choice([True, False]):
            #    m.lora_add(random.choice(loranms))
            
            #if random.choice([True, False]):
            nm=m.lora_add("hunged_girl")
            m.pset(nm,"strength_model_min",0.75)
            m.pset(nm,"strength_clip_min",0.75)
            caddin(cc,"NSFW_add","__hunged_girl__")
            
                #chars[c]["NSFW"]=chars[c]["NSFW"]+"__hunged_girl__"
            m.pset("EmptyLatentImage","height",768+64*1)
            m.pset("EmptyLatentImage","width",320+64*1)
            
            m.prompt_set(cc)
            
            print(m.prompts)
            queue_prompt(m.prompts,1)


#======================
"""
for ckptnm in random.sample(ckptnms,min(20,len(ckptnms))):#+myckpts
#for ckptnm in ckptnms:

    print(f"ckptnm : {ckptnm}")
    PromptClass.ckptnm=ckptnm
    #continue
    
    
    #for c  in chars:
    c="SaegusaMayumi"
    keys = list(chars.keys())
    random.shuffle(keys)
    #for j in range(1):
    for c in keys:
        for j in range(4):
            
            m=PromptClass()            
            #chars[c]["loraList"]=["amazonPositionSexAct_v10"]

            #if random.choice([True, False]):
            #    m.lora_add("femaleMasturbation_v1")
            #    cadd(chars[c],"NSFW","fingering, schlick, masturbation,")
            #if random.choice([True, False]):
            #    m.lora_add("amazonPositionSexAct_v10")
            #    cadd(chars[c],"NSFW","sex,pussy,")
            if random.choice([True, False]):
                m.lora_add(random.choice(loranms))
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
    
    """