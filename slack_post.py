import slackweb
import yaml

with open('config_sample.yaml') as f:
    conf = yaml.safe_load(f)


def slack_post(s):
    slack = slackweb.Slack(url=conf.slack_web_hook)
    attachments = []
    attachment = {"pretext": conf.slack_pretext,
                  "title": conf.slack_title,
                  "text": "Now, " + s + " is something different.",
                  "mrkdwn_in": ["text", "pretext"]
                  }
    attachments.append(attachment)
    slack.notify(channel=conf.slack_channel, username=conf.slack_user, attachments=conf.attachments)
