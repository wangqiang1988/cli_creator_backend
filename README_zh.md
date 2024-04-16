
# 功能

### 飞塔防火墙
策略生成
策略修改

# cli_creator_backend
如需想自己部署玩，本地部署
```shell
git clone https://github.com/wangqiang1988/cli_creator_backend
cd cli_creator_backend && cd cli_creator
pip install -r requirements.txt
python .\manage.py runserver 0.0.0.0:8080
```
docker部署
```
git clone https://github.com/wangqiang1988/cli_creator_backend
cd cli_creator_backend
cd cli_creator
docker build -t cli_creator_backend .
docker run -p 8080:8080 cli_creator_backend
```

# 开发中的版本
开发中的版本https://cli.madless.club

也希望有网络同学一起来更新维护这个库，共同提高技术，也为其他同学提供便利