import ast

import Eto.Drawing
import Eto.Forms
import Rhino
import Rhino.UI


class AddDefaultAttributeForm(Eto.Forms.Dialog[bool]):
    def __init__(self, width=300, height=140):
        self.Title = "Add Default Attribute"
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(10, 0), True, True)

        key_label = Eto.Forms.Label(Text="Key:")
        self.key = Eto.Forms.TextBox()

        value_label = Eto.Forms.Label(Text="Value:")
        self.value = Eto.Forms.TextBox()

        layout.AddRow(key_label, self.key, value_label, self.value)
        layout.EndVertical()

        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()
        self.key_value_pair = None
        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text="Cancel")
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_ok(self, sender, event):
        key = self.key.Text
        value = self.value.Text
        try:
            value = ast.literal_eval(value)
        except Exception as e:
            print(e)
        if isinstance(value, (list, dict, tuple)):
            Eto.Forms.MessageBox.Show(str(type(value)) + "is mutable, use with caution.", "WARNING")
        if key == "":
            Eto.Forms.MessageBox.Show("Key cannot be empty.", "ERROR")
            self.Close(False)
        else:
            self.key_value_pair = (key, value)
            self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)


class DefaultAttributesForm(Eto.Forms.Dialog[bool]):
    def __init__(
        self,
        item,
        title="Edit Default Attributes",
        default_attributes_names=[
            "default_vertex_attributes",
            "default_edge_attributes",
            "default_face_attributes",
        ],
        width=500,
        height=500,
    ):
        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)
        self.item = item
        self.default_attributes_names = default_attributes_names

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True)

        self.tab_control = Eto.Forms.TabControl()
        self.tab_control.TabPosition = Eto.Forms.DockPosition.Top

        self.tables = {}
        for attribute_name in self.default_attributes_names:
            if not hasattr(item, attribute_name):
                continue
            attributes = getattr(item, attribute_name)
            tab = Eto.Forms.TabPage(Text=attribute_name)
            self.tab_control.Pages.Add(tab)
            table = self.map_tree(attributes)
            tab.Content = table

        layout.AddRow(self.tab_control)
        layout.EndVertical()
        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(self.add, self.delete, None, self.ok, self.cancel)
        layout.EndVertical()

        self.Content = layout

    def map_tree(self, attributes):
        table = Eto.Forms.TreeGridView()
        collection = Eto.Forms.TreeGridItemCollection()
        for k in sorted(attributes.keys()):
            collection.Add(Eto.Forms.TreeGridItem(Values=(k, str(attributes[k]))))
        table.DataStore = collection
        table.ShowHeader = True

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(1)
        table.Columns.Add(column)
        return table

    @property
    def table(self):
        return self.tab_control.SelectedPage.Content

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text="OK")
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text="Cancel")
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    @property
    def add(self):
        self.DefaultButton = Eto.Forms.Button(Text="Add")
        self.DefaultButton.Click += self.on_add
        return self.DefaultButton

    @property
    def delete(self):
        self.AbortButton = Eto.Forms.Button(Text="Delete")
        self.AbortButton.Click += self.on_delete
        return self.AbortButton

    def on_ok(self, sender, event):
        try:
            for tab in self.tab_control.Pages:
                table = tab.Content
                new_attributes = {}
                for item in table.DataStore:
                    name = item.GetValue(0)
                    value = item.GetValue(1)
                    try:
                        value = ast.literal_eval(value)
                    except Exception as e:
                        print(e)
                    new_attributes[name] = value
                setattr(self.item, tab.Text, new_attributes)
                print("Updated {} to:".format(tab.Text))
                print(new_attributes)
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def on_add(self, sender, event):
        form = AddDefaultAttributeForm()
        if form.ShowModal(self):
            key, value = form.key_value_pair
            for item in self.table.DataStore:
                if item.GetValue(0) == key:
                    Eto.Forms.MessageBox.Show("Key already exists.", "ERROR")
                    return
            item = Eto.Forms.TreeGridItem(Values=(key, str(value)))
            self.table.DataStore.Add(item)
            self.table.ReloadData()
            self.table.SelectedItem = item

    def on_delete(self, sender, event):
        item = self.table.SelectedItem
        if not item:
            Eto.Forms.MessageBox.Show("No item selectged.")
        else:
            key = item.GetValue(0)
            if (
                Eto.Forms.MessageBox.Show(
                    "Confirm to delete the attribute: '{}'?".format(key),
                    Eto.Forms.MessageBoxButtons.YesNo,
                )
                == Eto.Forms.DialogResult.Yes
            ):
                self.table.DataStore.Remove(item)
                self.table.ReloadData()

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


if __name__ == "__main__":
    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get("faces.obj"))

    form = DefaultAttributesForm(mesh)
    form.show()

    form = DefaultAttributesForm(mesh)
    form.show()
