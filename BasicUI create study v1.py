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

 

import sys,os, webbrowser
import subprocess
import time

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


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
        with Horizontal():
            yield Button("Create Study", id="open")
            yield Label("Press the button to pick something")

 

        yield Horizontal(
            VerticalScroll(
                # Button.error("Options:", disabled=True),
                #Button("Create Study", classes="sidebar"),
                Button("Versioning", classes="sidebar"),
                Button("Run", classes="sidebar"),
            ),
            id="sidebar",  # for sidebar
        )
        yield Static(TEXT, id="body")  # for docking the sidebar

 

 

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
        #if str(event.button._reactive_label) == "Create Study":
            #result = subprocess.check_output("pxc auth login", shell=True, stderr=subprocess.STDOUT, text=True)
        if str(event.button._reactive_label) == "Versioning":
           
           file1 = open("tui_demo.txt","r")
           path2= file1.read()
           study_id = os.listdir(path2+"\\.plexoscloud")[0]
           ver_cmd = 'pxc study changeset push --studyId "' +study_id+'" --message "Chaged using TUI"'
           result = subprocess.check_output(ver_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
           
        elif str(event.button._reactive_label) == "Run":
           file1 = open("tui_demo.txt","r")
           path2= file1.read()
           study_id = os.listdir(path2+"\\.plexoscloud")[0]
           cloud_url = "https://cloud-web-eeprod-na.energyexemplar.com/studies/" + study_id + "/models"
           #result = subprocess.check_output(webbrowser.get(chrome_path).open(cloud_url), shell=False, stderr=subprocess.STDOUT, text=False)
           result = subprocess.run(webbrowser.open_new_tab(cloud_url))

    def show_selected(self, to_show: Path | None) -> None:
        path = str(to_show)
        folder_path = path.split("\\")
        folder_path = folder_path[0:-1]
        listToStr = '\\'.join(map(str, folder_path))
        f = open("tui_demo.txt", "w")
        f.write(listToStr)
        f.close()
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