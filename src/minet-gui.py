#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 --------------------------------------------------------------------------
 MINET(IP Gateway Client for NIMTE)
 Copyright (C) 2008 Wenbo Yang <solrex@gmail.com>
 Copyright (C) 2009 Hector Zhao <zhaobt@nimte.ac.cn>
 --------------------------------------------------------------------------

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 --------------------------------------------------------------------------
"""

import httplib
import os
import re
import sys
from os import path

import pygtk
if not sys.platform == 'win32':
  pygtk.require('2.0')
import gtk

# Import minet modules.
import minetconf
import minet

# Main gui class.
class MINETGui:
  account = ['', '', '1', '0']

  stat_str = '''
请先连线再查询流量信息
  '''
  # Status used as a signal. 0: offline, 1: online, -1: quit
  status = 0

  # Helper function for pop up a simple dialog window.
  def pop_dialog(self, title, data):
    dialog = gtk.Dialog(title, None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.set_border_width(25)
    dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    label = gtk.Label(data)
    dialog.vbox.pack_start(label, True, True, 0)
    label.show()
    if dialog.run() == gtk.RESPONSE_OK:
      dialog.destroy()
    return True

  # Show help dialog window.
  def help(self, widget, data=None):
    help_str = '''MINET 0.2 (20090804)
Copyright (C) 2008 Wenbo Yang <solrex@gmail.com>
Copyright (C) 2009 Hector Zhao <zhaobt@nimte.ac.cn>
\n　　MINET 是宁波材料所 IP 控制网关登录客户端，基于中科院研究生
院网关客户端 CASNET，支持 Linux 和 Windows 双系统。此软件使用
Python 语言写成，同时支持命令行和图形界面，使用简单，安装方便，
实乃宁波材料所 IP 网关用户居家旅行必备之良品 :)。
\n本软件遵从 GPL 协议<http://www.gnu.org/licenses/gpl.txt>，
在此协议保护之下，您可以自由地使用、修改或分发本软件。
\n感谢列表：
　　giv<goldolphin@163.com>: 命令行客户端脚本的原型作者
'''
    self.pop_dialog('关于 MINET', help_str)
    return True
  
  # Method called when status icon was clicked.
  def icon_pop(self, widget, data=None):
    # If the top window is hided, present it; else, hide it.
    if self.window.is_active():
      self.hide(widget, data)
    else:
      self.window.present()
    return True

  # Method called when close window button was clicked.
  def hide(self, widget, data=None):
    self.window.hide()
    while gtk.events_pending():
      gtk.main_iteration()
    return True

  # Pop up an menu when right clicking status icon.
  def pop_menu(self, widget, button, time, data=None):
    if data:
      data.show_all()
      if sys.platform == 'win32':
        data.popup(None, None, None, 3, time)
      else:
        data.popup(None, None, gtk.status_icon_position_menu, 3, time, widget)
    return True

  def callback_cb(self, widget, data=None):
    if data == 0:
      self.account[2] = ('0', '1')[widget.get_active()]
      if not widget.get_active():
        self.c_auto.set_active(False)
        self.account[3] = '0'
    elif data == 1:
      if self.c_rem.get_active():
        self.account[3] = ('0', '1')[widget.get_active()]
      else:
        self.c_auto.set_active(False)
    return True

  def close_app(self, widget, data=None):
    # Get account information.
    minetconf.ops['-u'] = self.account[0]
    minetconf.ops['-p'] = self.account[1]
    minetconf.ops['-r'] = self.account[2]
    minetconf.ops['-a'] = self.account[3]
    # Store account information to account file.
    minetconf.write_ops()

    self.status = -1
    gtk.main_quit()
    return False

  def stat(self, widget, data=None):
    #(ret, retstr) = minet.query()
    (ret, retstr) = self.query(data)
    if ret == True:
      stat_str = '''
%s
''' % retstr
      self.stat_frame.set_label("当前状态：已连线")
      self.stat_label.set_text(stat_str)
      self.stat_label.show()
      self.stat_frame.show()
      self.trayicon.set_from_file(path.join(self.iconpath, 'online.png'))
      self.trayicon.set_tooltip('MINET: Online')
      self.trayicon.set_visible(True)
    else:
      self.stat_frame.set_label("当前状态：未连线")
      self.stat_label.set_text(self.stat_str)
      self.stat_label.show()
      self.stat_frame.show()
      self.trayicon.set_from_file(path.join(self.iconpath, 'offline.png'))
      self.trayicon.set_tooltip('MINET: Offline')
      self.trayicon.set_visible(True)
    if not self.window.is_active():
      self.window.present()
    return True

  def online(self, widget, data=None):
    if widget == self.b_online:
      if widget.get_active() == False:
        return True
    # Disable changing username and passwd before login.
    self.e_user.set_editable(False)
    self.e_passwd.set_editable(False)
    # Get account information.
    self.account[0] = self.e_user.get_text()
    self.account[1] = self.e_passwd.get_text()
    # Connect
    (ret, retstr) = minet.connect(self.account)
    if ret == False:
      self.pop_dialog('网关错误', retstr)
      return False
    if retstr == 'Currently online.':
      self.pop_dialog('提示', '已经连线了，不要重复连线\n')
      self.b_online.set_active(False)
      return False
    # Online
    (ret, retstr) = minet.online(self.account)
    if ret == False:
      self.pop_dialog('连线错误', retstr)
      return False
    # Get account statistics information.
    self.stat(None)
    self.b_online.set_active(False)
    return True

  def offline(self, widget, data=None):
    if widget == self.b_offline:
      if widget.get_active() == False:
        return True
    (ret, retstr) = minet.connect(self.account)
    if ret == False:
      self.pop_dialog('网关错误', retstr)
      return False
    if retstr == 'Currently offline.':
      self.pop_dialog('提示', '已经离线了，不要重复离线\n')
      self.b_offline.set_active(False)
      return False
    (ret, retstr) = minet.offline(self.account)
    if ret == False:
      self.pop_dialog('离线错误', retstr)
      return False
    self.stat(None)
    self.e_user.set_editable(True)
    self.e_passwd.set_editable(True)
    self.b_offline.set_active(False)
    return True

  def query(self, stat):
    self.status = 1 if minet.connect(self.account)[1] == 'Currently online.' else 0
    if self.status and stat:
      conn = httplib.HTTPConnection('192.168.254.110')
      try:
        conn.connect()
      except socket.error:
        return (False, 'Socket error. Please check your network connection.')  
      headers = {'Host':'192.168.254.110','User-Agent':'minet_python'}
      conn.request('GET','/page/selfservice/login.jsp', None, headers)
      res = conn.getresponse()
      res.read()
      cookie = res.getheader('Set-Cookie').split(';')[0] 
      headers = {'Host':'192.168.254.110','User-Agent':'minet_python',
                 'Cookie':cookie,
                 'Referer':'http://192.168.254.110/page/selfservice/login.jsp'}
      conn.request('GET','/page/selfservice/include/image.jsp', None, headers)
      res = conn.getresponse()
      data = res.read()
      loader = gtk.gdk.PixbufLoader()
      loader.write(data)
      loader.close()

      dialog = gtk.Dialog('验证码', None, gtk.DIALOG_NO_SEPARATOR, (gtk.STOCK_OK, gtk.RESPONSE_OK))
      dialog.set_icon_from_file(os.path.join(self.iconpath, 'minet.png'))
      dialog.set_border_width(10)
      dialog.set_position(gtk.WIN_POS_CENTER_ALWAYS)
      dialog.set_default_response(gtk.RESPONSE_OK)
      image = gtk.Image()
      image.set_from_pixbuf(loader.get_pixbuf())
      dialog.vbox.pack_start(image, True, True, 0)
      image.show()
      captcha = gtk.Entry()
      captcha.set_max_length(4)
      captcha.set_activates_default(True)
      dialog.vbox.pack_start(captcha, True, True, 0)
      captcha.show()
      if dialog.run() == gtk.RESPONSE_OK:
        rand = captcha.get_text()
      dialog.destroy()

      data = 'loginName=%s&password=%s&rand=%s' % (self.account[0],self.account[1],rand)
      headers = {'Host':'192.168.254.110','User-Agent':'minet_python',
                 'Content-Length':str(len(data)),
                 'Content-Type':'application/x-www-form-urlencoded',
                 'Cookie':cookie}
      conn.request('POST','/selflogin.do', data, headers)
      res = conn.getresponse()
      res_html = res.read()

      aid = re.search('accountId=(\d{3})', res_html)
      if not aid:
        return (True, '验证码输入错误')
      headers = {'Host':'192.168.254.110','User-Agent':'minet_python',
                 'Cookie':cookie}
      conn.request('GET', '/selfUserInfo.do?action=viewUseSum&accountId=%s' % aid.groups()[0], data, headers)
      res = conn.getresponse()
      res_html = res.read().decode('gbk').encode('utf8')
      regex = ('<td  bgcolor="#FFFFFF">&nbsp;([\d\.]+) M\n</td>\s+'
               '<td  bgcolor="#FFFFFF">&nbsp;([\d\.]+) M\n</td>\s+'
               '<td  bgcolor="#FFFFFF">&nbsp;([\d\.]+) M\n</td>\s+'
               '<td  bgcolor="#FFFFFF">&nbsp;[\d]+</td>\s+<td  bgcolor="#FFFFFF">&nbsp;'
               '<a href="/selfUserInfo\.do\?action=viewUseDetail&accountId=\d+&year=\d+&month=\d+">查看详情</a>'
               '</td>\s+</tr>\s+</table>')
      stat = re.search(regex, res_html, re.S)
      if stat:
        return (True, '%s MB = %s MB↓ + %s MB↑' % stat.groups())
      else:
        return (True, '流量信息不可用')
    else:
      if self.status:
        return (True, '请点击“刷新”以获取流量信息')
      else:
        return (False, '请先连线再查询流量信息')

  def __init__(self):
    # Find minet icons path.
    if sys.platform == 'win32':
      file_dir = path.dirname(sys.argv[0]);
      self.iconpath = path.join(file_dir.decode('gbk').encode('utf8'), 'pics')
    else:
      script_dir = os.path.abspath(sys.path[0])
      self.iconpath = os.path.join(script_dir, 'pics')
      if not path.isdir(self.iconpath):
        self.pop_dialog('Error', 'Can not find minet icons.')
    # Get saved account information.
    s = minetconf.show()
    if s != False:
      self.account = s.split(':')

    # Set main window's attributes.
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title('中科院宁波材料所网关客户端')
    self.window.set_icon_from_file(path.join(self.iconpath, 'minet.png'))
    self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    self.window.set_resizable(False)
    self.window.set_border_width(10)

    # Connect close window events to user defined function.
    self.window.connect("destroy", self.hide)
    self.window.connect("delete-event", self.hide)
  
    # Add objects to the main window.
    main_vbox = gtk.VBox(False, 0)
    self.window.add(main_vbox)

    self.stat_frame = gtk.Frame('当前状态：未连线')
    main_vbox.pack_start(self.stat_frame, True, True, 0)

    self.stat_label = gtk.Label(self.stat_str)
    self.stat_frame.add(self.stat_label)
    self.stat_label.show()
    self.stat_frame.show()

    bbox = gtk.HButtonBox()
    bbox.set_border_width(10)
    main_vbox.pack_start(bbox, True, True, 0)
    b_stat = gtk.Button('刷新')
    b_stat.connect('clicked', self.stat, True)
    bbox.add(b_stat)
    b_stat.show()

    b_help = gtk.Button('帮助')
    b_help.connect('clicked', self.help, None)
    bbox.add(b_help)
    b_help.show()
    bbox.show()

    le_hbox = gtk.HBox(False,0)
    main_vbox.pack_start(le_hbox, True, True, 0)

    l_vbox = gtk.VBox(False, 0)
    le_hbox.pack_start(l_vbox, True, True, 0)
    e_vbox = gtk.VBox(False, 0)
    le_hbox.pack_start(e_vbox, True, True, 0)

    label = gtk.Label('用户名')
    l_vbox.pack_start(label, True, True, 0)
    label.show()

    self.e_user = gtk.Entry()
    self.e_user.set_max_length(20)
    self.e_user.set_text(self.account[0])
    e_vbox.pack_start(self.e_user, True, True, 0)
    self.e_user.show()

    label = gtk.Label('密  码')
    l_vbox.pack_start(label, True, True, 0)
    label.show()

    self.e_passwd = gtk.Entry()
    self.e_passwd.set_max_length(32)
    self.e_passwd.set_visibility(False)
    self.e_passwd.set_text(self.account[1])
    e_vbox.pack_start(self.e_passwd, True, True, 0)
    self.e_passwd.show()

    l_vbox.show()
    e_vbox.show()
    le_hbox.show()

    # General option check boxes.
    bbox = gtk.HButtonBox()
    bbox.set_border_width(10)
    main_vbox.pack_start(bbox, False, True, 0)

    self.c_rem = gtk.CheckButton('记住我的密码')
    self.c_rem.connect('toggled', self.callback_cb, 0)
    self.c_rem.set_active(int(self.account[2]))
    bbox.add(self.c_rem)
    self.c_rem.show()

    self.c_auto = gtk.CheckButton('下次自动登录')
    self.c_auto.connect('toggled', self.callback_cb, 1)
    self.c_auto.set_active(int(self.account[3]))
    bbox.add(self.c_auto)
    self.c_auto.show()
    bbox.show()

    separator = gtk.HSeparator()
    main_vbox.pack_start(separator, False, True, 0)
    separator.show()

    bbox = gtk.HButtonBox()
    bbox.set_border_width(10)
    main_vbox.pack_start(bbox, False, True, 0)

    self.b_online = gtk.ToggleButton('连线')
    self.b_online.connect('toggled', self.online, None)
    bbox.add(self.b_online)
    # Set it as the default button of this window.
    self.b_online.set_flags(gtk.CAN_DEFAULT)
    self.b_online.grab_default()
    self.b_online.show()

    self.b_offline = gtk.ToggleButton('离线')
    self.b_offline.connect('toggled', self.offline, None)
    bbox.add(self.b_offline)
    self.b_offline.show()


    b_help = gtk.Button('退出')
    b_help.connect('clicked', self.close_app, None)
    bbox.add(b_help)
    b_help.show()
    bbox.show()

    p_menu = gtk.Menu()
    menu_item = gtk.MenuItem('  弹出')
    menu_item.connect('activate', self.icon_pop, None)
    p_menu.append(menu_item)
    menu_item = gtk.SeparatorMenuItem()
    p_menu.append(menu_item)
    menu_item = gtk.MenuItem('  连线')
    menu_item.connect('activate', self.online, None)
    p_menu.append(menu_item)
    menu_item = gtk.MenuItem('  刷新')
    menu_item.connect('activate', self.stat, True)
    p_menu.append(menu_item)
    menu_item = gtk.MenuItem('  离线')
    menu_item.connect('activate', self.offline, None)
    p_menu.append(menu_item)
    menu_item = gtk.SeparatorMenuItem()
    p_menu.append(menu_item)
    menu_item = gtk.MenuItem('  帮助')
    menu_item.connect('activate', self.help, None)
    p_menu.append(menu_item)
    menu_item = gtk.SeparatorMenuItem()
    p_menu.append(menu_item)
    menu_item = gtk.MenuItem('  退出')
    menu_item.connect('activate', self.close_app, None)
    p_menu.append(menu_item)

    self.trayicon = gtk.StatusIcon()
    self.trayicon.connect('activate', self.icon_pop)
    self.trayicon.connect('popup-menu', self.pop_menu, p_menu)
    self.trayicon.set_from_file(path.join(self.iconpath, 'offline.png'))
    self.trayicon.set_tooltip('MINET: Offline')
    self.trayicon.set_visible(True)

    main_vbox.show()
    self.window.show()

    self.stat(None)
   
    # Auto login. 
    if self.account[3] == '1' and len(self.account[1]) > 0 and not self.status:
      self.b_online.clicked()

    if self.window.is_active() == False:
      self.window.present()

def main():
  MINETGui()
  gtk.main()
  return 0

if __name__ == '__main__':
  main()
