# User Documentation

## Running the program

```bash
python EZPLU.py
```

Optional arguments:

- `--cli` – run in Command Line Interface mode
- `--debug` – enable debug mode (prints extended information to the console)

If you already have a database, you can place a `plukody.json` file in the program's folder. This is not required, though – the program can create a database from scratch on its own.

## Opening Chrome

The program can start Chrome for you (the **Start Chrome** button in the GUI, or the `chrome` command in the CLI). Alternatively, you can create the following `.bat` file:

```bat
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\chrome-playwright"
```

- The first line is the default path of the Chrome installation. Change it if your Chrome is installed elsewhere.
- The third line sets the folder for the Chrome profile. Chrome does not allow debugging mode to use the same profile as a normal Chrome instance, so a separate folder is needed.

## Usage

- In the CLI, the `help` command lists all available commands.
- The first step is always to initialize the connection between Playwright and Chrome (`i` in the CLI / the **Init Page** button in the GUI).
- **Auto-bot** – if the database is empty, or an entry is missing from it, the program types `0000` into EasyPLU and then updates the database with the correct code that the website shows. Start and stop it with `r` / `run` in the CLI or the **Run** button in the GUI.
- **Helper** – the default hotkey is `b`, which can be changed (`changehotkey` in the CLI, or the hotkey field in the GUI). When you press the hotkey, the program looks up the current entry in the database and types it into the input field. Turn the helper on and off with `helper` in the CLI or the **Toggle Helper** button in the GUI.
- **Saving the database** – `s` / `save` in the CLI (or the **Save DB** button in the GUI) saves the current database to `plukody.json`. Remember to save, otherwise newly learned codes are lost when the program closes.
- **Loading the database** – `readdb` in the CLI reloads the database from `plukody.json`.