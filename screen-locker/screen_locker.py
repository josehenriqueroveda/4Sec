import pyautogui
import time

def get_screen_size():
    return pyautogui.size()

def is_position_blocked(x, y, blocked_area):
    return (
        blocked_area[0] <= x <= blocked_area[2]
        and blocked_area[1] <= y <= blocked_area[3]
    )

def move_to_safe_position(safe_position):
    pyautogui.moveTo(safe_position)

def main():
    screen_width, screen_height = get_screen_size()
    BLOCKED_AREA = (0, 230, 65, 1270)  # (x1, y1, x2, y2)F
    SAFE_POSITION = (screen_width / 2, screen_height / 2)

    while True:
        try:
            x, y = pyautogui.position()
            if is_position_blocked(x, y, BLOCKED_AREA):
                move_to_safe_position(SAFE_POSITION)
            time.sleep(0.01)
        except Exception:
            continue

if __name__ == "__main__":
    main()
