from getpass import getpass
import typing
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from .env import OWNERS

class MyClient(TelegramClient):
    def __init__(self, session, api_id, api_hash):
        super().__init__(session, api_id, api_hash)
        self.me = None

    def start(
            self: 'TelegramClient',
            phone: typing.Union[typing.Callable[[], str], str] = lambda: print('Please enter your phone: '),
            password: typing.Union[typing.Callable[[], str], str] = lambda: print('Please enter your phone: '),
            *,
            bot_token: str = None,
            force_sms: bool = False,
            code_callback: typing.Callable[[], typing.Union[str, int]] = None,
            first_name: str = 'New User',
            last_name: str = '',
            max_attempts: int = 3) -> 'TelegramClient':
        
        if code_callback is None:
            def code_callback():
                return input('Please enter the code you received: ')
        elif not callable(code_callback):
            raise ValueError(
                'The code_callback parameter needs to be a callable '
                'function that returns the code you received by Telegram.'
            )

        if not phone and not bot_token:
            raise ValueError('No phone number or bot token provided.')

        if phone and bot_token and not callable(phone):
            raise ValueError('Both a phone and a bot token provided, '
                             'must only provide one of either')

        coro = self._start(
            phone=phone,
            password=password,
            bot_token=bot_token,
            force_sms=force_sms,
            code_callback=code_callback,
            first_name=first_name,
            last_name=last_name,
            max_attempts=max_attempts
        )
        return (
            coro if self.loop.is_running()
            else self.loop.run_until_complete(coro)
        )

    # customs here:

    async def connectAndCheck(self, chatID = None):
        try:
            await self.connect()
            return True
        except Exception as e:
            if chatID:
                await self.send_message(chatID, "Error: " + str(e))
            else:
                print("Error: " + str(e))
            return False

    async def getMe(self):
        if not self.me:
            self.me = await self.get_me()
        return self.me
    
    async def saveAllGroups(self):
        dialogs = await self.get_dialogs()
        groups = []
        for dialog in dialogs:
            try:
                if dialog.is_group:
                    if dialog.entity.username:
                        groups.append(f"@{dialog.entity.username}")
                    else:
                        full_chat = await self(GetFullChannelRequest(dialog.id))
                        if full_chat.full_chat.exported_invite:
                            groups.append(full_chat.full_chat.exported_invite.link)
            except Exception as e:
                print(e)
                continue
        return groups
    
    async def checkCancel(self, event):
        if event.text == "/cancel":
            await event.respond("Cancelled The Command.")
            return True
        else:
            return False

    def checkOwner(self, event):
        if event.sender_id in OWNERS:
            return True
        else:
            return False

