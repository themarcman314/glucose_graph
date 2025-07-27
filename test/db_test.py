from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_sql_table('glucose', 'sqlite:///my_db')

# Initialize the app
app = Dash()

# The app components that will be displayed in the browser
# Can be provided as a list or dash component

#app.layout = [html.Div(children='Hello World')]
# print the glucose values in from the Series
#print(df['value'].values)
app.layout = [html.Div(children='Hello World'),
              dash_table.DataTable(df.to_dict('records'), page_size=10)
              ]



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
