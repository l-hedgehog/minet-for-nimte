#!/usr/bin/env python

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

import getpass
import sys
import os

# Options dictionary to store user information.
ops = {
  '-u': '',
  '-p': '',
  '-r': '1',
  '-a': '0',
}

# Print the help information.
def usage():
  print '''Usage: minetconf [options]
Options:
  -u <user name>\tUser name
  -p <password>\t\tPassword
  -r <remeber password>\t0:no, 1:yes, default: 1
  -a <auto login>\t0:no, 1:yes, default: 0
  --help \t\tPrint this message
  --show \t\tPrint account string, YOUR PASSWORD WILL BE SHOWN!

Examples:
  minetconf
  minetconf -u ******* -p ******
  
Configure file is saved in ~/.minet/account, use "minetconf --show"
to view your account setting.

MINET 0.2.2 by Hector Zhao <zhaobt@nimte.ac.cn>
'''
  sys.exit(0)

# Get user information from account file.
def show():
  # Get the path to account file, location different for POSIX and Windows.
  if sys.platform == 'win32':
    homedir = os.getenv('HOMEDRIVE')
    homedir += os.getenv('HOMEPATH').decode('gbk').encode('utf8')
  else:
    homedir = os.getenv('HOME')
  minetfname = os.path.join(homedir, '.minet', 'account')
  # Open and read account information from account file.
  if not os.path.isfile(minetfname):
    return False
  else:
    minetfile = open(minetfname, 'r')
    line = minetfile.readline()
    if line == '':
      return False
    minetfile.close()
    return line

# Parse arguments from the command line.
def parse_args(argv):
  i = 1
  while i < len(argv):
    if argv[i].startswith('--'):
      option = argv[i]
      i = i + 1
      if option == '--help':
        usage()
      elif option == '--show':
        ans = show()
        if ans == False:
          print 'You have no saved information. Please reconfig.'
        else:
          print ans
        sys.exit(0)
      else:
        print >>sys.stderr, "Unrecognized option \"%s\", ignored!" % option
        continue
    if argv[i].startswith('-'):
      option = argv[i]
      i = i + 1
      # Put the options start with one '-' into options dictionary.
      if option in ops:
        ops[option] = argv[i]
        i = i + 1
      else:
        print >>sys.stderr, "Unrecognized option \"%s\", ignored!" % option
    else:
      print >>sys.stderr, "Poor option value \"%s\", ignored!" % argv[i]
      i = i + 1
  return True

# Put str into options dictionary.
def input_arg(str, option, p=False):
  if p:
    s = getpass.getpass("%s: " % str)
  else:
    s = raw_input("%s: " % str)
  if s != '':
    ops[option] = s
  return True

# Write account information in options dictionary to account file.
def write_ops():
  # Get the path to account file, location different for POSIX and Windows.
  if sys.platform == 'win32':
    homedir = os.getenv('HOMEDRIVE')
    homedir += os.getenv('HOMEPATH').decode('gbk').encode('utf8')
  else:
    homedir = os.getenv('HOME')
  minetdir = os.path.join(homedir, '.minet')
  minetfname = os.path.join(minetdir, 'account')
  # If application directory does not exist, create it.
  if not os.path.isdir(minetdir):
    os.mkdir(minetdir)
    os.chmod(minetdir, 0700)
  # If account file does not exist, create it.
  if not os.path.isfile(minetfname):
    minetfile = open(minetfname, 'w+')
    os.chmod(minetfname, 0600)
  else:
    minetfile = open(minetfname, 'w+')
  # Format options directory to account string, write it to account file.
  if ops['-r'] == '0':
    line = ops['-u'] + '::'
  else:
    line = ops['-u'] + ':' + ops['-p'] + ':'
  line += ops['-r'] + ':' + ops['-a']
  minetfile.write(line)
  minetfile.close()
  return True

# Main function.
def main(argv=sys.argv, verbose=True):
  # Get user input, interactively or non-interactively.
  if len(argv) > 1:
    parse_args(argv)
    while ops['-u'] == '':
      input_arg('user name', '-u')
    while ops['-p'] == '':
      input_arg('password', '-p')
  else:
    while ops['-u'] == '':
      input_arg('user name', '-u')
    while ops['-p'] == '':
      input_arg('password', '-p', True)
    input_arg('remember password(0:no, 1:yes; default 1)', '-r')
    input_arg('auto login(0:no, 1:yes; default 0)', '-a')
  # If verbose is True(that means 'minetconf' runs alone), print user's
  # information to confirm. Or(that means 'minetconf' is called as a module)
  # do nothing. 
  if verbose:
    print 'You settings:'
    print '  User name: \t%s' % ops['-u']
    print '  Password: \t%s' % 'use "minetconf --show" to check your password'
    print '  Remember passwd(0:no,1:yes): \t%s' % ops['-r']
    print '  Auto login(0:no,1:yes): \t%s' % ops['-a']
  # Write the options to account file.
  write_ops()
  return True

# If 'minetconf' invoked in command line, run main function with no argument.
# Else if 'minetconf' invoked as a module, do nothing.
if __name__ == "__main__":
  main()
