#!/bin/bash
docker build -t guestros/tradingbot22-bot:lightgbm ./src/
docker push guestros/tradingbot22-bot:lightgbm