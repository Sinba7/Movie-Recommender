import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans,  KNNWithZScore
from load_data import rating_df 


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
        
    return pd.DataFrame(pred_rating)
    

# def collab_recommender(train_data, test_data, user_based=True):
#     """
#     Input: 
#     - train_data: n*3, 'userid','movieid','rating'
#     - test_data: n*2, 'userid', 'movieid'
#     Output:
#     - pred_rating: n*2, 'movieid', 'rating'
#     """
#     reader = Reader(rating_scale=(1,5))
#     data = Dataset.load_from_df(train_data, reader)

#     sim_options = {
#         'name':'cosine', 
#         'user_based': user_based
#     }
#     algo = KNNWithMeans(sim_options=sim_options)

#     train_set = data.build_full_trainset()
#     algo.fit(train_set)

#     pred_rating = {'movieid':[], 'rating':[]}
#     for idx in test_data.index:
#         pred_rating['movieid'].append(test_data.loc[idx, 'movieid'])
#         pred = algo.predict(test_data.loc[idx, 'userid'], test_data.loc[idx, 'movieid'])
#         pred_rating['rating'].append(pred.est)
        
#     return pd.DataFrame(pred_rating)
    