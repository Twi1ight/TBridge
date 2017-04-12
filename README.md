# TBridge

基于http协议的tunnel，可在**只支持http代理访问web**的网络环境中使用其他协议。

By. [twi1ight@t00ls.net](mailto:twi1ight@t00ls.net)

## 简介

上面一句话介绍有点绕，使用场景如下：

- 公司内部只支持http代理上网，所有人上网都从统一的http代理出去
- 代理只允许访问http/https协议，其他协议配置该代理无法使用
- 代理上传数据限制大小4K

因此，没办法用ssh直接连接自己的VPS，为解决该问题开发了TBridge。

## 原理

TBridge分为两部分：server运行在外部VPS上，会开放一个web服务；client运行在本地，会监听一个端口。

ssh客户端连接client监听的端口，然后client会将从ssh客户端收到的数据用base64编码后通过http代理发送到server端的web接口上，server端收到数据解码后发送给ssh服务器进程（sshd），然后将sshd的响应数据base64编码后返回给client，client将数据解码后发送给ssh客户端，至此完成一次数据交互。

```
+--------------+                                  +--------------+
|  SSH Client  |                                  |  SSH Server  |
+-----+--+-----+                                  +-----+--+-----+
      |  ^                                              |  ^
      |  |                                              |  |
  ssh |  |                                          ssh |  |
      |  |                                              |  |
      |  |                                              |  |
      v  |                                              v  |
+-----+--+-----+          +------------+          +-----+--+-----+
|TBridge Client<----------> HTTP Proxy <---------->TBridge Server|
+--------------+          +------------+          +--------------+
                        base64 encoded http

```

## 安装与使用

**安装：**

`pip install -r requirements.txt`

*注意：不要直接用pip install cherrypy安装cherrypy，在写该文档之时，cherrypy最新版与bottle最新版无法一起使用*

**使用：**

Server端需要在vps上运行

```
Twi1ight at Mac-Pro in ~/Code/TBridge (master)
$ python server.py
usage: python server.py port-for-client service-host service-port
e.g. for ssh: python server.py 8089 localhost 22
```

`python server.py 8089 localhost 22`

这条命令会建立一个web服务器，监听在8089端口，后端连接的服务是本地的ssh服务，理论上也支持连接其他服务器，那样vps就纯粹是一个中转服务器了。

Client端在本地运行

```
Twi1ight at Mac-Pro in ~/Code/TBridge (master)
usage: python client.py listen-port server-url http-proxy
e.g. python client.py 2222 http://12.34.56.78:8089/ http://proxy.yourcorp.com:8080
then "ssh root@localhost -p 2222" will ssh to 12.34.56.78
```

`python client.py 2222 http://12.34.56.78:8089/ http://proxy.yourcorp.com:8080`

这条命令会在本地监听2222端口，指定TBridge的Server为[http://12.34.56.78:8089/](http://12.34.56.78:8089/)，指定上网的代理服务器为[http://proxy.yourcorp.com:8080](http://proxy.yourcorp.com:8080)

然后用ssh客户端连接localhost:2222即可登录vps。

目前只测试过ssh协议，理论上支持其他协议。

**注意：目前只支持单实例运行，即本地只允许一个客户端进行连接，且服务端只能同时处理一个客户端。**

## 设置

所有设置都在settings.py中，为躲避proxy分析与拦截，采用的都是常见的web资源名称，如果vps没有域名，可以将headers中的Host字段注释去掉，伪装成baidu（不要改成google，会被GFW切断连接的）。

```python
route_to_init = 'favicon.ico'              #初始化服务器路径
route_to_transport = 'jquery-3.2.0.min.js' #服务端接收数据路径
route_to_shutdown = 'bootstrap.min.css'    #关闭服务器连接路径
post_param_name = 'z'     #数据包发送时变量名
post_fragment_size = 2048 #数据包分片大小，需与代理最大限制保留一定空间，base64编码后可能会变长
64

headers = {
    # 'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2987.133 Safari/537.36'
}
```

## 计划

- 加密通信替换base64
- 服务器可从客户端配置
- 服务器访问控制
- 多客户端、多协议支持