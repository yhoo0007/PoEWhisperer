import asyncio
import websockets
import json
import requests

# for pasting whispers
import pyperclip
import pyautogui
import win32gui
import win32com.client

from websockets.exceptions import ConnectionClosedError  # handle this


HEADERS = [
    ('Accept-Encoding', 'gzip, deflate, br'),
    ('Accept-Language', 'en-US,en;q=0.9'),
    ('Cache-Control', 'no-cache'),
    ('Cookie', 'POESESSID=506eca963f06aaeab2004dd589b67e30'),
    ('Host', 'www.pathofexile.com'),
    ('Origin', 'https://www.pathofexile.com'),
    ('Pragma', 'no-cache'),
    ('Sec-WebSocket-Extensions', 'permessage-deflate; client_max_window_bits')
]
headers = websockets.http.Headers(HEADERS)

MAX_ITEMS = 1


def url_to_uri(url, league):
    from re import match
    code = match('https://www.pathofexile.com/trade/search/\w*/(\w*)', url).group(1)
    return f'wss://www.pathofexile.com/api/trade/live/{league}/{code}'


def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_window(title):
    windows = []
    win32gui.EnumWindows(window_enumeration_handler, windows)
    window, = filter(lambda win:win[1] == title, windows)
    return window


def focus_window(title):
    window = get_window(title)
    hwnd, title = window
    win32gui.ShowWindow(hwnd, 5)
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


def send_whisper(whisper):
    pyperclip.copy(whisper)
    focus_window('Path of Exile')
    pyautogui.press('enter')
    pyperclip.paste()
    pyautogui.press('enter')


async def live_search(label, uri, item_found_event, exit_event, autowhisper=False, max_items=MAX_ITEMS):
    async with websockets.connect(
        uri,
        ssl=True,
        extra_headers=headers
    ) as websocket:
        auth = await websocket.recv()
        print(f"< {auth}")
        num_items_found = 0
        while True:
            print(f'Live searching for {label}\nAutowhisper: {autowhisper}\nMax items: {max_items}\n')
            new_ids = json.loads(await websocket.recv())['new']
            if exit_event.is_set():  # user has signaled termination
                print('Terminating task')
                return (label, num_items_found)
            num_items_found += len(new_ids)
            print(f"< {label}: {len(new_ids)} items found")

            if not item_found_event.is_set():
                item_found_event.set()  # notify other tasks that item has been found

                print('> Fetching whispers')
                whispers = list(map(
                    lambda id_: json.loads(
                        requests.get(f'http://www.pathofexile.com/api/trade/fetch/{id_}').content
                    )['result'][0]['listing']['whisper'],
                    new_ids[:min(max_items, len(new_ids))]  # limit number of items to fetch
                ))

                if autowhisper:
                    print('Sending whisper')
                    for whisper in whispers:
                        send_whisper(whisper)

                continue_ = input('Continue searching? (Y/N)')
                if continue_ in ('Y', 'y'):
                    item_found_event.clear()
                else:
                    exit_event.set()
                    print('Terminate signal set')
                    print('Terminating task\n')
                    return (label, num_items_found)


async def driver(urls, league):
    item_found_event = asyncio.Event()
    exit_event = asyncio.Event()
    tasks = []
    for label, url in urls.items():
        tasks.append(asyncio.create_task(
            live_search(label, url_to_uri(url, league), item_found_event, exit_event)
        ))

    for task in tasks:
        ret = await task
        print(ret)


def main(urls, league):
    asyncio.run(driver(urls, league))
