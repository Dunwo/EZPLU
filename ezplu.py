import sys
import json
from playwright.async_api import async_playwright
import asyncio
from pynput import keyboard
import flet as ft
import subprocess
import random
import winreg

import os
os.environ["NODE_OPTIONS"] = "--no-deprecation"

#Flet GUI code below
async def renderwindow(page:ft.Page):
    state = AppState()
    state.loop = asyncio.get_running_loop()
    listener = keyboard.Listener(on_release=cmd_releaseofkey(state,state.loop))
    listener.start()
    state.GUIOn = True
    page.title = "EZPLU"
    page.window_width = 500
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.START

    #Log
    log_output = ft.TextField(
        value="Log:\n",
        multiline=True,
        read_only=True,
        expand=True
    )

    def log(message):
        log_output.value += message + "\n"
        page.update()

    def clearLog():
        log_output.value =""
        page.update()

    state.log = log

    #Buttons
    buttons_row_1 = ft.Row(
        controls=[
            ft.ElevatedButton("Start Chrome", on_click=lambda e: cmd_StartBrowser(state)),
            ft.ElevatedButton("Init Page", on_click=lambda e: asyncio.create_task(cmd_init_page(state))),
            ft.ElevatedButton("Load EasyPlu", on_click=lambda e: asyncio.create_task(loadWeb(state))),
        ]
    )

    buttons_row_2 = ft.Row(
        controls=[
            ft.ElevatedButton("Run", on_click=lambda e: asyncio.create_task(cmd_run(state))),
            ft.ElevatedButton("Toggle Helper", on_click=lambda e: cmd_TurnHelper(state)),
            ft.ElevatedButton("Save DB", on_click=lambda e: cmd_savedb(state)),
            ft.ElevatedButton("Clear Log", on_click=lambda e: clearLog()),
        ]
    )

    #Hotkey
    hotkey_input = ft.TextField(
        width=60,
        max_length=1
    )

    hotkey_row = ft.Row(
        controls=[
            ft.Text("Helper Hotkey:"),
            hotkey_input,
            ft.ElevatedButton("Change Hotkey", on_click=lambda e: ChangeHotkey(hotkey_input.value,state)),
        ]
    )

    #Hotkey

    minWaitTimeInput = ft.TextField(
        value=str(state.min_max_waittime[0]),
        width=60,
        max_length=3,
    )
    
    maxWaitTimeInput = ft.TextField(
        value=str(state.min_max_waittime[1]),
        width=60,
        max_length=3,
    )

    WaitTime_row = ft.Row(
        controls=[
            ft.Text("Minimum Wait Time:"),
            minWaitTimeInput,
            ft.ElevatedButton("Change minimum time", on_click=lambda e: fletParseMinTime(state,minWaitTimeInput.value)),
            ft.Text("Maximum Wait Time:"),
            maxWaitTimeInput,
            ft.ElevatedButton("Change maximum time", on_click=lambda e: fletParseMaxTime(state,maxWaitTimeInput.value)),
        ]
    )

    def fletParseMinTime(state:AppState,newTimeString):
        try:
            changeMinWaitTime(state,float(newTimeString))
            log(f"Changed min wait time to {newTimeString}")
        except:
            log("Please type in valid number (0.1 , 1.2 , ...)")

    def fletParseMaxTime(state:AppState,newTimeString):
            try:
                changeMaxWaitTime(state,float(newTimeString))
                log(f"Changed max wait time to {newTimeString}")
            except:
                log("Please type in valid number (0.1 , 1.2 , ...)")


    #builder of the gui
    page.add(
        buttons_row_1,
        buttons_row_2,
        ft.Divider(),
        hotkey_row,
        WaitTime_row,
        ft.Divider(),
        log_output
    )


class AppState:
    def __init__(self):
        self.plupage: Page | None = None
        self.running = True
        self.database: DatabaseClass | None = None
        self.loop = None
        self.log = None
        self.debugging = False
        self.GUIOn = False
        self.current_hotkey = "b"
        self.min_max_waittime = [0.2,0.2]

