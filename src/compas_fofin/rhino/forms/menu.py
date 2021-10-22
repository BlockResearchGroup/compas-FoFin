from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Eto.Drawing as drawing
import Eto.Forms as forms
import Rhino.UI

import json
import os
import importlib
import sys


HERE = os.path.dirname(__file__)
UI_FOLDER = os.path.join(HERE, "..", "..", "ui/Rhino/FoFin/dev")
sys.path.append(UI_FOLDER)


class MenuForm(forms.Form):

    def setup(self):
        self.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        self.Title = "FoFin"
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.Padding = drawing.Padding(5)
        self.load_config(layout)

        self.Content = forms.Scrollable()
        self.Content.Content = layout
        self.Padding = drawing.Padding(0)
        self.Resizable = True

    def load_config(self, layout):
        config = json.load(open(os.path.join(UI_FOLDER, "config.json")))
        menu = config["ui"]["menus"][0]
        commands = {cmd["name"]: cmd for cmd in config["ui"]["commands"]}
        self.add_items(menu["items"], layout, commands)

    def add_items(self, items, layout, commands):
        for item in items:
            if "command" in item:
                cmd = commands[item["command"]]
                button = forms.Button(Text=cmd["menu_text"])
                layout.Items.Add(button)
                package = importlib.import_module("%s_cmd" % item["command"])

                def on_click(package):
                    def _on_click(sender, e):
                        package.RunCommand(True)
                    return _on_click

                button.Click += on_click(package)

            if "items" in item:
                sub_layout = forms.DynamicLayout()
                collapseButton = forms.Button(Text=item["name"] + "  >", MinimumSize=drawing.Size.Empty)
                sub_layout.AddRow(collapseButton)
                layout.Items.Add(forms.StackLayoutItem(sub_layout))
                groupbox = forms.GroupBox(Visible=False)
                groupbox.Padding = drawing.Padding(5, 1)
                grouplayout = forms.StackLayout()
                grouplayout.Spacing = 5
                self.add_items(item["items"], grouplayout, commands)
                groupbox.Content = grouplayout
                layout.Items.Add(groupbox)

                def on_click(groupbox):
                    def _on_click(sender, e):
                        if groupbox.Visible:
                            groupbox.Visible = False
                            sender.Text = sender.Text.replace("-", ">")
                        else:
                            groupbox.Visible = True
                            sender.Text = sender.Text.replace(">", "-")
                    return _on_click

                collapseButton.Click += on_click(groupbox)

            if "type" in item and item["type"] == "separator":
                label = Rhino.UI.Controls.Divider()
                label.Width = 250
                layout.Items.Add(label)


if __name__ == "__main__":

    m = MenuForm()
    m.setup()
    m.Show()
