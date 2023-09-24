import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import io
import base64
import openpyxl

import dash
from dash import dcc, html, no_update

import json
import os
import shutil
from pathlib import Path
import builtins

import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from utils.components.app_components import AppComponents
from utils.headers_getter import Headers
# from utils import folderPaths

import dash_uploader as du
from dash_uploader import callback as du_callback
import uuid
from io import BytesIO
from PyPDF2 import PdfReader
import fitz

app_components = AppComponents()
headers = Headers()


def read_pdf_file(contents, filename):
    """_summary_

    Args:
        contents (_type_): _description_
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    pdf_contents = ""
    sections = []

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        reader = PdfReader(BytesIO(decoded))
        doc = fitz.open(stream=BytesIO(decoded), filetype="pdf")

        # print("Here is the doc", doc)
        # print(doc.pages())
        # print(doc.get_page_text(0))
        # print(fonts(doc, True))

        sections = headers.get_title_headers(doc, False)

        print("We have", doc.page_count, "pages in this document...")

        for page_number in range(len(reader.pages)):

            try:
                page = reader.pages[page_number]
                pdf_contents += page.extract_text()
            except:
                
                print("Error while extracting text from page", page_number)
    except:
        print("Error while splitting or decoding document")

    return pdf_contents, sections

# layout
layout = html.Div([
    html.Div(id="output-index-hidden"),
    dcc.Download(id="download-dataframe-xlsx"),

    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Upload(
                            id='upload-pdf-file',
                            children=html.Div([
                                'Drag & drop or select ',
                                html.A('your pdf file')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '30'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),


                    ], style={'margin': 20, 'text-align':'center'}),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={"marginBottom": 20}),
            ]),

        ],  style={"marginBottom": 30}),
    ], title="1. Upload your Pdf file",), ],start_collapsed=True , style={"margin": 30}),

    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.H6("Section of paper", style={'textAlign': 'middle', 'font-weight': 'bold', 'margin':10})
                        ]),
                        dcc.Dropdown(
                            id='dpdn-section',
                            options=[],
                            multi=False,
                            placeholder='Select section...',
                            style=dict(width='100%', display='inline-block', verticalAlign='middle', marginLeft=5)
                        )
                    ]),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={"marginBottom": 20}),
            ], justify='center'),

        ],  style={"marginBottom": 30}),
    ], title="2. Select the section you want to summarize",), ],start_collapsed=True, style={"margin": 30}),
    
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([


            dbc.Row([
                dbc.Col(
                    [
                app_components.create_text_area(component_id="input-summary-text", placeholder="Review the section's content...")

            ], xs=12, sm=12, md=12, lg=12, xl=12, class_name="d-grid",
                        style={"margin": 10},
                    ),
                    ], style={"marginBottom": 20}, justify='center'),

        ],  style={"marginBottom": 30}),
    ], title="3. Review the section's text",), ],start_collapsed=True , style={"margin": 30}),

    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([


            dbc.Row([
                dbc.Col(
                    [
                app_components.create_text_area(component_id="input-prompt", placeholder="Enter your prompt here...")

            ], xs=12, sm=12, md=12, lg=12, xl=12, class_name="d-grid",
                        style={"margin": 10},
                    ),
                    ], style={"marginBottom": 20}, justify='center'),

        ],  style={"marginBottom": 30}),
    ], title="4. Modify your prompt",), ],start_collapsed=True , style={"margin": 30}),

    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    
                        dbc.Button("Generate Result", id="btn-gen-summary", className="me-1", style={"margin": 10}),
                    
                ], xs=12, sm=12, md=12, lg=12, xl=12, class_name="d-grid",
                        style={"margin": 10},),
            ], style={"marginBottom": 20},),
        ],  style={"marginBottom": 30}),

    ], title="5. Generate Summary",), ],start_collapsed=True , style={"margin": 30}),

    dbc.Accordion([ dbc.AccordionItem([

        dbc.Card([
            dbc.Row([
                dbc.Col([
                     dash_table.DataTable(
                                        id="export-table",
                                        data=[{}],
                                        page_size=50,
                                        sort_action="native",
                                        editable=False,
                                        style_table={'overflowX': 'auto'},
                                        columns=[],
                                        row_selectable=False,
                                        # export_format = "xlsx",
                                        export_columns ="all",
                                        export_headers = "display",
                                        row_deletable=False
                                    ),


                    ], xs=12, sm=12, md=12, lg=12, xl=12),
            ], style={"marginBottom": 20}, ),
        ],  style={"marginBottom": 30}),

     ], title="6. Review result",), ],start_collapsed=True , style={"margin": 30}),

     dbc.Accordion([ dbc.AccordionItem([

        dbc.Card([
            dbc.Row([
                dbc.Col([
                    dbc.Button("Download Excel", id="btn-xlsx", className="me-1", style={"margin": 10}),
                    
                    ], xs=12, sm=12, md=12, lg=12, xl=12, class_name="d-grid",style={"margin": 10},),
            ], style={"marginBottom": 20}, ),
        ],  style={"marginBottom": 30}),

     ], title="7. Download output file",), ],start_collapsed=True , style={"margin": 30}),


])


### 
@callback(
    [Output('dpdn-section', 'options'), Output('sessh', 'data', allow_duplicate=True)],
    [Input('upload-pdf-file', 'contents'), Input('upload-pdf-file', 'filename'), ],
    [State('sessh', 'data')],
    prevent_initial_call=True
)
def read_meta_data(list_of_contents, filename, sessh_data):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    sections = []

    if trigger_id == "upload-pdf-file":
        if list_of_contents is not None:
            pdf_contents, sections = read_pdf_file(
                list_of_contents, filename)

            sessh_data.update({"pdf_content":pdf_contents})
            sessh_data.update({"sections":sections})
            sessh_data.update({"filename":filename})
        
        return [{"label":x, "value":x} for x in sections], sessh_data
            
    return sections, sessh_data

### 
@callback(
    [Output('sessh', 'data'), Output('input-summary-text', 'value'), 
     Output('export-table', 'data'), Output('export-table', 'columns'),],
    [Input('dpdn-section', 'value'), Input('btn-gen-summary', 'n_clicks'),
     Input('input-prompt', 'value'), ],
    [State('sessh', 'data'),],
    prevent_initial_call=True
)
def summarize_data(section, n_clicks_gen, system_prompt, sessh_data):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
    user_input, gpt_response_lst, file_name, summary_section = "", [], "Data", "Summary"
    column_lst = ["summary"]
    export_df = pd.DataFrame(gpt_response_lst, columns=column_lst)
    

    if trigger_id == "dpdn-section":
        
        sections = sessh_data['sections']
        if section is None or sections is None or len(section) == 0 or len(sections) == 0:
            return no_update
        
        first_split = section[0]
        content = sessh_data['pdf_content']
        next_index = sections.index(first_split) + 1
        user_input = content.split(first_split)[1].split(sections[next_index])[0]

        sessh_data.update({"user_input":user_input})
        sessh_data.update({"summary_section":first_split})
        
    elif trigger_id == "input-prompt":
        sessh_data.update({"prompt":system_prompt})

    elif trigger_id == "btn-gen-summary":

        system_prompt = sessh_data['prompt']
        user_input = sessh_data['user_input']
        summary_section = sessh_data['summary_section']
        file_name = f'{sessh_data["filename"]}{"_"}{summary_section}' 

        # print("================")
        # print("system prompt is", system_prompt)
        # print(user_input)
        # print(summary_section)

        ##### GPT code goes here ######


        gpt_response = "Here's a nice summary of your input text"

        ##### End GPT code goes here ######

        gpt_response_lst = [gpt_response]
        sessh_data.update({"response":gpt_response_lst})

        column_lst = [f'summary_of_{summary_section.lower().replace(" ", "_")}']
        export_df = pd.DataFrame(sessh_data['response'], columns=column_lst)

        return sessh_data, sessh_data['user_input'], export_df.to_dict(orient="records"), [{'id': x, 'name': x} for x in column_lst]

    return sessh_data, sessh_data['user_input'], export_df.to_dict(orient="records"), [{'id': x, 'name': x} for x in column_lst]

@callback(
    Output("download-dataframe-xlsx", "data"),
    [Input('btn-xlsx', 'n_clicks'), ],
    [State('sessh', 'data'),],
    prevent_initial_call=True
)
def download_data(n_clicks_dwn, sessh_data):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if trigger_id == "btn-xlsx":
        
        summary_section = sessh_data['summary_section']
        file_name = f'{sessh_data["filename"]}{"_"}{summary_section}'
        column_lst = [f'summary_of_{summary_section.lower().replace(" ", "_")}']
        export_df = pd.DataFrame(sessh_data['response'], columns=column_lst)

        return dcc.send_data_frame(export_df.to_excel, file_name + ".xlsx", sheet_name=summary_section, index=False)


     