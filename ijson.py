#!/usr/bin/env python
#
# a parser for the ijson file format.
#
# Copyright (c) 2014 Dov Grobgeld <https://github.com/dov>
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
# 
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#

from pyparsing import *
import json
import collections
import re

# The following "magic" allows "dot access" to xnm files.
class dotdict(dict):
    def __init__(self):
        dict.__init__(self)
        self._mykeys = {}
        self._myorder = []

    def __getattr__(self, attr):
        return self.get(attr)

    def __dir__(self):
        return self.keys()

    def __setitem__(self, k, v):
        if not k in self.keys():
            self._myorder.append(k)
        dict.__setitem__(self,k,v)
        
    def iteritems(self):
        for k in self._myorder:
            yield k,self[k]

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)
        
def dotdictify(results):
    if isinstance(results, dict):
        res = dotdict()

        # Access as a list to get original order
        for kv in results.iteritems():
            k,v = kv
            res[k] = dotdictify(v)
        return res
    elif isinstance(results, list) or isinstance(results, tuple):
      return [
        dotdictify(v) for v in results
      ]
    return results

def load(hdl):
    return loads(hdl.read())

def loads(s):
    return dotdictify(json.loads(s))

def dumps(s, indent=2):
    return json.dumps(s, indent=indent)

if __name__=='__main__':
    a = { 'a':3,'b':4 }

    ja = loads(dumps(a))
    print ja.a
    
    
    
