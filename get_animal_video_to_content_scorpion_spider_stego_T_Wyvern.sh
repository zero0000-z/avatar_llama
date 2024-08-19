#!/bin/bash

# 设置主目录路径
#main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"
main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"





python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/TUKANALL" --animal_name "TUKANALL"

wait

# 监控GPU内存使用
echo "Checking GPU memory usage..."
while true; do
    memory_used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    if [ "$memory_used" -lt 1000 ]; then  # 设置合适的内存使用阈值
        break
    fi
    echo "Waiting for GPU memory to clear..."
    sleep 60  # 等待一段时间后再检查
done

# 可以在这里添加延迟，确保内存清理充分
sleep 30


python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Turtle" --animal_name "Turtle"

wait

# 监控GPU内存使用
echo "Checking GPU memory usage..."
while true; do
    memory_used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    if [ "$memory_used" -lt 1000 ]; then  # 设置合适的内存使用阈值
        break
    fi
    echo "Waiting for GPU memory to clear..."
    sleep 60  # 等待一段时间后再检查
done

# 可以在这里添加延迟，确保内存清理充分
sleep 30


python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Tyranno" --animal_name "Tyranno"

wait

# 监控GPU内存使用
echo "Checking GPU memory usage..."
while true; do
    memory_used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    if [ "$memory_used" -lt 1000 ]; then  # 设置合适的内存使用阈值
        break
    fi
    echo "Waiting for GPU memory to clear..."
    sleep 60  # 等待一段时间后再检查
done

# 可以在这里添加延迟，确保内存清理充分
sleep 30

