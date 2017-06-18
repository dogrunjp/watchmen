
import sys
import webapp2
import logging
import json
sys.path.insert(0, 'lib')

import slackweb
from webtest import TestApp
from bunch import Bunch


# --API settings--
cron_path = ''  # path for cron - as you like

# --Slack Settings--
slack_web_hook = '' # fill your slack web hook url
slack_channel = ''
slack_user = ''
slack = slackweb.Slack(url=slack_web_hook)
slack_pretext = ''
slack_title = ''

# --Test confs--
tests = Bunch.fromDict({
        'test1': {
            'title': 'Test 1',
            'test_url': 'http://xxx',
            'api': '/',
            'test': [('eq', 'res.status', '200 OK'), ('eq', 'res.content_type', 'application/json'), ('In', 'res', 'body')]
        },
        'test2': {
            'title': 'Test 2',
            'test_url': 'http://xxx',
            'api': '/xxx',
            'test': [('gt', 'res.content_length', 30000),('eq', 'res.status', '200 OK'), ('In', 'res', 'h1')]
        }
    })

# 'test' value is valriable length list of tuple.
# each tuple can contain 3 element( type, response element, expected value of response element).


# Target class
class DynamicTest():
    pass


def assert_gen(res, type, param, rt):
    res = res
    def In(res):
        return (rt in eval(param))

    def eq(res):
        return (eval(param) == rt)

    def gt(res):
        return (eval(param) > rt)

    return locals()[type](res)


def test_gen(test_name):
    def test(self):
        title = tests[test_name].title
        # test is object include tupls like (type, param, return val)
        try:
            test_app = TestApp(tests[test_name].test_url)
            res = test_app.get(tests[test_name].api)
            test = tests[test_name].test
            # test is object include tupls like (type, param, return val)
            for t in test:
                assert assert_gen(res, t[0], t[1], t[2])
        except AssertionError:
            slack_post(title)

        except:
            s = '{} settings'.format(title)
            slack_post(s)
    return test


class ApiTest(webapp2.RequestHandler):
    def get(self):
        for k, v in tests.iteritems():
            test_name = k
            test_item = test_gen(test_name)
            # create test instance with test_gene()
            setattr(DynamicTest, test_name, test_item)

        # get method name
        methods = [method for method in dir(DynamicTest) if callable(getattr(DynamicTest, str(method)))]
        dt = DynamicTest()
        for m in methods:
            print(m)
            getattr(dt, m)()


def slack_post(s):
    slack = slackweb.Slack(url=slack_web_hook)
    attachments = []
    attachment = {"pretext": slack_pretext,
                  "title": slack_title,
                  "text": "Now, " + s + " is something different.",
                  "mrkdwn_in": ["text", "pretext"]
                  }
    attachments.append(attachment)
    slack.notify(channel=slack_channel, username=slack_user, attachments=attachments)


app = webapp2.WSGIApplication([
    (cron_path, ApiTest)
], debug=True)
