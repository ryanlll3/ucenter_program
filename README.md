# U-CENTER2.0 API PLAYBOOK
see [https://github.com/ryanlll3/ucenter_program](https://github.com/ryanlll3/ucenter_program) for full codes

欢迎阅读ucenter_api使用指南，欢迎优化建议与二次开发分享。
# 注意事项与文件注释
- 本程序需要使用操作系统安装docker，电脑体验可以安装docker desktop，官方下载。
- 本程序需要连接ucenter2.0应用，保证本地可以访问ucenter2.0的前提下，在ucenter_api/main_config/config.yml配置正确ucenter2.0 url。
- 本程序需要启动3个容器，容器启动顺序为mysql、ucenter_api、grafana。
- ucenter_api/UCenter_API_Process.py为主进程启动文件，启动后会调用各个模块，创建子进程，用来加载各项API接口数据，插入数据库，所以建议在mysql就绪以后，再启动ucenter_api容器。
- grafana/*.json文件为Grafana Dashboard,可以导入Grafana。
- mysql/mnt/ucenter_db.sql为数据库执行脚本，可以在登录mysql数据库后，使用source /mnt/ucenter_db.sql来创建数据库以及表结构。（前提是将本地目录挂载到mysql容器的/mnt/目录）
- ucenter_api/main_config/config.yml里面包含数据库连接信息，U-Center信息，如有变化需要及时修改，e.g ip
- 以下部署方式没有将容器的主要数据存储目录、配置目录挂载到本地，所以当你删除容器，**重新启动镜像，数据会丢失**。Grafana需要备份dashboard；mysql需要备份数据库表结构。

# 下载所有文件
将ucenter_api/main_config/config.yml文件中的*号参数更新为实际配置。

# 创建ucenter_api镜像(也可以直接拉取镜像，参加下方)
创建镜像命令，通过windows命令行，进入ucenter_api目录(Dockerfile所在文件夹)。

例如：
`cd D:\ryan\ucenter_program\ucenter_api`

执行下面命令, ryanlll3/ucenter_api:1.0可以替换成自己的docker hub仓库与版本号，不影响使用。

`docker build --tag ryanlll3/ucenter_api:1.0 .`

# 拉取ucenter_api镜像

`docker pull ryanlll3/ucenter_api`

# 启动镜像
## 启动方式1：通过windows cmd或powershell，linux bash
启动容器,并挂载目录，方便修改配置文件中的数据库IP，将"D:\ryan\ucenter_program\ucenter_api\main_config"换成本地电脑配置文件所在目录，配置文件名与格式必须与当前ucenter_api/main_config/config.yml保持一致。

`docker run --name ucenter_api -e TZ=Asia/Shanghai -v D:\ryan\ucenter_program\ucenter_api\main_config:/opt/ucenter_api/main_config -d ryanlll3/ucenter_api:1.3`

## 启动方式2：通过Docker Desktop启动镜像

通过Docker Desktop，下载ucenter_api：1.0镜像
通过桌面端运行镜像：
- 添加Volumes，将前面host的路径选择本地/ucenter_api/main_config文件夹，后边容器的路径选择/opt/ucenter_api/main_config；这样可以通过修改本地ucenter_api_config文件夹中的配置文件，来更新已经创建好的镜像中的配置参数。
- 添加环境变量，左边填入TZ，右边填入Asia/Shanghai。


# 启动mysql

通过命令行运行mysql，并且设置时区、挂载电脑本地目录，准备导入数据库文件; "D:\ryan\ucenter_program\mysql\mnt"换成实际ucenter_db.sql的存放目录

`docker pull mysql`

`docker run --name mysql -v D:\ryan\ucenter_program\mysql\mnt:/mnt -e TZ=Asia/Shanghai -e MYSQL_ROOT_PASSWORD=root123 -p 33060:3306 -d mysql`

其他启动方式，仅供参考，需要理解并调整：
`docker run -p 3306:3306 --name mymysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -e TZ=Asia/Shanghai -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.0`

- 如果有mysql dump文件，可以通过mysql -u root -p < 备份文件.sql
- 如果有HeidiSQL导出的数据库脚本，可以存放在上面设置的挂载路径“D:\ryan\ucenter_program\mysql\mnt”下面，

## 登录mysql

根据MYSQL_ROOT_PASSWORD=root123的设定，输入密码；

登录容器：

`docker exec -it mysql /bin/bash`

登录数据库：

`mysql -u root -p` 

## 导入数据库与表结构
执行导入数据库脚本命令, 导入mysql文件，创建数据库及表结构：

`source /mnt/ucenter_db.sql`


# 启动grafana
通过命令行:

`docker pull grafana/grafana`

`docker run -d --name=grafana -e TZ=Asia/Shanghai -p 3000:3000 grafana/grafana`

## 登录grafana
浏览器打开localhost:3000, user/password = admin/admin
## 添加mysql数据源
参照ucenter_api/main_config/config.yml文件中的配置信息，mysql ip均需使用本地服务器/电脑ip, 不能使用localhost，仅需要填必填项

## 导入dashboard
Browse Dashboards,选择import dashboard, 上传grafana目录内JSON文件即可显示数据。

# 常用其他命令

查看ucenter_api容器内的文件，或文件目录，需要登录容器

`docker ps`

`docker images`

`docker rmi image_id`

`docker rm container_id`

`docker exec -it ucenter_api /bin/bash`

`docker exec -it mysql /bin/bash`

`docker exec -it grafana /bin/bash`

