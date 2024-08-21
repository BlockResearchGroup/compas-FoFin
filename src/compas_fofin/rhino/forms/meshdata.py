from ast import literal_eval

import Eto.Drawing
import Eto.Forms
import Rhino
import Rhino.UI


class MeshDataForm(Eto.Forms.Dialog[bool]):
    """Form for working with mesh data.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    title : str, optional
        Title of the dialog.
    width : int, optional
        Window width.
    height : int, optional
        Window height.
    exclude_vertex_attr : list[str], optional
        The names of vertex attributes to exclude.
    exclude_edge_attr : list[str], optional
        The names of edge attributes to exclude.
    exclude_face_attr : list[str], optional
        The names of face attributes to exclude.

    """

    def __init__(
        self,
        mesh,
        title="Mesh Data",
        width=800,
        height=800,
        excluded_vertex_attr=None,
        excluded_edge_attr=None,
        excluded_face_attr=None,
    ):
        self.mesh = mesh
        self.excluded_vertex_attr = excluded_vertex_attr
        self.excluded_edge_attr = excluded_edge_attr
        self.excluded_face_attr = excluded_face_attr

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.vertexpage = Page(
            title="Vertices",
            defaults=self.mesh.default_vertex_attributes,
            keys=list(self.mesh.vertices()),
            valuefunc=self.mesh.vertex_attribute,
            excluded=self.excluded_vertex_attr,
        )
        self.edgepage = Page(
            title="Edges",
            defaults=self.mesh.default_edge_attributes,
            keys=list(self.mesh.edges()),
            valuefunc=self.mesh.edge_attribute,
            excluded=self.excluded_edge_attr,
        )
        self.facepage = Page(
            title="Faces",
            defaults=self.mesh.default_face_attributes,
            keys=list(self.mesh.faces()),
            valuefunc=self.mesh.face_attribute,
            excluded=self.excluded_face_attr,
        )
        control = Eto.Forms.TabControl()
        control.TabPosition = Eto.Forms.DockPosition.Top
        control.Pages.Add(self.vertexpage.widget)
        control.Pages.Add(self.edgepage.widget)
        control.Pages.Add(self.facepage.widget)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(0, 12, 0, 12), Eto.Drawing.Size(0, 0), True, True)
        layout.AddRow(control)
        layout.EndVertical()
        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()
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
        """Callback for the OK event."""
        try:
            self.vertexpage.process()
            self.edgepage.process()
            self.facepage.process()
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        """Callback for the CANCEL event."""
        self.Close(False)

    def show(self):
        """Show the form dialog."""
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


class Page(object):
    """Wrapper for Eto tab pages.

    Parameters
    ----------
    title : str
        The title of the tab page.
    defaults : dict[str, Any]
        Default values of the data attributes.
    keys : list[int | tuple[int, int]]
        The identifiers of the mesh components.
    valuefunc : callable
        Function for retrieving the value of a named data attribute of a specific component.

    Attributes
    ----------
    names : list[str]
        The names of the attributes, in alphabetical order.
    public : list[str]
        The names of the editable attributes.
    private : list[str]
        The names of the read-only attributes.
    cols : list[dict]
        A list of dicts with each dict representing the properties of a data column.
    rows : list[list[str]]
        The data per mesh components corresponding to the columns.

    """

    def __init__(self, title, defaults, keys, valuefunc, excluded=None):
        self.defaults = defaults
        self.keys = keys
        self.valuefunc = valuefunc
        self.excluded = excluded or []
        self.table = Table(self.cols, self.rows)
        self.widget = Eto.Forms.TabPage()
        self.widget.Text = title
        if self.names:
            # replace this by a dynamic layout
            # with the first row an overview of the default attribute values
            # and second row the data table
            self.widget.Content = self.table.widget

    @property
    def names(self):
        return sorted([name for name in self.defaults.keys() if name not in self.excluded])

    @property
    def public(self):
        return sorted([name for name in self.names if not name.startswith("_")])

    @property
    def private(self):
        return sorted([name for name in self.names if name.startswith("_")])

    @property
    def cols(self):
        cols = [
            {
                "name": "ID",
                "is_editable": False,
                "is_checkbox": False,
                "precision": None,
            }
        ]

        for name in self.public:
            default = self.defaults[name]
            col = {
                "name": name,
                "is_editable": True,
                "is_checkbox": False,
                "precision": None,
            }
            if isinstance(default, bool):
                col["is_checkbox"] = True
            elif isinstance(default, float):
                col["precision"] = "3f"
            cols.append(col)

        for name in self.private:
            default = self.defaults[name]
            col = {
                "name": name,
                "is_editable": False,
                "is_checkbox": False,
                "precision": None,
            }
            if isinstance(default, bool):
                col["is_checkbox"] = True
            elif isinstance(default, float):
                col["precision"] = "3f"
            cols.append(col)

        return cols

    @property
    def rows(self):
        rows = []
        for key in self.keys:
            row = [str(key)]
            for col in self.cols[1:]:
                name = col["name"]
                checkbox = col["is_checkbox"]
                precision = col["precision"]
                value = self.valuefunc(key, name)
                if precision:
                    value = "{0:.{1}}".format(float(value), precision)
                elif not checkbox:
                    value = str(value)
                row.append(str(value))
            rows.append(row)
        return rows

    def process(self):
        """Process the data of the page."""
        for row in self.table.data:
            key = literal_eval(row[0])
            for index, col in enumerate(self.table.cols):
                name = col["name"]
                editable = col["is_editable"]
                precision = col["precision"]
                if not editable:
                    continue
                value = row[index]
                if isinstance(value, str):
                    try:
                        value = literal_eval(value)
                    except Exception as e:
                        print(key, name, value, e)
                    else:
                        if precision:
                            value = float(value)
                        self.valuefunc(key, name, value)
                else:
                    if precision:
                        value = float(value)
                    self.valuefunc(key, name, value)


class Table(object):
    """Wrapper for Eto grid view.

    Parameters
    ----------
    cols
    rows

    """

    def __init__(self, cols, rows):
        def on_cell_formatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
            except Exception as e:
                print(e)

        self.widget = Eto.Forms.GridView()
        self.widget.ShowHeader = True
        self.widget.DataStore = rows

        for i, col in enumerate(cols):
            column = Eto.Forms.GridColumn()
            column.HeaderText = col["name"]
            column.Editable = col["is_editable"]
            if col["is_checkbox"]:
                cell = Eto.Forms.CheckBoxCell(i)
                column.DataCell = cell
            else:
                cell = Eto.Forms.TextBoxCell(i)
                cell.AutoSelectMode = Eto.Forms.AutoSelectMode.OnFocus
                cell.VerticalAlignment = Eto.Forms.VerticalAlignment.Center
                cell.TextAlignment = Eto.Forms.TextAlignment.Right
                column.DataCell = cell

            self.widget.Columns.Add(column)

        self.widget.CellFormatting += on_cell_formatting

        self.cols = cols
        self.rows = rows
        self.data = self.widget.DataStore
