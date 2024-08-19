#!/bin/bash

# 设置主目录路径
#main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"
main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Mammoth" --animal_name "Mammoth"


sleep 7h



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Ostrich" --animal_name "Ostrich"

# 可以在这里添加延迟，确保内存清理充分
sleep 6h



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Piranna" --animal_name "Piranna"
# 可以在这里添加延迟，确保内存清理充分
sleep 6h



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Raptor" --animal_name "Raptor"
# 可以在这里添加延迟，确保内存清理充分
sleep 6h



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Rat" --animal_name "Rat"


