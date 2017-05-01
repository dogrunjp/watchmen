#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

import sys
import webapp2
import logging
import unittest
sys.path.insert(0, 'lib')

import slackweb
from webtest import TestApp
from bunch import Bunch

# --Slack Settings--
slack_web_hook = ''
slack_channel = ''
slack_user = ''
slack = slackweb.Slack(url=slack_web_hook)
slack_pretext = 'something wrong with your service'
slack_title = 'Checked it!'

# --Test settings--
test = Bunch.fromDict({
        'test1': {
        'title': '',
        'test_url': 'http://',
        'api': '/',
        'response_min_length': 30000,
        'response_contain': 'hoge'
        },
        'test2': {
            'title': '',
            'test_url': 'http://',
            'api': '/',
        }
    })


class WebTest(webapp2.RequestHandler):
    def get(self):
        try:
            test_app = TestApp(test.aoe.test_url)
            res = test_app.get(test.aoe.api)
            assert (res.status == '200 OK')
            assert (res.content_type == 'text/html')
            assert (res.content_length > test.test1.response_min_length)
            assert (test.test1.response_contain in res)
            #slack_post("nothing")
        except AssertionError:
            slack_post(test.test1.test_url)
        except:
            s = 'test {} setting'.format(test.test1.title)
            slack_post(s)


class ApiTest(unittest.TestCase):
    def test_api_root(self):
        test_app = TestApp(test.test2.test_url)
        res = test_app.get(test.test2.api)
        try:
            self.assertEqual(res.status, '200 OK', msg=res.status)
            self.assertEqual(res.content_type, 'application/json', msg=res.content_type)
            slack_post("nothing")
        except AssertionError:
            slack_post(test.test2.test_url)
        except:
            s = 'test {} setting'.format(test.test2.title)
            slack_post(s)


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


class TestHandler(webapp2.RequestHandler):
    def get(self):
        my_suit = suite()
        runner = unittest.TextTestRunner()
        runner.run(my_suit)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(ApiTest))
    return test_suite


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Not Found')
    response.set_status(404)


def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred')
    response.set_status(500)


app = webapp2.WSGIApplication([
    ('/web_test', WebTest),
    ('/tests', TestHandler)
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