class AutomateP:
    def __init__(self):
        pass
    def login(username,password):
        pass

class Page:
    def __init__(self):
        self.play = None
        self.browser = None
        self.context = None
        self.page = None

    async def init(self):
        self.play = await async_playwright().start()
        self.browser = await self.play.chromium.connect_over_cdp("http://localhost:9222")
        self.context = self.browser.contexts[0]
        self.page = self.context.pages[0]

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.play.stop()

    async def clicksubmit(self,state):
        locator = self.page.get_by_test_id("numpad_plu")
        if await locator.count() > 0:
            await self.page.get_by_test_id("numpad_plu").click()
        else:
            if state.debugging:
                print("Submit button not found")
            return None

    async def readname(self, state):
        plu_locator = self.page.locator(".stage-title h1")
        
        if await plu_locator.count() > 0:
            plu = await plu_locator.text_content()
        else:
            plu = None
            if state.debugging:
                print("PLU name not found")

        if plu == None:
            return None
        
        return plu.strip()
    
    async def writeplu(self,plucode,state):
        locator = self.page.get_by_test_id("plu-number-input")
        if await locator.count() > 0:
            await self.page.get_by_test_id("plu-number-input").fill(plucode)
        else:
            if state.debugging:
                print("PLU input field not found")
            return None
    
    async def checkvalidity(self,state):
        is_X_shown = await self.page.locator("#close-x").count() > 0
        is_check_shown = await self.page.locator("#aufgaben").count() > 0
        if is_check_shown:
            return True
        if is_X_shown:
            return False
        if state.debugging:
            print("Could not determine validity")
        return None
    
    async def readvalidplu(self,state):
        locator = self.page.locator(".plu-number-text")
        if await locator.count() > 0:
            plucode = await self.page.locator(".plu-number-text").inner_text()
            plucode = plucode[1:]
            plucode = plucode[:-1]
            return plucode
        else:
            if state.debugging:
                print("Valid PLU not found")
            return None
    
    async def testing(self):
            pluname = await self.page.locator(".stage-title h1").text_content()
            print(pluname.strip())

        

