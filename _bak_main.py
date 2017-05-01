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
from google.appengine.api.labs import taskqueue
sys.path.insert(0, 'lib')
import slackweb
from webtest import TestApp

# --Slack Settings--
slack_web_hook = ''  # slack web hook url
slack_channel = ''  # slack channel
slack_user = ''  # slack user
slack = slackweb.Slack(url=slack_web_hook)
slack_pretext = 'something wrong with your service'
slack_title = 'Checked it!'

# --Test settings--
test_url = ''  # your target service url
test_api = '/'  # api
response_min_length = 1000  # int
response_contain = ''  # sting must contain in response

class CheckSites(webapp2.RequestHandler):
    def get(self):
        try:
            test_app = TestApp(test_url)
            res = test_app.get(test_api)
            assert(res.status == '200 OK')
            assert(res.content_type == 'text/html')
            assert(res.content_length > response_min_length)
            assert(response_contain in res)
            #slack_post("nothing")
        except AssertionError as e:
            slack_post(test_url)
        except:
            s = 'test setting'
            slack_post(s)


def slack_post(s):
    slack = slackweb.Slack(url=slack_web_hook)
    attachments = []
    attachment = {"pretext": slack_pretext,
                  "title": slack_title,
                  "text": "Now, "+ s +" is something different.",
                  "mrkdwn_in": ["text", "pretext"]
                  }
    attachments.append(attachment)
    slack.notify(channel=slack_channel, username=slack_user, attachments=attachments)


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Not Found')
    response.set_status(404)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred')
    response.set_status(500)


app = webapp2.WSGIApplication([
    ('/basic_web_test', CheckSites)
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500