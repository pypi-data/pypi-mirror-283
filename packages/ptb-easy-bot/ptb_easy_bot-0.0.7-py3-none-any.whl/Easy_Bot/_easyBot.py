from telegram import Bot , InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import Application 
from telegram.ext import CommandHandler as COMMANDS
from telegram.ext import CallbackQueryHandler as CALLBACKS
from telegram.ext import InlineQueryHandler as INLINE_QUERY
from telegram.ext import MessageHandler  as MESSAGE_HANDLER
from telegram.ext import filters as Filters
from telegram._utils.defaultvalue import DEFAULT_80 ,DEFAULT_IP ,DEFAULT_NONE ,DEFAULT_TRUE ,DefaultValue
from telegram._utils.types import SCT, DVType, ODVInput
from typing import TYPE_CHECKING,Any,AsyncContextManager,Awaitable,Callable,Coroutine,DefaultDict,Dict,Generator,Generic,List,Mapping,NoReturn,Optional,Sequence,Set,Tuple,Type,TypeVar,Union

LOGO = """
........................................
.#####...####...##...##...####...#####..
.##..##.##..##..###.###..##..##..##..##.
.#####..######..##.#.##..##..##..##..##.
.##.....##..##..##...##..##..##..##..##.
.##.....##..##..##...##...####...#####..
........................................    
   ├ ᴄᴏᴘʏʀɪɢʜᴛ © 𝟸𝟶𝟸𝟹-𝟸𝟶𝟸𝟺 ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
   ├ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ  ɢᴘʟ-𝟹.𝟶 ʟɪᴄᴇɴsᴇ.
   └ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜsᴇ ᴛʜɪs ғɪʟᴇ ᴇxᴄᴇᴘᴛ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟɪᴄᴇɴsᴇ.
"""

class Client():
    def __init__(
            self, 
            TOKEN: str, 
            PORT: DVType[int] = DEFAULT_80,
            WEBHOOK_URL:  Optional[str] = None,
            HANDLERS: Dict = {},
    ):
        self.token = TOKEN
        self.port = PORT
        self.webhook_url = WEBHOOK_URL
        self.handlers = HANDLERS
        self.app = Application.builder().token(self.token).build()

        for handler , command_and_function in self.handlers.items():
            handler_list = [] 
            for command , function in dict(command_and_function).items():
                if handler == "Error":
                    self.app.add_error_handler(function)
                elif command != None:
                    self.app.add_handler(handler(command , function))
                else:    
                    self.app.add_handler(handler(function))
                handler_list.append(handler)


    def run_polling(
            self,
            drop_pending_updates:Optional[bool] = None,
            ):
        print(LOGO + "\n\n" )
        print("Bot Started")
        
        try:
            if self.webhook_url != None:
                print("running webhook...")
                self.app.run_webhook(
                    port=self.port,
                    listen="0.0.0.0",
                    webhook_url=self.webhook_url,
                    drop_pending_updates = drop_pending_updates,
                )
            else:
                print("running polling..")
                self.app.run_polling(
                    drop_pending_updates = drop_pending_updates,
                )
        except Exception as e:
            print(e)
        print("Bot Stoped")


class InlineReplyMarkup:
    """Create a Reply Markup easy 

    Args:
        keyboard (list): keyboard
            A List to create keyboard with line by line 
    
        Example:
            keyboard = [
                ['test - test'],
                ['test 01 - https://t.me/link','test 02 - test 02'],
                ['test 03 - inline_in_other']
            ]
    """
    def __init__(self,keyboard):

        new_keyboard = []
        for line in keyboard:
            new_line = []
            for data in line:
                text, button = str(data).split(' - ')
                if str(button).startswith('http'):
                    button = InlineKeyboardButton(text=text, url=button)
                elif str(button) =='inline':
                    button = InlineKeyboardButton(text=text, switch_inline_query_current_chat='')
                elif str(button) == 'inline_in_other':
                    button = InlineKeyboardButton(text=text, switch_inline_query='')
                else:
                    button = InlineKeyboardButton(text=text, callback_data=button)
                new_line.append(button)
            new_keyboard.append(new_line)
        self.keyboard =  InlineKeyboardMarkup(new_keyboard)
    def get_markup(self):
        return self.keyboard