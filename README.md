# lightphone
A short little app to handle chatting with txt. Based on https://chatbotslife.com/build-a-working-sms-chat-bot-in-10-minutes-b8278d80cc7a

# Instructions
Follow the instructions on https://chatbotslife.com/build-a-working-sms-chat-bot-in-10-minutes-b8278d80cc7a

Install Googler and add a symlink to it somewhere in your path.
https://github.com/jarun/googler

Make a `secrets.json` file in the root of the directory and put all the following things in it:

* account_sid - Your Trelio Account SID
* auth_token - Your Trelio Authorization Number
* account_num - Your Trelio Phone Number
* my_number - Your personal number. Only texts from this number will be approved.
* api.ai.AT - Your api.ai Authentication Token

# Use

Start your messages with:

* `?` Run in python
* `!` Run in bash
* `g?` Google Search
