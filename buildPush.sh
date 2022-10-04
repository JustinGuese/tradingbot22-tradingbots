#!/bin/bash
docker build -t guestros/tradingbot22-bot:simple-trendbot ./src/
docker push guestros/tradingbot22-bot:simple-trendbot