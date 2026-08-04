from dataclasses import dataclass


@dataclass
class DeveloperConsole:
    text: str = ""
    message: str = "Enter a cheat code"

    def add_text(self, value: str) -> None:
        self.text = (self.text + value)[:24]

    def backspace(self) -> None:
        self.text = self.text[:-1]

    def clear(self) -> None:
        self.text = ""
