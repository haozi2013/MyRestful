项目名称：RESTful API 服务


要求：

    系统：
        WindowsXP, Windows7
        Red Hat6.1（其他未试）

    环境：
        系统需安装 Python (本项目采用Python 2.6版本)

功能：

    通过 Python 搭建简单的 RESTful API，实现信息的采集和邮件发送

工作流程：

    1、搭建 RESTful API , 监听消息
    2、通过 post 模式接收到发送者的信息
    3、发送邮件给信息发送者、发送邮件给特定邮箱并记录下发送者的信息

目录结构:

    config/mail_config: 邮箱服务器的配置文件
    archive/: 存放发送者信息（根据发送者名字命名，一人一文件）
    pylibs/: 类库（restful, mail）
    log/: 项目运行日志（一天一文件）

项目示例：

    一、通过编写 config/mail_config 配置 邮箱服务器等信息。
    二、运行main.py，开启消息监听。
    三、通过 curl 指令发送个人信息给RESTful API（在Linux 运行，Windows 未测）：
        1、编写 json 格式文件，如 data.json，需要设置 "email"，"first_name"，"last_name"，
            "contact_number","title","content","link"
        2、$ curl -X POST -H "Accept: application/json" -d @data.json http://targethost:8000/rest  #rest和端口为固定值
            发送个人信息.

备注：目前邮箱服务器只支持 163 的和 QQ服务器 （其它未试）,其中QQ邮箱需要设置允许开启smtp服务,
      邮箱服务器可在配置文件mail_config中配置
