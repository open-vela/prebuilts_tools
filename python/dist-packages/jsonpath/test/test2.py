# tests from
# http://jsonpath.googlecode.com/svn/trunk/tests/jsonpath-test-js.html
# $Id: test2.py,v 1.6 2018/10/27 20:03:33 phil Exp $

from __future__ import print_function
import sys
import jsonpath
import re

# For python3 portability
if sys.version_info[0] == 3:
    xrange = range

tests = \
[
# 0
  { "o": { "a": "a",
           "b": "b",
           "c d": "e" 
         },
    "p": [ "$.a",
           "$['a']",
           "$.'c d'",
           "$.*",
           "$['*']" ,
           "$[*]"
         ],
    "r": [
            ["$['a']"],
            ["$['a']"],
            ["$['c d']"],
            ["$['a']", "$['b']", "$['c d']"],
            ["$['a']", "$['b']", "$['c d']"],
            ["$['a']", "$['b']", "$['c d']"]
         ]
  },
# 1
  { "o": [ 1, "2", 3.14, True, None ],
    "p": [ "$[0]",
           "$[4]",
           "$[*]",
	   "$[-1:]"
         ],
    "r" : [
            ["$[0]"],
            ["$[4]"],
            ["$[0]", "$[1]", "$[2]", "$[3]", "$[4]"],
            ["$[4]"]
          ]
  },
# 2
  { "o": { "points": [
             { "id": "i1", "x":  4, "y": -5 },
             { "id": "i2", "x": -2, "y":  2, "z": 1 },
             { "id": "i3", "x":  8, "y":  3 },
             { "id": "i4", "x": -6, "y": -1 },
             { "id": "i5", "x":  0, "y":  2, "z": 1 },
             { "id": "i6", "x":  1, "y":  4 }
           ]
         },
    "p": [ "$.points[1]",
           "$.points[4].x",
           "$.points[?(@.id=='i4')].x",
           "$.points[*].x",
           "$['points'][?(@.x*@.x+@.y*@.y > 50)].id",
           "$.points[?(@.z)].id",
           "$.points[(@.length-1)].id"
         ],
    "r": [
            ["$['points'][1]"],
            ["$['points'][4]['x']"],
            ["$['points'][3]['x']"],
            ["$['points'][0]['x']", "$['points'][1]['x']",
             "$['points'][2]['x']", "$['points'][3]['x']",
             "$['points'][4]['x']", "$['points'][5]['x']"],
            ["$['points'][2]['id']"],
            ["$['points'][1]['id']", "$['points'][4]['id']"],
            ["$['points'][5]['id']"]
         ]
  },
# 3
  { "o": { "menu": {
             "header": "SVG Viewer",
             "items": [
                 {"id": "Open"},
                 {"id": "OpenNew", "label": "Open New"},
                 None,
                 {"id": "ZoomIn", "label": "Zoom In"},
                 {"id": "ZoomOut", "label": "Zoom Out"},
                 {"id": "OriginalView", "label": "Original View"},
                 None,
                 {"id": "Quality"},
                 {"id": "Pause"},
                 {"id": "Mute"},
                 None,
                 {"id": "Find", "label": "Find..."},
                 {"id": "FindAgain", "label": "Find Again"},
                 {"id": "Copy"},
                 {"id": "CopyAgain", "label": "Copy Again"},
                 {"id": "CopySVG", "label": "Copy SVG"},
                 {"id": "ViewSVG", "label": "View SVG"},
                 {"id": "ViewSource", "label": "View Source"},
                 {"id": "SaveAs", "label": "Save As"},
                 None,
                 {"id": "Help"},
                 {"id": "About", "label": "About Adobe CVG Viewer..."}
             ]
           }
         },
    "p": [ "$.menu.items[?(@ and @.id and !@.label)].id",
# want "re.match(r'SVG', @.label)" -- but it contains a comma!!!!
           "$.menu.items[?(re.search(r'SVG', @.label))].id",
           "$.menu.items[?(not @)]",
           "$..[0]"
         ],
    "r": [
            ["$['menu']['items'][0]['id']", "$['menu']['items'][7]['id']",
             "$['menu']['items'][8]['id']", "$['menu']['items'][9]['id']",
             "$['menu']['items'][13]['id']", "$['menu']['items'][20]['id']"],
            ["$['menu']['items'][15]['id']", "$['menu']['items'][16]['id']"],
            ["$['menu']['items'][2]", "$['menu']['items'][6]",
             "$['menu']['items'][10]", "$['menu']['items'][19]"],
            ["$['menu']['items'][0]"]
         ]
  },
# 4
  { "o": { "a": [1,2,3,4],
           "b": [5,6,7,8]
         },
    "p": [ "$..[0]",
           "$..[-1:]",
           "$..[?(@%2==0)]"
         ],
    "r": [
            ["$['a'][0]", "$['b'][0]"],
            ["$['a'][3]", "$['b'][3]"],
            ["$['a'][1]", "$['a'][3]", "$['b'][1]", "$['b'][3]"]
         ]
  },
# 5
  { "o": { "lin": {"color":"red", "x":2, "y":3},
           "cir": {"color":"blue", "x":5, "y":2, "r":1 },
           "arc": {"color":"green", "x":2, "y":4, "r":2, "phi0":30, "dphi":120 },
           "pnt": {"x":0, "y":7 }
         },
    "p": [ "$.'?(@.color)'.x",
           "$['lin','cir'].color"
         ],
    "r": [
            ["$['cir']['x']", "$['lin']['x']", "$['arc']['x']"],
            ["$['lin']['color']", "$['cir']['color']"]
         ]
  },
# 6
  { "o": { "lin": {"color":"red", "x":2, "y":3},
           "cir": {"color":"blue", "x":5, "y":2, "r":1 },
           "arc": {"color":"green", "x":2, "y":4, "r":2, "phi0":30, "dphi":120 },
           "pnt": {"x":0, "y":7 }
         },
    "p": [ "$.'?(@.color)'.x",
           "$['lin','arc'].color"
         ],
    "r": [
            ["$['cir']['x']", "$['lin']['x']", "$['arc']['x']"],
            ["$['lin']['color']", "$['arc']['color']"]
         ]
  },
# 7
  { "o": { "text": [ "hello", "world2.0"] },
    "p": [ "$.text[?(@.length > 5)]",
           # was @.charAt(0):
           "$.text[?(@[0] == 'h')]"
         ],
    "r": [
            ["$['text'][1]"],
            ["$['text'][0]"]
         ]
  },
# 8
  { "o": { "a": { "a":2, "b":3 },
           "b": { "a":4, "b":5 },
           "c": { "a": { "a":6, "b":7}, "c":8}
         },
    "p": [ "$..a"
         ],
    "r": [
            ["$['a']", "$['a']['a']", "$['c']['a']",
             "$['c']['a']['a']", "$['b']['a']"]
         ]
  },
# 9
  { "o": { "a": [ { "a":5, '@':2, '$':3 },   # issue 7: resolved by escaping the '@' character 
                { "a":6, '@':3, '$':4 },   # in a JSONPath expression.
                { "a":7, '@':4, '$':5 } 
              ]
         },
    "p": [ "$.a[?(@['\\@']==3)]",
           "$.a[?(@['$']==5)]"
         ],
    "r": [
            ["$['a'][1]"],
            ["$['a'][2]"]
         ]
  }
]

def fetch(obj, path):
    str = "obj" + path[1:]
    return eval(str)

def test_it():
    n = 0
    debug = False
    for t in tests:
        obj = t['o']
        for i in xrange(0, len(t['p'])):
            path = t['p'][i]
            expect = t['r'][i]
            res = jsonpath.jsonpath(obj, path, "PATH")
            if 'r' in t:
                assert(sorted(res) == sorted(expect))

            if debug and res:
                for op in res:
                    print(" %s => %s" % (op, fetch(obj, op)))
        n += 1
    print(n, "tests passed")
