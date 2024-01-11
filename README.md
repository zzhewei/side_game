# Side Game
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Getting Started
**這是 Side Project 使用 MongoDB 當作資料庫 。 下面是如何安裝的步驟。**

### Prerequisites
* python 3.11
* pip
* MongoDB

### Installing
**1.clone repository 到 local。**
```shell
git clone https://github.com/zzhewei/side_game.git
```

**2.創建虛擬環境並安裝相關套件**
```shell
python -m venv .venv

pip install -r requirements.txt
```

**3.修改 config.py 裡的資料庫參數**

### Usage
**1.命令列輸入:**
```shell
python -m flask run --host=0.0.0.0
```
**2.[網址測試](http://127.0.0.1:5000/API/)**


### 根據 docker-compose.yml 產生 container
**1. 修改 config.py 的資料庫參數**

**2. 建立**
```shell
docker-compose up -d
```


## Authors

* **ZheWei** - *Initial work* - [ZheWei](https://github.com/zzhewei)