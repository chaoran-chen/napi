# napi

A tiny API to send notifications via different protocols (currently emails and Slack)


## Getting started

### Start application with Docker

1. Download [config.template.yml](./config.template.yml), fill it out and rename it to "config.yml"
2. Run `docker run -p 8080:8080 -v $PWD/config.yml:/config/config.yml ghcr.io/chaoran-chen/napis:public`

The API is now available at http://127.0.0.1:8080

### Send notification

To send a notification, send a POST request to `/send` with a JSON body in the following format:

```json
{
    "auth_key": "<auth key>",
    "channel": "<channel name>",
    "level": "<INFO, WARNING or ERROR>",
    "subject": "<subject>",
    "body": "<body>"
}
```
