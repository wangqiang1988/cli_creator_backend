# cli_creator_backend
如需想自己部署玩，本地部署
```shell
git clone https://github.com/wangqiang1988/cli_creator_backend
cd cli_creator_backend
cd cli_creator
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


