# FaceGenSeg

### FaceGenSeg 是个整合了面部侦测，性别识别, 和面部遮罩的工具  

### 6月大更新  
#### 更新了些微调合成的功能，调整了虚拟环境  
torch升级为2.0.1+CU118的编译版本,tensorflow更新为2.12  
其它各种依赖包的版本也都更新了，最好删了'venv'文件夹重新生成一次

---
## 环境配置

### Windows（测试环境Windows 11）
1. Nvidia显卡，驱动版本515以上

2. 安装 python 3.10.6 (3.10大版本都行,比如3.10.9)

    https://www.python.org/downloads/windows/

3. 安装Visual Studio Build Tool (测试版本2022)，  
    如果已经安装了visual studio, 那么buildtool应该已经有了       
    https://visualstudio.microsoft.com/downloads/

4. 复制或者下载本Repo并在目录下打开windows命令行,建立虚拟环境
    ```
    python -m venv venv
    ```
5. 启动虚拟环境并安装所需python组件
    ```
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    ```
    #### 注：run.bat 里其实就是 4 和 5  

    ### Windows下GPU加速（可选）
    
    ```
    安装Cuda11.7 （更新: Cuda11.8也可以），下载安装包按提示安装（需要注册Nvidia开发者账号），
    安装时选择自定义，只需要打第一个Cuda的勾，其它三项留空,
    https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64
    ```

    ```
    安装cuDNN
    1.自建文件夹到以下路经，中间没有的文件夹也自己建
    C:\Program Files\NVIDIA\CUDNN\v8.x\
    2.下载cuDNN8.5.0.96 (更新: 此版本以上貌似都行, 测试了8.9.2一切正常)
    https://developer.nvidia.com/rdp/cudnn-archive
    3.解压后把三个文件夹bin include lib复制到第1步我们建好的文件夹内
    4.把路径'C:\Program Files\NVIDIA\CUDNN\v8.x\bin'加入Windows系统变量'PATH'
    可以在管理员权限的命令终端输入 setx PATH "%PATH%;C:\Program Files\NVIDIA\CUDNN\v8.x\bin"
    也可以在系统设置里手动添加
    "控制面板" > "系统" > "高级系统设置" > "环境变量" > "系统变量" > "PATH" > "新建" > 复制路径 > “确定”
    5.重启系统
    ```
---
### Linux (测试环境Ubuntu22.04)

1. Nvidia显卡，驱动版本N社官方515  
    （525测试通过，<s>530我装不上CUDA，也许是我的问题</s> N社有详细的兼容性表格  
    包含了驱动版本，CUDA和CUDNN,全都要匹配  
    https://docs.nvidia.com/deeplearning/cudnn/support-matrix/index.html

    (nvidia driver metapackage from nvidia-driver-515(proprietary))
    ```
    sudo apt install nvidia-driver-515
    sudo reboot
    ```
2. 安装 python 3.10.6

    ```bash
    sudo apt-get install python-is-python3 -y
    ```
3. 安装 pip (测试版本22.0.2)

    ```bash
    sudo apt install python3-pip
    ```

4. 安装 venv package

    ```bash
    sudo apt install python3.10-venv
    ```

5. 复制或者下载本Repo并在目录下打开终端

6. 运行虚拟环境设置脚本

    ```bash
    bash setup.sh
    ```
    ### Linux下GPU加速（可选）
    ```
    //====安装cuda 11.7====  
    (更新: 11.8也可以, 在某些Ubuntu的发行版上貌似可以直接'sudo apt install nvidia-cuda-toolkit',不用手动下载CUDA)  

    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
    sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-ubuntu2204-11-7-local_11.7.0-515.43.04-1_amd64.debnv
    sudo cp /var/cuda-repo-ubuntu2204-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda

    nano ~/.bashrc
    //修改.bashrc,在末尾加三行
 
    export CUDA_HOME=/usr/local/cuda
    export PATH=$CUDA_HOME/bin:$PATH
    export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

    //然后Ctrl+X -> Y -> Enter 完成保存
    
    //生效
    source ~/.bashrc

    //运行以下命令检查cuda状态
    nvcc --version
    ```
    ```    
    //====安装cuDNN 8.5.0.96====  
    （更新: 8.5之后的版本到8.9.2貌似都可以）
    //下载地址
    https://developer.nvidia.com/rdp/cudnn-archive
    //需要N社开发者账号
    //测试系统是i7 13700k + 2080ti,所以下载了64位Ubuntu22.04的Deb安装包
    cudnn-local-repo-ubuntu2204-8.5.0.96_1.0-1_amd64.deb 

    //下载完成后在下载文件夹打开终端输入
    sudo dpkg -i cudnn-local-repo-ubuntu2204-8.5.0.96_1.0-1_amd64.deb 
    //根据上一条的运行提示复制gpg key到提示位置

    //更新源并安装
    sudo apt-get update
    sudo apt-get install libcudnn8 libcudnn8-dev

    //检查安装
    cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
    ```

---  

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
    #### 用http post给本地8800端口下的/process/直接发图片，遮罩文件会生成在项目目录下的/static/文件夹内.

    ```
    http://0.0.0.0:8800/process/
    ```
    ```
    更新：其它所有可调参数都在webAPI.py内修改

    遮罩文件名为:    
    原文件名+_mask_f(女)/m(男)_年龄_Padding_面孔序列.jpg
    例：test001_mask_f_31_921_1.jpg
    ```
    文件名解析示例
    ```python
    filename = "test001_mask_f_31_921_1.jpg"
    parts = filename.split("_")  # Split the filename by underscore

    # Split the last element by dot to separate the extension
    last_part = parts[-1].split(".")
    parts[-1] = last_part[0]
    parts.append(last_part[1])

    print(parts)
    ```
    得到
    ```python
    ['test001', 'mask', 'f', '31', '921', '1', 'jpg']
    ```

    #### 比如用curl发送
    ```bash
    curl -X POST "http://localhost:8800/process/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@path_to_your_file"
    ```
    #### 再比如用Python发送
    ```python
    import requests

    url = "http://localhost:8800/process/"
    file_path = "path_to_your_file"

    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file})

    print(response.json())  
    ```

3. ### GUI 版本

    #### 运行
    ```bash
    python webGUI.py
    ```

    #### 地址
    ```
    http://127.0.0.1:5500
    ```
4. ### 命令行直接调用main.py,后面跟图片本地地址    
    ```bash
    python main.py ~/Downloads/test.jpg
    ```