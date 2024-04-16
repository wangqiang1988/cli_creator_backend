
**Read this in other languages: [English](README.md), [中文](README_zh.md).**

# Features
### fortigate 
Policy generation
Policy modification

# cli_creator_backend
If you want to deploy it locally, follow these steps:

```shell
git clone https://github.com/wangqiang1988/cli_creator_backend
cd cli_creator_backend && cd cli_creator
pip install -r requirements.txt
python .\manage.py runserver 0.0.0.0:8080
```

docker
```
git clone https://github.com/wangqiang1988/cli_creator_backend
cd cli_creator_backend
cd cli_creator
docker build -t cli_creator_backend .
docker run -p 8080:8080 cli_creator_backend
```


Development version can be accessed at https://cli.madless.club

We also welcome network professionals to join us in updating and maintaining this repository, improving technical skills together, and providing convenience for other students.
