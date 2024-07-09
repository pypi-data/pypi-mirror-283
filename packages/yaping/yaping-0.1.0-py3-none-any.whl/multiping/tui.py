#
# This file is part of the multi-ping project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive


class Host(Static):
    name = reactive("---")

    def update_name(self, time):
        self.time = f"{time * 1000:.1f}ms"

    def watch_time(self, time):
        self.update(time)


class Time(Static):
    time = reactive("---")

    def update_time(self, time):
        self.time = f"{time * 1000:.1f}ms"

    def watch_time(self, time):
        self.update(time)


class Sequence(Static):
    sequence = reactive("---")

    def update_sequence(self, sequence):
        self.sequence = sequence

    def watch_sequence(self, sequence):
        self.update(f"{sequence}")


class PingHost(Static):
    time = reactive(None)
    sequence = reactive(None)

    def __init__(self, host, ip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.ip = ip

    def compose(self):
        yield Host(f"{self.host} ({self.ip})")
        yield Sequence()
        yield Time()


class PingApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield PingHost("www.google.com", "127.0.0.1")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


def main():
    app = PingApp()
    app.run()


if __name__ == "__main__":
    main()
