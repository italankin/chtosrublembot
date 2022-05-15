# Chto s rublem?

![chtosrublem](chtosrublem.jpg)

# Configuration

Parameter|Description
---|---
`TELEGRAM_BOT_TOKEN`|Telegram bot token
`BOT_TRIGGERS_FILE`|Triggers and symbols for bot
`FCSAPI_ACCESS_KEY`|Access key for [FCS API](https://fcsapi.com/)
`BOT_SUBSTRING_TRIGGER_RATE`|A float in range `[0..1]` which limits `substring` triggering 

### Triggers

Key|Type|Description
---|---|---
`symbol`|`string`|Currency pair which is supported by FCS API ([forex](https://fcsapi.com/document/forex-api#forexsupportedcurrency), [crypto](https://fcsapi.com/document/crypto-api#cryptosupportedcurrency))
`trigger`|`regex`|Regular expression (full match against the message) which will trigger `symbol` lookup
`source`|`enum`|Source of `symbol`, either `forex` (default) or `crypto`
`substring`|`regex`|Regular expression (partial match against the message) which will trigger `symbol` lookup at `BOT_SUBSTRING_TRIGGER_RATE`

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
    "trigger": "RUB to USD\\?"
  },
  {
    "symbol": "BTC/USD",
    "trigger": "BTC to USD\\?"
    "source": "crypto"
  }
]
 ```

Place it to `$(pwd)/data/triggers.json`.

## Run

You can either mount directory with triggers data, or create a separate volume for that. The following command uses
host directory as a `data` volume:

 ```sh
 $ docker run --rm -d -v $(pwd)/data/:/data/ --env-file .env chtosrublembot
 ```
 
