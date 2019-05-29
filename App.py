import numpy as np

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from plotly.offline import plot
import plotly.graph_objs as go

from src.dates.date import Date
from src.App.Figures import launch_layout, plot_Data
from src.App.objectsHTML import SA_Button, SA_CalendarRange, SA_ButtonOutput, SA_Dropdown
from src.BlackScholes.BlackScholes import European




BuySell = "Buy"
S = 28
K = 28
Rf = 0.03
sessionDate = Date(day=8, month=4, year =2019)
maturityDate = Date(day=17, month=5, year =2019)
vola = 0.25
CP = 'C'
Div = 0.0 #0.01981857442,#0.190423182809269
typeDiv = 'Cont'

kinput = [0.95, 1, 1.05]

args = {        'BuySell'            : BuySell,
                'S'                  : S,
                'K'                  : K,
                'Rf'                 : Rf,
                'sessionDate'        : sessionDate ,
                'maturityDate'       : maturityDate,
                'vola'               : vola,
                'CP'                 : CP,
                'Div'                : Div,
                'typeDiv'            : typeDiv}

OpC = European(BuySell=BuySell,
              S=S,
              K=K,
              Rf =Rf,
              sessionDate=sessionDate,
              maturityDate=maturityDate,
              vola = vola,
              CP = "C",
              Div= Div,
              typeDiv = typeDiv)

OpP = European(BuySell=BuySell,
              S=S,
              K=K,
              Rf =Rf,
              sessionDate=sessionDate,
              maturityDate=maturityDate,
              vola = vola,
              CP = "P",
              Div= Div,
              typeDiv = typeDiv)

cminusp = round(OpC.Price()-OpP.Price(),4)

Op = OpC if CP == "C" else OpP


Opgreeks = {
    'price'      : Op.Price(),
    'intrinsic'  : Op.intrinsic(),
    'delta'      : Op.Delta(),
    'gamma'      : Op.Gamma(),
    'vega'       : Op.Vega(),
    'rho'        : Op.Rho(),
    'theta'      : Op.Theta()
}


fig = launch_layout(data=plot_Data(args=args, parameter='S',  kinput=kinput), buysell=BuySell, callput='S', parameter="S",  kinput=kinput,Graphic='Greeks')

sessionDatedt = dt(sessionDate.year(), sessionDate.month(), sessionDate.day())
maturityDatedt = dt(maturityDate.year(), maturityDate.month(), maturityDate.day())

cpstart = [1,0] if CP == "C" else [0,1]
bsstart = [1,0] if BuySell== "Buy" else [0,1]

######################################################### BEGIN APP ##########################################################
app = dash.Dash(__name__)

app.title = "Option Greeks App"

app.config.supress_callback_exceptions = True
app.scripts.config.serve_locally=False

########## WIDGETS ############################

SButton = html.Div([SA_Button(name="Underlying", colorB= "danger", colorI="danger", id="S",value=S)
                    ],className="col justify-content-center text-center")
KButton = html.Div([SA_Button(name="Strike", colorB= "danger", colorI="danger", id="K",value=K)
                    ],className="col justify-content-center text-center")
RfButton = html.Div([SA_Button(name="Interest Rate", colorB= "danger", colorI="danger", id="Rf",value=Rf)
                     ],className="col justify-content-center text-center")
DivButton = html.Div([SA_Button(name="Dividend Yield", colorB= "danger", colorI="danger", id="Div",value=Div)
                      ],className="col justify-content-center text-center")
VolaButton = html.Div([SA_Button(name="Volatility", colorB= "danger", colorI="danger", id="Vola",value=vola)
                      ],className="col justify-content-center text-center")

DatesPicker = html.Div([SA_CalendarRange(name="Option Dates", colorB="danger", colorI="danger", id="Dates", iniDate=sessionDatedt, endDate=maturityDatedt)
          ], className="col justify-content-center text-center")


CALLPUTRadioDBC =html.Div([
    dbc.ButtonGroup([
        dbc.Button("Call",color="primary" ,id="C", n_clicks_timestamp=cpstart[0]),
        dbc.Button("Put", color="success", id ="P", n_clicks_timestamp =cpstart[1])
    ])
], className="col justify-content-center text-center")

BUYSELLRadioDBC =html.Div([
    dbc.ButtonGroup([
        dbc.Button("Buy",color="success" ,id="Buy", n_clicks_timestamp=bsstart[0]),
        dbc.Button("Sell", color="danger", id ="Sell", n_clicks_timestamp =bsstart[1])
    ])
], className="col justify-content-center text-center")

dropdownParameter =  html.Div([SA_Dropdown(name="Parameter", Options=["Underlying", "Volatility"], optionsValue=["S","Volatility"],colorB="danger", colorI="danger", id='param', value="S")
                               ],className="col  text-center")

dropdownGraphic =  html.Div([SA_Dropdown(name="Graph", Options=['Greeks','Price', 'Delta', 'Gamma', 'Vega', 'Rho', 'Theta'], optionsValue=['Greeks','Price', 'Delta', 'Gamma', 'Vega', 'Rho', 'Theta'],colorB="danger", colorI="danger", id='graphic', value="Greeks")
                               ],className="col  text-center")

PriceButton = html.Div([SA_ButtonOutput(name="Price", colorB= "dark", colorI="danger", id="Opprice",value=Opgreeks['price'])
                    ],className="col text-center")
DeltaButton = html.Div([SA_ButtonOutput(name="Delta", colorB= "dark", colorI="danger", id="Opdelta",value=Opgreeks['delta'])
                    ],className="col text-center")
