import pandas as pd


def functions():
    return {'expand_column': expand_column,
            'expand_rows': expand_rows}


def expand_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Expands DataFrame column with list values into multiple columns.
    :param df: pd.DataFrame
    :param col: name of the column to expand (str)
    :return: pd.DataFrame
    """
    maxlen = len(max(df[col], key=lambda l: len(l) if isinstance(l, list) else 0))
    df[col] = df[col].apply(lambda iterable: iterable + [None for _ in range(maxlen-len(iterable))])
    df[[f'{col}_{i+1}' for i in range(maxlen)]] = pd.DataFrame(df[col].to_list(), index=df.index)
    return df.drop(col, axis=1)


def expand_rows(df: pd.DataFrame) -> pd.DataFrame:
    new_ld = []
    ld = df.to_dict('records')
    for row in ld:
        new_ld.extend(pd.DataFrame(row).to_dict('records'))
    return pd.DataFrame(new_ld)
