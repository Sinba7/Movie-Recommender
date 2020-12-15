import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np
from load_data import rated_movie_df, genres


nmovies_per_row = 6
nmovies_sample = 300

# logo and header of website
logo_header = html.Div(children=[
            html.Img(src='assets/movie_logo_2.png', style={'width':'10%'}),
            html.Div([
                html.H1(children="Movie Recommender"),
                dbc.Alert(color='info', children="Hi, welcome to my movie store. To get movie recommendations, first, please select a recommendation engine. For genre-based recommender, please select your favorite genres; for collbarative recommender, plase rate the sample movies as many as possible and then click on get recommendations.")
            ], style={'marginLeft':40}),
        ], style={'display':'flex', 'alignItems':'top'})

# recom system dropdown menu
recom_dropdown = dbc.DropdownMenu(
    id='system-dropdownmenu',
    label="Recommenders",
    children=[
        dbc.DropdownMenuItem("Genres Based Recommender", id='system-1-button'),
        dbc.DropdownMenuItem("Collaborative Recommender", id='system-2-button'),
    ]
)

# clear button
clear_button = dbc.Button("Clear All", id='clear-button', color='light') 

def movie_display_layout(recom_mv_df):# movieid/title
    recom_mv_df.index = np.arange(len(recom_mv_df))
    return html.Div([
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(f'Rank {i+j*nmovies_per_row+1}', style={'fontWeight':'bold'}),
                            # dbc.CardImg(src=f"assets/MovieImages/{recom_mv_df.loc[i+j*nmovies_per_row, 'movieid']}.jpg", top=True, style={'width':'100%'}),
                            dbc.CardImg(src=f"https://liangfgithub.github.io/MovieImages/{recom_mv_df.loc[i+j*nmovies_per_row, 'movieid']}.jpg", top=True, style={'width':'100%'}),
                            dbc.CardBody(html.Div(recom_mv_df.loc[i+j*nmovies_per_row, 'title'], style={'fontSize': '14px'}))
                        ], outline=True, style={'marginTop':10, 'marginBottom':10})  # 'marginLeft':20, 'marginRight':40, 
                    ) for i in range(nmovies_per_row)
                ]) for j in range(len(recom_mv_df)//nmovies_per_row)
            ], style={'overflowY':'scroll','height':500})


# for system 1
system_1_content = html.Div([
    dbc.DropdownMenu(
        id='genre-dropdownmenu',
        label="Select Your Favorite Genres",
        children=[dbc.DropdownMenuItem(g, id=g) for g in genres]
    ),
    dbc.CardBody(id='genre-recom-movies')
])


# for system 2
rate_movie_div = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardImg(src=f"https://liangfgithub.github.io/MovieImages/{rated_movie_df.loc[(i+j*nmovies_per_row), 'movieid']}.jpg", top=True, style={'width':'100%'}),
                dbc.CardBody([
                    html.Div(children=rated_movie_df.loc[(i+j*nmovies_per_row), 'title'], style={'fontSize': '14px', 'marginBottom':'10px'}),
                    daq.Slider(id=f'slider_{i+j*nmovies_per_row}', min=0, max=5, value=0, marks={'0':'0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5'}, size=130)  
                ])
            ], outline=True, style={'marginTop':10, 'marginBottom':10})
        ) for i in range(nmovies_per_row)
    ]) for j in range(nmovies_sample//nmovies_per_row)
], style={'overflowY':'scroll','height':500})


# rate_book_collapse = html.Div(id='content', children=[
#                         dbc.Button(
#                             "Please rate your favorite movies",
#                             id="collapse-button",
#                             # className="mb-3",
#                             color="primary",
#                         ),
#                         dbc.Collapse(
#                             dbc.Card(dbc.CardBody(book_cards)),
#                             id="collapse-body",
#                             is_open=True
#                         ),
#                     ]
#                 )


collab_recom_div = html.Div(id='collab_recom_div')

system_2_content = html.Div(
    [
        # dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(id="tab-rate", label="Rate your favorite movies", tab_id="tab-rate", label_style={"color": "black", "font":"bold"}), # label_style={"color": "#00AEF9"}
                    dbc.Tab(id="tab-recom", label="Get your recommendations", tab_id="tab-recom", label_style={"color": "grey"}), # label_style={"color": "#00AEF9"}
                ],
                id="tabs",
                active_tab="tab-rate",
                # card=True,
            ),
        # ),
        # html.Div(id="tab-content", children=book_cards),
        dbc.CardBody(dcc.Loading(html.Div(id="tab-content", children=rate_movie_div), type='dot')), 
    ]
)


def get_layout():
    return html.Div(
        [
            html.Div(children=[
                html.Div(children=logo_header, style={'marginTop':40, 'marginBottom':20}),
                html.Div([
                    recom_dropdown,
                    clear_button,
                ], style={'display':'flex', 'justifyContent':'space-between'}),
                
                html.Div(id='recom-content', style={'marginTop':20}),

                # store informations
                dcc.Store(id='store-slider-rating', storage_type='memory', data='')
            ], style={'marginLeft':60, 'marginRight':60})
        ]
    )
    

