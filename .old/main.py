import pyautogui
import time
import win32gui
import win32com.client
import sys
from random import randrange

copy_img_path = 'img\\copy.png'
delete_img_path = 'img\\delete.png'
visibility_check_img_path = 'img\\visibility_check.png'
window_img_path = 'img\\window.png'


def copy_whisper(img):
    try:
        # click on copy button
        pyautogui.click(img)
        
        # delete message from search manager
        pyautogui.move(50, 0)
        pyautogui.click()
        return True
    except TypeError:
        return False


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


def find_on_screen(needle, haystack, title):
    hwnd, t = get_window(title)
    x, y, _, _ = win32gui.GetWindowRect(hwnd)
    left, top, _, _ = pyautogui.locate(needle, haystack)
    return (left + x, top + y)


def prog_bar_init():
    sys.stdout.write('\r[%s]' % (' ' * bar_width))
    sys.stdout.flush()
    sys.stdout.write('\b' * (bar_width + 1))


def paste_whisper():
    time.sleep(0.05)
    pyautogui.press('enter')
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
##    time.sleep(randrange(5, 30)/100)
    pyautogui.press('enter')


if __name__ == '__main__':
    while True:
        # start cycle
        op = input('''Start search? 'ctrl + c' to quit: ''')

        # check if buttons are visible
        if pyautogui.locateOnScreen(visibility_check_img_path) is None:
            # focus search manager window
            focus_window('PoE Live Search Manager')
        
        # copy whisper and delete from search manager
        sys.stdout.write('Waiting for item\n')
        blip_time = time.time()
        bar_width = 10
        count = 0
        prog_bar_init()
        while not (copy_whisper(copy_img_path)):
##        while not click_img(delete_img_path):
            if time.time() > blip_time + 1:
                sys.stdout.write('=')
                sys.stdout.flush()
                count += 1
                if count == bar_width + 1:
                    prog_bar_init()
                    count = 0
                blip_time = time.time()

        sys.stdout.write('\nItem found!\n')
        # focus PoE window
        focus_window('Path of Exile')
        
        # paste whisper
        paste_whisper()

