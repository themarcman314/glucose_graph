from dash import Dash, html, dash_table, dcc, Input, Output, callback, no_update
import pandas as pd
import plotly.express as px
from datetime import date
from datetime import datetime
import sqlite3
from dash.exceptions import PreventUpdate

con = sqlite3.connect("my_db")  

df = pd.read_sql_query("select timestamp, value from glucose WHERE date(timestamp) = date('now');", con)
con.close()

today = date.today()

def create_figure(df):
    df_sorted = df.sort_values('timestamp')
    fig = px.scatter(
        df_sorted,
        x='timestamp', 
        y='value', 
        range_y=[0, 300],
        title="My near real-time glucose levels",
        labels={"x": "Time", "y": "Glucose Reading (mg/dL)"}
    )

    fig.update_layout(
        shapes=[
            # Green zone
            dict(type="rect", xref="paper", yref="y",
                 x0=0, x1=1, y0=70, y1=200,
                 fillcolor="rgba(0,255,0,0.1)", line_width=0),

            # Red zone - low
            dict(type="rect", xref="paper", yref="y",
                 x0=0, x1=1, y0=0, y1=70,
                 fillcolor="rgba(255,0,0,0.1)", line_width=0),
    
            # Red zone - high
            dict(type="rect", xref="paper", yref="y",
                 x0=0, x1=1, y0=200, y1=300,
                 fillcolor="rgba(255,0,0,0.1)", line_width=0)
        ]
    )
    return fig

fig = create_figure(df)

#app = Dash(__name__, requests_pathname_prefix="/glucose/")
app = Dash(__name__, url_base_pathname="/glucose/")
app.layout = html.Div([
    html.H1('Glucose'),
    dcc.Graph(id="glucose-graph",figure=fig),
    html.Div(
        children=[
            html.P([
                "Select a date : ",
                dcc.DatePickerSingle(
                    id='date-picker',
                    date=today,
                    max_date_allowed=today,
                    display_format='DD-MM-YYYY')
                ]),
            html.P(id='err', style={'color': 'red'})
        ],
        style={'textAlign': 'center'},
    ),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # update every 10s
        n_intervals=0
    )
])

@callback(
        Output('glucose-graph', 'figure'),
        Output('err', 'children'),
        Input('interval-component', 'n_intervals'),
        Input(component_id='date-picker', component_property='date'))
def update_glucose_graph_from_date(n, date):
    if date:
        con_cb = sqlite3.connect("my_db")  
        query = """
        SELECT * FROM glucose
        WHERE date(timestamp) = ?
        """
        df_cb = pd.read_sql_query(query, con_cb, params=(date,))
        con_cb.close()

        if df_cb.empty:
            #raise PreventUpdate
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            return no_update, 'No data available for {}'.format(date_obj.strftime('%d-%m-%Y'))

        else:
            return create_figure(df_cb), ''
    else:
        con_cb = sqlite3.connect("my_db")  
        df_cb = pd.read_sql_query("select timestamp, value from glucose WHERE date(timestamp) = date('now');", con_cb)
        return create_figure(df_cb), ''

if __name__ == '__main__':
    app.run(debug=True)
