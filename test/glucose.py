from pylibrelinkup import PyLibreLinkUp
import creds

client = PyLibreLinkUp(email=creds.email, password=creds.key)
client.authenticate()

patient_list = client.get_patients()
patient = patient_list[0] # get the first patient (me)

# get data for graph from server
graph_data = client.graph(patient_identifier=patient)

print(f"graph data ({len(graph_data)} measurements):")

for measurement in graph_data:
    print(f"{measurement.value} {measurement.timestamp}")

print(type(measurement.value))
print(type(measurement.timestamp))

import plotly.express as px
import time

# extract the data
data = [obj.value for obj in graph_data]
timestamps = [obj.timestamp for obj in graph_data]
print(data)
print(timestamps)

# put it in a graph
fig = px.line(x=timestamps, y=data, markers=True, range_y=[0,300], title="CGM Glucose Graph", labels={"x":"time (hh:mm)", "y":"Glucose Reading (mg/dL)"})
# show the graph duh
fig.show()

# do website stuff (make it work with html idk)
from dash import Dash, dcc, html
app = Dash()
app.layout = html.Div([
    #html.H4('Interactive scatter plot with nada'),
    dcc.Graph(id="scatter-plot",figure=fig),
])

app.run(host="0.0.0.0", port=8050)