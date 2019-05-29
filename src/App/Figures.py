
from src.dates.date import Date
import numpy as np
from plotly.offline import plot
from plotly import tools
import plotly.graph_objs as go
from src.BlackScholes.BlackScholes import European

def callPut(x):
    out = {"C" : "C",
           "P" : "P"}
    return out[x]


def parameterName(x):
    out = {"S" : "Underlying Price",
           "Volatility" : "Volatility"}
    return out[x]

def graphicName(x):
    out = {"Price" : "traceprice_",
           "Delta" : "tracedelta_",
           "Gamma": "tracegamma_",
           "Vega": "tracevega_",
           "Rho": "tracerho_",
           "Theta": "tracetheta_"}
    return out[x]





def plot_Data(args, parameter:str, kinput):

    kcolors=['#28a745','#007bff','#dc3545']

    data = {}

    print('parameter is:')
    print(parameter)
    BuySell = args['BuySell']
    S = args['S']
    K = args['K']
    Rf = args['Rf']
    sessionDate = args['sessionDate']
    maturityDate = args['maturityDate']
    vola = args['vola']
    CP = args['CP']
    Div = args['Div']
    typeDiv = args['typeDiv']


    Kvalues = [round(K * kinput[0],2), round(K * kinput[1],2), round(K * kinput[2],2)]
    kcount=0
    for kv in Kvalues:

        price = []
        delta = []
        gamma = []
        vega = []
        theta = []
        rho = []
        intrinsic = []

        if parameter == 'S':
            steps = list(np.linspace(start=(S * 0.85), stop=(S * 1.15), num= 49).round(decimals=3))

            for i in range(0, len(steps)): # by S
                O = European(
                    BuySell=BuySell,
                    S=steps[i],
                    K=kv,
                    Rf=Rf,
                    sessionDate=sessionDate,
                    maturityDate=maturityDate,
                    vola=vola,
                    CP=CP,
                    Div=Div,
                    typeDiv=typeDiv)
                price.append(O.Price())
                delta.append(O.Delta())
                gamma.append(O.Gamma())
                vega.append(O.Vega())
                theta.append(O.Theta())
                rho.append(O.Rho())
                intrinsic.append(O.intrinsic())

        elif parameter == 'Volatility': # by Vola
            steps = list(np.linspace(start=(vola * 0.5), stop=(vola * 1.5), num=49).round(decimals=3))

            for i in range(0, len(steps)):  # by S
                O = European(
                    BuySell=BuySell,
                    S=S,
                    K=kv,
                    Rf=Rf,
                    sessionDate=sessionDate,
                    maturityDate=maturityDate,
                    vola=steps[i],
                    CP=CP,
                    Div=Div,
                    typeDiv=typeDiv)
                price.append(O.Price())
                delta.append(O.Delta())
                gamma.append(O.Gamma())
                vega.append(O.Vega())
                theta.append(O.Theta())
                rho.append(O.Rho())
                intrinsic.append(O.intrinsic())

        if kcount==0:
            traceprice = go.Scatter(x=steps, y=price, mode = 'lines', line = dict(width = 2,color = kcolors[kcount]), name = 'K = ' + str(round(kv,2)))
        elif kcount==1:
            traceprice = go.Scatter(x=steps, y=price, mode='lines', line=dict(width=2, color=kcolors[kcount]), name = 'K = ' + str(round(kv,2)))
        elif kcount==2:
            traceprice = go.Scatter(x=steps, y=price, mode='lines', line=dict(width=2, color=kcolors[kcount]), name = 'K = ' + str(round(kv,2)))

        traceintrinsic = go.Scatter(x=steps, y=intrinsic, mode='lines', line = dict(width = 2,color = kcolors[kcount],dash = 'dot'), name = 'K = ' + str(round(kv,2)), showlegend=False)
        tracedelta = go.Scatter(x=steps, y=delta, mode = 'lines', line = dict(width = 2,color = kcolors[kcount]), name = 'K = ' + str(round(kv,2)), showlegend=False)
        tracegamma = go.Scatter(x=steps, y=gamma,  mode = 'lines', line = dict(width = 2,color = kcolors[kcount]), name = 'K = ' + str(round(kv,2)), showlegend=False)
        tracevega = go.Scatter(x=steps, y=vega,  mode = 'lines', line = dict(width = 2,color = kcolors[kcount]),name = 'K = ' + str(round(kv,2)), showlegend=False)
        tracetheta = go.Scatter(x=steps, y=theta,  mode = 'lines',  line = dict(width = 2,color = kcolors[kcount]), name = 'K = ' + str(round(kv,2)), showlegend=False)
        tracerho = go.Scatter(x=steps, y=rho,  mode = 'lines', line = dict(width = 2,color = kcolors[kcount]),name = 'K = ' + str(round(kv,2)), showlegend=False)

        data['traceprice_' + str(kinput[kcount])] = traceprice
        data['traceintrinsic_' + str(kinput[kcount])] = traceintrinsic
        data['tracedelta_' + str(kinput[kcount])] = tracedelta
        data['tracegamma_' + str(kinput[kcount])] = tracegamma
        data['tracevega_' + str(kinput[kcount])] = tracevega
        data['tracetheta_' + str(kinput[kcount])] = tracetheta
        data['tracerho_' + str(kinput[kcount])] = tracerho

        kcount += 1


    return data

