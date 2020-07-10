# -*- coding: utf-8 -*-
import json
import sys
import urllib
from webtest import TestApp


def assert_gen(res, type, param, rt):
    def In(res):
        return (rt in eval(param))

    def eq(res):
        return (eval(param) == rt)

    def gt(res):
        return (eval(param) > rt)

    def lt(res):
        return (eval(param) < rt)

    # nf_lt, nf_gt dbcls-sra-dev apiの検索ヒット数のテスト
    # 例えばresponseにnumfoundが含まれていた場合の例
    def nf_lt(res):
        res_dct = json.loads(eval(param))
        numfound = res_dct["numfound"]
        return (int(numfound) < rt)

    def nf_gt(res):
        res_dct = json.loads(eval(param))
        numfound = res_dct["numfound"]
        return (int(numfound) > rt)

    def nf_eq(res):
        res_dct = json.loads(eval(param))
        numfound = res_dct["numfound"]
        return (int(numfound) == rt)

    return locals()[type](res)


def test_gen(test_name, test_conf):
    def test(self):
        title = test_conf.title
        # test is object include tupls like (type, param, return val)
        try:
            test_app = TestApp(test_conf.test_url)
            params = urllib.parse.quote(test_conf.api)
            res = test_app.get(params)
            test = test_conf.test
            # test is object include tupls like (type, param, return val)
            for t in test:
                assert assert_gen(res, t[0], t[1], t[2])
            print("OK", title)
        except AssertionError:
            print('AssertionError: ', title)
            # any error message action ex. slack_post(title)
        except:
            e = sys.exc_info()[0]
            s = '{} settings'.format(title)
            print("error: ", s, e)
            # any error message action ex. slack_post(s)

    return test


