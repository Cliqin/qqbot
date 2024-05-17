# Lagrange
> https://github.com/LagrangeDev/Lagrange.Core

## 介绍
- 使用的是 Lagrange

## 首次启动
```bash
docker compose up
```

然后扫码登录即可，会登录到 linux 平台

## 测试
- 进群发送 python 即可看到回复
- 所有关键字以及自动回复的消息均存于 [`ws/botmsg.txt`](ws/botmsg.txt) 文件中
- 修改了 `ws/botmsg.txt` 文件后需要重启

## 后台启动
```bash
docker compose up -d
```

## 配置文件
- 配置文件是 [`data/appsetting.json`](data/appsetting.json)