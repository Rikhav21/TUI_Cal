from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Label
from textual.containers import Grid, Vertical, Center
from textual.screen import Screen
import datetime

class DayScreen(Screen):
    CSS = """
    DayScreen {
        align: center middle;
    }

    #dialog {
        width: 50;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 2;
        align: center middle;
    }

    #dialog Label {
        width: 100%;
        text-align: center;
        margin-bottom: 1;
    }
    """

    gifts = {
        1: "React Workshop!",
        2: "A Fusering Workshop!",
        3: "Keyring with Onshape!",
        4: "Hono Backend!",
        5: "Full Stack App with Flask!",
        6: "3D Printable Ruler!",
        7: "Interactive Christmas Tree!",
        8: "Automating Cookie Clicker!",
        9: "TUI in Textual!",
        10: "No leeks :3",
        11: "No leeks :p",
        12: "Still no leeks :3c"
    }

    def __init__(self, day: int) -> None:
        self.day = day
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Here's what's in day {self.day}: {self.gifts.get(self.day)}")
            with Center():
                yield Button("Close", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
        event.stop()

class AdventCalendarApp(App):
    CSS = """
    Grid {
        grid-size: 4 3;
        grid-gutter: 1 1;
    }

    Grid Button {
        width: 9;
        height: 5;
        padding: 0;
        background: yellow;
        color: black;
        border: none;
    }

    Grid Button.opened {
        background: green;
    }

    Grid Button.locked {
        background: grey;
    }

    Grid Button:focus,
    Grid Button:focus-within {
        outline: none;
        border: none;
    }

    Grid Button:hover {
        background: $secondary;
    }
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    START_DATE = datetime.date(2025, 12, 13)

    def compose(self) -> ComposeResult:
        yield Header()
        with Grid():
            today = datetime.date.today()
            for day in range(1, 13):
                unlock_day = self.START_DATE + datetime.timedelta(days=day - 1)
                button = Button(str(day), id=f"day-{day}")
                if today < unlock_day:
                    button.add_class("locked")
                yield button
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.button
        day = int(button.id.split("-")[1])
        unlock_day = self.START_DATE + datetime.timedelta(days=day - 1)

        if button.has_class("locked"):
            self.notify(f"You can unlock day {day} on {unlock_day}")
            return

        if not button.has_class("opened"):
            button.add_class("opened")

        self.push_screen(DayScreen(day))

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

def main():
    AdventCalendarApp().run()

if __name__ == "__main__":
    main()
