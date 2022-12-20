#author
import os
#from eralchemy import render_er
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]) 


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
#credits to https://plotly.com/python/sliders/
conn = sqlite3.connect("hr")
df = pd.read_sql_query('select * from employees;', conn)
df2 = pd.read_sql("SELECT employees.first_name, jobs.job_title " +
                            "FROM employees " + 
                            "INNER JOIN jobs ON employees.job_id " + 
                            "= jobs.job_id",conn)

count  = df2['job_title'].value_counts()                          
fig = go.Figure()
fig = px.bar(x=count.index, y = count.values, color=count.index)

fig.update_layout(title='Number of eployees with the same job', 
                    xaxis_title='Job title',
                    yaxis_title='Count')



#exercise 3
#credits to https://sqlite.org/forum/info/9e1576587473d12d 
js=pd.read_sql_query("select * from jobs;",conn)
js = js.iloc[1: , :]
js["difference"]=js['max_salary']-js['min_salary']
j=js[['job_title','difference']]
max_salary=j['difference'].max()

#exercise 4
#credits to https://realpython.com/beautiful-soup-web-scraper-python/ 
#credits to https://stackoverflow.com/questions/24398302/bs4-featurenotfound-couldnt-find-a-tree-builder-with-the-features-you-requeste 
#credits to https://www.youtube.com/watch?v=R3XJZAldhYQ  
def last_ex():
    URL = "https://www.itjobswatch.co.uk/jobs/uk/sqlite.do"
    a = requests.get(URL)
    soup = BeautifulSoup(a.content, 'html5lib') 
    content = soup.find('table', attrs = {'class':'summary'}) 
    content.find('form').decompose()
    data = content.tbody.find_all("tr")
    content = []
    for i in data:
        r = []
        all = i.find_all("td")
        if len(all) == 0:
            all = i.find_all("th")
        for j in all:
            r.append(j.text)
        content.append(r)

    sal = content[1]
    sal[0] = "index"
    salary = pd.read_sql("SELECT employees.salary " +
                                "FROM employees",conn)
    average_sal = salary['salary'].mean()
    df4 = pd.DataFrame(content)
    df4.drop(index=[0,1,2,3,4,5,6,7,10,11,14,15],axis=0,inplace=True)
    df4.columns = sal
    df4.set_index("index",inplace=True)
    df4.reset_index(inplace=True)
    df4['Same period 2021'] = df4['Same period 2021'].str.replace('£','')
    df4['Same period 2021'] = df4['Same period 2021'].str.replace(',','')
    df4['Same period 2021'] = df4['Same period 2021'].str.replace('-','0').astype(float)
    df4['6 months to19 Dec 2022'] = df4['6 months to19 Dec 2022'].str.replace('£','')
    df4['6 months to19 Dec 2022'] = df4['6 months to19 Dec 2022'].str.replace(',','').astype(float)
    df4['Same period 2020'] = df4['Same period 2020'].str.replace('£','')
    df4['Same period 2020'] = df4['Same period 2020'].str.replace(',','').astype(float)
    df4.loc[4] = ['Average', average_sal, average_sal,average_sal] 
    return df4

ex4= last_ex()

x_azia = ex4["index"]
ex4.drop("index",inplace=True,axis=1)
years = ex4.columns




def update(year):
    return ex4[year]




app.layout = html.Div(children=[ 
    dbc.Row([html.H1(children='HR Analysis Dashboard', style={"text-align": "center"})]),
    dbc.Row([

        dbc.Col([
            html.P("Diagram", style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "margin": "0px -12px"}), 
            html.Img(id='picture', src=app.get_asset_url('erd_from_sqlite.png'), className="picture")], style = {"padding":"10px"}, className="col-3"), 
        dbc.Col([
            dbc.Row([html.P("Exercise 2", style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
    dcc.Graph(
        id='input2',
        figure = fig
    )]),
            dbc.Row([html.H1(),
    html.P("Exercise 3", style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
    dcc.RangeSlider(0, max_salary, 1000, value=[0, max_salary],
    id="input3"),
    dcc.Graph(id="output3"), 
    html.H1()]), 
        dbc.Row([html.P("Exercise 4", style={'textAlign': 'center', "padding": "10px", "fontSize": "20px", "backgroundColor": "#4744ff", "color": "beige", "margin": "0px -12px", "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px", "marginBottom":"30px"}),
    dcc.Dropdown(years,
                value='all',
                placeholder="6 months to19 Dec 2022",
                id="years"
                             ),
        dcc.Graph(id="output4")])
        ]),
    ])], style = {"padding":"10px"})

@app.callback(
Output('output3', 'figure'),
Input('input3', 'value')
)


def update_output(value):
    min=value[0]
    max=value[-1]
    fig3 = go.Figure()
    fig3["layout"]["xaxis"]["title"] = "Max and min difference"
    fig3["layout"]["yaxis"]["title"] = "Job Title"
    t = j[j["difference"]>=min][j["difference"]<=max]
    fig3.add_trace(go.Bar(x=t['difference'], y=t['job_title'], orientation='h',
    name='Job differences'))
    return fig3

@app.callback(
        Output('output4', 'figure'),
        Input('years', 'value')
        )

def update_output(value1):
    if value1 == "all" or value1 == None:
        y_azia = ex4["6 months to19 Dec 2022"]
    else:
        y_azia =update(value1)
    fig4 = px.scatter(df,x=x_azia.values,y=y_azia.values,  title="Average salary per year", 
    labels={
                     "x": "Salary value",
                     "y": "Count"})
    col = ['black','black','black','black','green' ]
    fig4.update_traces(marker_size=20, marker_color = col )
    
    return fig4

if __name__ == '__main__':
    app.run_server("0.0.0.0", debug=False, port=int(os.environ.get('PORT', 8000)))
server = app.server

