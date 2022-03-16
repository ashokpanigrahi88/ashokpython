import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


def preprocess(df):
    """This function takes a dataframe and preprocesses it so it is
    ready for the training stage.

    The DataFrame contains columns used for training (features)
    as well as the target column.

    It also contains some rows for which the target column is unknown.
    Those are the observations you will need to predict for KATE
    to evaluate the performance of your model.

    Here you will need to return the training set: X and y together
    with the preprocessed evaluation set: X_eval.

    Make sure you return X_eval separately! It needs to contain
    all the rows for evaluation -- they are marked with the column
    evaluation_set. You can easily select them with pandas:

         - df.loc[df.evaluation_set]

    For y you can either return a pd.DataFrame with one column or pd.Series.

    :param df: the dataset
    :type df: pd.DataFrame
    :return: X, y, X_eval
    """
    pattern = r'(?<="slug":")(\w*\s*.*)(?=")'
    df['short_category'] = df.category.str.extract(pattern)
    df[['cat', 'subcat']] = df.short_category.str.split('/', n=0, expand=True)
    df['cat'] = df.cat.astype('category').cat.codes
    df['subcat'] = df.subcat.astype('category').cat.codes
    # df["usa"] = df["country"] == "US"
    df['usa'] = df['country'].astype('category').cat.codes
    df["goal_usd"] = df["goal"] * df["static_usd_rate"]
    

    # save labels to know what rows are in evaluation set
    # evaluation_set is a boolean so we can use it as mask
    msk_eval = df.evaluation_set

    df = df[["goal_usd", 'cat', 'subcat', "usa", "state"]]

    X = df[~msk_eval].drop(["state"], axis=1)
    y = df[~msk_eval]["state"]
    X_eval = df[msk_eval].drop(["state"], axis=1)

    return X, y, X_eval


def train(X, y):
    """Trains a new model on X and y and returns it.

    :param X: your processed training data
    :type X: pd.DataFrame
    :param y: your processed label y
    :type y: pd.DataFrame with one column or pd.Series
    :return: a trained model
    """

    model = KNeighborsClassifier(n_neighbors=10)
    model.fit(X, y)

    return model


def predict(model, X_test):
    """This functions takes your trained model as well
    as a processed test dataset and returns predictions.

    On KATE, the processed test dataset will be the X_eval you built
    in the "preprocess" function. If you're testing your functions locally,
    you can try to generate predictions using a sample test set of your
    choice.

    This should return your predictions either as a pd.DataFrame with one column
    or a pd.Series

    :param model: your trained model
    :param X_test: a processed test set (on KATE it will be X_eval)
    :return: y_pred, your predictions
    """

    y_pred = model.predict(X_test)

    return pd.DataFrame(y_pred)
