中科院宁波材料所 IP 网关登录客户端(MINET)

Copyright (C) 2008 Wenbo Yang <solrex@gmail.com>
Copyright (C) 2009 Hector Zhao <zhaobt@nimte.ac.cn>

本软件遵从 GPL 协议<http://www.gnu.org/licenses/gpl.txt>，在此协议保护之下，
您可以自由地使用、修改或分发本软件。

MINET 是宁波材料所 IP 控制网关登录客户端，基于中科院研究生院网关客户端CASNET，
同时支持 Linux 和 Windows 操作系统。此软件使用 Python 语言写成，拥有命令行和图
形界面，使用简单，安装方便，实乃宁波材料所 IP 网关用户居家旅行必备之良品 :)。

===== 系统要求 =====

==== Linux ====
    * Python >= 2.4
    * PyGTK >= 2.10
    * Gtk lib

===== 安装与卸载 =====

==== Linux ====
使用命令行运行 sudo make install 即可将本软件安装到您的操作系统里。
使用命令行运行 sudo make uninstall 即可将本软件从您的操作系统卸载。

==== Windows ====
直接将压缩包解压到安装文件夹即可。
使用安装文件安装或卸载。

===== 使用方法 =====

命令行客户端：

==== Linux ====
    在命令行输入 minetconf，根据提示输入您的用户信息，您的用户信息将被保存到
    ~/.minet/account
    注意，帐户信息仅需输入一次，然后执行下列命令：
    $ minet on|off|query
    来连线|离线|查询

==== Windows ====
    在命令行输入 minetconf.py，根据提示输入您的用户信息，您的用户信息将被保存到
    HOMEDRIVE:\HOMEPATH\.minet\account
    注意，帐户信息仅需输入一次，然后执行下列命令：
    $ minet.py on|off|query
    来连线|离线|查询

图形界面客户端：

==== Linux ====
    从 Applications->Internet->MINET 直接执行即可;
    或者在终端中输入 minet-gui

==== Windows ====
    * Stand alone: 安装后运行 minet-gui.exe

===== BUG 报告 =====

如果您在使用中发现 BUG，请将 BUG 提交到 http://( not currently )
非常感谢！
