#%%----------------------------------------------------------------------------
'''
Preparations
'''
import pandas as pd
import matplotlib.pyplot as plt
import math

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [13, 8]
plt.rcParams['axes.facecolor'] = '#121417'
plt.rcParams['figure.facecolor'] = '#282C34'


#%%----------------------------------------------------------------------------
class TrendBox:
    '''
    Class definition
    '''
    def __init__(self, hi_lo_df):
        '''
        Constructor
        '''
        self.df = hi_lo_df
        self.df['top_slope'] = pd.Series(float('NaN'), index=self.df.index)
        self.df['bot_slope'] = pd.Series(float('NaN'), index=self.df.index)
        self.df['bar_no'] = range(0, len(self.df))
        self.df = self.df.set_index(keys='bar_no')
    
        self.max_high_pos = self.df['High'].idxmax()
        self.min_low_pos = self.df['Low'].idxmin()

        #support points and slope to them from the previous point
        self.top_support_points = [[self.max_high_pos, float('NaN')]]
        self.bot_support_points = [[self.min_low_pos, float('NaN')]]

        self.top_rot_pos = self.max_high_pos
        self.bot_rot_pos = self.min_low_pos

        if (self.max_high_pos > self.min_low_pos):
            self.positive_slope = True
        else:
            self.positive_slope = False

        if (self.positive_slope):
            self.startpos_high = 0
            self.endpos_high = self.top_rot_pos - 1
            self.startpos_low = self.bot_rot_pos + 1
            self.endpos_low = self.df.shape[0] - 1
        else:
            self.startpos_high = self.top_rot_pos + 1
            self.endpos_high = self.df.shape[0] - 1
            self.startpos_low = 0
            self.endpos_low = self.bot_rot_pos - 1

        self.last_trendbox_width = 0

        # self.calc_trendbox() aufrufen?


    def __calc_top_slope(self):
        '''
        Calculate top-slope values for all positions
        slope = (y-yi)/(x-xi)
        '''
        # Preparations
        self.df['top_slope'] = pd.Series(float('NaN'), index=self.df.index)
        length = self.endpos_high - self.startpos_high

        # Get top rotation value
        y = self.df.loc[self.top_rot_pos, 'High']
        # Transforn to homogenous series
        y = pd.Series(y, index=range(self.startpos_high, self.startpos_high + length))
        # Get other 'High' values
        yi = self.df.loc[self.startpos_high:self.endpos_high, 'High']

        # Get top rotation position
        x = self.top_rot_pos
        # Transforn to homogenous series
        x = pd.Series(x, index=range(self.startpos_high, self.startpos_high + length))
        # Get other position values
        xi = self.df.index.tolist()[self.startpos_high:self.endpos_high]

        # Paste all series into formula
        self.df.loc[self.startpos_high:self.endpos_high, 'top_slope'] = (
            (y.sub(yi)).div(x.sub(xi))).mul(100)

        # Add closest support piont to list
        if (self.positive_slope):
            self.top_support_points.append([self.df['top_slope'].idxmin(), self.df['top_slope'].min()])
        else:
            self.top_support_points.append([self.df['top_slope'].idxmax(), self.df['top_slope'].max()])


    def __calc_bottom_slope (self):
        '''
        Calculate bot-slope values for all positions
        slope = (y-yi)/(x-xi)
        '''
        # Preparations
        self.df['bot_slope'] = pd.Series(float('NaN'), index=self.df.index)
        length = self.endpos_low - self.startpos_low

        # Get bottom rotation value
        y = self.df.loc[self.bot_rot_pos, 'Low']
        # Transforn to homogenous series
        y = pd.Series(y, index=range(self.startpos_low, self.startpos_low + length))
        # Get other 'Low' values
        yi = self.df.loc[self.startpos_low:self.endpos_low, 'Low']

        # Get bottom rotation position
        x = self.bot_rot_pos
        # Transforn to homogenous series
        x = pd.Series(x, index=range(self.startpos_low, self.startpos_low + length))
        # Get other position values
        xi = self.df.index.tolist()[self.startpos_low:self.endpos_low]

        # Paste all series into formula
        self.df.loc[self.startpos_low:self.endpos_low, 'bot_slope'] = (
            (y.sub(yi)).div(x.sub(xi))).mul(100)

        # Add closest support piont to list
        if (self.positive_slope):
            self.bot_support_points.append([self.df['bot_slope'].idxmin(), self.df['bot_slope'].min()])
        else:
            self.bot_support_points.append([self.df['bot_slope'].idxmax(), self.df['bot_slope'].max()])


    def __update_upper_rotation_pos(self):
        '''
        Set new upper rotation position plus start-/endpiont
        '''
        if (self.positive_slope):
            self.top_rot_pos = self.df['top_slope'].idxmin()
            self.endpos_high = self.top_rot_pos - 1
        else:
            self.top_rot_pos = self.df['top_slope'].idxmax()
            self.startpos_high = self.top_rot_pos + 1
            
    
    def __update_lower_rotation_pos(self):
        '''
        Set new lower rotation position plus start-/endpiont
        '''
        if (self.positive_slope):
            self.bot_rot_pos = self.df['bot_slope'].idxmin()
            self.startpos_low = self.bot_rot_pos + 1
        else:
            self.bot_rot_pos = self.df['bot_slope'].idxmax()
            self.endpos_low = self.bot_rot_pos - 1


    def calc_trendbox(self):
        '''
        Calculate trendbox
        '''
        self.__calc_top_slope()
        self.__calc_bottom_slope()
        
        while True:
            self.last_trendbox_width = self.get_trendbox_width()
            
            if (self.positive_slope):
                if (self.top_support_points[-1][1] < self.bot_support_points[-1][1]):
                    self.__update_upper_rotation_pos()
                    self.__calc_top_slope()
                else:
                    self.__update_lower_rotation_pos()
                    self.__calc_bottom_slope()
            else:
                if (self.top_support_points[-1][1] > self.bot_support_points[-1][1]):
                    self.__update_upper_rotation_pos()
                    self.__calc_top_slope()
                else:
                    self.__update_lower_rotation_pos()
                    self.__calc_bottom_slope()
            
            if(self.get_trendbox_width() > self.last_trendbox_width):
                break


    def get_trendbox_slope(self):
        if (self.positive_slope):
            if (self.top_support_points[-1][1] < self.bot_support_points[-1][1]):
                m = self.top_support_points[-1][1]
            else:
                m = self.bot_support_points[-1][1]
        else:
            if (self.top_support_points[-1][1] > self.bot_support_points[-1][1]):
                m = self.top_support_points[-1][1]
            else:
                m = self.bot_support_points[-1][1]
        return m


    def get_trendbox_width(self):
        '''
        Get distance of current trendbox based on current rotation pionts

        Distance of two parallel straights y=mx+b:
        d = |b2-b1| / sqrt(m*m+1)

        Get b from point and slope:
        b1 = y1 - m*x1
        '''
        m = self.get_trendbox_slope()
        
        x1 = self.top_support_points[-1][0]
        y1 = self.df.loc[x1, 'High']
        b1 = y1 - (m * x1)

        x2 = self.bot_support_points[-1][0]
        y2 = self.df.loc[x2, 'Low']
        b2 = y2 - (m * x2)

        d = abs(b2 - b1) / math.sqrt(m * m + 1)
        return d


    def get_trendbox_upper_endpos(self):
        return self.top_support_points[-1][0]


    def plot(self):
        '''
        Plot result
        '''
        # 'High' and 'Low' values
        # plt.plot(self.df.index.values, self.df['High'])
        # plt.plot(self.df.index.values, self.df['Low'])

        # Support points
        # plt.plot(self.top_support_points)
        # plt.plot(self.bot_support_points)

        # Trendbox
        if (self.positive_slope):
            if (self.top_support_points[-1][1] < self.bot_support_points[-1][1]):
                x1 = self.top_support_points[-1][0]
                y1 = self.df.loc[x1, 'High']
                
                x2 = self.top_support_points[-2][0]
                y2 = self.df.loc[x2, 'High']

                x3 = self.bot_support_points[-2][0]
                y3 = self.df.loc[x3, 'Low']
                
                x4 = self.bot_support_points[-1][0]
                y4 = y1 - self.get_trendbox_width()
            else:
                x1 = self.bot_support_points[-1][0]
                y1 = self.df.loc[x1, 'Low']
                
                x2 = self.bot_support_points[-2][0]
                y2 = self.df.loc[x2, 'Low']

                x3 = self.top_support_points[-2][0]
                y3 = self.df.loc[x3, 'High']
                
                x4 = self.top_support_points[-1][0]
                y4 = y1 + self.get_trendbox_width()
        else:
            if (self.top_support_points[-1][1] > self.bot_support_points[-1][1]):
                pass
            else:
                pass

        # plt.plot([x1, x2], [y1, y2])
        # plt.plot([x3, x4], [y3, y4])

        print('x1: ' + str(x1))
        print('x2: ' + str(x2))
        print('x3: ' + str(x3))
        print('x4: ' + str(x4))
        
        print('y1: ' + str(y1))
        print('y2: ' + str(y2))
        print('y3: ' + str(y3))
        print('y4: ' + str(y4))
        
#%%----------------------------------------------------------------------------
# def main():
'''
Call methods
'''
# Prepare data
editor = 'vscode'
if (editor == 'vscode'):
    path = 'C:\\Users\\Martin\\Dev\\trendbox\\Data\\MSFT.csv'
else:
    path = 'Data\\MSFT.csv'
df = pd.read_csv(filepath_or_buffer=path, header=1, index_col=0)
df = df.drop(['Open', 'Close', 'Adj Close', 'Volume'], axis='columns')

my_trendbox = TrendBox(hi_lo_df=df)
my_trendbox.calc_trendbox()
my_trendbox.plot()

#%%----------------------------------------------------------------------------
# my_trendbox_slope = my_trendbox.get_trendbox_slope()
