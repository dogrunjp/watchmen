from flask import Flask
import logging
import json
import inspect
import watchmen

# API
API_ROOT = 'http://hoge.dotcom'

class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


# --Test confs--
# Webtestがhttpsは対応していないかも
tests = {
    'sample-1': {
        'title': 'sample-1',
        'test_url': API_ROOT,
        'api': '/api',
        'test': [('eq', 'res.status', '200 OK'), ('eq', 'res.content_type', 'application/json')]
    },
    'sample-2':{
        'title': 'sample-2',
        'test_url': API_ROOT,
        'api': '/api/search?term=tenpura',
        'test': [('eq', 'res.status', '200 OK'), ('In', 'res.body', "some sords")]
    },
    'sample-3':{
        'title': 'sample-3',
        'test_url': API_ROOT,
        'api': '/api/search?days=2',
        'test': [('eq', 'res.status', '200 OK'), ('nf_eq', 'res.body', 10)]
    }

}

tests = DotDict(tests)


# Target class
class DynamicTest():
    pass


def main():
    for k, v in tests.items():
        test_item = watchmen.test_gen(k, v)
        # create test instance with test_gene()
        setattr(DynamicTest, k, test_item)

    # get method name
    methods = [method for method in inspect.getmembers(DynamicTest, inspect.isfunction)]
    dt = DynamicTest()
    for m in methods:
        # DynamicTest()に登録された関数を実行
        getattr(dt, m[0])()


main()
