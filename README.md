# Flask网站项目

这是一个使用Flask框架构建的基础网站项目。

## 环境要求

- Python 3.8+
- pip（Python包管理器）

## 安装步骤

1. 创建虚拟环境（推荐）：
```bash
python -m venv venv
```

2. 激活虚拟环境：
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行项目

1. 确保已激活虚拟环境
2. 运行以下命令：
```bash
python app.py
```
3. 在浏览器中访问：http://127.0.0.1:5000

## 项目结构

```
.
├── app.py              # 主应用文件
├── requirements.txt    # 项目依赖
├── templates/         # HTML模板目录
│   └── index.html    # 主页模板
└── README.md          # 项目说明文档
``` 