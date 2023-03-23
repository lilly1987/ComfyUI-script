import os, glob, sys
import json
from urllib import request, parse
import random
import copy
import time
import types
import traceback
import os
if __name__ == os.path.splitext(os.path.basename(__file__))[0] or __name__ =='__main__':
    from ConsoleColor import print, console
else:
    from .ConsoleColor import print, console
#print(__file__)
#print(os.path.basename(__file__))
from rich.progress import Progress,Console
#----------------------------
"""
This script is written under the premise of using my own node.
https://github.com/lilly1987/ComfyUI_node_Lilly
"""
#----------------------------
# wildcards support check
wildcardsOn=False
#print(f"PromptClass __name__ {__name__}")
try:
    if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
        from wildcards import wildcards 
    else:
        from .wildcards import wildcards 
    wildcardsOn=True
    #wildcards.card_path=os.path.dirname(__file__)+"\\..\\wildcards\\**\\*.txt"
    print("import wildcards succ")
except Exception as e:     
    print(f"import wildcards fail ", e)
    err_msg = traceback.format_exc()
    print(err_msg)
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
print(f"[cyan]ckpts cnt : [/cyan]{len(ckptnms)}")
print(f"[cyan]ckpts dat : [/cyan]{ckptnm}")
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

print(f"[cyan]loras cnt : [/cyan]{len(loranms)}")
print(f"[cyan]loras dat : [/cyan]{loranm}")
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

print(f"[cyan]vaes cnt : [/cyan]{len(vae_names)}")
print(f"[cyan]vaes dat : [/cyan]{vae_names}")

#----------------------------
# global static



#----------------------------

def lget(a):
    return random.choice(a) if type(a) is list else a

def cadd(c,v,t):
    c[v]=c[v]+t if v in c else t
    return c[v]
    
def caddin(c,v,t):
    
    if v in c:
        #print(f"t c[v] : {c[v]}")
        if t in c[v]:
            #print(f"r c[v]")
            return
        c[v]+=t
    else:
        #print(f"c : {c}")
        #print(f"e c    : {c}")
        c[v]=t
        return c[v]
    
def cget(c,v,t):
    #print("c",type(c),c)
    #print("v",type(v),v)
    #print("t",type(t),t)
    p=c[v] if v in c else t
    #print("p",type(p),p)
    l=lget(p)
    #print("l",type(l),l)
    return l
    
