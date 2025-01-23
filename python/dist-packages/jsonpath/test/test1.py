# tests from Perl version of jsonpath: JSONPathTest.pm
# at http://github.com/masukomi/jsonpath-perl/tree/master
# $Id: test1.py,v 1.6 2018/10/27 20:03:33 phil Exp $

from __future__ import print_function
import jsonpath
import jsonmatch

test = \
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

def check_normalize(input, expected):
    got = jsonpath.normalize(input)
    assert got == expected

def test_normalize_author():
    check_normalize('$..author', '$;..;author')

def test_normalize_store_book_author():
    check_normalize('$.store.book[*].author', '$;store;book;*;author')

def test_normalize_store_star():
    check_normalize('$.store.*', '$;store;*')

def test_normalize_book_2():
    check_normalize('$..book[2]', '$;..;book;2')

def test_normalize_book_last():
    check_normalize('$..book[(@.length-1)]', '$;..;book;(@.length-1)')

def test_normalize_book_last_to():
    check_normalize('$..book[-1:]', '$;..;book;-1:')

def test_normalize_book_zero_one():
    check_normalize('$..book[0,1]', '$;..;book;0,1')

def test_normalize_book_zero_to_two():
    check_normalize('$..book[:2]', '$;..;book;:2')

def test_normalize_book_isbn():
    check_normalize('$..book[?(@.isbn)]', '$;..;book;?(@.isbn)')

def test_normalize_book_price_lt_10():
    check_normalize('$..book[?(@.price<10)]', '$;..;book;?(@.price<10)')

def test_normalize_store_price():
    check_normalize('$.store..price', '$;store;..;price')

def test_normalize_dotdot_star():
    check_normalize('$..*', '$;..;*')

def check_array(expr, exp_len, expected=None):
    result = jsonpath.jsonpath(test, expr)
    assert result != 0
    assert len(result) == exp_len
    if expected is not None:
        assert jsonmatch.jsonmatch(result, expected)
    return result

def test_array_book_authors():
    check_array('$.store.book[*].author', 4)

def test_array_authors():
    check_array('$..author', 4)

def test_array_price_lt_10():
    result = check_array('$..book[?(@.price<10)]', 2)
    expected = [
    	{"category":"reference", "author":"Nigel Rees", "title":"Sayings of the Century", "price":8.95}, 
        {"category":"fiction", "author":"Herman Melville", "title":"Moby Dick", "isbn":"0-553-21311-3", "price":8.99}
    ]

    for book in result:
        assert 'category' in book
        assert 'author' in book
        assert 'title' in book
        assert 'price' in book
        if 'isbn' in book:
            # moby dick
            assert 8.99 == book['price']
            assert 'Moby Dick' == book['title']
        else:
            #sayings of the century
            assert 8.95 == book['price']
            assert 'Sayings of the Century' == book['title']

def test_array_store():
    check_array('$.store.*', 2)       #book array and one bicycle

def test_array_store_prices():
    #the price of everything (value of nothing?)
    check_array('$.store..price', 5, [ 8.95, 12.99, 8.99, 22.99, 19.95 ])

def test_array_book_zero_one():
    check_array('$..book[0,1]', 2)

def test_array_book_zero_two():
    check_array('$..book[:2]', 2)

def test_array_book_five():
    assert jsonpath.jsonpath(test, '$..book[5]') is False

def test_array_book_isbn():
    check_array('$..book[?(@.isbn)]', 2)

def test_array_store_keys():
    check_array('$.store.!', 2)       #the keys in the store hash 

def test_array_star():
    check_array('$..*', 27)

