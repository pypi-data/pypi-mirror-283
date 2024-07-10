Introduction
============

We’ve built the bot framework you’ve been waiting for!
======================================================

Unlock seamless Telegram bot development with our intuitive, powerful framework. Tap into our thriving community for support and inspiration

Installing
==========

You can install or upgrade ``ptb-easy-bot`` via

.. code:: shell

    $ pip install ptb-easy-bot --upgrade

To install a pre-release, use the ``--pre`` `flag <https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-pre>`_ in addition.


Quick Start
===========
::

    from Easy_bot import Client , COMMANDS 
    from telegram import Bot, Update
    from telegram.ext import ContextTypes
    import asyncio
    import os

    TOKEN = os.environ.get('TOKEN')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', None)
    PORT = int(os.environ.get('PORT', '8443'))

    async def main():
        if WEBHOOK_URL:
            bot = Bot(TOKEN)
            await bot.set_webhook(WEBHOOK_URL + "/" + TOKEN)

        
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello..")

    Handlers = {
        COMMANDS :  {
            'start' : start_command,
        },
        
    }
    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        app = Client(TOKEN=TOKEN,PORT=PORT,WEBHOOK_URL=WEBHOOK_URL,HANDLERS=Handlers)
        app.run_polling()
    