#----------------------------
# sand to api
# max : wait max queue
def queue_prompt(prompt, max=1):
    try:
        with Progress() as progress:
            
            #progress.update(task, completed =60)
            while True:
                if progress.finished:
                    task = progress.add_task("waiting", total=60)
                req =  request.Request("http://127.0.0.1:8188/prompt")        
                response=request.urlopen(req) 
                #with request.urlopen(req) as response:
                html = response.read().decode("utf-8")            
                #print(type(html))
                ld=json.loads(html)
                #print(f"data : {data}" )
                cnt=ld['exec_info']['queue_remaining']
                
                if cnt <max:
                    progress.stop()
                    break
                    f+=0.1
                progress.update(task, advance=1)

                #print(f"wait queue cnt. now {cnt} < max {max}" )
                time.sleep(1)
                
            p = {"prompt": prompt}
            data = json.dumps(p).encode('utf-8')
            req =  request.Request("http://127.0.0.1:8188/prompt", data=data)

        request.urlopen(req)
        print(f"send" )
    except Exception as e:     
        console.print_exception()
        #print(traceback.format_exc())
        #traceback.format_exc()
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
    vae_name="Anything-V3.0.vae.safetensors"

    #----------------------------
    positivenames=[
            "quality"  ,
            "char"     ,
            "dress"    ,
            "shoulder" ,
            "acc"      ,
            "NSFW"     ,
            "body"     ,
            "pose"     ,
            "focus"    ,
            "style"    ,
    ]
    quality="masterpiece, best quality, clear details, detailed beautiful face, ultra-detailed,detailed face,"
    char="long hair, sharp eyes, sharply eyelashes, sharply eyeliner, small breasts,"
    dress="dress,"
    shoulder="off shoulder, bare shoulders, Strapless,"
    acc="{acc,|}"
    NSFW="NSFW, (breastsout, breasts exposure, nipple exposure:1.2),"
    body="small breasts, slender, nature, curvy,"
    pose=""
    focus=""
    style=""
    negative="worst quality, low quality, bad hands, extra arms, extra legs, multiple viewer, grayscale, multiple views, monochrome , swimsuit,"
    positive=eval(f"{'+'.join(positivenames)}")    
    #quality + char + dress + shoulder + NSFW + acc + pose+ focus + body+ style
    print("positive : ",positive)
    #----------------------------
    def pget(self,name,input):        
        #print(self.prompts[self.names[name]]["inputs"])
        return self.prompts[self.names[name]]["inputs"][input]
        
    def pset(self,name,input,value):
        #print(f"pset : ", name,input,value)
        #print(f"pset : {self.names[name]}")
        #print(f"pset : {self.prompts[self.names[name]]['inputs']}")
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
        #print(f"padd : {name}" )
        #print(f"padd : {self.names}" )
        
    #----------------------------
    
    
    
    def LoraLoaderT(self,name):
        return [
        "LoraLoaderText",
        {
            "model" : [self.loraModelLast,0],
            "clip"  : [self.loraClipLast ,1],
            "lora_name": name,
            "strength_model": random.uniform(0.5,1.0),
            "strength_clip" : random.uniform(0.5,1.0),
        }    ]
        
    def LoraLoaderR(self,name):
        return [
        "LoraLoaderTextRandom",
        {
            "model" : [self.loraModelLast,0],
            "clip"  : [self.loraClipLast ,1],
            "lora_name": name,
            "seed": random.randint(0, 0xffffffffffffffff ),
            "strength_model_min": 0.50,
            "strength_model_max": 1.00,
            "strength_clip_min" : 0.50,
            "strength_clip_max" : 1.00
        }]
        
    def lora_addc(self,c=None):
        if not c:
            c=self.c
        if not type(c) is dict:
            print("prompt_set error. not dict")
            return None
            
        #print(f"lora_addc1 : " , c )
        if "lora" in c: 
            r=self.lora_add(lget(c["lora"]))        
            #print(f"lora_addc2 : " , r )
            
        if "loraList" in c: 
            for lora in c["loraList"]:
                r=self.lora_add(lget(lora))
                #print(f"lora_addc3 : " , r )
                
    def lora_add(self, name):
        #print(f"lora_add1 : ",name , self.loratag)
        if not name in self.loratag:
        
            #n=f"{name}_{self.loraModelLast}_{self.loraClipLast}"
            t=self.LoraLoader(name)
            self.padd(
                name,
                t[0],
                t[1]
            )
            
            self.loraModelLast=self.names[name]
            self.loraClipLast =self.names[name]
            self.lora_add_after()
        
            #self.loratag[name]+=[n]
            self.loratag[name]=name
        #else:
        
        #print(f"loratag[{name}] : {self.loratag[name]}")
        #print(f"lora_add2 : ",name , self.loratag)
        return self.loratag[name]
        
    def lora_add_after(self):
        self.pset("KSampler"        , "model", [self.loraModelLast,0])
        self.pset("CLIPTextEncodeN" , "clip" , [self.loraClipLast ,1])
        self.pset("CLIPTextEncodeP" , "clip" , [self.loraClipLast ,1])

    def lora_set(self,key,value):#,index=0
        #print("lora_set : " , key,value)
        if not 'lora' in self.c:
            return
        
        if type(self.c['lora']) is list:
            for l in self.c['lora']:
                if l in self.loratag:
                    self.pset(self.loratag[l],key,value)
        else:
            #print(self.c['lora'])
            #print(self.loratag)
            #print(self.loratag[self.c['lora']][index])
            self.pset(self.loratag[self.c['lora']],key,value)



    #----------------------------
    def caddin(self,v,t):
        #print(f"---" )
        #print(f"caddin : {t}" )
        #print(f"self.c : {self.c}" )
        caddin(self.c,v,t)
        #print(f"self.c : {self.c}" )
        #print(f"---" )

    #----------------------------
    def promptGet(self,c=None):
        
        #print(f"dict : {c}" )
        if not c:
            c=self.c
        if not type(c) is dict:
            print("prompt_set error. not dict")
            return None
        #print("c : ", c)
            
        #print(f"promptSet : {c}" )
        tmp=""
        
        #--------------------------------
        tmp=""
        r={}
        if "positive" in c:        
            r["positive"]=lambda c: cget(c,"positive" ,self.positive)
        else:
            #print("self.quality:",type(self.quality),self.quality)
            for positivename in PromptClass.positivenames:
                #eval(f"{'+'.join(positivenames)}")  
                po=eval(f"self.{positivename}")
                #print("po : ", po)
                r[positivename]=cget(c,positivename ,po)
            
            #r["quality" ]=lambda c: cget(c,"quality" ,self.quality)
            #r["char"    ]=lambda c: cget(c,"char"    ,self.char)
            #r["dress"   ]=lambda c: cget(c,"dress"   ,self.dress)
            #r["shoulder"]=lambda c: cget(c,"shoulder",self.shoulder)
            #r["acc"     ]=lambda c: cget(c,"acc"     ,self.acc)
            #r["NSFW"    ]=lambda c: cget(c,"NSFW"    ,self.NSFW)
            #r["focus"   ]=lambda c: cget(c,"focus"   ,self.focus)
            #r["pose"    ]=lambda c: cget(c,"pose"    ,self.pose)
            #r["body"    ]=lambda c: cget(c,"body"    ,self.body)
            #r["style"   ]=lambda c: cget(c,"style"   ,self.style)
        
        r["NSFW_add" ]=cget(c,"NSFW_add" ,"")
        r["style_add"]=cget(c,"style_add","")
        
        #print(f"NSFW_add : "+cget(c,"NSFW_add",""))
        random.shuffle([list(r.keys())])
        for f in r:
            #print("f",f)
            #if type(r[f]) is types.FunctionType:
            #    t=f(c)
            #else:
            #    t=f
            #print("promptGet t : ", t)
            #tmp+=lget(t)
            #t=r[f](c)
            #print(type(f))
            #print(type(r[f]))
            #print(f"f,t : ",f ," ; ",t)
            #print("r[f]",r[f])
            tmp+=r[f]
        #print(f"positive : {tmp}")
        if wildcardsOn:
            tmp=wildcards.run(tmp)
        #print(f"positive : {tmp}")
        self.pset("CLIPTextEncodeP","text", tmp)
        #--------------------------------
        if "negative" in c:
            tmp=c["negative"]
        else:
            tmp=self.pget("CLIPTextEncodeN","text")
        #print(f"negative : ",tmp)
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
            
        return self.prompts
        """
    def promptSet(self,c=None):
        if not c:
            c=self.c
        if not type(c) is dict:
            print("prompt_set error. not dict")
            return None
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
        #print()
        #print(f"promptSet : {self.prompts}")
        #print()
        return self.prompts
        """
    #print(f"ckpts {ckptnms}")
    def __init__(self,c):
        #print(f"__init__ ")
        #global ckptnm
        self.c=copy.deepcopy(c)
        
        self.prompts={}
        self.names={}
        
        self.loratag={}
        self.LoraLoader=self.LoraLoaderT
        
        self.ckptnm=PromptClass.ckptnm
        self.vae_name=PromptClass.vae_name

        self.positive=PromptClass.positive
        self.negative=PromptClass.negative
        
        for positivename in PromptClass.positivenames:
            exec(f"self.{positivename}=PromptClass.{positivename}")
        
        self.padd(
            "CheckpointLoaderSimple",
            "CheckpointLoaderSimpleText",
            {
                "ckpt_name": self.ckptnm
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
                "text": self.positive
            }
        )

        self.padd(
            
            "CLIPTextEncodeN",
            "CLIPTextEncodeWildcards",
            {
                "clip" : [self.loraClipLast,1],
                "text": self.negative
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
            "SaveImageSimple",
            {
                "images": [self.names["VAEDecode"],0],
                "filename_prefix": os.path.splitext(
                    self.pget("CheckpointLoaderSimple","ckpt_name")
                )[0]
                #+"-"+str(random.randint(0, 0xffffffffffffffff )),
            }
        )
        
        self.lora_addc()
        #self.cpromptSet(self.c)
        #print( f"self.prompts {self.prompts}")
        #print( f"self.names {self.names}")
    #print(names)
    #print(prompt)
