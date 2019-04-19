# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

def send_help(message):
  response = """
  Currently I only can show the status of service and host problems
  I will listen for *status* in a channel and share for everyone to see
  But if you made a booboo and want nobody to know, you can also say _status_ in a direct message to me
  """
  message.send(response)

@respond_to('help', re.IGNORECASE)
def help(message):
  send_help(message)
