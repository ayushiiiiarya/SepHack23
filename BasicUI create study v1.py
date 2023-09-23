from __future__ import annotations
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Static, Footer, Label, Input
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll, HorizontalScroll
from textual.css.query import NoMatches
from textual.reactive import var
from textual_select import Select
from textual.containers import Vertical, Horizontal, Center
from textual import on
from textual_fspicker import FileOpen, FileSave, Filters, SelectDirectory

import sys,os
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

            id="main_container"
        )

        yield Horizontal(
            VerticalScroll(
                # Button.error("Options:", disabled=True),
                Button("Create Study", classes="sidebar"),
                Button("Versioning", classes="sidebar"),
                Button("Run", classes="sidebar"),
            ),
            id="sidebar",  # for sidebar
        )
        yield Static(TEXT, id="body")  # for docking the sidebar
        with Horizontal():
            yield Button("Open a file", id="open")
            yield Label("Press the button to pick something")

    def on_select_changed(self, event: Select.Changed) -> None:
        if str(event.value) == "0":
           result = subprocess.check_output("pxc environment set NA", shell=True, stderr=subprocess.STDOUT, text=True)
           time.sleep(5)
           result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)
        elif str(event.value) == "1":
           result = subprocess.check_output("pxc environment set EMEA", shell=True, stderr=subprocess.STDOUT, text=True)
           time.sleep(5)
           result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)
        elif str(event.value) == "2":
           result = subprocess.check_output("pxc environment set APAC", shell=True, stderr=subprocess.STDOUT, text=True)
           time.sleep(5)
           result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if str(event.button._reactive_label) == "Create Study":
            result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)
        elif str(event.button._reactive_label) == "Versioning":
           result = subprocess.check_output("pxc environment set NA", shell=True, stderr=subprocess.STDOUT, text=True)
        elif str(event.button._reactive_label) == "Run":
           result = subprocess.check_output("pxc environment set NA", shell=True, stderr=subprocess.STDOUT, text=True)

    def show_selected(self, to_show: Path | None) -> None:
        #if to_show is not None:
        #    label_text = str(to_show)
        #else:
        #   label_text = ""

        #self.query_one(Label).update(label_text)

        #print(str(to_show))
        path = str(to_show)
        xml_base_name = os.path.basename(to_show)
        xml_name=xml_base_name[0:-4]
        cmd = 'pxc study create --name "' +  xml_name + '" --database "' + path + '" --description "Created by TUI"'
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        
    @on(Button.Pressed, "#open")
    def open_file(self) -> None:
        """Show the `FileOpen` dialog when the button is pushed."""
        self.push_screen(
            FileOpen(
                ".",
                filters=Filters(
                    ("Any", lambda _: True),
                ),
            ),
            callback=self.show_selected,
        )


if __name__ == "__main__":
    app = HeaderApp()
    app.run()