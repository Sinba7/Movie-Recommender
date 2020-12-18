import pytest
from src.genres_based_recom import top_popular_movie, top_high_rated_movie
from src.collaborative_recom import collab_recommender
from src.load_data import rating_df, movie_df, rated_movie_df


@pytest.fixture()
def data_fixture():
    return rating_df, movie_df, rated_movie_df


def test_load_data(data_fixture):
    rating_df, movie_df, rated_movie_df = data_fixture
    assert rating_df.shape==(1000209, 4)
    assert all(rating_df.columns == ['userid', 'movieid', 'rating', 'timestamp'])

    assert movie_df.shape == (3883, 3)
    assert all(movie_df.columns == ['movieid', 'title', 'genres'])

    assert rated_movie_df.shape == (3706, 3)
    assert all(rated_movie_df.columns == ['movieid', 'title', 'genres'])


def test_genre_recom(g='Animation'):
    assert len(top_popular_movie(g)) == 105
    assert len(top_high_rated_movie(g)) == 82


def test_collab_recom(data_fixture):
    # value error
    with pytest.raises(ValueError):
        collab_recommender(None, None)
    # successfful case
    rating = data_fixture[0]
    pred = collab_recommender(rating.loc[:1000, ['userid', 'movieid', 'rating' ]], rating.loc[:1000, ['userid', 'movieid', 'rating' ]])
    assert pred.shape == (1001, 2)
    assert all(pred.columns == ['movieid', 'rating'])




