FROM python:3.6-alpine
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH="/plugins:/settings" \
    MATTERMOST_BOT_SETTINGS_MODULE=mmpy_bot_settings
CMD mmpy_bot
