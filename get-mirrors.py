#!/usr/bin/python
#
# This is a Python script to parse state.txt file.
#
# The first argument should be the path to the mirmon state (e.g. 
# state.txt).

import sys
import string
import os
import re
import socket
import time

verbose = 0
timeout = 10

error = __name__ + '.error'

class MirrorError (Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return `self.value`

try:
  sys.argv[1]
except IndexError:
  print "Usage: " + sys.argv[0] + " <mirror-database>"
  sys.exit(0)

if verbose:
  print "Opening state database " + sys.argv[1] + "..."

f = open(sys.argv[1])
lines = f.readlines()

for line in lines:
  line = string.strip(line)
  splitline = string.split(line)

  if splitline[2]=='ok':
    url = splitline[0]
    #age = time.ctime(int(splitline[1]))
    age = int(splitline[1])
  
    p = re.compile(r'^(f|ht)tp://(?P<hn>[^/]*)/?.*$')
    m = p.search(splitline[0])
  
    mname = m.group('hn')

    if time.time()-age<=18*60*60:
      if verbose:
        print "Allowing mirror " + mname + " [" +  time.ctime(age) + "]"
      else:
        print url
  
sys.exit()