class DatabaseClass:
    def __init__(self):
        self.data = {}
        self.entries = 0


    def db_create(self):
        print("created new database")

    def db_write(self,name:str,plu:str,state):
        name = name.lower()
        curentry = self.data.get(name)
        if curentry is None:
            self.data[name] = plu
            if state.debugging :
                print("Created entry for: "+name+" ; "+ plu )

        else:
            self.data[name] = plu
            if state.GUIOn:
                state.log("Updated PLU for "+name+"from: "+curentry+"to: "+plu)
            else:
                print("Updated PLU for "+name+"from: "+curentry+"to: "+plu)

    def db_get(self,name:str):
        name = name.lower()
        curentry = self.data.get(name)
        if curentry is None:
            return None
        return curentry
    
    def db_jsoncreate(self):
        with open("plukody.json","w",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False)
    
    def read_DB(self,state):
        if not os.path.exists("plukody.json"):
            if state.GUIOn:
                pass
            else:
                print("Current database is None/Empty/Corrupted")
                print("Do you want to automatically create a new one?   y/n")
                dbn = input()
                while True:
                    if dbn.lower() in ("y","yes"):
                        self.db_create()
                        return
                    if dbn.lower() in ("n","no"):
                        print("Please keep in mind that the program wont work without database for writing/reading. You can use 'readdb' to read the database from plukody.json after you add it.")
                        return
                    print("Unknown command, please write y/n")
                    dbn = input()
        try:
            with open("plukody.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.entries = len(self.data)
        except:
            self.data = {}
            self.entries = 0
        if state.GUIOn:
            state.log("Database loaded with " + str(self.entries) + " entries.")
        else:
            print("Loaded : " + str(self.entries) + " entries")
        return

##################################################################################################################

#COMMANDS FUNCTIONS

async def cmd_init_page(state: AppState):
    state.plupage = Page()
    await state.plupage.init()

    state.database = DatabaseClass()
    if state.GUIOn:
        state.log("Page initialized.")
        state.log("Initializing PLU database")
    else:
        print("Page initialized.")
        print("Initializing PLU database")
    state.database.read_DB(state)

async def cmd_quit(state: AppState):
    if state.plupage is not None:
        await state.plupage.close()
    state.running = False

def cmd_savedb(state:AppState):
    if state.database is not None:
        state.database.db_jsoncreate()
        if state.GUIOn:
            state.log("Database saved to file.")
        else:
            print("Database saved to file.")
    else:
        if state.GUIOn:
            state.log("No database to save.")
        else:
            print("No database to save.")

async def cmd_run(state:AppState):
    global filler_task

    if state.plupage is None:
        if state.GUIOn:
            state.log("Page not initialized. Initialize first.")
        else:
            print("Page not initialized. Use 'i' first.")
        return

    if filler_task is not None and not filler_task.done():
        filler_task.cancel()
        if state.GUIOn:
            state.log("Stopping autofill process...")
        else:
            print("Stopping autofill process...")
        try:
            await filler_task
        except asyncio.CancelledError:
            pass
        filler_task = None
        return

    async def _filler():
        try:
            while True:
                curname = await state.plupage.readname(state)
                if curname is not None:

                    isindb = state.database.db_get(curname)
                    if isindb is None:
                        curplu = "0000"
                    else:
                        curplu = isindb
                    
                    await state.plupage.writeplu(curplu,state)

                    await asyncio.sleep(random.uniform(state.min_max_waittime[0],state.min_max_waittime[1]))

                    await state.plupage.clicksubmit(state)
                    await asyncio.sleep(0.1)

                    valid = await state.plupage.checkvalidity(state)
                    if not valid:
                        realplu = await state.plupage.readvalidplu(state)
                        state.database.db_write(curname,realplu,state)
                    await asyncio.sleep(1)
                else:
                    if state.GUIOn:
                        state.log("Cant find PLU name, maybe not on PLU test page?")
                        state.log("Waiting for 5 seconds before retrying...")
                        await asyncio.sleep(5)
                    else:
                        print("")
                        print("Cant find PLU name, maybe not on PLU test page?")
                        print("Waiting for 5 seconds before retrying...")
                        print("")
                        print("EZPLU: ", end="")
                        await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

    filler_task = asyncio.create_task(_filler())

async def cmd_Helper(state:AppState):
    curname = await state.plupage.readname(state)
    if curname is not None:
        isindb = state.database.db_get(curname)
        if isindb is None:
            return
        else:
            curplu = isindb
        
        await state.plupage.writeplu(curplu,state)

def cmd_releaseofkey(state:AppState,loop):
    def on_release(key):
        global helper
        if not helper:
            return
        try:
            if key.char == state.current_hotkey:
                loop.call_soon_threadsafe(asyncio.create_task, cmd_Helper(state))
        except AttributeError:
            pass
    return on_release

def cmd_TurnHelper(state:AppState):
    global helper
    if helper:
        helper = False
        if state.GUIOn:
            state.log("Turned off helper")
        else:
            print("Turned off helper")
    else:
        helper = True
        if state.GUIOn:
            state.log("Turned on helper, press '"+state.current_hotkey+"' to autofill current PLU")
        else:
            print("Turned on helper, press '"+state.current_hotkey+"' to autofill current PLU")

def cmd_ChangeHotkey(state:AppState):
    while True:
        newhotkey = input("Enter new hotkey: ")
        if len(newhotkey) == 1:
            ChangeHotkey(newhotkey,state)
            print("Changed hotkey to: "+newhotkey)
            break
        else:
            print("Invalid hotkey. Please enter a single character.")

def ChangeHotkey(newhotkey,state):
    if len(newhotkey) != 1:
        state.log("Please enter something first.")
    else:
        if state.GUIOn:
            state.log("Changed hotkey to: "+newhotkey)
        if len(newhotkey) == 1:
            state.current_hotkey = newhotkey

def cmd_Debug(state:AppState):
    if state.debugging:
        state.debugging = False
    else:
        state.debugging = True

def cmd_ReadDB(state:AppState):
    if state.database is not None:
        state.database.read_DB(state)
    else:
        if state.GUIOn:
            state.log("Please use initialize function first.")
        else:
            print("Please use initialize function first.")

def get_chrome_path():
    """Finds the Chrome executable path via the Windows Registry or common locations."""
    # 1. Check Registry (System-wide installation)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
            return winreg.QueryValue(key, None)
    except FileNotFoundError:
        pass

    # 2. Check Registry (User-specific installation)
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
            return winreg.QueryValue(key, None)
    except FileNotFoundError:
        pass

    # 3. Fallback to common hardcoded paths
    common_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe")
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError("Could not find chrome.exe on this system.")

def cmd_StartBrowser(state: AppState):
    try:
        chrome_path = get_chrome_path()
    except FileNotFoundError as e:
        print(f"Error starting browser: {e}")
        return

    user_data_dir = r"C:\chrome-playwright"
    debug_port = "9222"
    command = [
        chrome_path,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={user_data_dir}"
    ]
    subprocess.Popen(command)

async def loadWeb(state:AppState):
    await state.plupage.page.goto('https://easy-plu.knowledge-hero.com/login')

def cmd_changeWaitTime(state:AppState):
    while True:
            newMinTimeString = input("Enter new minimum waittime: ")
            try:
                newMinTime = float(newMinTimeString)
                while True:
                    newMaxTimeString = input("Enter new maximum waittime")
                    try:
                        newMaxTime = float(newMaxTime)

                    except:
                        print("Invalid time, please use format 0.1 , 1.2 , ...")

            except:
                print("Invalid time, please use format 0.1 , 1.2 , ...")

def changeMinWaitTime(state:AppState, newTime):
    state.min_max_waittime[0] = newTime

def changeMaxWaitTime(state:AppState, newTime):
    state.min_max_waittime[1] = newTime

async def cmd_test(state:AppState):
    await state.plupage.testing()
    state.plupage.clicksubmit(state)

def cmd_Help(state:AppState):
    helptext = """
    Available commands:
    i / initialize - Initializes the page and database
    r / run - Toggles the autofill process on/off
    s / save - Saves the current database to file
    readdb - Reads the current database from file
    helper - Toggles the helper hotkey functionality on/off
    changehotkey - Changes the hotkey for the helper function
    debug - Toggles debug mode on/off (prints extra info to console)
    q / quit - Quits the program
    chrome - Starts the browser required to run this app
    load - Loads up easyplu webpage
    help - Shows this help message
    """
    print(helptext)


##################################################################################################################

COMMANDS = {
    "i": cmd_init_page,
    "initialize" : cmd_init_page,
    "q": cmd_quit,
    "quit": cmd_quit,
    "r" : cmd_run,
    "run" : cmd_run,
    "s" : cmd_savedb,
    "save" : cmd_savedb,
    "debug" : cmd_Debug,
    "helper" : cmd_TurnHelper,
    "changehotkey" : cmd_ChangeHotkey,
    "help" : cmd_Help,
    "readdb" : cmd_ReadDB,
    "chrome" : cmd_StartBrowser,
    "load" : loadWeb,
    "test" : cmd_test
}

##################################################################################################################

async def main():
    state = AppState()
    state.loop = asyncio.get_event_loop()
    listener = keyboard.Listener(on_release=cmd_releaseofkey(state,state.loop))
    listener.start()
    if "--debug" in sys.argv:
        state.debugging = True
    else:
        state.debugging = False
    state.current_hotkey = "b"
    while state.running:
        cmd = (await asyncio.to_thread(input, "EZPLU: ")).lower()
        if cmd == "6":
            print(7)
            continue

        handler = COMMANDS.get(cmd)
        
        if handler is None:
            print("Unknown command")
            continue

        if asyncio.iscoroutinefunction(handler):
            await handler(state)
        else:
            handler(state)


if __name__ == "__main__":
    if "--cli" in sys.argv:
        GUIOnGlobal = False
    else:
        GUIOnGlobal = True
    filler_task = None
    helper = False

    if GUIOnGlobal:
        ft.app(target=renderwindow)
    else:
        asyncio.run(main())