def launch_layout_only1(data, buysell:str,callput:str, parameter:str, kinput, Graphic:str):

    itemname = graphicName(Graphic)
    fig = tools.make_subplots(rows=1, cols=1)

    for i in range(0,len(kinput)):

        data_single = data[itemname + str(kinput[i])]
        data_single.showlegend=True

        fig.append_trace(data_single, 1,1)

        if Graphic == 'Price':
            fig.append_trace(data['traceintrinsic_' + str(kinput[i])], 1, 1)


    CP = "Call" if callput == "C" else "Put"

    fig['layout'].update(title=buysell + " " +CP +' Option: Option '+ Graphic +' by '+ parameterName(parameter)+ '.')


    return fig

def launch_layout_all(data, buysell:str, callput:str, parameter:str, kinput):


    fig = tools.make_subplots(rows=3, cols=2, subplot_titles=('Option Price','Option Vega','Option Delta',
                                                              'Option Rho', 'Option Gamma','Option Theta'))

    for i in range(0,len(kinput)):

        fig.append_trace(data['traceprice_' + str(kinput[i])], 1,1)
        #fig.append_trace(data['traceintrinsic_' + str(kinput[i])], 1, 1)
        fig.append_trace(data['tracedelta_' + str(kinput[i])], 2, 1)
        fig.append_trace(data['tracegamma_' + str(kinput[i])], 3, 1)

        fig.append_trace(data['tracevega_' + str(kinput[i])], 1, 2)
        fig.append_trace(data['tracerho_' + str(kinput[i])], 2, 2)
        fig.append_trace(data['tracetheta_' + str(kinput[i])], 3, 2)

    CP = "Call" if callput == "C" else "Put"

    fig['layout'].update(title=buysell + " " + CP +' Option: Option Greeks by '+ parameterName(parameter)+ '.')
    #fig.layout.paper_bgcolor = bgcol
    #fig.layout.plot_bgcolor = bgcol


    return fig


def launch_layout(data, buysell:str, callput:str, parameter:str, kinput, Graphic:str):

    if Graphic == 'Greeks':

        return launch_layout_all(data=data,buysell=buysell, callput=callput, parameter=parameter, kinput=kinput)

    else:
        return launch_layout_only1(data=data, buysell=buysell, callput=callput, parameter=parameter, kinput=kinput, Graphic=Graphic)





if __name__ == "__main__":
    kinput = [0.9,1,1.1]

    BuySell = "Buy"


    args = {    'BuySell'            : "Buy",
                'S'                  : 4.9,
                'K'                  : 4.9,
                'Rf'                 : 0.03,
                'sessionDate'        : Date(day=11, month=2, year =2018),
                'maturityDate'       : Date(day=11, month=3, year =2018),
                'vola'               : 0.25,
                'CP'                 : "C",
                'Div'                : 0.025,#0.01981857442,#0.190423182809269,
                'typeDiv'            : 'Cont'}

    plot(launch_layout(data=plot_Data(args=args, parameter='S', kinput=kinput), buysell=BuySell, callput="C", parameter='S', kinput=kinput, Graphic="Rho"), filename='Greeks.html')


