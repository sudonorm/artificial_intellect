
import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc

class AppComponents:

    def create_text_area(self, component_id:str, placeholder:str) -> html.Div:

        text_area = html.Div(className='textareacontainer',
            children=[
                dbc.Textarea(id=component_id, className="mb-3", placeholder=placeholder, style={'width': '100%', 'height': '300px', 'overflowY': 'scroll'}),
               
            ]
        )

        return text_area