import json
from urllib import request, parse
import random
import os, glob

#this is the ComfyUI api prompt format. If you want it for a specific workflow you can copy it from the prompt section
#of the image metadata of images generated with ComfyUI
#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow
prompt_text = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 8566257,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "weriDiffusion_v10-fp16.safetensors"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "masterpiece best quality girl"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "bad hands"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "10",
                0
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    },
    "10": {
        "class_type": "VAELoader",
        "inputs": {
            "vae_name": "BerrysMix.vae.safetensors"
        }
    },
    "11": {
        "class_type": "LoraLoader",
        "inputs": {
            "model" : [
                "4",0
            ],
            "clip" : [
                "4",1
            ],
            "lora_name": "dianaCavendishLittle_v11ClothesFix.safetensors"
        }
    }
}
"""

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)

prompt = json.loads(prompt_text)

prompt["3"]["inputs"]["seed"] =  random.randint(0, 0xffffffffffffffff )
prompt["3"]["inputs"]["steps"] =  random.randint(20, 30 )
prompt["3"]["inputs"]["cfg"] =  random.randint( int(5*2) , int(9*2) ) / 2
prompt["3"]["inputs"]["denoise"] =  random.uniform(0.5,1.0) 
prompt["5"]["inputs"]["height"] =  768
prompt["5"]["inputs"]["width"] =  320
prompt["6"]["inputs"]["text"] = """
masterpiece, best quality, 
diana cavendish, long wavy hair, multicolored two-tone streaked hair, light green hair, light blonde hair, {sharp eyes, sharply eyelashes, sharply eyeliner,| } small breasts,
{sweater|maid|princess royal|santa|lolita fashion|china|witch|wedding|{yukata|kimono}} {frilled |}{long |}dress, {{puffy | }{wide | }{long | }sleeves,| } high heels,
off shoulder, bare shoulders, Strapless,
NSFW, breasts exposure, breastsout, nipple exposure, 
"""
prompt["7"]["inputs"]["text"] = "worst quality, low quality, bad hands, extra arms, extra legs,"
prompt["4"]["inputs"]["ckpt_name"] = "macaronMix_v10-fp16.safetensors"

file_list=glob.glob(
    os.path.join(
        os.path.dirname(__file__),
        "..\\models\\checkpoints"
    )+"\\*-fp16.safetensors"
)

for i in range(3):
    prompt["4"]["inputs"]["ckpt_name"] = os.path.basename(random.choice(file_list))
    for j in range(3):
        prompt["3"]["inputs"]["seed"] =  random.randint(0, 0xffffffffffffffff )
        prompt["3"]["inputs"]["steps"] =  random.randint(20, 30 )
        prompt["3"]["inputs"]["cfg"] =  random.randint( int(5*2) , int(9*2) ) / 2
        prompt["3"]["inputs"]["denoise"] =  random.uniform(0.5,1.0) 
        queue_prompt(prompt)





