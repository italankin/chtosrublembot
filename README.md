# Chto s rublem?

![chtosrublem](chtosrublem.jpg)

# Configuration

Parameter|Description
---|---
`TELEGRAM_BOT_TOKEN`|Telegram bot token
`BOT_TRIGGERS_FILE`|Triggers and symbols for bot
`FCSAPI_ACCESS_KEY`|Access key for [FCS API](https://fcsapi.com/)

# Docker

## Build image

 ```sh
 $ docker build -t chtosrublembot .
 ```

## Configure

Create file `.env` with the following contents:

 ```env
 TELEGRAM_BOT_TOKEN=<your-bot-token>
 BOT_TRIGGERS_FILE=/data/triggers.json
 FCSAPI_ACCESS_KEY=<your-access-key>
 ```

### Triggers file

JSON file with triggers:

 ```json
 [
  {
   "symbol": "USD/RUB",
   "trigger": "USD OK\\?"
  },
  {
   "symbol": "EUR/RUB",
   "trigger": "EUR OK\\?"
  }
]
 ```

Place it to `$(pwd)/data/triggers.json`.

## Run

You can either mount directory with responses data, or create a separate volume for that. The following command uses
host directory as a `data` volume:

 ```sh
 $ docker run --rm -d -v $(pwd)/data/:/data/ --env-file .env chtosrublembot
 ```
 
