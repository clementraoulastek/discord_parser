# TCP Sniffer for Dofus retro game & Discord Bot

This repository is a Discord bot that listen to a TCP client and send the messages to a discord channel.

# Conda env

A virtual environment is used to run the project. It is managed by conda.

## Create the environment

```bash
conda env create -f environment.yml
```

## Activate the environment

```bash
conda activate discord-parser
```

# Run the app 

## In dev mode
```bash
make run
```

# Run the tests

```bash
make test
```

# Deploy the app

## Create an executable

```bash
pyinstaller --onefile src/main.py --name "DofusParser"
```

