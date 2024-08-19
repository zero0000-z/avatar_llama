"""
Adapted from: https://github.com/Vision-CAIR/MiniGPT-4/blob/main/demo.py
Run the data differently by animal
"""
import argparse
import re
import os
import json
import random
import datetime

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import gradio as gr

from video_llama.common.config import Config
from video_llama.common.dist_utils import get_rank
from video_llama.common.registry import registry
from video_llama.conversation.conversation_video import Chat, Conversation, default_conversation,SeparatorStyle,conv_llava_llama_2
import decord
decord.bridge.set_bridge('torch')

#%%
# imports modules for registration
from video_llama.datasets.builders import *
from video_llama.models import *
from video_llama.processors import *
from video_llama.runners import *
from video_llama.tasks import *

import torch

#device_count = torch.cuda.device_count()
#device = torch.device("cuda:1" if device_count > 0 else "cpu")


#os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
#os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

#%%
def parse_args():
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument("--cfg-path", required=True, help="path to configuration file.")
    parser.add_argument("--gpu-id", type=int, default=0, help="specify the gpu to load the model.")
    parser.add_argument("--model_type", type=str, default='vicuna', help="The type of LLM")
    parser.add_argument("--video_root", type=str, help="The root of video which is .mp4")
    parser.add_argument("--animal_name", type=str, help="Folder name, aka animal name")
    parser.add_argument(
        "--options",
        nargs="+",
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file (deprecate), "
        "change to --cfg-options instead.",
    )
    args = parser.parse_args()
    return args


def setup_seeds(config):
    seed = config.run_cfg.seed + get_rank()

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    cudnn.benchmark = False
    cudnn.deterministic = True

def delmotion(motion):
    #除去文件不要的部分
    if len(re.findall('[A-Z][^A-Z]*', motion.split("-")[-1])):
        line = " ".join(re.findall('[A-Z][^A-Z]*', motion.split("-")[-1]))
    else:
        if len(motion.split("-")[-1])>0:
            line= motion.split("-")[-1]
        else:
            line=""
    return line

def delmotion2(motion):
    #除去不要的部分

    mot = re.split('/', motion)[-1].split('.')[0]
    mot = mot.split('_')[0]
    mot = mot.split('-')
    return mot

# ========================================
#             Model Initialization
# ========================================

print('Initializing Chat')
args = parse_args()
cfg = Config(args)

model_config = cfg.model_cfg
model_config.device_8bit = args.gpu_id
model_cls = registry.get_model_class(model_config.arch)
# model = model_cls.from_config(model_config).to('cpu')
model = model_cls.from_config(model_config).to('cuda:{}'.format(args.gpu_id))
model.eval()
vis_processor_cfg = cfg.datasets_cfg.webvid.vis_processor.train
vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)
#chat = Chat(model, vis_processor, device='cpu')
chat = Chat(model, vis_processor, device='cuda:{}'.format(args.gpu_id))
print('Initialization Finished')

# ========================================
#             Gradio Setting
# ========================================

def gradio_reset(chat_state, img_list):
    if chat_state is not None:
        chat_state.messages = []
    if img_list is not None:
        img_list = []
    return None, gr.update(value=None, interactive=True), gr.update(value=None, interactive=True), gr.update(placeholder='Please upload your video first', interactive=False),gr.update(value="Upload & Start Chat", interactive=True), chat_state, img_list

def upload_imgorvideo(gr_video, gr_img, text_input, chat_state):
    if args.model_type == 'vicuna':
        chat_state = default_conversation.copy()
    else:
        chat_state = conv_llava_llama_2.copy()
    if gr_img is None and gr_video is None:
        return chat_state, None
    elif gr_img is not None and gr_video is None:
        # print(gr_img)
       # chatbot = chatbot + [((gr_img,), None)]
        chat_state.system =  "You are able to understand the visual content that the user provides. Follow the instructions carefully and explain your answers in detail."
        img_list = []
        llm_message = chat.upload_img(gr_img, chat_state, img_list)
        return  chat_state, img_list
    elif gr_video is not None and gr_img is None:
        print(gr_video)
       # chatbot = chatbot + [((gr_video,), None)]
        chat_state.system =  "You are able to understand the visual content that the user provides. Follow the instructions carefully and explain your answers in detail."
        img_list = []
        llm_message = chat.upload_video_without_audio(gr_video, chat_state, img_list)
        return  chat_state, img_list
    else:
        # img_list = []
        return  chat_state, None

