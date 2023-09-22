from textual.app import App, ComposeResult
from textual.widgets import Header
from textual.binding import Binding
from textual.widgets import Footer
from textual.widgets import Static
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Static

TEXT = """\
Main UI 
"""

class HeaderApp(App):

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="delete", action="delete", description="Delete the thing"),
        Binding(key="j", action="down", description="Scroll down", show=False),
    ]

    def on_mount(self) -> None:
        self.title = "CLI TUI"
        self.sub_title = "With title and sub-title"
        
    
    
    CSS_PATH = "css.tcss"

    def compose(self) -> ComposeResult:
        yield Header(id="header")  # for header
        yield Footer()  # for footer
        yield Horizontal(
            VerticalScroll(
                Button("OPTIONS", classes="sidebar"),
                Button("LOGIN", classes="sidebar"),
                Button("Create Study", variant="primary", classes="sidebar"),
                Button("Versioning", classes="sidebar"),
                Button("Run", classes="sidebar"),
            ), id="sidebar")  # for sidebar
        yield Static(TEXT, id="body")  # for docking the sidebar

if __name__ == "__main__":
    app = HeaderApp()
    app.run()