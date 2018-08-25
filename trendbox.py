'''
Preparations
'''
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os

plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [13, 8]
plt.rcParams['axes.facecolor'] = '#121417'
plt.rcParams['figure.facecolor'] = '#282C34'


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
        self.top_support_points = np.array([[
            self.max_high_pos, self.df.loc[self.max_high_pos, 'High'], float('NaN')]])
        self.bot_support_points = np.array([[
            self.min_low_pos, self.df.loc[self.min_low_pos, 'Low'], float('NaN')]])

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
        self.slope_defined_by_upside = False


    def __calc_top_slopes(self):
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
            (y.sub(yi)).div(x.sub(xi)))

        # Add closest support piont to list
        if (self.positive_slope):
            pos = self.df['top_slope'].idxmin()
            self.top_support_points = np.append(self.top_support_points, [[
                pos, self.df.loc[pos, 'High'], self.df['top_slope'].min()]], axis=0)
        else:
            pos = self.df['top_slope'].idxmax()
            self.top_support_points = np.append(self.top_support_points, [[
                pos, self.df.loc[pos, 'High'], self.df['top_slope'].max()]], axis=0)


    def __calc_bottom_slopes(self):
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
            (y.sub(yi)).div(x.sub(xi)))

        # Add closest support piont to list
        if (self.positive_slope):
            pos = self.df['bot_slope'].idxmin()
            self.bot_support_points = np.append(self.bot_support_points, [[
                pos, self.df.loc[pos, 'Low'], self.df['bot_slope'].min()]], axis=0)
        else:
            pos = self.df['bot_slope'].idxmax()
            self.bot_support_points = np.append(self.bot_support_points, [[
                pos, self.df.loc[pos, 'Low'], self.df['bot_slope'].max()]], axis=0)


    def __set_slope_defining_side(self):
        '''
        Set slope defining side
        '''
        if (self.positive_slope):
            if (self.top_support_points[-1, 2] < self.bot_support_points[-1, 2]):
                self.slope_defined_by_upside = True
            else:
                self.slope_defined_by_upside = False
        else:
            if (self.top_support_points[-1, 2] > self.bot_support_points[-1, 2]):
                self.slope_defined_by_upside = True
            else:
                self.slope_defined_by_upside = False


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
        self.__calc_top_slopes()
        self.__calc_bottom_slopes()
        self.__set_slope_defining_side()

        while True:
            self.last_trendbox_width = self.get_trendbox_width()
            
            if (self.slope_defined_by_upside):
                self.__update_upper_rotation_pos()
                if (self.top_rot_pos == 0):
                    break
                self.__calc_top_slopes()
                if(self.get_trendbox_width() > self.last_trendbox_width):
                    self.top_support_points = np.delete(self.top_support_points, -1, axis=0)
                    self.__set_slope_defining_side()
                    break
            else:
                self.__update_lower_rotation_pos()
                if (self.bot_rot_pos == 0):
                    break
                self.__calc_bottom_slopes()
                if(self.get_trendbox_width() > self.last_trendbox_width):
                    self.bot_support_points = np.delete(self.bot_support_points, -1, axis=0)
                    self.__set_slope_defining_side()
                    break
            self.__set_slope_defining_side()
            if (self.top_rot_pos == 0 or self.bot_rot_pos == 0):
                break
            
        
    def get_trendbox_slope(self):
        '''
        TODO
        '''
        if (self.slope_defined_by_upside):
            m = self.top_support_points[-1, 2]
        else:
            m = self.bot_support_points[-1, 2]
            
        return m


    def get_trendbox_width(self):
        '''
        Get distance of current trendbox based on current rotation pionts

        Distance of two parallel straights y=mx+b:
        d = |b2-b1| / sqrt(m*m+1)

        Get b from point and slope:
        b1 = y1 - m * x1
        '''
        m = self.get_trendbox_slope()
        
        if (self.slope_defined_by_upside):
            x1 = self.top_support_points[-1, 0]
            y1 = self.top_support_points[-1, 1]
            b1 = y1 - (m * x1)

            x2 = self.bot_support_points[-2, 0]
            y2 = self.bot_support_points[-2, 1]
            b2 = y2 - (m * x2)
        else:
            x1 = self.bot_support_points[-1, 0]
            y1 = self.bot_support_points[-1, 1]
            b1 = y1 - (m * x1)

            x2 = self.top_support_points[-2, 0]
            y2 = self.top_support_points[-2, 1]
            b2 = y2 - (m * x2)

        d = abs(b2 - b1) / math.sqrt(m * m + 1)

        return d


    def plot(self):
        '''
        Plot result
        '''
        # 'High' and 'Low' values
        plt.plot(self.df.index.values, self.df['High'])
        plt.plot(self.df.index.values, self.df['Low'])

        # Support points
        plt.plot(self.top_support_points[:, 0], self.top_support_points[:, 1], 'ro')
        plt.plot(self.bot_support_points[:, 0], self.bot_support_points[:, 1], 'ro')

        # Trendbox
        # y=mx+b (explicit form)
        # y-y1=m(x-x1) (piont slope form)
        # -> b=y1-m*x1
        # -> y=m(x-x1)+y1
        m = self.get_trendbox_slope()

        if (self.slope_defined_by_upside):
            x1 = self.top_support_points[-1, 0]
            y1 = self.top_support_points[-1, 1]
            # x2 = self.top_support_points[-2, 0]
            # y2 = self.top_support_points[-2, 1]
            x_top_min = 0
            y_top_min = m * (x_top_min - x1) + y1
            x_top_max = len(self.df)
            y_top_max = m * (x_top_max - x1) + y1

            x_bot = self.bot_support_points[-2, 0]
            y_bot = self.bot_support_points[-2, 1]
            x_bot_min = 0
            y_bot_min = y_bot - (m * x_bot)
            x_bot_max = len(self.df)
            y_bot_max = m * (x_bot_max - x_bot) + y_bot
        else:
            x1 = self.bot_support_points[-1, 0]
            y1 = self.bot_support_points[-1, 1]
            # x2 = self.bot_support_points[-2, 0]
            # y2 = self.bot_support_points[-2, 1]
            x_bot_min = 0
            y_bot_min = m * (x_bot_min - x1) + y1
            x_bot_max = len(self.df)
            y_bot_max = m * (x_bot_max - x1) + y1

            x_top = self.top_support_points[-2, 0]
            y_top = self.top_support_points[-2, 1]
            x_top_min = 0
            y_top_min = y_top - (m * x_top)
            x_top_max = len(self.df)
            y_top_max = m * (x_top_max - x_top) + y_top
        
        plt.plot([x_bot_min, x_bot_max], [y_bot_min, y_bot_max])
        plt.plot([x_top_min, x_top_max], [y_top_min, y_top_max])
        # plt.plot([x_top_min, x_top_max], [0, 0])
        plt.show()