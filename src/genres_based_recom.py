import pandas as pd
# from src.load_data import rating_df, movie_df
from src.load_data import load_data
import logbook
import sys

rating_df, movie_df, genres, rated_movie_df = load_data()

# logbook
function_log = logbook.Logger('RECOMMENDER')
level = logbook.TRACE
logbook.StreamHandler(sys.stdout, level=level).push_application()


try:
    function_log.trace('Start parsing data for genres based function')
    # get n_reviewers and average rating
    movie_rating_df = movie_df.copy()
    # movie_rating_df['n_reviewers'] = rating_df.groupby('movieid')['rating'].count().reset_index()['rating']
    # movie_rating_df['avg_rating'] = rating_df.groupby('movieid')['rating'].mean().reset_index()['rating']

    # calculate total number of reviewers for each movie
    n_reviewers = rating_df.groupby('movieid')['rating'].count()
    n_reviewers.name = 'n_reviewers'
    movie_rating_df = movie_rating_df.join(n_reviewers, on='movieid', how='left')
    # calculate average rating for each movie
    avg_rating = rating_df.groupby('movieid')['rating'].mean()
    avg_rating.name = 'avg_rating'
    movie_rating_df = movie_rating_df.join(avg_rating, on='movieid', how='left')
    function_log.trace('Finish parsing data for genres based function')
except Exception as x:
    function_log.exception(f'Parse data for genres based function failed due to {x}')


# recommend functions
# recommend most popular movies, measure for "most popular": viewed/rated by most users. 
def top_popular_movie(genres):
    try:
        function_log.trace('Start top popular movie function')
        genres_filter = movie_rating_df['genres'].apply(lambda x: genres in x)
        rating_theshold = 0 #movie_rating[genres_filter]['n_reviewers'].mean()
        rating_filter = movie_rating_df['avg_rating']>rating_theshold
        sorted_filtered_movies = movie_rating_df[genres_filter&rating_filter].sort_values(by='n_reviewers', ascending=False)
        function_log.trace('Finish top popular movie function')
        return sorted_filtered_movies[['movieid', 'title']]

    except Exception as x:
        function_log.exception(f'Top popular function failed due to {x}')


# recommend high-rated movies, measure for "highly-rating": sorted by avg rating, but only movies with more than certain number of viewers will be considered. 
def top_high_rated_movie(genres):
    try:
        function_log.trace('Start top high rated movie function')
        genres_filter = movie_rating_df['genres'].apply(lambda x: genres in x)
        nreviewers_theshold = 100 # movie_rating[genres_filter]['n_reviewers'].mean()
        nreviewers_filter = movie_rating_df['n_reviewers'] > nreviewers_theshold
        sorted_filtered_movies = movie_rating_df[genres_filter&nreviewers_filter].sort_values(by='avg_rating', ascending=False)
        function_log.trace('Finish top high rated movie function')
        return sorted_filtered_movies[['movieid', 'title']]

    except Exception as x:
        function_log.exception(f'Top high rated function failed due to {x}')



