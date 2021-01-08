import pandas as pd
import numpy as np
import urllib
import sys
import logbook
from urllib.error import HTTPError


def load_data():

    # logging
    load_data_log = logbook.Logger('LOAD DATA')
    level = logbook.TRACE
    logbook.StreamHandler(sys.stdout, level=level).push_application()
    # logbook.TimedRotatingFileHandler(filename, level=level).push_application()

    # load data
    myurl = "https://liangfgithub.github.io/MovieData/"

    # load rating data
    try:
        load_data_log.trace('Start loading rating data')
        rating_df = pd.read_csv(myurl+"ratings.dat?raw=true", sep=':', header=None, usecols=[0,2,4,6])
        load_data_log.trace('Finish loading rating data')
        rating_df.columns = ['userid', 'movieid', 'rating', 'timestamp']

    except urllib.error.HTTPError as x:
        msg = f'Cannot find rating data at {myurl}'
        load_data_log.warn(msg)
    except Exception as x:
        msg = f'cannot load rating data due to {x}'
        load_data_log.exception(msg)

    # load movie data, genres, rated_movie_df
    try:
        load_data_log.trace('Start loading movie data')
        mv_file = urllib.request.urlopen(myurl+"movies.dat?rw=true")
        load_data_log.trace('Finish loading movie data')

        load_data_log.trace('Start parsing movie data')
        movie_dict = {'movieid': [], 'title': [], "genres": []}
        for line in mv_file:
            decode_line = line.decode('latin-1')[:-1]
            mv_id, title, genre = decode_line.split("::")
            # if not mv_id:
            #     continue
            movie_dict['movieid'].append(int(mv_id))
            movie_dict['title'].append(title)
            movie_dict['genres'].append(genre)
        movie_df = pd.DataFrame(movie_dict)
        load_data_log.trace('Finish parsing movie data')

        load_data_log.trace('Start making rated_movie_df')
        genres = np.unique("|".join(movie_df.genres.unique()).split('|'))

        rated_mv_id_all = rating_df.movieid.unique()
        rated_movie_df = movie_df[movie_df.movieid.isin(rated_mv_id_all)]
        rated_movie_df.index = np.arange(len(rated_movie_df))
        load_data_log.trace('Finish making rated_movie_df')
        return rating_df, movie_df, genres, rated_movie_df

    except urllib.error.HTTPError:
        msg = f'Cannot find movie data at {myurl}'
        load_data_log.warn(msg)
    except Exception as x:
        load_data_log.exception(f'Movie data parsing failed due to {x}')


    # movie_df = pd.read_csv("./dataset/movies.txt", sep='::', header=None, engine='python')
    # movie_df.columns = ['movieid', 'title', 'genres']

    # user_df = pd.read_csv(myurl+"users.dat?raw=true", sep = ':', header=None, usecols=[0,2,4,6,8])
    # user_df.columns = ['userid', 'gender', 'age', 'occupation', 'zipcode']
