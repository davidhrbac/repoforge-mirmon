#!/usr/local/bin/python
#
# =============================================================================
#
#   Copyright 2005 The Apache Software Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# =============================================================================
#
# This is a Python script that tests mirrors to see if their IP address
# is actually located in the country specified in the database. Lookups are
# done with GeoIP.
#
# The first argument should be the path to the mirror database (e.g. 
# mirrors.list).

import timeoutsocket
import sys
import string
import os
import re
import socket
import GeoIP

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

# If a mirror doesn't respond in this time, consider it dead.
timeoutsocket.setDefaultSocketTimeout(timeout)

if verbose:
  print "Opening mirror database " + sys.argv[1] + "..."

f = open(sys.argv[1])
lines = f.readlines()

for line in lines:
  line = string.strip(line)
  splitline = string.split(line)

  mcountry = splitline[1]

  p = re.compile(r'^(f|ht)tp://(?P<hn>[^/]*)/?.*$')
  m = p.search(splitline[2])

  mname = m.group('hn')

  if verbose:
    print "Checking mirror " + mname + " [" + mcountry + "]..."

  try:
    try:
      mip = socket.gethostbyname_ex(mname)[2][0]
    except (socket.error, socket.gaierror):
      raise MirrorError, "Unable to determine IP address"

    if verbose:
      print "Got IP address: " + mip

    gi = GeoIP.new(GeoIP.GEOIP_STANDARD)
    region = string.strip(string.lower(gi.country_code_by_addr(mip)))

    if region == 'gb':
      region = 'uk'

    if not region == mcountry:
      raise MirrorError, "Actual mirror location [" + region + \
                         "] does not match reference [" + mcountry + "]"

  except timeoutsocket.Timeout:
    print "*** ERROR for " + mname + " [" + mcountry + "]:"
    print "Connection timed out"

  except (IOError, TypeError, MirrorError), msg:
    print "*** ERROR for " + mname + " [" + mcountry + "]:"
    print msg

sys.exit()
