import random, numpy as np
import plotly.express as px

timestamps = []
data = []
for i in range(20):
    timestamps.append(200*random.random())
    data.append(200*random.random())

# put it in a graph
fig = px.line(x=timestamps, y=data, markers=True, range_y=[0,300], title="My near real-time glucose levels", labels={"x":"time (hh:mm)", "y":"Glucose Reading (mg/dL)"})


# Working with Dash

# do website stuff (make it work with html idk)
import dash
app = dash.Dash(url_base_pathname="/glucose/")
app.layout = dash.html.Div([
    dash.dcc.Graph(id="scatter-plot",figure=fig),
])

# do this only for tests, app should be run using gunicorn or waitress instead in production
#app.run(host="127.0.0.1", port=8050)

# instead we should do the following :
server = app.server  # IMPORTANT: expose the Flask server to Gunicorn
