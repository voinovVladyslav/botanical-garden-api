# Botanical Garden Website

**This is a Kherson State University project for creating a website for our botanical garden.**

**This repository contains Back-end part of website. Front-end part located at [this](https://github.com/danylo-morhun/botanical-garden-front) repository.**

## Set up guide

This section will tell you how to run base application and run custom command

### Initial setup

```
docker compose build
```

This command builds 2 images for you. First is api image, second is database image.

We using postgres as database.

### Up server

```
docker compose up
```

This command runs django server on 127.0.0.1:8000

Before running server this also applies all migrations to the database

### Down server

```
docker compose down
```

This command removes all docker containers

### Run custom command

```
docker compose run --rm app sh -c "your command"
```

Usually used to make migrations file or run tests

## Docs

Docs located at 127.0.0.1:8000/api/docs
