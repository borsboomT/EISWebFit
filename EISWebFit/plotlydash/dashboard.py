"""Instantiate a Dash app."""
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import glob
import cmath
from impedance.models.circuits import CustomCircuit

from .data import create_dataframe
from .layout import html_layout
from .fitEIS import *


def makeFig(rawdf,fitDF=pd.DataFrame()):

    figN = go.Figure(
        layout=go.Layout(
            {
                "title": "Nyquist",
                'yaxis': {
                    'title': '-Im(Z) / \u03A9 cm<sup>-2</sup> '
                },
                'xaxis': {
                    'title': 'Re(Z) / \u03A9 cm<sup>-2</sup>'
                },
                "margin": {"b": 0}
            }
        )
    )

    figN.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )

    df = rawdf.copy()

    df["negIm"] = -df["Im"]

    df = df.astype(float)

    figN.add_trace(go.Scatter(x=df["Re"], y=df["negIm"], name="Data", mode="markers"))

    if not fitDF.empty:
        fitDF = fitDF.astype(float)
        figN.add_trace(go.Scatter(x=fitDF["mRe"], y=fitDF["mIm"], mode="lines", name="Fits"))

    figB = make_subplots(specs=[[{"secondary_y": True}]])


    figB.update_layout(title_text="Bode")
    figB.update_yaxes(title_text='|Z| / \u03A9 cm<sup>-2</sup> ', secondary_y=False)
    figB.update_xaxes(title_text='f / Hz',type="log")
    figB.update_yaxes(title_text='Phase / \u00b0', secondary_y=True)



    df["mag"] = (df["Re"] + df["Im"]*1j).abs()
    df["phase"] = (df["Re"] + df["Im"]*1j).apply(cmath.phase)

    df = df.astype(float)


    figB.add_trace(go.Scatter(x=df["f"], y=df["mag"], name="Magnitude", mode="markers"))
    figB.add_trace(go.Scatter(x=df["f"], y=df["phase"], name="Phase", mode="markers"),secondary_y=True)


    return figN, figB



def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Load DataFrame


    inputList = glob.glob("data/*")

    tickerList = []

    for item in inputList:
        name = item.split("\\")[1]
        ext = name.split(".")[1]
        name = name.split(".")[0]
        if ext =="txt":
            tickerList.append({"label":name,"value":item})

    df = create_dataframe("Start")



    circuitOptions = [
        {"value":"R0-p(C1,R1)","label":"RCR"},
        {"value": 'R0-p(Q1,R1)', "label": "RQR"},
        {"value": 'R0-p(C1,R1-p(C2,R2))', "label": "RCRCR"},
        {"value": 'R0-p(Q1,R1-p(C2,R2))', "label": "RQRCR"}
    ]

    # Custom HTML layout
    dash_app.index_string = html_layout

    figN,figB = makeFig(df)


    # Create Layout
    dash_app.layout = html.Div(
        children=[
            "File: ",
            dcc.Dropdown(
                id="inputDropdown",
                options=tickerList,
                placeholder="Select a file."
            ),
            html.Div([
                "Circuit: ",
                dcc.Dropdown(
                    id="circuitDropdown",
                    options=circuitOptions,
                    value="RCR",
                    placeholder="Select a circuit."
                ),
                html.Div(children=[
                    html.Button('Submit', id='submit-val', n_clicks=0),
                    html.Div(id='container-button-basic',
                             children='Choose an input file and a circuit to fit.')

                ],
                id = "possibleInputVals"
                ),
            dcc.Graph(
                id="nyquistPlot",
                figure=figN,
                ),
            dcc.Graph(
                id="bodePlot",
                figure=figB,
                )
            ]),

            create_data_table(df),
        ],
        id="dash-container",
    )

    @dash_app.callback(
        [Output("nyquistPlot","figure"),
        Output("bodePlot", "figure"),
        Output("database-table","data"),
        Output('container-button-basic', 'children')],

        Input("inputDropdown","value"),
        Input('submit-val', 'n_clicks'),

        State('circuitDropdown', 'value'),
        State({"index":ALL,"type":"valInput"}, 'value'),
        State({"index": ALL, "type": "valInput"}, 'id')
    )
    def updateFigure(inputStr,clicks,circuit,values,labels):


        print("************")
        print("UPDATE")
        print("************")

        ctx = dash.callback_context

        print(ctx.triggered)

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        df = create_dataframe(inputStr)

        tableDF = df.applymap(lambda x: round(x,2))


        # circuit = circuit["value"]

        create_data_table(df)


        if button_id == "submit-val" and values[0] is not None:



            initial = values
            initial = [float(i) for i in initial]




            fitDF,fits = fitData(df,circuit,initial)








            figN,figB = makeFig(df,fitDF)


            outputString = "Fit Results: "
            for entry,fit in zip(labels,fits):
                element = entry["index"]
                if "R" in element:
                    outputString = outputString+element+" = " + str(round(fit,1))+"\n"
                elif "A" in element:
                    outputString = outputString + element + " = " + str(round(fit, 2)) + "\n"
                elif "C" in element or "Q" in element:
                    outputString = outputString + element + " = " + str(round(fit, 8)) + "\n"


            fitRes = outputString
        else:

            figN,figB = makeFig(df)

            fitRes = "Enter initial guesses."


        # return [fig, create_data_table(df), fitRes]
        return [figN,figB,tableDF.to_dict("records"),fitRes]

    @dash_app.callback(
        [Output("possibleInputVals", "children")],

        Input('circuitDropdown', 'value'),

    )
    def updateInputVals(circuit):

        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]


        Rnum = 0
        Cnum = 0
        Qnum = 0
        childList = []
        if circuit is not None:
            for char in circuit:
                if char == "R":
                    Rnum = Rnum + 1
                    childList.append(dcc.Input(id={"index":"R"+str(Rnum),"type":"valInput"}, type="text", placeholder=
                                               "R" + str(Rnum),value=""))
                elif char == "C":
                    Cnum = Cnum + 1
                    childList.append(dcc.Input(id={"index":"C"+str(Cnum),"type":"valInput"}, type="text", placeholder=
                                               "C" + str(Cnum),value=""))
                elif char == "Q":
                    Qnum = Qnum + 1
                    childList.append(dcc.Input(id={"index": "Q" + str(Qnum), "type": "valInput"}, type="text",
                                               placeholder= "Q" + str(Qnum)))
                    childList.append(dcc.Input(id={"index": "A" + str(Qnum), "type": "valInput"}, type="text", placeholder=
                                               "Alpha" + str(Qnum),value=""))


            childList.append(html.Button('Submit', id='submit-val', n_clicks=0))
            childList.append(html.Div(id='container-button-basic',
                         children='Enter a value and press submit'))
        else:
            childList.append(html.Div(id='container-button-basic',
                                      children='Choose an input file and a circuit to fit.'))

        return [childList]

    return dash_app.server



def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns = [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table
