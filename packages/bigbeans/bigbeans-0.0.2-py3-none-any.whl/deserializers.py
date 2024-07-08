import numpy as np
import pandas as pd


def deserialize(path, file_format):
    """
    Deserialize the object from a file
    """
    if file_format == 'pkl':
        df: pd.DataFrame = pd.read_pickle(path)
        data = df.filter(like='data_')
        target = df.filter(like='target_')
        data.columns = data.columns.str.replace('data_', '')
        target.columns = target.columns.str.replace('target_', '')
        return data, target
    elif file_format == 'npz':
        npzfile = np.load(path)
        return npzfile['data'], npzfile['target']
    else:
        raise ValueError('Unsupported format')
