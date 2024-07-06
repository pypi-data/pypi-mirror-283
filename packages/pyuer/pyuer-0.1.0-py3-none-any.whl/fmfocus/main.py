import pyautogui




def mouse_move(x, y):
    pyautogui.moveTo(x, y)

def mouse_move_click(x, y, clicks=1, button='left'):
    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=clicks, button=button)


def focus():
    pyautogui.press('tab')

def writ(text):
    pyautogui.typewrite(text)