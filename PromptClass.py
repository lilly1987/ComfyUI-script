import os, glob, sys
import json
from urllib import request, parse
import random
import time



wildcardsOn=False
try:
    import wildcards
    wildcardsOn=True
    #wildcards.card_path=os.path.dirname(__file__)+"\\..\\wildcards\\**\\*.txt"
    print("import wildcards succ")
except:
    print("import wildcards fail")
    wildcardsOn=False


ckpts_path=os.path.join(
        os.path.dirname(__file__),
        "..\\..\\models\\checkpoints"
    )+"\\*-fp16.safetensors"
ckpts=glob.glob(ckpts_path)
ckptnms=[os.path.basename(ckpt) for ckpt in ckpts]
print(f"ckptn cnt : {len(ckptnms)}")
if len(ckptnms) ==0 :
    print(f"!!!!!!!!!! ckptn cnt 0 !!!!!!!!!!!!!")
    

shoulder="off shoulder, bare shoulders, Strapless,"
quality="masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,"
dress="dress,"
NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:1.2),"
char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, small breasts,"
negative="worst quality, low quality, bad hands, extra arms, extra legs, multiple viewer, grayscale, multiple views, monochrome , swimsuit,"
positive=quality + char + dress + shoulder + NSFW

def lget(a):
    return random.choice(a) if type(a) is list else a

def cget(c,v,t):
    p=c[v] if v in c else t
    return lget(p)
    
def queue_prompt(prompt):
    
    while True:
        req =  request.Request("http://127.0.0.1:8188/prompt")        
        with request.urlopen(req) as response:
            html = response.read().decode("utf-8")            
            #print(type(html))
            ld=json.loads(html)
            #print(f"data : {data}" )
            cnt=ld['exec_info']['queue_remaining']
            
            if cnt <1:
                break
            print(f"wait queue cnt. now {cnt} < max 1" )
            time.sleep(2)
        
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)
    print(f"send" )
    time.sleep(2)


