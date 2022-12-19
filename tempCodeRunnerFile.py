#from eralchemy import render_er
import pandas as pd
import sqlite3
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)
server =  app.server

#exercise 1
#credits to https://pypi.org/project/ERAlchemy/#:~:text=ERAlchemy%20generates%20Entity%20Relation%20(ER,databases%20or%20from%20SQLAlchemy%20models. 
#credits to https://stackoverflow.com/questions/66381950/error-when-trying-to-install-eralchemy-in-jupyter-from-a-windows-device 
#NOTE: if eralchemy is not installed through pip, try installing Graphiz 
#https://graphviz.org/download/, and sqlalchemy library using pip, but the version should be below 1.4. 
# Also, eralchemy and sqlalchemy libraries can be run in google colab 
# In https://stackoverflow.com/questions/66381950/error-when-trying-to-install-eralchemy-in-jupyter-from-a-windows-device
# there is info on how to run eralchemy and sqlalchemy in google colab 

# Uncomment the lines 19 and 20, to get the diagram as png file 

# f = render_er("sqlite:///hr.db", '/erd_from_sqlite.png')
# f.render("/erd_from_sqlite")


#exercise2
conn = sqlite3.connect("hr.db")
df = pd.read_sql_query('select * from employees;', conn)
data_connected = pd.read_sql("SELECT employees.first_name, jobs.job_title " +
                                "FROM employees " + 
                                "INNER JOIN jobs ON employees.job_id " + 
                                "= jobs.job_id",conn)



fig = go.Figure()
fig = px.bar(data_connected, x='job_title')


app.layout = html.Div(children=[
    html.H1(children='Dashboard'),
     dcc.Graph(
        id='dashboard1',
        figure=fig
    )
    
])

if __name__ == "_main_":
    app.run_server(debug=True)

