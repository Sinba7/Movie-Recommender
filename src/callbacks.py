import pandas as pd
import json
import dash
from dash.dependencies import Input, Output, State
import logbook
import sys
# from src.load_data import rated_movie_df, rating_df
# from src.genres_based_recom import top_popular_movie, top_high_rated_movie
# from src.collaborative_recom import collab_recommender
# from src.layout_functions import *
from src.collaborative_recom import collab_recommender
from src.layout_functions import *

# logging
app_log = logbook.Logger('APP')
callback_log = logbook.Logger('CALLBACK')
level = logbook.TRACE
logbook.StreamHandler(sys.stdout, level=level).push_application()


def register_callbacks(app):

    # @app.callback(
    #     Output("collapse-body", "is_open"),
    #     [Input("collapse-button", "n_clicks")],
    #     [State("collapse-body", "is_open")],
    # )
    # def toggle_collapse(n, is_open):
    #     if n:
    #         return not is_open
    #     return is_open

    @app.callback(
        [Output('system-dropdownmenu', 'label'), Output('recom-content', 'children')],
        [Input('system-1-button', 'n_clicks'), Input('system-2-button', 'n_clicks'), Input('clear-button', 'n_clicks')],
        [State('system-1-button', 'children'), State('system-2-button', 'children')]
    )
    def update_recom_content(n_s1, n_s2, n_clear, label1, label2):
        ctx = dash.callback_context
        clicked_button = ctx.triggered[0]['prop_id'].split('.')[0]
        if clicked_button:
            if '1' in clicked_button:
                app_log.trace(f'User choose {label1}')
                return [label1, system_1_content]
            elif '2' in clicked_button:
                app_log.trace(f'User choose {label2}')
                return [label2, system_2_content]
            elif 'clear' in clicked_button:
                callback_log.trace(f'User clean the engine choice')
                return ['Recommenders', None]
        raise dash.exceptions.PreventUpdate
        

    ## update genre recommendation content
    @app.callback(
        [Output('genre-dropdownmenu', 'label'), Output('genre-recom-movies', 'children')],
        [Input('clear-button', 'n_clicks')]+[Input(g,'n_clicks') for g in genres],
        [State(g, 'children') for g in genres]
    )
    def get_genre_recom(n_clear, *args):
        ctx = dash.callback_context
        clicked_button = ctx.triggered[0]['prop_id'].split('.')[0]
        if 'clear' in clicked_button:
            callback_log.trace(f'User clean the genre choice')
            return ['Select Your Favorite Genres', None]
        elif clicked_button:
            app_log.trace(f'User select favorite genres: {clicked_button}')
            recom_mv_df = top_high_rated_movie(clicked_button)
            app_log.trace(f'Recommend {len(recom_mv_df)} {clicked_button} movies')
            recom_mv_layout = movie_display_layout(recom_mv_df)
            return ['Genre: '+clicked_button, recom_mv_layout]
        raise dash.exceptions.PreventUpdate


    ## update collaberative recommendation content
    # store rating info
    @app.callback(
        Output('store-slider-rating','data'), 
        [Input(f'slider_{i}', 'value') for i in range(nmovies_sample//nmovies_per_row*nmovies_per_row)]
    )
    def update_user_rating(*arg):
        movie_rating = list([*arg])
        return json.dumps(movie_rating)

    # update tab content
    @app.callback(
        [Output("tab-content", "children"), Output('tab-rate', 'label_style'), Output('tab-recom', 'label_style')], 
        [Input("tabs", "active_tab")]
    )
    def tab_content(active_tab):
        if active_tab == 'tab-rate':
            # callback_log.trace('User switches to rating page')
            app_log.trace('User starts rating movies')
            return [rate_movie_div, {"color": "black", "fontWeight":"bold"}, {"color": "grey"}]
        else:
            # callback_log.trace('User switches to result page')
            app_log.trace('User finish rating movies')
            return [collab_recom_div, {"color": "grey"}, {"color": "black", "fontWeight":"bold"}]


    @app.callback(
        Output('collab_recom_div','children'),
        [Input("tabs", "active_tab")],
        [State('store-slider-rating','data')]
    )
    def get_collab_recom(active_tab, user_rating):
        if active_tab == 'tab-recom':
            callback_log.trace(f'Start collaborative recommendation process')
            # create new id for user
            userid = np.sort(rating_df.userid.unique())[-1] + 1
            # get user rated movie id and rating and add to training data
            user_rating = json.loads(user_rating)
            rated_mv_idx = []
            user_mv_rating = []
            for i,r in enumerate(user_rating):
                if r!=0:
                    rated_mv_idx.append(i)
                    user_mv_rating.append(r)
            # callback_log.trace(f"Finish collecting and parsing user ratings")
            app_log.trace(f'User rated {len(rated_mv_idx)} movies.')
            # if user label 0 movie
            if len(rated_mv_idx)==0:
                callback_log.trace(f"Return default movie ranking")
                random_movie_layout = movie_display_layout(rated_movie_df.loc[:100,['movieid','title']]) 
                return random_movie_layout
            callback_log.trace(f"Start preprocessing data for collaborative recommender")
            user_rated_mv_id = rated_movie_df.loc[rated_mv_idx, 'movieid']
            user_training_data = pd.DataFrame({'userid':[userid]*len(user_rated_mv_id), 'movieid':user_rated_mv_id, 'rating':user_mv_rating})
            training_data = pd.concat([rating_df.loc[:50000,['userid','movieid','rating']], user_training_data], axis=0)
            # test 
            user_unrated_mv_id = list(set(rated_movie_df.movieid) - set(user_rated_mv_id))
            user_test_data = pd.DataFrame({'userid':[userid]*len(user_unrated_mv_id), 'movieid':user_unrated_mv_id})
            callback_log.trace(f"Finish preprocessing data for collaborative recommender")
            # get predictive rating for all movies which this user not rated
            pred_rating = collab_recommender(training_data, user_test_data, user_based=False, normalization= False, k=100, sim='cosine') # movieid, rating
            # sort movieid by predictive rating
            recom_mv_df = pred_rating.sort_values(by='rating', ascending=False)[['movieid']]
            # get movie title
            recom_mv_df['title'] = rated_movie_df.loc[rated_movie_df.movieid.isin(recom_mv_df.movieid), 'title']
            recom_mv_layout = movie_display_layout(recom_mv_df.iloc[:100])
            callback_log.trace(f"Recommend 100 movies with highest similarity score")
            return recom_mv_layout
        raise dash.exceptions.PreventUpdate

    