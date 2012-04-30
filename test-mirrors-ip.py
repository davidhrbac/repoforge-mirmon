#!/usr/bin/python
#
# This is a Python script that tests mirrors to see if there are any
# duplicates within.
#
# The first argument should be the path to the mirror database (e.g. 
# mirrors.list).

import sys
import string
import os
import re
import socket

verbose = 0
timeout = 10
ips= {} 
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
  print "Opening mirror database " + sys.argv[1] + "..."

f = open(sys.argv[1])
lines = f.readlines()

for line in lines:
  line = string.strip(line)
  splitline = string.split(line)

  mcountry = splitline[0]

  p = re.compile(r'^(f|ht)tp://(?P<hn>[^/]*)/?.*$')
  m = p.search(splitline[1])

  mname = m.group('hn')

  if verbose:
    print "Checking mirror " + mname + " [" + mcountry + "]..."

  try:
    mip = socket.gethostbyname_ex(mname)[2][0]
  except (socket.error, socket.gaierror):
    raise MirrorError, "Unable to determine IP address"

  if verbose:
    print "Got IP address: " + mip

  if mip in ips:
    ips[mip]=ips[mip] + " " + mname 
  else:
    ips[mip]=mname

for ip in ips:
  names=ips[ip].split()
  if len(names)>1:
    print "Duplicate IP found: " + ip
    for name in names:
      print "\t" + name

sys.exit()
