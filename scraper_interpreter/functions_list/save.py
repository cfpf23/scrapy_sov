import pandas as pd
import json
import typing
import datetime


def today():
    """
    :return: str now
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')


def now():
    """
    :return: str now
    """
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def functions():
    return {'to_json': to_json,
            'to_excel': to_excel}


def to_json(df: pd.DataFrame, **kwargs) -> typing.Tuple[pd.DataFrame, str]:
    filename = f'{kwargs.get("destination")}\\Audit_{kwargs.get("label")}_{now()}.json'
    with open(filename, 'w') as json_file:
        json.dump(df.to_dict('records'), json_file)
    return df, filename


def to_excel(df: pd.DataFrame, **kwargs) -> typing.Tuple[pd.DataFrame, str]:
    filename = f'{kwargs.get("destination")}\\Audit_{kwargs.get("label")}_{now()}.xlsx'
    df.to_excel(filename)
    return df, filename