def gradio_ask(user_message,  chat_state):
    if len(user_message) == 0:
        return 'Input should not be empty!', chat_state
    chat.ask(user_message, chat_state)
 #   chatbot = chatbot + [[user_message, None]]
    return '',  chat_state


def gradio_answer( chat_state, img_list, num_beams, temperature):
    llm_message = chat.answer(conv=chat_state,
                              img_list=img_list,
                              num_beams=num_beams,
                              temperature=temperature,
                              max_new_tokens=300,
                              max_length=2000)[0]
 #   chatbot[-1][1] = llm_message
    # print(chat_state.get_prompt())
    # print(chat_state)
    return llm_message, chat_state, img_list


def read_json(file_path):
    '''
    get json data
    '''
    with open(file_path, "r",encoding="utf-8") as f:
        data= json.load(f)
    return data


def write_json(data, file_path):
    '''
    write json data
    '''
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def get_mp4_files(directory):
    mp4_files = []
    for root, dirs, files in os.walk(directory):
        first_mp4_found = False
        mp4s_in_dir = [file for file in files if file.endswith('.mp4')  and not 'input' in file and not 'sample' in file]
        if mp4s_in_dir:
            for mp4 in mp4s_in_dir:
            # Only add one mp4 file per directory
                mp4_files.append(os.path.join(root, mp4))
            # break  # Only take the first .mp4 file in each subfolder
        # if first_mp4_found:
        #     break  # Once a .mp4 file is found in the current folder, skip to next folder
    return mp4_files




def generate_content(templete_require, video_path):
    '''
    using llama model, mainly generate content
    and use order templete to design content
    '''
    #lima dataset, Read line by line
    chat_state = None

    temp_data= {
    "label": templete_require,
    "predict": [],
    "video_path":video_path
    }
    text_input = templete_require

    chat_state, img_list = upload_imgorvideo(video_path, image, text_input, chat_state)
    message,  chat_state = gradio_ask(text_input, chat_state)
    llm_message,chat_state, img_list=gradio_answer( chat_state, img_list, num_beams, temperature)
    chat_state=chat_state.dict()
    # print("test------", chat_state)
    chat_message = chat_state["messages"]

    for message in chat_message:
        if args.model_type == "vicuna":
            if "Human" in message[0] :
                print(message[0],": ",message[1])
            elif "Assistant" in message[0]:
                # print(message[0],": ",message[1])
                message = message[1]
                temp_data['predict']=message
        else:
            if "USER" in message[0] :
                print(message[0],": ",message[1])
            elif "ASSISTANT" in message[0]:
                # print(message[0],": ",message[1])
                message = message[1]
                temp_data['predict']=message
    return temp_data

def get_filepath(folder_path):
    path_list = []
    for file in os.listdir(folder_path):
        path_list.append(os.path.join(folder_path, file))
    return path_list

import time
#TODO show examples below
num_beams = 1
temperature=0.1
output = "output/"

# question = input('please choice 1.only one video generate, 2.many videos generate and give path')
question = 2
video_path_root = args.video_root
animal_name = args.animal_name
# print(video_path_root)
image = None

# 获取当前日期和时间
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")


# templete of prompt 
input_sentence_file = "templete.txt"


#get templete : 生成文本的指令
input_sentence =[]
with open(input_sentence_file) as f:
    for line in f.readlines():
        input_sentence.append(line)
input_sentence_1 = [line.lstrip() for line in "".join(input_sentence).split('---')]



filelist = get_mp4_files(video_path_root)

data_all = []
count = 0
for file_path in filelist[:]:
    #get video label
    print('read file-------',file_path)
    video_lable = delmotion2(file_path)
    
    for input_sentence in input_sentence_1[:1]:
        #获取视频标签
        instruction= input_sentence.format(' '.join(video_lable))
        try:
            data = generate_content(instruction, video_path=file_path)
            data_all.append(data)
            # data_all.append(file_path)
            count +=1
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



# 格式化日期和时间为 "YYYYMMDD_HHMMSS" 格式
#创建子文件夹放入数据
timestamp = now.strftime("%Y%m%d_%H%M%S")
date = datetime.datetime.now().strftime("%Y%m")
output_path = os.path.join(output, "output_"+date)
if not os.path.exists(output_path):
    os.makedirs(output_path)
    
#写入结果
print('spending time is :', (datetime.datetime.now() - now)/count)
# exists_create_file(output_path)
output_file = f"{output_path}/{animal_name}_{timestamp}_llama13B.txt"
# output + "/" + animal_name + "_llama13B.json"
write_json(data_all, output_file)
print('finish ------------',animal_name,'&',output_file)











