import os, glob, sys
import json
from urllib import request, parse
import random
import wildcards

prompt={}
names={}
ckpts=glob.glob(
    os.path.join(
        os.path.dirname(__file__),
        "..\\models\\checkpoints"
    )+"\\*-fp16.safetensors"
)
ckptnms=[os.path.basename(ckpt) for ckpt in ckpts]

sys.exit()

def lget(a):
    return random.choice(a) if type(a) is list else a

def pget(name,input):
    return prompt[names[name]]["inputs"][input]
    
def pset(name,input,value):
    prompt[names[name]]["inputs"][input] = lget(value)

def psetd(name,kv):
    for k, v in kv.items():
        pset(name,k,v)

def cget(c,v,t):
    p=chars[c][v] if v in chars[c] else t
    return lget(p)
    
def prompt_add(name,class_type,inputs):
    n=f"{len(names)}"
    names[name]=n
    prompt[n]={
        "class_type":class_type,
        "inputs":inputs
    }
    

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)
    

#print(f"ckpts {ckptnms}")

prompt_add(
    "CheckpointLoaderSimple",
    "CheckpointLoaderSimple",
    {
        "ckpt_name": "weriDiffusion_v10-fp16.safetensors"
    }
)
"""
prompt_add(
    "LoraLoader",
    "LoraLoader",
    {
        "model" : [names["CheckpointLoaderSimple"],0],
        "clip" : [names["CheckpointLoaderSimple"],1],
        "lora_name": "dianaCavendishLittle_v11ClothesFix.safetensors",
        "strength_model": 1.0,
        "strength_clip": 1.0
    }
)
"""
prompt_add(
    "LoraLoaderTextRandom",
    "LoraLoaderTextRandom",
    {
        "model" : [names["CheckpointLoaderSimple"],0],
        "clip" : [names["CheckpointLoaderSimple"],1],
        "lora_name": "dianaCavendishLittle_v11ClothesFix.safetensors",
        "seed": random.randint(0, 0xffffffffffffffff ),
        "strength_model_min": 0.50,
        "strength_model_max": 1.0,
        "strength_clip_min": 0.50,
        "strength_clip_max": 1.0
    }
)

prompt_add(
    "CLIPTextEncodeN",
    "CLIPTextEncode",
    {
        "clip" : [names["CheckpointLoaderSimple"],1],
        "text": "worst quality, low quality, bad hands, extra arms, extra legs, multiple viewer, grayscale, multiple views, monochrome"
    }
)

prompt_add(
    "CLIPTextEncodeP",
    "CLIPTextEncode",
    {
        "clip" : [names["CheckpointLoaderSimple"],1],
        "text": ""
    }
)

prompt_add(
    "EmptyLatentImage",
    "EmptyLatentImage",
    {
        "batch_size": 1,
        "height": 768,
        "width": 320
    }
)

prompt_add(
    "KSampler",
    "KSampler",
    {
        "model": [names["LoraLoaderTextRandom"],0],
        "positive": [names["CLIPTextEncodeP"],0],
        "negative": [names["CLIPTextEncodeN"],0],
        "latent_image": [names["EmptyLatentImage"],0],
        "sampler_name": "dpmpp_sde",
        "scheduler": "karras",
        "seed": random.randint(0, 0xffffffffffffffff ),
        "steps": random.randint(20, 30 ),
        "cfg": random.randint( int(5*2) , int(9*2) ) / 2,
        "denoise": random.uniform(0.5,1.0) ,
    }
)

prompt_add(
    "VAELoader",
    "VAELoader",
    {
        "vae_name": "BerrysMix.vae.safetensors"
    }
)

prompt_add(
    "VAEDecode",
    "VAEDecode",
    {
        "samples": [names["KSampler"],0],
        "vae": [names["VAELoader"],0],
    }
)

prompt_add(
    "SaveImage",
    "SaveImage",
    {
        "images": [names["VAEDecode"],0],
        "filename_prefix": "ComfyUI",
    }
)

#print(names)
#print(prompt)

shoulder="off shoulder, bare shoulders, Strapless,"
quality="masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,"
dress="{sweater|maid|princess royal|santa|lolita fashion|china|witch|wedding|yukata|kimono|} {frilled |}{long |}dress, {{puffy | }{wide |}{long |}sleeves,|} high heels, "+shoulder
NSFW=["NSFW, breasts exposure, breastsout, nipple exposure, "]
prompt_my="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, small breasts,"

