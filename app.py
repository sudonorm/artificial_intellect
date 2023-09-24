import dash
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import os
from sys import platform as pltfrm_type
import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from Pages import prompttester
# import dash_daq as daq

PROD = False
DEBUG_MODE = True ### this should only be set to true when developing and not in production

# if pltfrm_type in ['win32', 'cygwin']:
#     PROD = False
#     DEBUG_MODE = True

dark_hljs = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.4.0/styles/stackoverflow-dark.min.css"

app = Dash(__name__, use_pages=True, pages_folder="", external_stylesheets=[dbc.themes.SPACELAB,
                          dark_hljs, dbc.icons.BOOTSTRAP],
            meta_tags=[{'name': 'viewport',
                                        'content': 'width=device-width, initial-scale=1.0'}], url_base_pathname="/artificialintellect/")

dash.register_page("prompttester", path='/', layout=prompttester.layout, name='Intellectual Summary Hub')
# dash.register_page("prompttester", layout=prompttester.layout, name='Prompt Tester')

navbar = dbc.Navbar([
    dbc.Container([
        html.A([
            html.Span('Intellectual Summary Hub',
                        className='d-none d-lg-inline-block align-middle'
                        ),
        ], href='/artificialintellect', className='navbar-brand fw-bold'),
        
    ], fluid=True)
])

footer = html.Span('Created with 💙 by Artificial Intellect',
    className="p-4 mt-5 text-left",
)

rootLayout = html.Div([
    dcc.Store(id='sessh', storage_type = 'session', data = {"filename":"", "pdf_content":"", "sections":[], "prompt":"", "user_input":"", "summary_section":"", "response":""}),
    navbar,                   
    dbc.Container(dash.page_container, fluid=True),
    footer,
    ])

app.layout = html.Div(id='dark-theme-container',
    children=[

    rootLayout,
    ])

if not PROD:
    if __name__ == "__main__":
        app.run(debug=DEBUG_MODE, port= 8181)
