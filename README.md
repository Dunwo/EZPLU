# EZPLU

## Overview

EZPLU is a tool that helps with taking PLU tests on the EasyPLU website (used, for example, by large retail chains). It uses the Playwright framework to attach to your browser and has two main features:

- **Helper**: fills in the PLU code when you press a hotkey (e.g. when you can't remember a code).
- **Auto-bot**: automatically fills in and submits answers, and learns the correct codes along the way.

The program currently works through a graphical interface (Flet GUI) and a command line interface (CLI).

## Requirements

- Python
- Google Chrome
- [Playwright](https://playwright.dev/python/) library
- [Flet](https://flet.dev/) library
- [pynput](https://pypi.org/project/pynput/) library

Install the dependencies with:

```bash
pip install playwright flet pynput
```

## Usage

Run the program with:

```bash
python EZPLU.py
```

Optional arguments:

- `--cli` – run in command line interface mode (instead of the GUI)
- `--debug` – enable debug mode (prints extra information to the console)

Playwright connects to Chrome through its remote debugging port (`9222`), so Chrome has to be started with `--remote-debugging-port=9222`. The program can start it for you (the "Start Chrome" button in the GUI, or the `chrome` command in the CLI).

## Documentation

- [User documentation](docs/user.md)
- [Usage examples](docs/examples.md)

---

> **Note:** This project was originally developed elsewhere, so this repository only contains the latest version and not the full commit history. The documentation was originally written in Slovak and translated into English with the help of AI.