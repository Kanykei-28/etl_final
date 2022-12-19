import pandas as pd
import bs4
import requests
import sqlite3
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from bs4 import BeautifulSoup

con = sqlite3.connect("hr")


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
                            "FROM employees",con)
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

 



x_azia = df4["index"]
df4.drop("index",inplace=True,axis=1)
years = df4.columns




def update(year):
    return df4[year]


app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(years,
                             
                             value='all',
                             placeholder="6 months to19 Dec 2022",
                             id="years"
                             ),
        dcc.Graph(id="output4"),
])









@app.callback(
        Output('output4', 'figure'),
        Input('years', 'value')
        )
def update_output(value1):
    if value1 == "all" or value1 == None:
        y_azia = df4["6 months to19 Dec 2022"]
    else:
        y_azia =update(value1)
    fig4 = px.scatter(df4,x=x_azia.values,y=y_azia.values,  title="Average salary per year", 
    labels={
                     "x": "Percentile and Average",
                     "y": "Count"})
    col = ['black','black','black','black','green' ]
    fig4.update_traces(marker_size=20, marker_color = col )
    
    return fig4

if __name__ == '__main__':
    app.run_server(debug=True)