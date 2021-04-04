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
 
 ## Run
 
 ```sh
 $ docker run --rm -d -v $(pwd)/data/:/data/ --env-file .env chtosrublembot
 ```
 
