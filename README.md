# Check Matters
Chat bot mattermost to talk to Check MK  

# Components used
https://github.com/attzonko/mmpy_bot  
https://mathias-kettner.com/  

# Usage
Create an user in Mattermost and add this user to channels you want  
Create an user in Check MK with an automation secret for machine accounts

This container needs to be run with a volume mount on /settings  
/settings requires two files. cmk_settings.py and mmpy_bot_settings.py

mmpy_bot_settings.py:
```python
DEBUG = True
BOT_URL = 'https://mattermost.example.com:8065/api/v4'
BOT_LOGIN = 'bot@example.com'
BOT_PASSWORD = 'secret'
BOT_TEAM = 'General'
PLUGINS = [
    'mmpy_bot.plugins',
    'check_mk',
]
```

cmk_settings.py:
```python
cmk_proto= 'https://'
cmk_server = 'cmk.example.com'
cmk_site = 'my_site'
cmk_user = 'matter_bot'
cmk_pass = 'secret'
```
