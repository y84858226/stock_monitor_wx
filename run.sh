#!/bin/bash

# 定义服务的名称和日志文件路径
SERVICE_NAME="app.py"
LOG_FILE="server.log"

# 检查是否有相同的服务已经在运行
PID=$(pgrep -f "$SERVICE_NAME")

if [ -n "$PID" ]; then
    echo "服务 $SERVICE_NAME 已经在运行，PID: $PID。正在尝试停止..."
    kill -9 "$PID"  # 强制终止进程
    echo "服务已停止。"
    sleep 2  # 等待2秒，确保进程已经停止
fi

# 启动服务
echo "正在启动服务 $SERVICE_NAME..."
nohup python "$SERVICE_NAME" > "$LOG_FILE" 2>&1 &
echo "服务已启动，日志文件：$LOG_FILE"

