# tests from http://code.google.com/p/jsonpath/wiki/Javascript
# $Id: test3.py,v 1.5 2018/10/27 20:03:33 phil Exp $

from __future__ import print_function
import sys
import jsonpath
import jsonmatch

# For python3 portability
if sys.version_info[0] == 3:
    xrange = range

json = \
{ "store": {
        "book": [
                { "category": "reference",
                      "author": "Nigel Rees",
                      "title": "Sayings of the Century",
                      "price": 8.95
                },
                { "category": "fiction",
                      "author": "Evelyn Waugh",
                      "title": "Sword of Honour",
                      "price": 12.99
                },
                { "category": "fiction",
                      "author": "Herman Melville",
                      "title": "Moby Dick",
                      "isbn": "0-553-21311-3",
                      "price": 8.99
                },
                { "category": "fiction",
                      "author": "J. R. R. Tolkien",
                      "title": "The Lord of the Rings",
                      "isbn": "0-395-19395-8",
                      "price": 22.99
                }
              ],
              "bicycle": {
                "color": "red",
                "price": 19.95
              }
        }
}

tests = [
        "$.store.book[*].author",
        "$..author",
        "$.store.*",
        "$.store..price",
        "$..book[(@.length-1)]",
        "$..book[-1:]",
        "$..book[0,1]",
        "$..book[:2]",
        "$..book[?(@.isbn)]",
        "$..book[?(@.price<10)]",
#        "$..*"
]

values = [
# 0
        ["Nigel Rees","Evelyn Waugh","Herman Melville","J. R. R. Tolkien"],
# 1
        ["Nigel Rees","Evelyn Waugh","Herman Melville","J. R. R. Tolkien"],
# 2
        [[{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99},{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99},{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],{"color":"red","price":19.95}],
# 3
        [8.95,12.99,8.99,22.99,19.95],
# 4
        [{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],
# 5
        [{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],
# 6
        [{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99}],
# 7
        [{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99}],
# 8
        [{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99},{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],
# 9
        [{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99}],
# 10
#       [{"book":[{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99},{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99},{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],"bicycle":{"color":"red","price":19.95}},[{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99},{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99},{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99}],{"color":"red","price":19.95},{"category":"reference","author":"Nigel Rees","title":"Sayings of the Century","price":8.95},{"category":"fiction","author":"Evelyn Waugh","title":"Sword of Honour","price":12.99},{"category":"fiction","author":"Herman Melville","title":"Moby Dick","isbn":"0-553-21311-3","price":8.99},{"category":"fiction","author":"J. R. R. Tolkien","title":"The Lord of the Rings","isbn":"0-395-19395-8","price":22.99},"reference","Nigel Rees","Sayings of the Century",8.95,"fiction","Evelyn Waugh","Sword of Honour",12.99,"fiction","Herman Melville","Moby Dick","0-553-21311-3",8.99,"fiction","J. R. R. Tolkien","The Lord of the Rings","0-395-19395-8",22.99,"red",19.95]
]

paths = [
    ["$['store']['book'][0]['author']","$['store']['book'][1]['author']","$['store']['book'][2]['author']","$['store']['book'][3]['author']"],
    ["$['store']['book'][0]['author']","$['store']['book'][1]['author']","$['store']['book'][2]['author']","$['store']['book'][3]['author']"],
    ["$['store']['book']","$['store']['bicycle']"],
    ["$['store']['book'][0]['price']","$['store']['book'][1]['price']","$['store']['book'][2]['price']","$['store']['book'][3]['price']","$['store']['bicycle']['price']"],
    ["$['store']['book'][3]"],
    ["$['store']['book'][3]"],
    ["$['store']['book'][0]","$['store']['book'][1]"],
    ["$['store']['book'][0]","$['store']['book'][1]"],
    ["$['store']['book'][2]","$['store']['book'][3]"],
    ["$['store']['book'][0]","$['store']['book'][2]"],
#    ["$['store']","$['store']['book']","$['store']['bicycle']","$['store']['book'][0]","$['store']['book'][1]","$['store']['book'][2]","$['store']['book'][3]","$['store']['book'][0]['category']","$['store']['book'][0]['author']","$['store']['book'][0]['title']","$['store']['book'][0]['price']","$['store']['book'][1]['category']","$['store']['book'][1]['author']","$['store']['book'][1]['title']","$['store']['book'][1]['price']","$['store']['book'][2]['category']","$['store']['book'][2]['author']","$['store']['book'][2]['title']","$['store']['book'][2]['isbn']","$['store']['book'][2]['price']","$['store']['book'][3]['category']","$['store']['book'][3]['author']","$['store']['book'][3]['title']","$['store']['book'][3]['isbn']","$['store']['book'][3]['price']","$['store']['bicycle']['color']","$['store']['bicycle']['price']"]
]

def test_data():
    assert len(tests) == len(values)
    assert len(tests) == len(paths)

def test_it():
    debug = False
    for i in xrange(0, len(tests)):
        if debug: print(">>>", i, tests[i])
        v = jsonpath.jsonpath(json, tests[i])
        assert jsonmatch.jsonmatch(v, values[i])
        p = jsonpath.jsonpath(json, tests[i], "PATH")
        assert jsonmatch.jsonmatch(p, paths[i])
        if debug: print("OK")
    print(len(tests), "tests passed")
