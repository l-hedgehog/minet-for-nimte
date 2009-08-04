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
import sys
import socket
import urllib
import minetconf

# Global variable to share connection information between functions.
conn_info = []

# Display helper information.
def usage():
  print '''Useage: minet [options]
Options:
  [None]\tPrint this message
  on\t\tToggle online/offline
  off\t\tSame as "on"
  query\t\tOnly available in GUI
  --help\tPrint this message

Examples:
  minet on
  minet query

*NOTE*: Before use "minet", you must configure your account with
        "minetconf" command. 

MINET 0.2 by Hector Zhao <zhaobt@nimte.ac.cn>
'''
  sys.exit(0)

def connect(account):
  if len(conn_info) == 0:
    conn = httplib.HTTPConnection('192.168.192.1')
    conn_info.insert(0, conn)
  else:
    conn = conn_info[0]
  try:
    conn.connect()
  except socket.error:
    return (False, 'Socket error. Please check your network connection.')  
  headers = {'Host':'192.168.192.1','User-Agent':'minet_python'}
  conn.request('GET','/cgi-bin/cgiipauth', None, headers)
  res = conn.getresponse()
  res.read()
  if res.status == 302:
    res_loc = res.getheader('location')
    if res_loc.find('cgireadylogout') != -1:
      session = res_loc.split('=')[1]
      conn_info.insert(1, session)
      return (True, 'Currently online.')
    elif res_loc == 'http://192.168.192.1:80/founderbnLogin.html':
      session = ''
      conn_info.insert(1, session)
      return (True, 'Currently offline.')
    else:
      return (False, 'Unknown error!')
  else:
    return (False, 'Not a 302 response!')

#Global functions
def online(account):
  conn = conn_info[0]
  session = conn_info[1]
  if not session:
    data = 'UserName=%s&PassWord=%s&IDType=1' % (account[0],account[1])
    headers = {'Host':'192.168.192.1','User-Agent':'minet_python',
               'Content-Length':str(len(data)),
               'Content-Type':'application/x-www-form-urlencoded'}
    conn.request('POST','/cgi-bin/cgilogin', data, headers)
    res=conn.getresponse()
    res.read()
    if res.status == 302:
      res_loc = res.getheader('location')
      if res_loc.find('cgiportal') != -1:
        return (True, 'Online succeeded.')
      elif res_loc.find('cgifault') != -1:
        fault = urllib.unquote(res_loc.split('=')[1]).decode('gbk')
        return (False, fault)
      else:
        return (False, 'Unknown online error!')
    else:
      return (False, 'Not a 302 response!')
  else:
    headers = {'Host':'192.168.192.1','User-Agent':'minet_python'}
    conn.request('GET','/cgi-bin/cgilogout?SessionID=%s' % session, None, headers)
    res = conn.getresponse()
    res.read()
    if res.status == 302:
      res_loc = res.getheader('location')
      if res_loc.find('deletesession') != -1:
        return (True, 'Offline succeeded.')
      elif res_loc.find('cgifault') != -1:
        fault = urllib.unquote(res_loc.split('=')[1]).decode('gbk')
        return (False, fault)
      else:
        return (False, 'Unknown offline error!')
    else:
      return (False, 'Not a 302 response!')

def offline(account):
  return online(account)

def main(account=[], verbose=True):
  if len(account) != 4:
    s = minetconf.show()
    account = s.split(':')

  #Global settings
  result = ''
  ret, retstr = connect(account);
  if(ret == False):
    result += retstr;
  else:
    if len(sys.argv) == 1:
      usage()
    elif sys.argv[1] == 'on':
      ret, retstr = online(account)
      result += '\n' + retstr
    elif(sys.argv[1] == 'off'):
      ret, retstr = offline(account)
      result += '\n' + retstr
    elif(sys.argv[1] == 'query'):
      result += 'Only available in GUI'
    else:
      if verbose:
        conn_info[0].close()
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
