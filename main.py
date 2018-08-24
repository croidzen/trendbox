#%%----------------------------------------------------------------------------
import trendbox_v1
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Execute only if run as a script
    main()
    
def main():
    '''
    Generate object and call methods
    '''

    # Prepare data
    editor = 'vscode'
    if (editor == 'vscode'):
        path = 'C:\\Users\\Martin\\Dev\\trendbox\\Data\\MSFT.csv'
    else:
        path = 'Data\\MSFT.csv'
    df = pd.read_csv(filepath_or_buffer=path, header=1, index_col=0)
    df = df.drop(['Open', 'Close', 'Adj Close', 'Volume'], axis='columns')

    # TODO:
    my_trendbox_slope = get_trendbox()


 