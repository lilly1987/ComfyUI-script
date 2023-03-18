import json
from urllib import request, parse
import random
import os, glob

prompt={}
names={}

quality="masterpiece, best quality,"
dress="{sweater|maid|princess royal|santa|lolita fashion|china|witch|wedding|{yukata|kimono}} {frilled |}{long |}dress, {{puffy | }{wide | }{long | }sleeves,| } high heels, off shoulder, bare shoulders, Strapless,"
NSFW="NSFW, breasts exposure, breastsout, nipple exposure, "

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
    
ckpts=glob.glob(
    os.path.join(
        os.path.dirname(__file__),
        "..\\models\\checkpoints"
    )+"\\*-fp16.safetensors"
)

prompt_add(
    "CheckpointLoaderSimple",
    "CheckpointLoaderSimple",
    {
        "ckpt_name": "weriDiffusion_v10-fp16.safetensors"
    }
)

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
        "clip" : [names["LoraLoader"],1],
        "text": quality+dress+NSFW
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
        "model": [names["LoraLoader"],0],
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

chars={ 
    "diana" : {
        "prompt" : "diana cavendish, long wavy hair, multicolored two-tone streaked hair, light green hair, light blonde hair, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : "dianaCavendishLittle_v11ClothesFix.safetensors"
    },
    "schnee" : {
        "prompt" : "weiss schnee, white long hair, bangs, hair between eye, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,",
        "lora" : ["weissSchneeRWBY_weissSchneeV10.safetensors","weissSchneeLORA_weissSchnee.safetensors"]
    },

}

for i in range(1):

    prompt[names["CheckpointLoaderSimple"]]["inputs"]["ckpt_name"] = os.path.basename(random.choice(ckpts))
    prompt[names["SaveImage"]]["inputs"]["filename_prefix"] = os.path.splitext(prompt[names["CheckpointLoaderSimple"]]["inputs"]["ckpt_name"])[0]
    
    for j in range(1):

        for c  in chars:
            
            if "prompt" in chars[c]: 
                #print("prompt" , chars[c]["prompt"])
                prompt[names["CLIPTextEncodeP"]]["inputs"]["text"] = quality+chars[c]["prompt"]+dress+NSFW
            else:
                #print(f"prompt no {c}")
                prompt[names["CLIPTextEncodeP"]]["inputs"]["text"] = quality+dress+NSFW
                
            if "lora" in chars[c]: 
                
                print("lora" , type(chars[c]["lora"]))
                if type(chars[c]["lora"]) is list :
                    #print("lora1" , random.choice(chars[c]["lora"]))
                    prompt[names["LoraLoader"]]["inputs"]["lora_name"] = random.choice(chars[c]["lora"])
                else:
                    #print("lora2" , (chars[c]["lora"]))
                    prompt[names["LoraLoader"]]["inputs"]["lora_name"] = chars[c]["lora"]
                prompt[names["LoraLoader"]]["inputs"]["strength_model"] =  random.uniform(0.5,1.0) 
                prompt[names["KSampler"]]["inputs"]["model"] =  [names["LoraLoader"],0]
                prompt[names["CLIPTextEncodeP"]]["inputs"]["clip"] =  [names["LoraLoader"],1]
            else:
                #print(f"lora no {c}")
                prompt[names["KSampler"]]["inputs"]["model"] =  [names["CheckpointLoaderSimple"],0]
                prompt[names["CLIPTextEncodeP"]]["inputs"]["clip"] =  [names["CheckpointLoaderSimple"],1]
                
            prompt[names["KSampler"]]["inputs"]["seed"] =  random.randint(0, 0xffffffffffffffff )
            prompt[names["KSampler"]]["inputs"]["steps"] =  random.randint(20, 30 )
            prompt[names["KSampler"]]["inputs"]["cfg"] =  random.randint( int(5*2) , int(9*2) ) / 2
            prompt[names["KSampler"]]["inputs"]["denoise"] =  random.uniform(0.5,1.0) 
            
            #print(prompt)
            
            #continue
            
            queue_prompt(prompt)