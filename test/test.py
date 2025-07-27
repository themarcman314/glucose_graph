from dash import Dash, html

# Initialize the app
app = Dash()

# The app components that will be displayed in the browser
# Can be provided as a list or dash component

# A single component is added to the list: an `html.Div`
# The div has properties such as `children` which can be used to add content to the page.
app.layout = [html.Div(children='Hello World')]


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
