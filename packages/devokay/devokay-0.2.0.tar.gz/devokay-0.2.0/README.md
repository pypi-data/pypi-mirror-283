# Devokay

## Doc

### ubuntu 安装 py312

```
# deadsnakes 团队维护了一个专门的 Launchpad PPA，可以帮助 Ubuntu 用户轻松安装最新版本的 Python 及附加模块。
sudo add-apt-repository ppa:deadsnakes/ppa

# 安装
sudo apt install python3.12

# 版本
python3.12 --version

# 安装 pip
sudo apt install python3-pip

# 配置环境
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 4
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 5
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 6
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 7

# 切换环境
sudo update-alternatives --config python
```