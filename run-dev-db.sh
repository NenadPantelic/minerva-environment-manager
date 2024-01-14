#!/usr/bin/zsh

# for testing
docker run --name environment -e POSTGRES_USER=environment -e POSTGRES_PASSWORD=pass123 -e POSTGRES_DB=environment -p 5450:5432 -d postgres