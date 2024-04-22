from typing import Callable
import platform


__all__ = ["KeyboardEventManager"]


class KeyboardEventManager:
    def __init__(self) -> None:
        self.__event_pool = {}

    def keypress(self, key: str) -> Callable[[], bool | None]:
        def wrapper(function: Callable[[], bool | None]) -> Callable[[], bool | None]:
            self.__event_pool[key] = function
            return function

        return wrapper

    def listen(self):
        system = platform.system()
        if system == "Windows":
            import msvcrt

            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key.decode() in self.__event_pool:
                        if self.__event_pool[key.decode()]():
                            break
        else:
            import sys
            import tty
            import termios

            while True:

                try:
                    old_settings = termios.tcgetattr(sys.stdin)
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    if key in self.__event_pool:
                        if self.__event_pool[key]():
                            break
                except SystemExit:
                    ...
                except ValueError:
                    break


if __name__ == "__main__":
    event = KeyboardEventManager()

    @event.keypress(key="q")
    def test():
        print("Pressed [q]")
        exit()

    event.listen()
