
# DevilBot
#A Slack Bot that interacts and motivates you to keep up with your assignments
#python version - 3.9.0
#Steps to Run
#Launch ngrock.exe and execute the command
#   ngrok.exe http 3000
#
#In another command window
#	python -m venv .venv
#	source .venv/Scripts/activate
#	export SLACK_BOT_TOKEN=''//input the token
#	export SLACK_SIGNING_SECRET=''//input the secret
#	pip install slack-bolt
#	python app.py
#	
#Commands and mentions
#Team name: DevilBots
#Team members:
#Nevedita Kailasam : @nkailasa
#Kunal Patel : @kgpatel6
#GitHub Repository URL: https://github.com/nkailasa/DevilBot  Branch: main
#What is your inspiration?
#Assignments are exhausting and we have felt the need for a companion(real or virtual) to comfort us.
#
#What it does?
#DevilBot is going to be your companion for the day.
#You can ask DevilBot to motivate you by typing '/motivateme' before starting your tedious assignment work
#@DevilBot to initiate your interaction with the bot(Think of it as the power button to switch the bot on!)
#It will greet you with a usual morning message and asks for your choice.
#	1.Choose 'Let's do assignments' to get a list of your upcoming assignments with due dates
#		a.The assignment list will be shown with an option to checkmark it once done!
#		b.Check mark each assignment as you progress.
#		c.If you are done with all the assignments the bot provides you with a leisure option
#	2.Choose 'Not today' and get some "Constructive feedback" from the bot.
#	  It will also take you to the leisure option but it knows that you don't deserve it.
#'/assignmentreminder' is going to help you to get back from the undeserved leisure option.
#	a.A modal popup appears on typing the slash command
#	b.You can either set reminder to yourself or you can alert a friend with your own customized message and time.
#	The bot takes care of the timezone difference too!
#		
#How We built it?
#We decided on the base idea and started implementing one use case at a time.
#And obviously we followed the session of Dr.Mehlhase and used her codebase which made our life easier.
#Frequent team meeting was conducted to stay on the same page.
#
#Challenges We ran into:
#Only one of us could do the setup so the other one had to rely to debug the code.
#Most of the errors were because of wrong JSON parsing.
#Since we are new to python we had minor syntactical errors during development.
#
#Accomplishments that the team is proud of.
#DevilBot Works!!!!!! As intended!!!
#We are happy that we could learn and implement a completely new App in two days with no prior plan or experience.What the team learned.
#Team learnt how to parse and read from a JSON.
#Python indentation, usage of punctuations(the absence of : , {} and the importance of :)
#Few of the SlackAPI commands and how to tweak it according to our implementation
=======

