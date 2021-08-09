import pandas as pd
# import geopandas as gp
import sys

def run():
    print(f'python version: {sys.version_info}')

    print('First job - start')
    print(pd.__version__)
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    print(df)
    print('First job - stop')

if __name__ == '__main__':
    print(f'{__name__} - local run')
    run()
