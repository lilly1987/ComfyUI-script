import os, glob, sys
import json
from urllib import request, parse
import random
import copy
import time

#----------------------------
"""
This script is written under the premise of using my own node.
https://github.com/lilly1987/ComfyUI_node_Lilly
"""
#----------------------------
# wildcards support check
wildcardsOn=False
try:
    import wildcards
    wildcardsOn=True
    #wildcards.card_path=os.path.dirname(__file__)+"\\..\\wildcards\\**\\*.txt"
    print("import wildcards succ")
except:
    print("import wildcards fail")
    wildcardsOn=False
    
#----------------------------
# F:\WEBUI\ComfyUI_windows_portable\ComfyUI\models\checkpoints\*.safetensors
ckpts_path=os.path.join( 
    os.path.dirname(__file__),
    "..\\..\\models\\checkpoints\\*fp16.safetensors"
)    
ckpts=glob.glob(ckpts_path)
# F:\WEBUI\ComfyUI_windows_portable\ComfyUI\models\checkpoints\artistKidmo_v10.safetensors
# If want sub folder change to
"""
ckpts_path=os.path.join( 
        os.path.dirname(__file__),
        "..\\..\\models\\checkpoints"
    )+"\\**\\*fp16.safetensors"
ckpts=glob.glob(ckpts_path,recursive=True)
"""
ckptnms=[os.path.basename(ckpt) for ckpt in ckpts] # file name list
ckptnm=random.choice(ckptnms)
print(f"ckpts cnt : {len(ckptnms)}")
print(f"ckpts dat : {ckptnms[0]}")
if len(ckptnms) ==0 :
    print(f"!!!!!!!!!! ckpts cnt 0 !!!!!!!!!!!!!")
    quit()
#----------------------------
loras_path=os.path.join(
    os.path.dirname(__file__),
    "..\\..\\models\\loras\\*.safetensors"
)
loras=glob.glob(loras_path)
"""
loras_path=os.path.join(
        os.path.dirname(__file__),
        "..\\..\\models\\loras"
    )+"\\**\\*.safetensors"
loras=glob.glob(loras_path,recursive=True)
"""
loranms=[os.path.basename(lora) for lora in loras]
loranm=random.choice(loranms)

print(f"loras cnt : {len(loranms)}")
print(f"loras dat : {loranms[0]}")
#----------------------------
vaes_path=os.path.join(
    os.path.dirname(__file__),
    "..\\..\\models\\VAE\\*.safetensors"
)
vaes=glob.glob(vaes_path)
"""
vaes_path=os.path.join(
        os.path.dirname(__file__),
        "..\\..\\models\\VAE\\**\\*.safetensors"
    )
vaes=glob.glob(vaes_path,recursive=True)
"""
vae_names=[os.path.basename(vae) for vae in vaes]
vae_name=random.choice(vae_names)

print(f"loras cnt : {len(loranms)}")
print(f"loras dat : {loranms[0]}")

#----------------------------
# global static
shoulder="off shoulder, bare shoulders, Strapless,"
quality="masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,"
dress="dress,"
acc="{acc,|}"
NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:1.2),"
char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, small breasts,"
negative="worst quality, low quality, bad hands, extra arms, extra legs, multiple viewer, grayscale, multiple views, monochrome , swimsuit,"
focus=""
pose=""
positive=quality + char + dress + shoulder + NSFW + acc + pose+ focus


#----------------------------

def lget(a):
    return random.choice(a) if type(a) is list else a

def cadd(c,v,t):
    c[v]=c[v]+t if v in c else t
    return c[v]
    
def caddin(c,v,t):
    
    if v in c:
        #print(f"c[v] : {c[v]}")
        if t in c[v]:
            return
        c[v]+=c[v]+t
    else:
        #print(f"c : {c}")
        #print(f"c[v] : {c[v]}")
        c[v]=t
        return c[v]
    
def cget(c,v,t):
    p=c[v] if v in c else t
    return lget(p)
    
#----------------------------
# sand to api
# max : wait max queue
def queue_prompt(prompt, max=1):
    
    while True:
        req =  request.Request("http://127.0.0.1:8188/prompt")        
        with request.urlopen(req) as response:
            html = response.read().decode("utf-8")            
            #print(type(html))
            ld=json.loads(html)
            #print(f"data : {data}" )
            cnt=ld['exec_info']['queue_remaining']
            
            if cnt <max:
                break
            print(f"wait queue cnt. now {cnt} < max {max}" )
            time.sleep(2)
        
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)
    print(f"send" )
    time.sleep(2)

