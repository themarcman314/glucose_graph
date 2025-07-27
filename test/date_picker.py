from dash import Dash, dcc, html
from datetime import date

app = Dash()

today = date.today()

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='date-picker',
        date=today,
        max_date_allowed=today,
        display_format='DD-MM-YYYY'
        )
    ])

if __name__ == '__main__':
    app.run(debug=True)
