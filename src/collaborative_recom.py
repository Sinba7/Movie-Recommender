import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans,  KNNWithZScore
import logbook
import sys


# logging
function_log = logbook.Logger('RECOMMENDER')
level = logbook.TRACE
logbook.StreamHandler(sys.stdout, level=level).push_application()


def collab_recommender(train_data, test_data, user_based=True, normalization= False, k=100, sim='cosine'):
    """
    Input: 
    - train_data: dataframe, n*3, columns are ['userid','movieid','rating']
    - test_data: dataframe, n*2, columns are ['userid', 'movieid']
    - user_base: boolean, use user-based knn algorithm if True, use item-based knn algorithm if False
    - normalization: boolean, conduct z-score normalization on user/item matrix if True
    - k: int, number of nearest neighbors
    - sim: string, define the similarity matrix from ['cosine', 'pearson', 'msd', 'pearson_baseline']
    
    Output:
    - pred_rating: dataframe, n*2, columns are ['movieid', 'rating']
    """
    try:
        function_log.trace('Start collaborative recommendation function')
        if train_data is None or test_data is None:
            function_log.exception("Training and test data cannot be none")
            raise ValueError("Training and test data cannot be none.")

        reader = Reader(rating_scale=(1,5))
        data = Dataset.load_from_df(train_data, reader)

        sim_options = {
            'name':sim,
            'user_based': user_based
        }

        if normalization:
            algo = KNNWithZScore(k=k, sim_options=sim_options, verbose=False)
        else:
            algo = KNNWithMeans(k=k, sim_options=sim_options, verbose=False)

        train_set = data.build_full_trainset()
        algo.fit(train_set)

        pred_rating = {'movieid':[], 'rating':[]}
        for idx in test_data.index:
            pred_rating['movieid'].append(test_data.loc[idx, 'movieid'])
            pred = algo.predict(test_data.loc[idx, 'userid'], test_data.loc[idx, 'movieid'])
            pred_rating['rating'].append(pred.est)
        function_log.trace('Finish collaborative recommendation function')
        return pd.DataFrame(pred_rating)

    except Exception as x:
        function_log.exception(f'collaborative recommendation function failed {x}')
