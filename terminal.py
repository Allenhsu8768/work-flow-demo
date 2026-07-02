import os
import sys
import time
import threading

def clear_screen():
    """自動清空終端機畫面，讓排版看起來像一個獨立的系統頁面"""
    os.system('cls' if os.name == 'nt' else 'clear')


class TerminalSpinner:
    def __init__(self, message: str = "Agent 思考中") -> None:
        self.message = message
        self.symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.stop_running = False
        self.thread = None

    def _spin(self) -> None:
        idx = 0
        while not self.stop_running:
            sys.stdout.write(f"\r{self.symbols[idx % len(self.symbols)]} {self.message}...")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.08)
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def start(self) -> None:
        self.stop_running = False
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()

    def stop(self) -> None:
        self.stop_running = True
        if self.thread:
            self.thread.join()


def get_visual_width(text: str) -> int:
    return sum(2 if ord(c) > 127 else 1 for c in text)

def terminal_display_panel(
    future_work_name: str,
    hint_message: str, 
    agent_name: str
    ):
    
    title_width = get_visual_width(f" [ {future_work_name} ] ")
    hint_width = get_visual_width(hint_message)
    agent_width = get_visual_width(agent_name)
    
    content_inner_width = max(hint_width + 8, title_width + 4)
    total_outer_width = content_inner_width + 2
    title_padding = (total_outer_width - title_width) // 2
    agent_padding = content_inner_width - 19 - agent_width
    hint_padding_left = (content_inner_width - hint_width) // 2
    hint_padding_right = content_inner_width - hint_width - hint_padding_left
    
    print(f"{'=' * title_padding} [ {future_work_name} ] {'=' * title_padding}")
    print(f"|      負責專員: [{agent_name}] {' ' * agent_padding}|")
    print(f"|{'-' * content_inner_width}|")
    print(f"|{' ' * hint_padding_left}{hint_message}{' ' * hint_padding_right}|")
    print(f"{'':=^{total_outer_width}}\n")
    
