import pyautogui
import time

screen_width, screen_height = pyautogui.size()
BLOCKED_AREA = (0, 230, 65, 1270)  # (x1, y1, x2, y2)
SAFE_POSITION = (screen_width / 2, screen_height / 2)

while True:
    try:
        x, y = pyautogui.position()
        if (
            BLOCKED_AREA[0] <= x <= BLOCKED_AREA[2]
            and BLOCKED_AREA[1] <= y <= BLOCKED_AREA[3]
        ):
            pyautogui.moveTo(SAFE_POSITION)
        time.sleep(0.01)
    except Exception:
        continue
