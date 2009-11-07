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
import re
import sys
import socket
import urllib
import minetconf

# Global variable to share connection information between functions.
conn_info = []

# Display helper information.
def usage():
  conn_info[0].close()
  print '''Usage: minet [options]
Options:
  [None]\tPrint this message
  on\t\tToggle online/offline
  off\t\tSame as "on"
  query\t\tQuery the current status (online/offline)
  --help\tPrint this message

Examples:
  minet on
  minet query

*NOTE*: Before use "minet", you must configure your account with
        "minetconf" command. 

MINET 0.2.2 by Hector Zhao <zhaobt@nimte.ac.cn>
'''
  sys.exit(0)

def connect():
  if len(conn_info) == 0:
    conn = httplib.HTTPConnection('192.168.254.100')
    conn_info.insert(0, conn)
  else:
    conn = conn_info[0]
  try:
    conn.connect()
  except socket.error:
    return (False, 'Socket error. Please check your network connection.')
  return (True, 'Socket OK!')

def query():
  conn = conn_info[0]
  headers = {'Host':'192.168.254.100','User-Agent':'minet_python'}
  conn.request('GET','/', None, headers)
  res = conn.getresponse()
  res = res.read().decode('gbk').encode('utf8')
  if res.find('请您确认要注销') != -1:
    return (True, 'Currently online.')
  elif res.find('请输入您的帐号和密码') != -1:
    return (True, 'Currently offline.')
  else:
    return (False, 'Unknown error!')

#Global functions
def online(account):
  conn = conn_info[0]
  data = 'DDDDD=%s&upass=%s&0MKKey=登录 Login' % (account[0],account[1])
  headers = {'Host':'192.168.254.100','User-Agent':'minet_python',
             'Content-Length':str(len(data)),
             'Content-Type':'application/x-www-form-urlencoded'}
  conn.request('POST','/', data, headers)
  res = conn.getresponse()
  res = res.read().decode('gbk').encode('utf8')
  if res.find('您已经成功登录') != -1:
    return (True, 'Online succeeded.')
  elif res.find('DispTFM') != -1:
    msg = re.search('Msg=(\d{2})', res)
    msga = re.search('msga=\'(\w?)\'', res)
    if msg and msga:
      msg = str(int(msg.groups()[0]))
      msga = msga.groups()[0]
      if msga:
        emsg = re.search('\s\'%s\':\s*document\.write\("(.*?)".*?\);' % msga, res, re.S)
      elif msg == '1':        
        emsg = re.search('else\sdocument\.write\("(.*?)".*?\);', res, re.S)
      else:
        emsg = re.search('\s%s:\s*document\.write\("(.*?)".*?\);' % msg, res, re.S)
      if emsg:
        emsg = emsg.groups()[0]
        return (False, emsg)
    return (False, 'Unknown error!')
  else:
    return (False, 'Unknown error!')

def offline():
  conn = conn_info[0] 
  headers = {'Host':'192.168.254.100','User-Agent':'minet_python'}
  conn.request('GET','/F', None, headers)
  res = conn.getresponse()
  res = res.read().decode('gbk').encode('utf8')
  if res.find('注销成功') != -1:
    return (True, 'Offline succeeded.')
  else:
    return (False, 'Unknown error!')

def main(account=[], verbose=True):
  if len(account) != 4:
    s = minetconf.show()
    account = s.split(':')

  #Global settings
  result = ''
  ret, retstr = connect();
  if(ret == False):
    result += retstr;
  else:
    if len(sys.argv) == 1:
      usage()
    elif sys.argv[1] == '--help':
      usage()
    elif sys.argv[1] == 'on':
      ret, retstr = online(account)
      result += '\n' + retstr
    elif(sys.argv[1] == 'off'):
      ret, retstr = offline()
      result += '\n' + retstr
    elif(sys.argv[1] == 'query'):
      ret, retstr = query()
      result += '\n' + retstr
    else:
      if verbose:
        print 'Unknow option!'
        usage()
      else:
        conn_info[0].close()
        return False
  conn_info[0].close()
  if verbose:
    print result

if __name__ == "__main__":
  main()
