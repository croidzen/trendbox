import time
import os
import trendbox
import pandas as pd
import matplotlib.pyplot as plt
 
def main():
    '''
    Generate object and call methods
    '''   
    # t0 = time.clock()

    # Prepare data
    path = 'Data\\nflx.csv'
    df = pd.read_csv(filepath_or_buffer=path, header=1, index_col=0)
    df = df.drop(['Open', 'Close', 'Adj Close', 'Volume'], axis='columns')
    # df = df[2300:2500]

    # t1 = time.clock()
    # print('Preparation in main(): %.4f' %(t1-t0))

    my_trendbox = trendbox.TrendBox(hi_lo_df=df)
    my_trendbox.calc_trendbox()
    my_trendbox.plot()

    # t0 = time.clock()
    # for filename in os.listdir('Data'):
                
    #     df = pd.read_csv(filepath_or_buffer=('Data\\' + filename), header=1, index_col=0)
    #     print(filename)
    #     df = df.drop(['Open', 'Close', 'Adj Close', 'Volume'], axis='columns')
    #     df = df[-250:]

    #     my_trendbox = trendbox.TrendBox(hi_lo_df=df)
    #     my_trendbox.calc_trendbox()
    #     # my_trendbox.plot()

    # t1 = time.clock()
    # print('All files calculated: %.4f' %(t1-t0))

    # my_trendbox_slope = my_trendbox.get_trendbox_slope()


if __name__ == "__main__":
    # Execute only if run as a script
    main()