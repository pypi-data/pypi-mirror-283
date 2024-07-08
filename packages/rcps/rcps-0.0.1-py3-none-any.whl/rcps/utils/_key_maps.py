from pynput.keyboard import Key, KeyCode

key_mapping = {
    'Key.alt': 'alt',
    'Key.alt_l': 'altleft',
    'Key.alt_r': 'altright',
    'Key.backspace': 'backspace',
    'Key.caps_lock': 'capslock',
    'Key.cmd': 'win',
    'Key.cmd_l': 'winleft',
    'Key.cmd_r': 'winright',
    'Key.ctrl': 'ctrl',
    'Key.ctrl_l': 'ctrlleft',
    'Key.ctrl_r': 'ctrlright',
    'Key.delete': 'delete',
    'Key.down': 'down',
    'Key.end': 'end',
    'Key.enter': 'enter',
    'Key.esc': 'esc',
    'Key.f1': 'f1',
    'Key.f2': 'f2',
    'Key.f3': 'f3',
    'Key.f4': 'f4',
    'Key.f5': 'f5',
    'Key.f6': 'f6',
    'Key.f7': 'f7',
    'Key.f8': 'f8',
    'Key.f9': 'f9',
    'Key.f10': 'f10',
    'Key.f11': 'f11',
    'Key.f12': 'f12',
    'Key.home': 'home',
    'Key.left': 'left',
    'Key.page_down': 'pagedown',
    'Key.page_up': 'pageup',
    'Key.right': 'right',
    'Key.shift': 'shift',
    'Key.shift_l': 'shiftleft',
    'Key.shift_r': 'shiftright',
    'Key.space': 'space',
    'Key.tab': 'tab',
    'Key.up': 'up',
    
    'Key.`': '`',
    'Key.-': '-', 
    'Key.=': '=', 
    'Key.[': '[', 
    'Key.]': ']',
    'Key.\\': '\\', 
    'Key.;': ';', 
    "Key.'": "'", 
    'Key.,': ',', 
    'Key..': '.',
    'Key./': '/'
}

for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
    key_mapping[f"Key.{char}"] = char

def convert_key(pynput_key_str):
    return key_mapping.get(pynput_key_str, None)


def convert_key_to_str(key):
    if isinstance(key, Key):
        return str(key)
    elif isinstance(key, KeyCode):
        return f'Key.{key.char}'
    return str(key)