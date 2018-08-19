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


    '''
    Plot trendbox
    '''

    # plt.figure(1)
    # plt.subplot(311)

    # plt.plot(my_trendbox.df.index.values, my_trendbox.df['High'])
    # x1 = my_trendbox.df['top_slope'].idxmin()
    # x2 = my_trendbox.top_rot_pos
    # y1 = my_trendbox.df.loc[my_trendbox.df['top_slope'].idxmin(), 'High']
    # y2 = my_trendbox.df.loc[my_trendbox.top_rot_pos, 'High']
    # plt.plot([x1, x2], [y1, y2])

    # plt.plot(my_trendbox.df.index.values, my_trendbox.df['Low'])
    # x1 = df['bot_slope'].idxmin()
    # x2 = bot_rot_pos
    # y1 = df.loc[df['bot_slope'].idxmin(), 'Low']
    # y2 = df.loc[bot_rot_pos, 'Low']
    # plt.plot([x1, x2], [y1, y2])

    # plt.subplot(312)
    # plt.plot(df.index.values, df['top_slope'])

    # plt.subplot(313)
    # plt.plot(df.index.values, df['bot_slope'])