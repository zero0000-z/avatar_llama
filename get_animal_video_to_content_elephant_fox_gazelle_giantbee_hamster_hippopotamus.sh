#!/bin/bash

# 设置主目录路径
#main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"
main_directory="/code/Video-LLaMA-main/data/zoo_300k/zoo_300k/zoo_300k"



# 运行每个动物的子目录


python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Crab" --animal_name "Crab"

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



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Cricket" --animal_name "Cricket"

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



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Fire_ant" --animal_name "Fire_ant"

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




python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Giantbee" --animal_name "Giantbee"

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



python chat_videoV2.py  --cfg-path "eval_configs/video_llama_eval_only_vl.yaml"  --model_type "llama_v2"  --gpu-id 0  --video_root "${main_directory}/Goat" --animal_name "Goat"


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