class PromptClass:

    ckptnm="weriDiffusion_v10-fp16.safetensors"

    def pget(self,name,input):        
        #print(self.prompts[self.names[name]]["inputs"])
        return self.prompts[self.names[name]]["inputs"][input]
        
    def pset(self,name,input,value):
        if type(self.prompts[self.names[name]]["inputs"][input]) is list :
            self.prompts[self.names[name]]["inputs"][input] = value
        else:
            self.prompts[self.names[name]]["inputs"][input] = lget(value)

    def psetd(self,name,kv):
        for k, v in kv.items():
            self.pset(name,k,v)

    def padd(self, name,class_type,inputs):
        n=f"{len(self.names.keys())}"
        #print(f"names : {n}" )
        #print(f"names : {self.names}" )
        self.names[name]=n
        self.prompts[n]={
            "class_type":class_type,
            "inputs":inputs
        }
        
    def prompt_set(self,c):
        #print(f"dict : {c}" )
        #print(type(c))
        if not type(c) is dict:
            print("prompt_set error. not dict")
            return False
        tmp=""
        
        #--------------------------------
        if "positive" in c:
            tmp=c["positive"]
        else:
            tmp+=cget(c,"quality",self.quality)
            r=[]
            r.append(lambda c: cget(c,"prompt",self.char))
            r.append(lambda c: cget(c,"dress",self.dress))
            r.append(lambda c: cget(c,"NSFW",self.NSFW)  )
            random.shuffle(r)
            for f in r:
                tmp+=f(c)
        
        if wildcardsOn:
            tmp=wildcards.run(tmp)
        self.pset("CLIPTextEncodeP","text", tmp)
        #--------------------------------
        if "negative" in c:
            tmp=c["negative"]
        else:
            tmp=self.pget("CLIPTextEncodeN","text")
            
        if wildcardsOn:
            tmp=wildcards.run(tmp)
        self.pset("CLIPTextEncodeN","text", tmp)
        #--------------------------------
        if "lora" in c: 
            self.lora_add(lget(c["lora"]))        
            
        if "loraList" in c: 
            for lora in c["loraList"]:
                self.lora_add(lget(lora))
        #--------------------------------
        #self.psetd(
        #    "KSampler",
        #    {
        #        "seed":random.randint(0, 0xffffffffffffffff ),
        #        "steps":random.randint(20, 30 ),
        #        "cfg":random.randint(int(5*2) , int(9*2) ) / 2,
        #        "denoise":random.uniform(0.75,1.0) ,
        #    }
        #)
        #--------------------------------
        #self.pset("SaveImage","filename_prefix" , 
        #    os.path.splitext(
        #        self.pget("CheckpointLoaderSimple","ckpt_name")
        #    )[0]+"-"+str(random.randint(0, 0xffffffffffffffff ))
        #)
        
    def lora_add(self, name):
        n=f"{name}_{self.loraModelLast}_{self.loraClipLast}"
        self.padd(
            n,
            "LoraLoaderTextRandom",
            {
                "model" : [self.loraModelLast,0],
                "clip"  : [self.loraClipLast ,1],
                "lora_name": name,
                "seed": random.randint(0, 0xffffffffffffffff ),
                "strength_model_min": 0.50,
                "strength_model_max": 1.0,
                "strength_clip_min": 0.50,
                "strength_clip_max": 1.0
            }
        )
        
        self.loraModelLast=self.names[n]
        self.loraClipLast =self.names[n]
        
        self.lora_add_after()
        
    def lora_add_after(self):
        self.pset("KSampler"        , "model", [self.loraModelLast,0])
        self.pset("CLIPTextEncodeN" , "clip" , [self.loraClipLast ,1])
        self.pset("CLIPTextEncodeP" , "clip" , [self.loraClipLast ,1])
        
    #print(f"ckpts {ckptnms}")
    def __init__(self):
        #print(f"__init__ ")
        
        self.prompts={}
        self.names={}
        self.shoulder=shoulder
        self.quality=quality
        self.dress=dress
        self.NSFW=NSFW
        self.char=char
       
        self.padd(
            "CheckpointLoaderSimple",
            "CheckpointLoaderSimpleText",
            {
                "ckpt_name": PromptClass.ckptnm
            }
            # model
            # clip
            # vae
        )

        self.loraModelLast=self.names["CheckpointLoaderSimple"]
        self.loraClipLast =self.names["CheckpointLoaderSimple"]

        """
        self.padd(
            
            "LoraLoaderTextRandom",
            "LoraLoaderTextRandom",
            {
                "model" : [self.names["CheckpointLoaderSimple"],0],
                "clip" : [self.names["CheckpointLoaderSimple"],1],
                "lora_name": "",
                "seed": random.randint(0, 0xffffffffffffffff ),
                "strength_model_min": 0.50,
                "strength_model_max": 1.0,
                "strength_clip_min": 0.50,
                "strength_clip_max": 1.0
            }
        )
        """
        """
        self.padd(
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

        self.padd(
            
            "CLIPTextEncodeP",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": positive
            }
        )

        self.padd(
            
            "CLIPTextEncodeN",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": negative
            }
        )

        self.padd(
            
            "EmptyLatentImage",
            "EmptyLatentImage",
            {
                "batch_size": 1,
                "height": 768,
                "width": 320
            }
        )

        self.padd(
            
            "KSampler",
            "KSampler",
            {
                "model": [self.loraModelLast,0],
                "positive": [self.names["CLIPTextEncodeP"],0],
                "negative": [self.names["CLIPTextEncodeN"],0],
                "latent_image": [self.names["EmptyLatentImage"],0],
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "seed": random.randint(0, 0xffffffffffffffff ),
                "steps": random.randint(20, 30 ),
                "cfg": random.randint( int(5*2) , int(9*2) ) / 2,
                "denoise": random.uniform(0.75,1.0) ,
            }
        )

        self.padd(
            
            "VAELoader",
            "VAELoader",
            {
                "vae_name": "BerrysMix.vae.safetensors"
            }
        )

        self.padd(
            
            "VAEDecode",
            "VAEDecode",
            {
                "samples": [self.names["KSampler"],0],
                "vae": [self.names["VAELoader"],0],
            }
        )

        self.padd(
            
            "SaveImage",
            "SaveImage",
            {
                "images": [self.names["VAEDecode"],0],
                "filename_prefix": os.path.splitext(
                    self.pget("CheckpointLoaderSimple","ckpt_name")
                )[0]+"-"+str(random.randint(0, 0xffffffffffffffff )),
            }
        )
        #print( f"self.prompts {self.prompts}")
        #print( f"self.names {self.names}")
    #print(names)
    #print(prompt)
