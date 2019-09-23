## Adding one more component, no style yet

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.tools import mpl_to_plotly
import dash_core_components as dcc
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('ggplot')  #R like style
import plotly_express as px
import numpy as np
import json
import pprint
app = dash.Dash()
mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)
pd.DataFrame({'xa':np.random.rand(10), 'ya':np.random.rand(10)}).plot.scatter(x='xa', y='ya', alpha=0.5, ax = ax)
plotly_fig = mpl_to_plotly(mpl_fig)
# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501
df = pd.read_csv('../data/display_df.csv')
class_names =  ["athletics", "cricket", "football", "rugby", "tennis"]
print(df.tail(1).T)
print(df.Category.unique())
print(class_names)

#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'


graph_figures = [px.scatter(df, x="Dim1", y="Dim2", log_x=False,
                         hover_name="index", color = "Category",  hover_data=["Prediction"] + class_names ).update_yaxes(hoverformat=".2f"),
                           {}]



app.layout = html.Div(
     html.Div([
        html.Div([
            html.H1(children='Text Analyzer', className = 'eight columns'),

                html.Img(
                    src="https://www.fadoq.ca/wp-content/uploads/2017/06/bdebcoul-1024x212.jpg",
                    className='four columns',
                    style={
                        'height': '16%',
                        'width': '16%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0
                    },
                ),
                 ], className = 'row'
                 )
     , html.Div([
            html.Div(id='text-content',
                children='''
                        Dash: A web application framework for Python.
                    ''', className = 'ten columns'),
        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Category:'),
                        dcc.Checklist(
                                id = 'catSelection',
                                options=[ {  'label': category.capitalize()
                                           , 'value': category} for category in class_names],
                                values=class_names,
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )

            ],
            className='row' 
        ),
                
            ], className = 'row'
              )

     , html.Div([

         dcc.Graph(
            id='ReuceDimPlot',
            figure = graph_figures[0],
            className = 'twelve columns')
        #dcc.Graph(
        #    id='mplPlot',
        #    figure = graph_figures[1],
        #    className = 'four columns'),

                  ], className = 'row')
    , html.Div(
               [
        html.Div(id='text-content-long',
            children='''
                    
                ''', className = 'twelve columns'
                 )
                 ], className = 'row') 
    , html.Div([
                html.Div(
                    [
                        html.P('Developed by  José Alejandro - ', style = {'display': 'inline'}),
                        html.A('josalelg@hotmail.com', href = 'mailto:josalelv@hotmail.com')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row")
             ], className='ten columns offset-by-one')

)



@app.callback(
    dash.dependencies.Output('text-content', 'children'),
    [dash.dependencies.Input('ReuceDimPlot', 'hoverData')])
def update_text(hoverData):
    #print(type(hoverData))  #Hovver attributes dic including columns 'x', 'y', etc as keys
    if hoverData is not None:
        s = df[df['Dim1'] == hoverData['points'][0]['x']]
        return html.H3('Predicion: ' + s['Prediction'])


@app.callback(
    dash.dependencies.Output('text-content-long', 'children'),
    [dash.dependencies.Input('ReuceDimPlot', 'hoverData')])
def update_text(hoverData):
    if hoverData is not None:
        s = df[df['Dim1'] == hoverData['points'][0]['x']]
        return html.P( 'Result {}'.format(list(s['Text'])[0]))

@app.callback(  #Cat Update plot
    dash.dependencies.Output('ReuceDimPlot', 'figure'),
    [dash.dependencies.Input('catSelection', 'values')]
    )
    
def update_image_src(values):
    df_aux = df.copy()
    select_mask = df_aux.Category.isin([s for s in values])
    figure = px.scatter(df_aux.loc[select_mask,:], x="Dim1", y="Dim2", log_x=False,
                 hover_name="index", color = "Category",  hover_data=["Prediction"] + class_names ).update_yaxes(hoverformat=".2f")
    return figure


#@app.callback(  #Cat Selector callback
#    dash.dependencies.Output('text-content-long', 'children'),
#    [dash.dependencies.Input('ReuceDimPlot', 'clickData')]
#    )
#def update_pre_callback(clickData):
#    if clickData:
#        pprint.pformat(clickData    )
#    else:
#        print("Nothing clicked yet! :)")


if __name__ == '__main__':
    app.run_server(debug=True)
