import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import webbrowser

# Initialize the app
app = dash.Dash(__name__)
app.title = "SUVAT Simulator"

# App layout
app.layout = html.Div([
    html.H1("Uniformly Accelerated Linear Motion (SUVAT) Simulator", style={'textAlign': 'center'}),

    html.Div([
        # Left column: input fields and button
        html.Div([
            html.Label("Initial position (s₀):"),
            dcc.Input(id='s0', type='number', value=0, debounce=True, step=1),
            html.Br(), html.Br(),

            html.Label("Initial velocity (v₀):"),
            dcc.Input(id='v0', type='number', value=10, debounce=True, step=1),
            html.Br(), html.Br(),

            html.Label("Acceleration (a):"),
            dcc.Input(id='a', type='number', value=5, debounce=True, step=1),
            html.Br(), html.Br(),

            html.Label("Final time (s):"),
            dcc.Input(id='t_max', type='number', value=10, debounce=True, step=1, min=1),
            html.Br(), html.Br(),

            html.Button('Start', id='start-button', n_clicks=0, style={'margin-top': '10px'}),
            dcc.Interval(id='interval', interval=100, n_intervals=0, disabled=True)
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '20px', 'verticalAlign': 'top'}),

        # Right column: stacked graphs
        html.Div([
            dcc.Graph(id='pos_graph', config={'displayModeBar': False}),
            dcc.Graph(id='vel_graph', config={'displayModeBar': False}),
            dcc.Graph(id='acc_graph', config={'displayModeBar': False}),
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ])
])

# Enable animation on button click
@app.callback(
    Output('interval', 'disabled'),
    Input('start-button', 'n_clicks')
)
def start_animation(n_clicks):
    return False if n_clicks > 0 else True

# Update the graphs as the animation progresses
@app.callback(
    [Output('pos_graph', 'figure'),
     Output('vel_graph', 'figure'),
     Output('acc_graph', 'figure')],
    [Input('interval', 'n_intervals'),
     Input('s0', 'value'),
     Input('v0', 'value'),
     Input('a', 'value'),
     Input('t_max', 'value')]
)
def update_graphs(n, s0, v0, a, t_max):
    t = np.linspace(0, t_max, 200)
    t_index = min(n % 200, len(t) - 1)
    t_now = t[:t_index + 1]

    s_now = s0 + v0 * t_now + 0.5 * a * t_now**2
    v_now = v0 + a * t_now
    a_now = np.full_like(t_now, a)

    # Position graph
    pos_fig = go.Figure()
    pos_fig.add_trace(go.Scatter(x=t_now, y=s_now, mode='lines', name='s(t)', line=dict(color='blue')))
    pos_fig.add_trace(go.Scatter(x=[t_now[-1]], y=[s_now[-1]], mode='markers',
                                 marker=dict(size=10, color='black'), name='Particle'))
    pos_fig.update_layout(title='Position vs Time',
                          xaxis_title='Time (s)', yaxis_title='Position (m)',
                          height=250, margin=dict(l=40, r=20, t=40, b=40))

    # Velocity graph
    vel_fig = go.Figure()
    vel_fig.add_trace(go.Scatter(x=t_now, y=v_now, mode='lines', name='v(t)', line=dict(color='green')))
    vel_fig.update_layout(title='Velocity vs Time',
                          xaxis_title='Time (s)', yaxis_title='Velocity (m/s)',
                          height=250, margin=dict(l=40, r=20, t=40, b=40))

    # Acceleration graph
    acc_fig = go.Figure()
    acc_fig.add_trace(go.Scatter(x=t_now, y=a_now, mode='lines', name='a(t)', line=dict(color='red', dash='dot')))
    acc_fig.update_layout(title='Acceleration vs Time',
                          xaxis_title='Time (s)', yaxis_title='Acceleration (m/s²)',
                          height=250, margin=dict(l=40, r=20, t=40, b=40))

    return pos_fig, vel_fig, acc_fig

# Automatically open browser
webbrowser.open("http://127.0.0.1:8050")
if __name__ == '__main__':
    app.run(debug=True)
