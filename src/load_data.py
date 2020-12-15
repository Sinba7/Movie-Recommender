import pandas as pd
import numpy as np
import urllib

# load data
myurl = "https://liangfgithub.github.io/MovieData/"

rating_df = pd.read_csv(myurl+"ratings.dat?raw=true", sep=':', header=None, usecols=[0,2,4,6])
rating_df.columns = ['userid', 'movieid', 'rating', 'timestamp']

mv_file = urllib.request.urlopen(myurl+"movies.dat?rw=true")
movie_dict = {'movieid':[], 'title':[], "genres":[]}
for line in mv_file:
    decode_line = line.decode('latin-1')[:-1]
    mv_id, title, genre = decode_line.split("::")
    if not mv_id:
        continue
    movie_dict['movieid'].append(int(mv_id))
    movie_dict['title'].append(title)
    movie_dict['genres'].append(genre)
movie_df = pd.DataFrame(movie_dict)

# movie_df = pd.read_csv("./dataset/movies.txt", sep='::', header=None, engine='python')
# movie_df.columns = ['movieid', 'title', 'genres']

# user_df = pd.read_csv(myurl+"users.dat?raw=true", sep = ':', header=None, usecols=[0,2,4,6,8])
# user_df.columns = ['userid', 'gender', 'age', 'occupation', 'zipcode']

# parse dataset
genres = np.unique("|".join(movie_df.genres.unique()).split('|'))

rated_mv_id_all = rating_df.movieid.unique()
rated_movie_df = movie_df[movie_df.movieid.isin(rated_mv_id_all)]
rated_movie_df.index = np.arange(len(rated_movie_df))
