import os
# Use the package we installed
import logging
import random

from slack_bolt import App, Say, BoltContext
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)

# creating some hard coded tips
tips = ["Every Accomplishment starts with the decision to try.",
"Being different is one of the most Beautiful things on earth.",
"Creativity is intelligence having fun.",
"The surest way not to fail is to Determine to succeed.",
"The Expert in anything was once a beginner.",
"The best way to predict the Future is to create it.",
"You are never too old to set another Goal or to dream a new dream.",
"There is no substitute for Hard work.",
"Logic will get you from A to Z; Imagination will get you anywhere.",
"A Journey of a thousand miles begins with a single step.",
"The art of being wise is the art of Knowing what to overlook.",
"Today a reader, tomorrow a Leader." ,
"One way to keep Momentum going is to constantly have greater goals."
]

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# This reacts to you calling the bot
# it just prints a message and says something back to you in the channel where you call it
# and in a specified channel "hellothere"


@app.event("app_mention")
def event_test(body, say, logger, client):
    logger.info(body)
    say(f"Hello there <@{body['event']['user']}>")
    channelList = client.conversations_list()

    logger.info("######################")
    logger.info(channelList)
    for l in channelList['channels']:
        if l['name'] == 'hellothere':
            text = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":wave: Hello <@{body['event']['user']}>,\n how are you today? Let me introduce myself: "
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "• I can say hello when you call me\n • I can give a tip if you call /py_tip\n • I can help you introduce yourself in a channel you join"
                        }
                    ]
                }
            ]
            client.chat_postMessage(
                channel=l['id'], user=body['event']['user'], blocks=text)


# whenever a memeber joins a channel they are asked to introduce themselves with buttons
# this would be better if it only happens when a specific channel is joined e.g. the new hackathon channel
# or an intro channel. Maybe you want to try that
@app.event("member_joined_channel")
def event_join(body, say, logger, client):
    text = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hello <@{body['event']['user']}>,\n would you like to introduce yourself a bit? "
            },
            "accessory": {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/approvalsNewDevice.png",
                "alt_text": "computer thumbnail"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "YES"
                    },
                    "action_id": "intro_yes_button",
                    "style": "primary",
                    "value": "yes"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "nope"
                    },
                    "action_id": "intro_nope_button",
                    "style": "danger",
                    "value": "nope"
                }
            ]
        }
    ]
    client.chat_postMessage(
        channel=body['event']['channel'], user=body['event']['user'], blocks=text)

# Implementing the yes button which opens a model which the user can fill out and then overwrites
# the original message


@app.action("intro_yes_button")
def yes_button(body, action, logger, client, ack):
    ack()

    ## triggering a modal view
    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "intro_modal",
            "title": {"type": "plain_text", "text": "My Intro",},
            "submit": {"type": "plain_text", "text": "Submit",}, # has a submit button is optional, that submit will trigger callback_id
            "close": {"type": "plain_text", "text": "Cancel",},
            "private_metadata": f"{body['channel']['id']},{body['message']['ts']}", ## stored so we can update the original message
            "blocks": [ ## create 4 input fields
                {
                    "type": "input",
                    "block_id":"where",
                    "element": {"type": "plain_text_input", "action_id": "where"},
                    "label": {"type": "plain_text", "text": "Where are you from?",},
                },
                {
                    "type": "input",
                    "block_id":"you",
                    "element": {"type": "plain_text_input", "action_id": "you"},
                    "label": {"type": "plain_text", "text": "Tell us about yourself",},
                },
                {
                    "type": "input",
                    "block_id":"learn",
                    "element": {"type": "plain_text_input", "action_id": "learn"},
                    "label": {"type": "plain_text", "text": "What do you want to learn",},
                },
                {
                    "type": "input",
                    "block_id":"project",
                    "element": {"type": "plain_text_input", "action_id": "project"},
                    "label": {"type": "plain_text", "text": "What project would you like to work on?",},
                }
            ],
        },
    )


    logger.info(res)

### reads out our simple modal and formats the result a bit
@app.view('intro_modal')
def intro_modal_submitted(body, ack, logger, client):
	ack()
	logger.info("Modal Submitted")

	## reading the data from the input fields
	you = body['view']['state']['values']['you']['you']['value']
	learn = body['view']['state']['values']['learn']['learn']['value']
	where = body['view']['state']['values']['where']['where']['value']
	project = body['view']['state']['values']['project']['project']['value']

	# reading metadata from the original channel and ts that was added 
	data = body['view']['private_metadata'].split(',')
	block = [
		        {
		            "type": "section",
		            "text": {
		                "type": "mrkdwn",
		                "text": f"<@{body['user']['id']}> INTRO"
		            }
		        },
		        {
		            "type": "section",
		            "text": {
		                "type": "mrkdwn",
		                "text": f"*From:* \n {where}"
		            }
		        },
		        {
		            "type": "section",
		            "text": {
		                "type": "mrkdwn",
		                "text": f"*Who I am:* \n {you}"
		            }
		        },
		        {
		            "type": "section",
		            "text": {
		                "type": "mrkdwn",
		                "text": f"*What I want to learn:* \n {learn}"
		            }
		        },
		        {
		            "type": "section",
		            "text": {
		                "type": "mrkdwn",
		                "text": f"*What I want to work on:* \n {project}"
		            }
		        }
	        ]
	client.chat_update(channel=data[0],
                       ts=data[1], blocks=block)

# print shame on you when they do not want to introduce themselves
@app.action("intro_nope_button")
def yes_button(body, action, logger, client, ack):
    ack()

    # creating a new message which has parts of the old messag and adds a section
    oldMessage = [body['message']['blocks'][0]]
    oldMessage.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"You said nope, SHAME on you!"
        }
    })

    # we are updating an existing message here and remove the buttons
    client.chat_update(channel=body['channel']['id'],
                       ts=body['message']['ts'], blocks=oldMessage)

# waits for slash command, if command comes checks if it has arguments
# if not prints a tip if arguments adds a new tip


@app.command("/motivateme")
def motivation_called(body, command, logger, client, ack):
    ack()
    logger.info("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    logger.info(command)
    tip = random.choice(tips)
    client.chat_postMessage(channel=command['channel_id'], user=command['user_id'], text=tip)

    


def checkKey(dict, key):

    if key in dict.keys():
        return True
    else:
        return False


# With this you can create a simple App home
# You need to go to App home on Slack and enable App home so that you can listen to this event

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:

        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id = event["user"],
            # the view object that appears in the app home
            view = {
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "action_id": "HelloThere",
                                "type": "button",
                                "style": "primary",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me now!"
                                }
                            },
                            {
                                # this button is not implemented you can implement it in the same was as HelloThere
                                "action_id": "whythere2",
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me now2!"
                                }
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

# Example button for button on App home which just posts a message to the user in the
# apps user channel
@app.action("HelloThere")
def react_to_button(body, logger, client):
    logger.info(body)
    client.chat_postMessage(
        channel=body["user"]["id"], text="You pushed a button!")

# Not used in our app, to use it you would need to subscribe to the message.channels event
# to bot then listens to all public messages and replies if you write "test"

# @app.message("test")
# def reply_to_test(say):
#     say("Yes, tests are important!")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

