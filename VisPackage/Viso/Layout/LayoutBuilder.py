import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from ..Model.Model import Model
import json
from flask import request
# https://plotly.com/python/reference

class LayoutBuilder:

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP,dbc.themes.GRID]

    def __init__(self, data=None):
        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.models = self.__loadData(data)
        self.app.layout = self.getTopNav()
        self.loadCallbacks()
        self.loadShutdown()

    def __loadData(self, datain=None):
        data = datain
        if data is None:
            data = [json.load(open("../../static/data/cifar.json")),  json.load(open("../../static/data/cifernew.json")) ]
        ms = [Model(data_item) for data_item in data]
        [m.buildModel() for m in ms]
        return ms


    def getSummaryFigurePerScore(self, model, epochIndex=None, scale=None):
        if epochIndex == None:
            epochIndex = model.epochCount() - 1

        if scale == None:
            scale = 1

        # print(self.model.epoch(0).classNames)
        figure = {
            'data': model.epoch(epochIndex).getSummaryFramePerScore(),
            'layout': {
                'title': 'Summary Per Score',
                'barmode': 'stack',
                'yaxis': {
                    'title': 'Probability (MAX)',
                    'range': [-0.1,1],
                    'autorange': False,
                    'tickmode': 'array',
                    'tickvals': [0,0.11,0.21,0.31,0.41,0.51,0.61,0.71,0.81,0.91],
                    #'ticktext': ['0 - 0.1','0.11 - 0.2','0.21 - 0.3','0.31 - 0.4','0.41- 0.5','0.51 - 0.6','0.61 - 0.7','0.71 - 0.8','0.81 - 0.9','0.91 - 1']
                    'ticktext': ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1']
                },
                'xaxis': {
                    'title': 'Samples Count',
                    'range': [- round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex)), round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex))],
                    'autorange': False,
                    'tickmode':'array',
                    'tickvals': [- round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex)), - round((scale * model.maxRangeXAxisSummaryPerScore(epochIndex)) / 2) , round((scale * model.maxRangeXAxisSummaryPerScore(epochIndex)) / 2), round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex))],
                    'ticktext': [round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex)), round((scale * model.maxRangeXAxisSummaryPerScore(epochIndex)) / 2) , round((scale * model.maxRangeXAxisSummaryPerScore(epochIndex)) / 2), round(scale * model.maxRangeXAxisSummaryPerScore(epochIndex))]
                },
                'transition': {
                    'duration': 300,
                    'easing': 'linear'
                },
                'updatemenus': [
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                      method="animate",
                                      args=[None, {"frame": {"duration": 500},
                                                   "fromcurrent": True, "transition": {"duration": 300,
                                                                                       "easing": "linear"}}])
                                 ]),
                ]
            },
            'frames': model.modelFramesSummaryPerScore()
        }
        return figure

    def getSummaryFigure(self, model, epochIndex=None, scale=None):
        if epochIndex == None:
            epochIndex = model.epochCount() - 1

        if scale == None:
            scale = 1

        # print(self.model.epoch(0).classNames)
        figure = {
            'data': model.epoch(epochIndex).getSummaryFrame(),
            'layout': {
                'title': 'Summary',
                'barmode': 'stack',
                'yaxis': {
                    'title': 'Class Names',
                    'range': [-1, 10],
                    'autorange': False,
                    'tickmode': 'array',
                    'tickvals': [0, 1, 2,3, 4, 5,6, 7, 8,9],
                    # 'ticktext': ['0 - 0.1','0.11 - 0.2','0.21 - 0.3','0.31 - 0.4','0.41- 0.5','0.51 - 0.6','0.61 - 0.7','0.71 - 0.8','0.81 - 0.9','0.91 - 1']
                    'ticktext': [x for x in model.epoch(0).classNames]
                },
                'xaxis': {
                    'title': 'Samples Count',
                    'range': [- round(scale * model.maxRangeXAxisSummary(epochIndex)), round(scale * model.maxRangeXAxisSummary(epochIndex))],
                    'autorange': False,
                    'tickmode':'array',
                    'tickvals': [- round(scale * model.maxRangeXAxisSummary(epochIndex)), - round((scale * model.maxRangeXAxisSummary(epochIndex)) / 2) , round((scale * model.maxRangeXAxisSummary(epochIndex)) / 2), round(scale * model.maxRangeXAxisSummary(epochIndex))],
                    'ticktext': [round(scale * model.maxRangeXAxisSummary(epochIndex)), round((scale * model.maxRangeXAxisSummary(epochIndex)) / 2) , round((scale * model.maxRangeXAxisSummary(epochIndex)) / 2), round(scale * model.maxRangeXAxisSummary(epochIndex))]
                },
                'transition': {
                    'duration': 300,
                    'easing': 'linear'
                },
                'updatemenus': [
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                      method="animate",
                                      args=[None, {"frame": {"duration": 500},
                                                   "fromcurrent": True, "transition": {"duration": 300,
                                                                                       "easing": "linear"}}])
                                 ]),
                ]
            },
            'frames': model.modelFramesSummary()
        }
        return figure

    def getFigure(self, model, classIndex, epochIndex=None, scale=None):
        if epochIndex == None:
            epochIndex = model.epochCount() - 1

        if scale == None:
            scale = 1


        figure = {
            'data': model.epoch(epochIndex).getFrame(classIndex),
            'layout': {
                'title': 'Class Name: ' + model.epoch(epochIndex).classNames[classIndex],
                'barmode': 'stack',
                'yaxis': {
                    'title': 'Probability (MAX)',
                    'range': [-0.1,1],
                    'autorange': False,
                    'tickmode': 'array',
                    'tickvals': [0,0.11,0.21,0.31,0.41,0.51,0.61,0.71,0.81,0.91],
                    #'ticktext': ['0 - 0.1','0.11 - 0.2','0.21 - 0.3','0.31 - 0.4','0.41- 0.5','0.51 - 0.6','0.61 - 0.7','0.71 - 0.8','0.81 - 0.9','0.91 - 1']
                    'ticktext': ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1']
                },
                'xaxis': {
                    'title': 'Samples Count',
                    'range': [- round(scale * model.maxRangeXAxis()), round(scale * model.maxRangeXAxis())],
                    'autorange': False,
                    'tickmode':'array',
                    'tickvals': [- round(scale * model.maxRangeXAxis()), - round((scale * model.maxRangeXAxis()) / 2) , round((scale * model.maxRangeXAxis()) / 2), round(scale * model.maxRangeXAxis())],
                    'ticktext': [round(scale * model.maxRangeXAxis()), round((scale * model.maxRangeXAxis()) / 2) , round((scale * model.maxRangeXAxis()) / 2), round(scale * model.maxRangeXAxis())]
                },
                'transition': {
                    'duration': 300,
                    'easing': 'linear'
                },
                'updatemenus': [
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                      method="animate",
                                      args=[None, {"frame": {"duration": 500},
                                                   "fromcurrent": True, "transition": {"duration": 300,
                                                                                       "easing": "linear"}}])
                                 ]),
                ]
            },
            'frames': model.modelFrames(classIndex)
        }
        return figure

    def getTopNav(self):

        SIDEBAR_STYLE = {
            "top": 0,
            "left": 0,
            "bottom": 0,
            "height": "5rem",
            "line-height": "2.5rem",
            "font-weight": "400",
            "font-size": "1.5rem",
            "padding": ".5rem 1rem"
        }
        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "2rem",
            "margin-right": "2rem",
        }
        PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
        navbar = dbc.Navbar(
            children=[

                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
                        ],
                        align="center" ,
                        no_gutters=True,
                    ),
                    href="https://plot.ly",
                ),

                dbc.NavLink("Active", active=True, href="#"),
                dbc.NavLink("A link", href="#"),
                dbc.NavLink("Another link", href="#"),
                dbc.NavLink("Disabled", disabled=True, href="#"),
                # dbc.DropdownMenu(
                #     [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
                #     label="Dropdown",
                #     nav=True,
                # ),

                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(id="navbar-collapse", navbar=True),
            ],
            style=SIDEBAR_STYLE,
            color="dark",
            dark=True
        )
        content = html.Div(id="page-content", children=[self.initVisForModels(self.models)], style=CONTENT_STYLE)
        return html.Div([dcc.Location(id="url"),navbar,content])

    def initVisForModels(self, models):
        return html.Div(dbc.Row([self.initVis(models[i], i) for i in range(len(models))]))

    def initVis(self, model, modelIndex):
        w = 6

        return dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Row(html.Br()),
                            dbc.Row([
                                dbc.Col(dbc.Alert("Cifer Model", color="success"), width={'size': 2}),
                                dbc.Col(dbc.Alert('Epochs Count : ' + str(model.epochCount()), color="primary"),
                                        width={'size': 2}),

                                # dbc.Col(html.H1(id='header', children='Cifar Model, Epochs Count : ' + str(
                                # model.epochCount()) + ', Selected Epoch: ' + str(model.epochCount())
                                #          ,
                                #          style={
                                #              'textAlign': 'center'
                                #          }
                                #          ),width={'size':8}),
                                dbc.Col(html.H2("Scale: "), width={'size': 2}, style={'textAlign': 'center'}),
                                dbc.Col(dcc.Dropdown(id='range-'+str(modelIndex),
                                                     options=[
                                                         {'label': '0.2X', 'value': '0.2'},
                                                         {'label': '0.25X', 'value': '0.25'},
                                                         {'label': '0.3X', 'value': '0.3'},
                                                         {'label': '0.5X', 'value': '0.5'},
                                                         {'label': 'X', 'value': '1'},
                                                         {'label': '2X', 'value': '2'},
                                                         {'label': '3X', 'value': '3'},
                                                         {'label': '4X', 'value': '4'},
                                                         {'label': '5X', 'value': '5'},
                                                     ],
                                                     value='1',
                                                     searchable=False,
                                                     clearable=False,
                                                     # style={'textAlign': 'center'}
                                                     ), width={'size': 2})

                            ], justify="center"),
                            dbc.Row([
                                dbc.Col(html.Div([html.Br(), dcc.Slider(
                                    id='epoch-slider-'+str(modelIndex),
                                    min=0,
                                    max=model.epochCount() - 1,
                                    value=model.epochCount() - 1,
                                    marks={str(x): str(x + 1) for x in range(model.epochCount())},
                                    step=None
                                )]))
                            ]),
                            dbc.Row(dbc.Col(html.Div(html.H3("Summary Histograms", style={
                                'textAlign': 'center'
                            }))), align="center"),
                            dbc.Row([
                                dbc.Col(html.Div(dcc.Graph(id='summaryHist' + '-' + str(modelIndex),
                                                           figure=self.getSummaryFigure(
                                                               model))),
                                        width={'size': 4, 'offset': 1}),
                                dbc.Col(html.Div(dcc.Graph(id='summaryHistPerScore' + '-' + str(modelIndex),
                                                           figure=self.getSummaryFigurePerScore(
                                                               model))),
                                        width={'size': 4, 'offset': 2})
                            ]),
                            dbc.Row(dbc.Col(html.Div(html.H3("Detailed Histograms", style={
                                'textAlign': 'center'
                            }))), align="center"),
                            dbc.Row([
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[0] + '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 0))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[1]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 1))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[2]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 2))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[3]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 3))),
                                        width=w),

                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[4]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 4))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[5]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 5))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[6]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 6))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[7]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 7))),
                                        width=w),

                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[8]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 8))),
                                        width=w),
                                dbc.Col(html.Div(dcc.Graph(id=model.lastEpoch().classNames[9]+ '-' + str(modelIndex),
                                                           figure=self.getFigure(model, 9))),
                                        width=w)

                            ], align="center")
                        ]
                    )
                ),

            ]
            , width={'size': 12/len(self.models)})

    def loadCallbacks(self):

        for j in range(len(self.models)):
            @self.app.callback([Output(x + '-' + str(j), 'figure') for x in self.models[j].lastEpoch().classNames],
                               [Input('range-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'id')])
            def update_histograms_figure(scaleValue, epochIndex, id):
                modelIndex = int(id.split('-')[len(id.split('-')) - 1])
                return [self.getFigure(self.models[modelIndex], i, epochIndex, float(scaleValue)) for i in range(len(self.models[modelIndex].lastEpoch().classNames))]


        for j in range(len(self.models)):
            @self.app.callback(Output('summaryHistPerScore-' + str(j), 'figure'),
                               [Input('range-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'id')])
            def update_summaryHistPerScore_figure(scaleValue, epochIndex, id):
                modelIndex = int(id.split('-')[len(id.split('-')) - 1])
                return self.getSummaryFigurePerScore(self.models[modelIndex],epochIndex,float(scaleValue))


        for j in range(len(self.models)):
            @self.app.callback(Output('summaryHist-' + str(j), 'figure'),
                               [Input('range-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'value'), Input('epoch-slider-'+str(j), 'id')])
            def update_summaryHist_figure(scaleValue, epochIndex, id):
                modelIndex = int(id.split('-')[len(id.split('-')) - 1])
                return self.getSummaryFigure(self.models[modelIndex],epochIndex,float(scaleValue))

        @self.app.callback(Output("page-content", "children"), [Input("url", "pathname")])
        def render_page_content(pathname):
            if pathname in ["/", "/page-1"]:
                return self.initVisForModels([self.models[0],self.models[1]])
            elif pathname == "/page-2":
                return self.initVisForModels([])
            elif pathname == "/page-3":
                return html.P("Oh cool, this is page 3!")
            # If the user tries to reach a different page, return a 404 message
            return dbc.Jumbotron(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ]
            )



    def run(self, debug):
        print("Stop Server: " + 'http://127.0.0.1:5000' + "/shutdown")
        self.app.run_server(debug=debug, port=5000)


    def loadShutdown(self):
        def shutdown_server():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @self.app.server.route('/shutdown', methods=['GET'])
        def shutdown():
            shutdown_server()
            return 'Server shutting down...'