GammaButton = html.Div([SA_ButtonOutput(name="Gamma", colorB= "dark", colorI="danger", id="Opgamma",value=Opgreeks['gamma'])
                    ],className="col text-center")
VegaButton = html.Div([SA_ButtonOutput(name="Vega", colorB= "dark", colorI="danger", id="Opvega",value=Opgreeks['vega'])
                    ],className="col text-center")
RhoButton = html.Div([SA_ButtonOutput(name="Rho", colorB= "dark", colorI="danger", id="Oprho",value=Opgreeks['rho'])
                    ],className="col text-center")
ThetaButton = html.Div([SA_ButtonOutput(name="Theta", colorB= "dark", colorI="danger", id="Optheta",value=Opgreeks['theta'])
                    ],className="col text-center")
cminuspButton = html.Div([SA_ButtonOutput(name="C - P", colorB= "primary", colorI="danger", id="cminusp",value=cminusp)
                    ],className="col-2 col-xs text-center")
skButton = html.Div([SA_ButtonOutput(name="S - K exp(-rt)", colorB= "primary", colorI="danger", id="sk",value=Op.sk())
                    ],className="col-2 col-xs text-center")

########## LAYOUT ############################

app.layout =\
    html.Div([  ## Container Div
        html.Div([  ## Title div
            html.H3(["",dbc.Badge("Option Greeks App", color="danger")])
        ],className="row justify-content-center"), ## Title div
        html.Div([
            html.Div([
                html.Div([
                    BUYSELLRadioDBC,
                    CALLPUTRadioDBC
                ], className="row"),
                html.Div([" "], className="row"),
                html.Div([
                    dropdownParameter,
                    dropdownGraphic
                ], className="row")
            ], className="col-3 center"),
            html.Div([
                html.Div([
                    SButton,
                    RfButton
                ], className="row center"),
                html.Div([
                    KButton,
                    DivButton
                ], className="row")
            ], className="col-6 center"),
            html.Div([
                html.Div([
                    VolaButton],
                    className="row"),
                html.Div([
                    DatesPicker
                ], className="row")
            ], className="col-3 center")
        ], className="row"),  ## Widgets Div row 1
        html.Div([ ## Image div
            dcc.Graph( ## Graph
                id='Greeks_plot', figure=fig, style={'height': '75vh'},
           className="col-md-12"), ## Graph
            ],className="row justify-content-center"), ## Image Div
        html.Div(className="row"),
        html.Div(className="row"),
        html.Div([
            PriceButton,
            DeltaButton,
            GammaButton,
            VegaButton,
            RhoButton,
            ThetaButton
        ],className="row")

],className="container-fluid")


########## CALLBACKS ############################

@app.callback([Output('Greeks_plot', 'figure'),
               Output('Opprice', 'value'), Output('Opdelta', 'value'), Output('Opgamma', 'value'), Output('Opvega', 'value'), Output('Oprho', 'value'), Output('Optheta', 'value'),
               Output('cminusp', 'value'), Output('sk', 'value')],
              [Input('Buy', 'n_clicks_timestamp'), Input('Sell', 'n_clicks_timestamp'),Input('S', 'value'), Input('K', 'value'), Input('Rf', 'value'), Input('Div', 'value'),
               Input('Dates', 'start_date'), Input('Dates', 'end_date'),  Input('Vola', 'value'),Input('C', 'n_clicks_timestamp'), Input('P', 'n_clicks_timestamp'),
               Input('param', 'value'), Input('graphic', 'value')])
def update_figure(Buy, Sell,S, K, Rf, Div, start_Date, end_Date, vola, C, P, Param, Graphic):
    print(start_Date)
    print(end_Date)
    print(C)
    print(P)

    CP = "C" if C>P else "P"
    BS = "Buy" if Buy > Sell else "Sell"

    sessionDate = Date(year=int(start_Date[0:4]), month=int(start_Date[5:7]), day=int(start_Date[8:10]))
    maturityDate = Date(year=int(end_Date[0:4]), month=int(end_Date[5:7]), day=int(end_Date[8:10]))

    args = {'BuySell': BS,
            'S': S,
            'K': K,
            'Rf': Rf,
            'sessionDate': sessionDate,
            'maturityDate': maturityDate,
            'vola': vola,
            'CP': CP,
            'Div': Div,
            'typeDiv': typeDiv}

    OpC = European(BuySell=BS,
                  S=S,
                  K=K,
                  Rf=Rf,
                  sessionDate=sessionDate,
                  maturityDate=maturityDate,
                  vola=vola,
                  CP="C",
                  Div=Div,
                  typeDiv=typeDiv)

    OpP = European(BuySell=BS,
                  S=S,
                  K=K,
                  Rf=Rf,
                  sessionDate=sessionDate,
                  maturityDate=maturityDate,
                  vola=vola,
                  CP="P",
                  Div=Div,
                  typeDiv=typeDiv)

    Op = OpC if CP == "C" else OpP

    cminusp = round(OpC.Price() - OpP.Price(),4)


    return launch_layout(data=plot_Data(args=args, parameter=Param,  kinput=kinput), buysell=BS ,callput=CP, parameter=Param,  kinput=kinput, Graphic=Graphic) , Op.Price(), Op.Delta(),  Op.Gamma(), Op.Vega(), Op.Rho(), Op.Theta(), cminusp, Op.sk()




if __name__ == '__main__':
    app.run_server(debug=False)


