import dash
from dash import dcc
from dash import html
from dash.dependencies import Output
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# treating dataFrame
df = pd.read_excel('compras.xlsx', engine='openpyxl')
df = df.rename(columns={'Unnamed: 0': 'Situação', 'Unnamed: 1': 'Descrição', 'Unnamed: 2': 'Família de Produto',
               'Unnamed: 3': 'Municipio', 'Unnamed: 6': 'Preço Unitário de Venda', 'Unnamed: 7': 'Estoque Disponível'})
df.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 8',
        'Unnamed: 9', 'Unnamed: 10'], index=[0, 1], inplace=True)
df.loc[6, 'Municipio'] = 'Boca da Mata - AL'
df['Preço Unitário de Venda'] = pd.to_numeric(df['Preço Unitário de Venda'])
df['Estoque Disponível'] = pd.to_numeric(df['Estoque Disponível'])

family_inventory = df.groupby(
    ['Família de Produto'], as_index=True, sort=False).sum().reset_index()


app.layout = html.Div(children=[
    html.H1(children='Dashboard de Estoque'),

    html.Span(children='''
        Modifique o grafico para observar melhor os dados utilizando os dropdown e o slider
    '''),

    html.Div(children=[
        html.Div(children=[
            html.H5(children='Selecione o dado a ser estudado'),

            dcc.Dropdown(
                id='graph-type-dropdown',
                options=[
                    {'label': 'Preço Unitário de Venda',
                        'value': 'Preço Unitário de Venda'},
                    {'label': 'Estoque Disponível', 'value': 'Estoque Disponível'}],
                value='Estoque Disponível',
                style={'width': '300px'}
            ),

            html.H5(
                children='Visualizar por produto ou por familia de produto'),

            dcc.Dropdown(
                id='graph-product-dropdown',
                options=[{'label': 'Família de Produto',
                          'value': 'Família de Produto'}, {'label': 'Produto', 'value': 'Descrição'}],
                value='Descrição',
                style={'width': '300px'}
            ),

            html.H5(children='Selecione a quantidade que deseja observar'),

            html.Div(style={'width': '300px'}, children=[
                dcc.Slider(id='graph-slider',
                           min=0,
                           max=20,
                           step=1,
                           value=4,
                           tooltip={"placement": "bottom", "always_visible": True},),
            ]),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-direction': 'column', 'margin-right': '30px'}),

        html.Div(children=[
            dcc.Graph(
                id='graph',
                style={'width': '1000px'}
            ),
        ])

    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '100%'}),

], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-direction': 'column'})


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='graph-slider', component_property='value'),
    Input(component_id='graph-type-dropdown', component_property='value'),
    Input(component_id='graph-product-dropdown', component_property='value')
)
def changeText(slider, graph_type_dropdown, graph_product_dropdown):
    if(graph_product_dropdown == 'Descrição'):
        return px.line(df.sort_values(graph_type_dropdown, ascending=False).head(slider),
                       x=graph_product_dropdown, y=graph_type_dropdown)
    else:
        return px.line(family_inventory.sort_values(graph_type_dropdown, ascending=False).head(slider),
                       x=graph_product_dropdown, y=graph_type_dropdown)


family_inventory
if __name__ == '__main__':
    app.run_server(debug=True)
