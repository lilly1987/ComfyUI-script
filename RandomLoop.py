import os, glob, sys
import json
from urllib import request, parse
import random
import time
#from LinkedList import LinkedList 
import time
import copy  

print(f"RandomLoop __name__ {__name__}")
print(f"RandomLoop __file__ {os.path.splitext(os.path.basename(__file__))[0]}")

from PromptClass import *
import mypath  
#----------------------------
PromptClass.dress="{__character_dress__|__dress_my__|},__acc_my__,"
PromptClass.shoulder="{off shoulder, bare shoulders, Strapless,|__shoulder__,}"
PromptClass.quality="{masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,|__quality_my__,}"
PromptClass.dress="{__character_dress__|__dress_my__|},__acc_my__,"
PromptClass.NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:__1.00_1.49__), __NSFW_my__,"
PromptClass.pose="{standing,|}"
PromptClass.focus="{full body,|}"
PromptClass.acc="{__acc_my__|}"
PromptClass.char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, __body1__"
PromptClass.negative="__no2d__"
PromptClass.positive=PromptClass.quality + PromptClass.char + PromptClass.dress + PromptClass.shoulder + PromptClass.NSFW + PromptClass.acc + PromptClass.focus + PromptClass.pose + PromptClass.body
#----------------------------

chars={ 
    "SaegusaMayumi" : {
        "char" : "{mayumi,__breasts__,|__mayumi__},",
        #"dress" : [ "mahouka_uniformm, green_jacket, see-through lace white long sleeveless dress, shoulder, black high heels, black_pantyhose,","__SaegusaMayumidress__" ,dress],
        "dress" : "{__SaegusaMayumidress__|__character_dress__|__dress_my__|}, " ,
        "lora" : "SaegusaMayumiTheIrregularAt_mayumi",
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
#    "sailorMercury" : {
#        "char" : "sailormercury, hat,",
#       # "negative" : "__no2d__",
#        "lora" : "sailorMercury_v10"
#    },
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
    "shalltearBloodfallen_v10" : {
        "char" : "shalltear, shalltearcostume, ponytail, ",
        #"negative" : "__no3d__",
        "lora" : "shalltearBloodfallen_v10"
    },
    "blackarona_v10" : {
        "char" : "arona, white hair, ",
        #"negative" : "__no3d__",
        "lora" : "blackarona_v10"
    },
    "gloriousAzurLaneSpring_GloriousSpiring" : {
        "char" : "blonde hair,",
        #"negative" : "__no3d__",
        "lora" : "gloriousAzurLaneSpring_GloriousSpiring"
    },
    "kidmoStyle_v1" : {
        #"char" : "blonde hair,",
        #"negative" : "__no3d__",
        "lora" : "kidmoStyle_v1"
    },
    "fuyusakaIori13SentinelsAegisRim_fuyusakaIoriSoftV10" : {
        "char" : "fuyusaka iori, fuyusaka iori 1, long hair, grey hair,",
        #"negative" : "__no3d__",
        "lora" : "fuyusakaIori13SentinelsAegisRim_fuyusakaIoriSoftV10"
    },
    "9a91GirlsFrontline_v10" : {
        "char" : "BREAK 9a91maid, ",
        #"negative" : "__no3d__",
        "lora" : "9a91GirlsFrontline_v10"
    },
    "my" : {
        "positive" : "__my__",
        #"negative" : "__no2d__",
    },

}

#----------------------
loradic={
    "femaleMasturbationBoob_v1" : "masturbation, fingering, female_masturbation, grabbing_own_breast,",
    "femaleMasturbation_v1" : "fingering, schlick, masturbation,",
    "amazonPositionSexAct_v10" : "sex,pussy,",
    "artistKidmo_v10" : "Artist_Kidmo,porn,sex,realism, blush,sweat,saliva, orgasm, lewd, hentai,",
    "artistYimao_v10" : "Artist_Yimao,sexy,porn, blush,sweat,saliva, orgasm, ahegao, bondage,",
    "artistHimitsu_v10" : "Artist_Himitsu, sexy,porn, blush,sweat,saliva, gag, ",
    "artistMeito_v10" : "Artist_Meito, sex,porn, blush,sweat,saliva, orgasm, ahegao, rape, speech bubble, ",
    "fromBelowPOV_v1" : "from_below,  foreshortening ,uncensored,pussy, no panties,",
    "conceptCowgirl_v10" : "cowgirl, sex, cowgirl position, {arms bound,| }",
    "horosukeSTentacle_v10" : "tentacle, entacle fellatio,  nipple sex, tentacle sex, chushou, {arms bound,| }",
    "tentacles_v10" : "tentacle, entacle fellatio,  nipple sex, tentacle sex, chushou, {arms bound,| }",
    "shirtPullTestSexAct_v10" : "no bra, shirt pull,",
    "breastsOutExposed_24" : "breastsout, no bra,",
    #"conceptStainedSheets_v10" : "stained sheets,",
    #"lrCumInStomach_lrCumInStomachV10" : "deepthroat, fellatio, x-ray, cum in stomach,",
}

#----------------------
ckptnmsmy=[
    "AOM3-fp16",
    "AOM3A1-fp16",
    "AOM3A1B-fp16",
    "AikimiXCv1.5-fp16",
    "AnyTwam-pruned-fp16"
    "Balor-V3.1featACT-fp16",
    "dreamboxMix-A-fp16-fp16",
    "dualPersonality_dualdalcenull-fp16",
    "libmix_v20-fp16",
    "whitespace_Quasar-fp16",
    "RememberMix-pruned-fp16",
    "RDtMix-fp16",
    "vividicimix_-fp16",
    "VIC-BACLA-MIX-V1-fp16",
]
#----------------------
def loradicRandom(m):
    loradnm=random.choice(list(loradic.keys()))
    m.lora_add(loradnm)
    m.caddin("NSFW_add",loradic[loradnm])
#======================
keys = [list(chars.keys()),["SaegusaMayumi","Tomoyo","diana","primKuroinu_10"]]
ckptcnt=0
while True:
    
    #random.shuffle(keys)
    c=random.choice(random.choice(keys))
    #for c in keys:
        #c=random.choice(
        #    random.choice(
        #        [
        #            ,
        #            list(chars.keys())
        #        ]
        #    )
        #)
    c="Tomoyo"
    cc=chars[c]
    for j in range(2):
        if ckptcnt <=0 :
            PromptClass.ckptnm=random.choice(random.choice([ckptnms,ckptnmsmy]))
            #PromptClass.ckptnm="VIC-BACLA-MIX-V1-fp16"
            print()
            print(f"ckptnms,ckptnmsmy : {len(ckptnms)},{len(ckptnmsmy)}")
            print(f"PromptClass.ckptnm : {PromptClass.ckptnm}")
            ckptcnt=6
        ckptcnt-=1
        print()
        print(f"ckptcnt {ckptcnt}")
        if random.choice([True, False]):
            cc["positive"]=["__quality1__,","__dress1__,","__NSFW1__,","__body1__,"]
            if "char" in cc:
                cc["positive"]+=[cc["char"]]
        
        m=PromptClass(cc)            
        #r=m.promptSet()
        #print(f"promptSet : {r}")
        
        if "lora" in cc:
            #print(f"")
            #print(f"chars[c]['lora'] : {cc['lora']}")
            #print(f"chars[c]['lora'] : {type(cc['lora'])}")
            #print(f"loratag : {m.loratag}")
            if m.LoraLoader==m.LoraLoaderT :
                m.lora_set("strength_model",random.uniform(1/8*5,1.0))
                m.lora_set("strength_clip" ,random.uniform(1/8*12,1.0))                
            if m.LoraLoader==m.LoraLoaderR :
                m.lora_set("strength_model_min",random.uniform(1/8*5,1.0))
                m.lora_set("strength_clip_min" ,random.uniform(1/8*12,1.0))

        """
        """
        if random.choice([True, False]):
            loradicRandom(m)
        
        if random.choice([True, False]):
            m.lora_add(random.choice(loranms))
            
        if random.choice([True, False]):
        #if True:
            nm=m.lora_add("breastsOutExposed_24")
            if m.LoraLoader==m.LoraLoaderT :
                m.pset(nm,"strength_model",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip" ,random.uniform(1.25,1.0))
            if m.LoraLoader==m.LoraLoaderR :
                m.pset(nm,"strength_model_min",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip_min" ,random.uniform(1.25,1.0))
            m.caddin("NSFW_add",loradic["breastsOutExposed_24"])
            
        if random.choice([True, False]):
        #if True:
            nm=m.lora_add("conceptCowgirl_v10")
            if m.LoraLoader==m.LoraLoaderT :
                m.pset(nm,"strength_model",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip" ,random.uniform(1.25,1.0))
            if m.LoraLoader==m.LoraLoaderR :
                m.pset(nm,"strength_model_min",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip_min" ,random.uniform(1.25,1.0))
            m.caddin("NSFW_add","__Cowgirl1__,")
        
        if random.choice([True, False]):
        #if True:
            nm=m.lora_add("hunged_girl")
            if m.LoraLoader==m.LoraLoaderT :
                m.pset(nm,"strength_model",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip" ,random.uniform(1.25,1.0))
            if m.LoraLoader==m.LoraLoaderR :
                m.pset(nm,"strength_model_min",random.uniform(0.5,1.0))
                m.pset(nm,"strength_clip_min" ,random.uniform(1.25,1.0))
            m.caddin("NSFW_add","__hunged_girl1__,")
        
        m.pset("EmptyLatentImage","height",768+64*1)
        m.pset("EmptyLatentImage","width",320+64*1)
        
        
        r=m.promptSet()
        r=m.promptGet()
        #print()
        #print(f"promptSet : {r}")
        print()
        print(f'm.CLIPTextEncodeP : {m.pget("CLIPTextEncodeP","text")}')
        print()
        print(f'm.CLIPTextEncodeN : {m.pget("CLIPTextEncodeN","text")}')
        print()
        print(f"m.loratag : {m.loratag}")
       
        queue_prompt(r,1)

