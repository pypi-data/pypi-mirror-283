from importlib import resources

from dash import Dash, Input, Output, State, html, ALL, ctx

from .queries import check_foreign_key_uniqueness, LoadTableCallback, UpdateCellCallback
from .layout import layout
from .models import BananaTables, Config
from .utils import read_yaml


class Banana(Dash):
    def __init__(self):
        # Read config file
        data = read_yaml("config.yaml")
        config = Config(**data)
        check_foreign_key_uniqueness(config)

        # Create app
        super().__init__(
            assets_folder=resources.files("banana") / "assets",
            title=config.title,
        )
        self.layout = layout

        @self.callback(
            Output("banana--menu", "children"),
            Input("banana--menu", "style"),
        )
        def load_menu(_):
            data = read_yaml(config.tables_file)
            tables = BananaTables(**data)

            return [
                html.A(
                    table.display_name,
                    href=f"/{table.name}",
                    className="menu-item",
                    id={"type": "menu-item", "id": table.name},
                )
                for table in tables.tables
            ]

        @self.callback(
            Output("banana--table", "columnDefs"),
            Output("banana--table", "rowData"),
            Output("banana--table", "getRowId"),
            Output("banana--table-title", "children"),
            Input("banana--location", "pathname"),
            prevent_initial_call=True,
        )
        def load_table(pathname: str):
            obj = LoadTableCallback(pathname, config)
            return obj.column_defs, obj.row_data, obj.row_id, obj.table_title

        @self.callback(
            Input("banana--table", "cellValueChanged"),
            State("banana--location", "pathname"),
        )
        def update_cell(data, pathname):
            obj = UpdateCellCallback(data, pathname, config)
            obj.exec()

        @self.callback(
            Output({"type": "menu-item", "id": ALL}, "className"),
            Input("banana--location", "pathname"),
        )
        def change_menu_item_style_on_selected(table_name):
            return [
                (
                    "menu-item selected"
                    if item["id"]["id"] == table_name[1:]
                    else "menu-item"
                )
                for item in ctx.outputs_list
            ]
