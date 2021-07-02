# Chto s rublem?

![chtosrublem](chtosrublem.jpg)

# Configuration

Parameter|Description
---|---
`TELEGRAM_BOT_TOKEN`|Telegram bot token
`TINKOFF_INVEST_API_TOKEN`|Token of Tinkoff Invest OpenAPI
`TINKOFF_INVEST_API_BASE_URL`|Base URL of endpoint
`BOT_TRIGGER_PATTERN`|Regex which will trigger bot responses
`BOT_RESPONSES_FILE`|A path to a responses json file

# Docker

## Build image

 ```sh
 $ docker build -t chtosrublembot .
 ```
 
 ## Configure
 
 Create file `.env` with the following contents:
 
 ```env
 TELEGRAM_BOT_TOKEN=<your-bot-token>
 TINKOFF_INVEST_API_TOKEN=<your-tinkoff-invest-api-token>
 TINKOFF_INVEST_API_BASE_URL=<base-url-of-tinkoff-invest-api>
 BOT_TRIGGER_PATTERN=<regex-pattern-of-message-to-trigger-bot>
 BOT_RESPONSES_FILE=/data/responses.json
 ```
 
 ### Responses file
 
 JSON file with possible bot answers:
 
 ```json
 {
   "usd_down" : ["USD goes down"],
   "rub_down" : ["RUB goes down"],
   "neutral": ["Difference is not significant"]
 }
 ```
 
 Place it to `$(pwd)/data/responses.json`.
 
 ## Run
 
 You can either mount directory with responses data, or create a separate volume for that. The following command uses host directory as a `data` volume:
 
 ```sh
 $ docker run --rm -d -v $(pwd)/data/:/data/ --env-file .env chtosrublembot
 ```
 
