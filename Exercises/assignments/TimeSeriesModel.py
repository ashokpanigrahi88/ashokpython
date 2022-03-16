"""
    ts1 = ts.copy()
    ts1['diff_by_t'] = ts.consumption.diff(7)
    ts1['rolling_avg'] = (ts.consumption - ts.consumption.rolling(window=14).mean())
      / ts.consumption.rolling(window=14).var()
    ts1['rolling_avg_lag'] = ts1.consumption - ts1.rolling_avg.shift(14)
    ts1['rolling_window']  = ts.consumption.rolling(window=12).mean()
    #ts['consumption'] = ts1['rolling_window']
    #ts['consumption'] = ts1['diff_by_t']
    #ts.consumption.apply(lambda x: np.log(x))
    #ts['consumption'] = ( ts.consumption - ts.consumption.rolling(window=5).mean())
      / ts.consumption.rolling(window=5).std()
"""
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA


def preprocess(df):
    """This function takes a dataframe and preprocesses it so it is
    ready for the training stage.

    import numpy as np
    from statsmodels.api import tsa
    The DataFrame contains the time axis and the target column.

    It also contains some rows for which the target column is unknown.
    Those are the observations you will need to predict for KATE
    to evaluate the performance of your model.

    Here you will need to return the training time serie: ts together
    with the preprocessed evaluation time serie: ts_eval.

    Make sure you return ts_eval separately! It needs to contain
    all the rows for evaluation -- they are marked with the column
    evaluation_set. You can easily select them with pandas:

         - df.loc[df.evaluation_set]


    :param df: the dataset
    :type df: pd.DataFrame
    :return: ts, ts_eval
    """
    # Set day as index
    df.set_index(pd.to_datetime(df.day), inplace=True)
    df.drop("day", axis=1, inplace=True)

    # Save msk to split data later
    msk_eval = df.evaluation_set
    df.drop("evaluation_set", axis=1, inplace=True)

    # Split training/test data
    ts = df[~msk_eval]
    ts.dropna(inplace=True)
    ts_eval = df[msk_eval]

    return ts, ts_eval


def train(ts):
    """Trains a new model on ts and returns it.

    :param ts: your processed training time serie
    :type ts: pd.DataFrame
    :return: a trained model

    #model = tsa.AR(ts.consumption).fit(maxlag=62)
    # 4,0,2 mape 3.02 % 3,0,0 3.2%, 2, 0, 0
    #model = tsa.ARMA(ts.consumption , order=(3, 3)).fit()
    """
    model = ARIMA(ts.consumption, (2, 0, 0)).fit()

    return model


def predict(model, ts_test):
    """This functions takes your trained model as well
    as a processed test time serie and returns predictions.

    On KATE, the processed testt time serie will be the ts_eval you built
    in the "preprocess" function. If you're testing your functions locally,
    you can try to generate predictions using a sample test set of your
    choice.

    This should return your predictions either as a pd.DataFrame with one column
    or a pd.Series

    :param model: your trained model
    :param ts_test: a processed test time serie (on KATE it will be ts_eval)
    :return: y_pred, your predictions
    """

    # Find starting and end date
    start = ts_test.index[0]
    end = ts_test.index[-1]

    # Generate predictions
    preds = model.predict(start=start, end=end)

    return preds
