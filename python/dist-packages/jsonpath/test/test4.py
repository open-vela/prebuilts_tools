# From: Petr Szturc
# Wed, 26 Jun 2019 18:00:03 +0200

from __future__ import print_function
from jsonpath import jsonpath

DATA = {
    "offers": [
        {
            "customFields": {
                "TestCustomField1Name": "TestCustomFieldValue1"
            }
        },
        {
            "customFields": {
                "TestCustomField1Name": "TestCustomFieldValue2"
            }
        }
    ]
}


def test_it():
    res = jsonpath(DATA, "$.offers[?(@.customFields.TestCustomField1Name == 'TestCustomFieldValue1')]", debug=True)
    print(res)

if __name__ == '__main__':
    test_it()
