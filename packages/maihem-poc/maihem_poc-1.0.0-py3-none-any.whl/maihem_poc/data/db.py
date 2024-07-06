import os
import pandas as pd


def get_vector_db(filename: str) -> pd.DataFrame:
    try:
        return load_file(filename, scope='vectordb')
    except FileNotFoundError:
        return None


def save_file(df: pd. DataFrame, filename: str, scope: str):
    if not os.path.exists('database/{}'.format(scope)):
        os.makedirs('database/{}'.format(scope))

    file_name_no_path = filename.rsplit('/',  maxsplit=1)[1]
    df.to_csv('database/{}/{}.csv'.format(scope, file_name_no_path), index=False)
    print("Saved file: {}".format(file_name_no_path))


def load_file(filename: str, scope: str) -> pd.DataFrame:
    file_name_no_path = filename.rsplit('/', maxsplit=1)[1]
    return pd.read_csv('database/{}/{}.csv'.format(scope, file_name_no_path))