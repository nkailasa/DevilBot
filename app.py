import os
import logging
import random
from datetime import datetime, timedelta 

from slack_bolt import App, Say, BoltContext
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)

# creating some hard coded motivations
motivations = ["Every Accomplishment starts with the decision to try.",
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
#@DevilBot to initiate your interaction with the bot(Think of it as the power button to switch the bot on!)
#It will greet you with a usual morning message and asks for your choice in the channel where you call it


@app.event("app_mention")
def event_test(body, say, logger, client):
    say(f"Good Morning <@{body['event']['user']}>. Please make sure you are in #general channel to proceed further")
    channelList = client.conversations_list()

    logger.info("######################")
    logger.info(channelList)
    for l in channelList['channels']:
        if l['name'] == 'general':
            text = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":wave: <@{body['event']['user']}>,\n how are you today fellow Sun Devil? How can I help you?: "
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
                            "text": "• I can greet you when you call me\n • I can motivate you when you call /motivateme\n • I can show you the list of assignments you have due today"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                "type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Let's do assignments",
						"emoji": True
					},
					"value": "yes",
                    "action_id": "proceed_button"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Not today",
						"emoji": True
					},
					"value": "no",
                    "action_id": "halt_button",
					"url": "https://youtube.com"
				}
			]
                }
            ]
            client.chat_postMessage(
                channel=l['id'], user=body['event']['user'], blocks=text)
                       
@app.action("proceed_button")
def proceed_button(body, action, logger, client, ack):
    ack()
    block = [{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Brace up! You are about to see a list of Assignments and Due Dates"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [{
						"text": {
							"type": "mrkdwn",
							"text": "*SER 515 - Reliability and Safety*"
						},
						"description": {
							"type": "mrkdwn",
							"text": "*Due today*"
						},
						"value": "515"
					},
					{
						"text": {
							"type": "mrkdwn",
							"text": "*CSE 564 - Design Patterns*"
						},
						"description": {
							"type": "mrkdwn",
							"text": "*Due tomorrow*"
						},
						"value": "564"
					},
					{
						"text": {
							"type": "mrkdwn",
							"text": "*CSE 565 - Usability Testing*"
						},
						"description": {
							"type": "mrkdwn",
							"text": "*Due 12/15/2020*"
						},
						"value": "565"
					}
				],
				"action_id": "checkboxes-action"
			}
		}
	]
 
    client.chat_postMessage(channel=body['channel']['id'],
                       ts=body['message']['ts'], blocks=block)

@app.action("checkboxes-action")
def checkboxes_action(body, action, logger, client, ack):
    ack()
    completed = ""
    for option in action['selected_options']:
        completed+=","
        completed+=option['text']['text']
    
   
    oldMessage = [body['message']['blocks'][0]]
    oldMessage.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"WOW! Let's forget about {completed} now!"
        }
    })
    logger.info(len(action['selected_options']))
    
    if len(action['selected_options']) == 3:
        oldMessage.append({
        "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*You are a warrior!! It's time to rest!*"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "I Know!",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "url": "https://www.youtube.com/watch?v=y-HKSdLms8Y",
                    "action_id": "button-action"
                }
        })
    

    
    client.chat_postMessage(channel=body['channel']['id'],
                       ts=body['message']['ts'], blocks=oldMessage)
                       
# print shame on you when they do not want to do assignments
@app.action("halt_button")
def halt_button(body, action, logger, client, ack):
    ack()

    
    oldMessage = [body['message']['blocks'][0]]
    oldMessage.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"You are procrastinating, SHAME on you!"
        }
    })

    
    client.chat_postMessage(channel=body['channel']['id'],
                       ts=body['message']['ts'], blocks=oldMessage)



@app.view('Reminder_back')
def reminder_Submited(body, command,ack,  logger, client):
    ack()
    user = body['view']['state']['values']['User']['user']['selected_user']
    date = body['view']['state']['values']['Date']['date']['value'].split('/')
    hour_min = body['view']['state']['values']['Hour']['time']['value'].split(':')
    message = body['view']['state']['values']['Message']['message']['value']
    timet = datetime(int(date[2]), int(date[0]), int(date[1]), int(hour_min[0]), int(hour_min[1])).timestamp()
    client.chat_postEphemeral(channel=body['user']['id'], user=body['user']['id'], text=f"You just schedule a message to <@{user}>")
    client.chat_scheduleMessage(post_at=timet, channel=user, text=message)


# waits for slash command, if command matches checks and prints a motivational quote
@app.command("/motivateme")
def motivation_called(body, command, logger, client, ack):
    ack()
    tip = random.choice(motivations)
    client.chat_postMessage(channel=command['channel_id'], user=command['user_id'], text=tip)

# waits for slash command, if command matches opens a modal popup to get inputs for reminder   
@app.command("/assignmentreminder")
def assignmentReminder_called(body, say, action, command, logger, client, ack):
    ack()
    try:
        timet = datetime.now() + timedelta(minutes = 1)
       
        res = client.views_open(trigger_id=body["trigger_id"],
        view = {
            "title": {
                "type": "plain_text",
                "text": "Send Reminder"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "callback_id": "Reminder_back",
            "blocks": [
                {
                    "type": "section",
                    "block_id": "User",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Who would you like to send a Reminder to."
                    },
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "action_id": "user"
                    }
                },
                {
                    "type": "input",
                    "block_id": "Date",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "date",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "(MM/DD/YYYY)"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Date"
                    }
                },
                {
                    "type": "input",
                    "block_id": "Hour",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "time",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "HH:MM"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Time"
                    }
                },
                {
                    "type": "input",
                    "block_id": "Message",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "message",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "What would you like to say?"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Message"
                    }
                }
            ],
            "type": "modal"
            },)
        client.chat_scheduleMessage(post_at=timet.timestamp(), channel=command['text'], text=f"You were sent a reminder right now by <@{command['user_id']}> ")
        client.chat_postEphemeral(channel=command['channel_id'], user=command['user_id'], text=f"<@{command['user_id']}> has set a reminder to remind {command['text']} about the assignment.")
       
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")



# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

