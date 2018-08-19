#%%----------------------------------------------------------------------------
'''
Preparations
'''
import pandas as pd
import matplotlib.pyplot as plt

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
        self.top_support_points = [[self.max_high_pos], [float('NaN')]]
        self.bot_support_pionts = [[self.min_low_pos], [float('NaN')]]

        self.top_rot_pos = self.max_high_pos
        self.bot_rot_pos = self.min_low_pos

        if (self.max_high_pos > self.min_low_pos):
            self.positive_slope = True
        else:
            self.positive_slope = False

        if(self.positive_slope):
            self.startpos_high = 0
            self.endpos_high = self.top_rot_pos - 1
            self.startpos_low = self.bot_rot_pos + 1
            self.endpos_low = self.df.shape[0] - 1
        else:
            self.startpos_high = self.top_rot_pos + 1
            self.endpos_high = self.df.shape[0] - 1
            self.startpos_low = 0
            self.endpos_low = self.bot_rot_pos - 1

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

        # TODO Add closest support piont to list
        # self.top_support_points.append(df['top_slope'].idxmin())

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

        # TODO Add closest support piont to list
        # self.top_support_points.append(df['bot_slope'].idxmin())

    def __update_rotation_pos(self):
        '''
        Set new rotation position plus start-/endpiont
        '''

        if(self.positive_slope):
            if self.df['top_slope'].min() < self.df['bot_slope'].min():
                self.top_rot_pos = self.df['top_slope'].idxmin()
                self.endpos_high = self.top_rot_pos - 1
            else:
                self.bot_rot_pos = self.df['bot_slope'].idxmin()
                self.startpos_low = self.bot_rot_pos + 1
        else:
            if self.df['top_slope'].max() > self.df['bot_slope'].max():
                self.top_rot_pos = self.df['top_slope'].idxmax()
                self.startpos_high = self.top_rot_pos + 1
            else:
                self.bot_rot_pos = self.df['bot_slope'].idxmax()
                self.endpos_low = self.bot_rot_pos - 1
    
    def calc_trendbox(self):
        '''
        Calculate trendbox
        '''
        self.__calc_top_slope()
        self.__calc_bottom_slope()
        self.__update_rotation_pos()

        # TODO: return values


def get_trendbox():
    # Create object and call its methods
    my_trendbox = TrendBox(hi_lo_df=df)
    
    # TODO: return