chars={ 
    "my" : {
        "prompt" : prompt_my,
        #"strength_model" : [0.5,1.0]
    },
    "diana" : {
        "prompt" : "diana cavendish, long wavy hair, multicolored two-tone streaked hair, light green hair, light blonde hair, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : "dianaCavendishLittle_v11ClothesFix.safetensors",
        
    },
    "schnee" : {
        "prompt" : "weiss schnee, white long hair, bangs, hair between eye, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : ["weissSchneeRWBY_weissSchneeV10.safetensors","weissSchneeLORA_weissSchnee.safetensors"],
    },
    "Tomoyo" : {
        "prompt" : "(daidouji_tomoyo:1.2), (tomoyo:1.2), black long hair, blunt bangs, small breasts, cardcaptor sakura \(style\),",
        #"dress" : [ "" ,dress],
        "lora" : ["daidoujiTomoyo_v01.safetensors","tomoyo_V1Epoch6.safetensors","sakuraKinomoto_sakuraV1Epoch6.safetensors","cardcaptorSakura_sakuraEpoch6.safetensors"],
    },
    "SaegusaMayumi" : {
        "prompt" : "mayumi,",
        "dress" : [ "mahouka_uniformm, green_jacket, see-through lace white long sleeveless dress, shoulder, black high heels, black_pantyhose, " ,dress],
        "lora" : ["SaegusaMayumiTheIrregularAt_mayumi"],
    },

}

myckpts=["AOM3A1-fp16","libmix_v20-fp16"]

random.shuffle(ckptnms)

#for ckptnm in random.sample(ckptnms,100)+myckpts:
for ckptnm in ckptnms:

    print(f"ckptnm : {ckptnm}")
    pset("CheckpointLoaderSimple","ckpt_name",ckptnm)
    #pset("CheckpointLoaderSimple","ckpt_name","AOM3A1-fp16.safetensors")

    #continue
    
    for c  in chars:
        for j in range(4):
            
            print(f"char : {c}" )
            
            tmp=""
            tmp+=cget(c,"quality",quality)
            tmp+=cget(c,"prompt",prompt_my)
            tmp+=cget(c,"dress",dress)
            tmp+=cget(c,"NSFW",NSFW)
            pset("CLIPTextEncodeP","text", tmp)
                
            if "lora" in chars[c]: 
                
                pset("LoraLoaderTextRandom","lora_name",lget(chars[c]["lora"]))
                    
                pset("LoraLoaderTextRandom","seed", random.randint(0, 0xffffffffffffffff ))
                #if "strength_model" in chars[c]: 
                #    prompt[names["LoraLoaderTextRandom"]]["inputs"]["strength_model"] =  random.uniform(chars[c]["strength_model"][0],chars[c]["strength_model"][1]) 
                #else:
                #    prompt[names["LoraLoaderTextRandom"]]["inputs"]["strength_model"] =  random.uniform(0.25,1.0) 

                pset("KSampler","model", [names["LoraLoaderTextRandom"],0]   )
                pset("CLIPTextEncodeP","clip", [names["LoraLoaderTextRandom"],1] )
                pset("CLIPTextEncodeN","clip", [names["LoraLoaderTextRandom"],1] )
            else:
                #print(f"lora no {c}")
                pset("KSampler","model", [names["CheckpointLoaderSimple"],0] )
                pset("CLIPTextEncodeP","clip",[names["CheckpointLoaderSimple"],1] )
                pset("CLIPTextEncodeN","clip",[names["CheckpointLoaderSimple"],1] )
                
                psetd(
                    "KSampler",
                    {
                        "seed":random.randint(0, 0xffffffffffffffff ),
                        "steps":random.randint(20, 30 ),
                        "cfg":random.randint(int(5*2) , int(9*2) ) / 2,
                        "denoise":random.uniform(0.75,1.0) ,
                    }
                )
            
            #print(prompt)
            
            #continue
            pset("SaveImage","filename_prefix" , 
                os.path.splitext(
                    pget("CheckpointLoaderSimple","ckpt_name")
                )[0]+"-"+str(random.randint(0, 0xffffffffffffffff ))
            )
            queue_prompt(prompt)