#----------------------------
"""
        - hou to use
            PromptClass.ckptnm="VIC-BACLA-MIX-V1-fp16"
            m=PromptClass(
                {
                    "positive" : "__my__",
                    #"negative" : "__no2d__",
                    "lora" : "IrisPokemon_v10"
                }
            )  
            nm=m.lora_add("hunged_girl")
            m.pset(nm,"strength_model_min",0.75)
            m.pset(nm,"strength_clip_min",0.75)
            m.caddin("NSFW_add","__hunged_girl__")
            r=m.promptGet()
            print(r)
            queue_prompt(r,2)
-----------------------------------------------
    - ckptnm : static ckpt file name
        - self.c=copy.deepcopy(chars[c])
        
            node change value
            dict
            {
                key : value,
                key : value
                ...
            }
            
            - support key
            
                positive
                negative
                ckptnm
                vae_name
                lora
                loraList
                
            - if not use key positive
                - self.quality=quality
                - self.dress=dress
                - self.NSFW=NSFW
                - self.char=char
                - self.acc=acc
                - self.focus=focus
                - self.pose=pose
                - self.shoulder=shoulder
                
            - if not use key negative then use global negative
            
            
            
        - self.prompts={}
            for sand to api 
            
        - self.names={}
            { node name : node no }
            not edit self.names
            need use self.padd(node name,node type, {inputs} )
            No duplication node name 

"""
class PromptClass:

    ckptnm="weriDiffusion_v10-fp16.safetensors"

    #----------------------------
    def pget(self,name,input):        
        #print(self.prompts[self.names[name]]["inputs"])
        return self.prompts[self.names[name]]["inputs"][input]
        
    def pset(self,name,input,value):
        print(f"pset : {name}")
        print(f"pset : {self.names[name]}")
        print(f"pset : {self.prompts[self.names[name]]['inputs']}")
        if not type(self.prompts[self.names[name]]["inputs"][input]) is list :
            while type(value) is list:
                value=lget(value)
                
        self.prompts[self.names[name]]["inputs"][input] = value

    def psetd(self,name,kv):
        for k, v in kv.items():
            self.pset(name,k,v)

    def padd(self, name,class_type,inputs):
        n=f"{len(self.names.keys())}"
        self.names[name]=n
        self.prompts[n]={
            "class_type":class_type,
            "inputs":inputs
        }
        print(f"padd : {name}" )
        print(f"padd : {self.names}" )
        
    #----------------------------
    def lora_add(self, name):
        print(f"lora_add : {name}")
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
        return n
        
    def lora_add_after(self):
        self.pset("KSampler"        , "model", [self.loraModelLast,0])
        self.pset("CLIPTextEncodeN" , "clip" , [self.loraClipLast ,1])
        self.pset("CLIPTextEncodeP" , "clip" , [self.loraClipLast ,1])
        
    #----------------------------
    def caddin(self,v,t):
        caddin(self.c,v,t)

    #----------------------------
    def promptGet(self,c=None):
        #print(f"dict : {c}" )
        #print(type(c))
        if not c:
            c=self.c
        if not type(c) is dict:
            print("prompt_set error. not dict")
            return None
        tmp=""
        
        #--------------------------------
        if "positive" in c:
            tmp=c["positive"]
        else:
            tmp=""
            r=[]
            r.append(lambda c: cget(c,"quality",self.quality))
            r.append(lambda c: cget(c,"char",self.char))
            r.append(lambda c: cget(c,"dress",self.dress))
            r.append(lambda c: cget(c,"shoulder",self.shoulder))
            r.append(lambda c: cget(c,"acc",self.acc)  )
            r.append(lambda c: cget(c,"NSFW",self.NSFW)  )
            r.append(lambda c: cget(c,"NSFW_add","")  )
            r.append(lambda c: cget(c,"focus",self.focus)  )
            r.append(lambda c: cget(c,"pose",self.pose)  )
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
            
        if "negative_add" in c:
            tmp+=c["negative_add"]
            
        if wildcardsOn:
            tmp=wildcards.run(tmp)
        self.pset("CLIPTextEncodeN","text", tmp)
        #--------------------------------
        if "ckptnm" in c:
            self.pset("CheckpointLoaderSimple","ckpt_name", c["ckptnm"])
        #--------------------------------
        if "vae_name" in c:
            self.pset("VAELoader","vae_name", c["vae_name"])
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
        return self.prompts

    #print(f"ckpts {ckptnms}")
    def __init__(self,c):
        #print(f"__init__ ")
        self.c=copy.deepcopy(c)
        self.prompts={}
        self.names={}
        self.shoulder=shoulder
        self.quality=quality
        self.dress=dress
        self.NSFW=NSFW
        self.char=char
        self.acc=acc
        self.focus=focus
        self.pose=pose
        self.ckptnm=ckptnm
        self.vae_name=vae_name
       
        self.padd(
            "CheckpointLoaderSimple",
            "CheckpointLoaderSimpleText",
            {
                "ckpt_name": ckptnm
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
                "vae_name": vae_name
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
