Feedback Bot

A Telegram bot for feedback. Users send messages to the bot, they get forwarded to the admin, and the admin can reply using Telegram's Reply feature.

How to get a token

Go to @BotFather in Telegram and create a new bot with /newbot. It will give you a token like 1234567890:ABCdefGHIjklmNOPqrstUVwxyz. Save it.

How to find your ID

Message @userinfobot or @getmyid_bot -- they will send you your numeric ID.

How to run

Open bot.py and put your token and ID into BOT_TOKEN and ADMIN_ID. Then in your terminal:

pip install -r requirements.txt
python bot.py

How it works

A user sends any message (text, photo, document, audio, voice) to the bot. The bot forwards it to the admin. The admin presses Reply on the forwarded message and types an answer. The bot delivers the answer back to the user.

If the user blocked the bot, the admin gets an error message. The bot does not crash.

Notes

It uses in-memory dictionaries, so everything resets on restart. If the user has a hidden profile, it still works because the bot keeps its own mapping.
