import platform
import subprocess
import webbrowser
from typing import Literal

def open_browser(env: Literal['pi', 'pc'], url: str) -> None:
    if env == 'pi':
        subprocess.Popen([
            'chromium-browser',
            '--kiosk',
            '--noerrdialogs',
            '--disable-session-crashed-bubble',
            url
        ])

def close_browser(env: Literal['pi', 'pc']) -> None:
    if env == 'pi':
        subprocess.run(['pkill', '-o', 'chromium'])
