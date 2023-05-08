# FaceGenSeg

FaceGenSeg 是个整合了面部侦测，性别识别, 和面部遮罩的工具 

## 环境配置

### Windows（测试环境Windows 11）
1. Nvidia显卡，驱动版本515以上

2. 安装Cuda 11.7

3. 安装 python 3.10.6

    https://www.python.org/downloads/windows/

### Linux (测试环境Ubuntu22.04)

1. 安装 python 3.10.6

    ```bash
    sudo apt-get install python-is-python3 -y
    ```
2. 安装 pip (测试版本22.0.2)

    ```bash
    sudo apt install python3-pip
    ```

3. 安装 venv package

    ```bash
    sudo apt install python3.10-venv
    ```

4. 复制或者下载本Repo并在目录下打开终端

5. 运行虚拟环境设置脚本

    ```bash
    bash setup.sh
    ```
## 使用


1. ### 启动虚拟环境
    ### Windows

    ```bat
    call venv\Scripts\activate.bat
    ```
    ### Linux

    ```bash
    source venv/bin/activate
    ```
2. ### API 版本

    #### 运行
    ```bash
    python webAPI.py
    ```
    #### 用http post给本地8800端口下的/process/直接发图片，结果会出现在项目目录下的/static/文件夹内.

    ```
    http://0.0.0.0:8800/process/
    ```
    ```
    遮罩文件名为:
    原文件名+_mask(遮罩成功)/_failed(遮罩失败)_f(女)/m(男)_面孔序列.jpg
    例：test001_mask_f_1.jpg
    ```
    #### 比如用curl
    ```bash
    curl -X POST -F "file=@$HOME/Downloads/test10.jpg" http://0.0.0.0:8800/process/
    ```
3. ### GUI 版本

    #### 运行
    ```bash
    python webGUI.py
    ```

    #### 地址
    ```
    http://localhost:5500/
    ```

    #### Windows下可用run.bat同时快捷运行API和GUI版本