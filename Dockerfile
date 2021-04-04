FROM python:3.9
WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
VOLUME "/data"
CMD [ "python", "./bot.py" ]
