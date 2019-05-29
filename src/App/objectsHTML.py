import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

def SA_Button(name:str, colorB:str, colorI:str, id:str,value ):
    return html.Div([
        html.Div([
            html.Button(name, className="btn btn-" + colorB)
        ], className="input-group-prepend"),
        dcc.Input(id=id, step= value * 0.1 ,type='number', value=value, className="btn btn-sm btn-" + colorI + " text-dark text-strong")
    ], className="input-group input-group-xs mb-2")



def SA_Dropdown(name:str, Options:list, optionsValue:list, colorB:str, colorI:str, id:str,value):

    return html.Div([
        html.Div([
            html.Button(name, className="btn btn-" + colorB)
        ], className="input-group-prepend"),
        dcc.Dropdown(id=id,
                     options=[{'label': Options[i], 'value': optionsValue[i]} for i in range(0, len(Options))],
                     value=value,
                     className="btn btn-sm btn-" + colorI + " text-dark")
    ], className="input-group input-group-xs mb-2")



def SA_ButtonOutput(name:str, colorB:str, colorI:str, id:str,value ):
    return html.Div([
        html.Div([
            html.Button(name, className="btn btn-" + colorB)
        ], className="input-group-prepend"),
        dbc.Input(id=id, placeholder=value, className="btn btn-sm btn-" + colorI + " text-dark text-strong")
    ], className="input-group input-group-xs mb-2")


def SA_CalendarRange(name:str, colorB:str, colorI:str, id:str, iniDate, endDate):
    return html.Div([
        html.Button(name,
                    className="btn btn-" + colorB),
        html.Div([dcc.DatePickerRange(
            id=id,
            start_date_placeholder_text="Session Date",
            end_date_placeholder_text="Maturity Date",
            start_date=iniDate,
            end_date=endDate,
            number_of_months_shown=4,
            with_portal=True,
            calendar_orientation='horizontal',
            className= "btn btn-sm btn-outline-" + colorI )]
        )]
        ,className="input-group input-group-xs mb-2")
