# Usage Examples

## 1. Running the program in GUI mode

Command:

```bash
python EZPLU.py
```

Steps:

1. Run the program.
2. Start Google Chrome in debugging mode (see the [User documentation](user.md)).
3. If you already have a PLU code database (`plukody.json`), you can place it in the folder containing `EZPLU.py`. A database of your own is not required, though.
4. Click the **Init Page** button and wait for Playwright to connect. Then log in to the EasyPLU website and open a test.
5. Click **Run** (auto-bot) or **Toggle Helper** (helper).
6. The bot will automatically fill in and submit PLU codes, or, in helper mode, it will only fill in the current code when you press the hotkey (default `b`).
7. Save the database with **Save DB**.
8. Close the window to exit the program.

## 2. Running the program in CLI mode

Command:

```bash
python EZPLU.py --cli
```

Steps:

1. Run the program with the `--cli` argument.
2. Start Google Chrome in debugging mode (see the [User documentation](user.md)).
3. If you already have a PLU code database (`plukody.json`), you can place it in the folder containing `EZPLU.py`. A database of your own is not required, though.
4. Enter the `i` command in the console to initialize the connection between Playwright and the browser.
5. Log in to the EasyPLU website and open a test.
6. Enter `r` (or `run`) to start automatic filling.
7. Alternatively, turn on the helper with the `helper` command. Once it is active, just press the hotkey (default `b`) to fill in the current PLU code.
8. Save the database with the `s` (save) command.
9. Exit the program with the `q` command.