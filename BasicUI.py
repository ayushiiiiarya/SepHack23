from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Static, Footer, Label, Input
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll
from textual.css.query import NoMatches
from textual.reactive import var
from textual_select import Select
from textual.containers import Vertical

import sys 
import subprocess
import time

TEXT = """\
Main UI 
"""
class HeaderApp(App):

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
    ]

    def on_mount(self) -> None:
        self.title = "CLI TUI"
        self.sub_title = " PLEXOS Cloud"
        
        CSS_PATH = "css.tcss"

    def compose(self) -> ComposeResult:
        yield Header(id="header")  # for header
        yield Footer()  # for footer
        dropdown_data = [
            {"value": 0, "text": "NA"},
            {"value": 1, "text": "EMEA"},
            {"value": 2, "text": "APAC"},
        ]
        yield Vertical(
            Label("Login Options:"),
            Select(
                placeholder="please select",
                items=dropdown_data,
                list_mount="#main_container"
            ),

            Label("Selected value:"),
            Input(value="-", id="selected_value"),
            id="main_container"
        )

        yield Horizontal( 
            VerticalScroll(
                #Button.error("Options:", disabled=True),
                Button("Create Study", classes="sidebar"),
                Button("Versioning", classes="sidebar"),
                Button("Run", classes="sidebar"),
            ), id="sidebar")  # for sidebar
        yield Static(TEXT, id="body") # for docking the sidebar

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if str(event.button._reactive_label) == "Login":
            result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)
        
        elif str(event.button._reactive_label) == "Change Environment":
           result = subprocess.check_output("pxc environment set NA", shell=True, stderr=subprocess.STDOUT, text=True)
           time.sleep(15)
           result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)

    def on_select_changed(self, event: Select.Changed) -> None:
        self.query_one("#selected_value").value = str(event.value)
        if 

if __name__ == "__main__":
    app = HeaderApp()
    app.run()