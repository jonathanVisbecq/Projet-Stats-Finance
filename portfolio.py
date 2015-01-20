# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import warnings
import bisect

from dataloader import DataLoader

class Portfolio:
    
    def __init__(self,symbols=[]):
        # Store the symbols for the stocks in the portfolio. The actual timeseries
        # are not stored.
        self.stocks = symbols

        # Store the starting date and ending_date of the historical records for each stock.
        # Dates are stored as pandas' datetime objects 
        self.start_dates = []
               
        # Sort stocks and starting dates from the oldest the the newest
        self.stocks,self.start_dates = self._sort_by_start_date()        
        # Check if all stocks have the same last date (specified in class DataLoader)
        # In case a warning is issued, it has to dealt with manually        
        self._check_last_date()

    #--------------------------------------------------------------------------        

    def nb_stocks(self):
        """
        """
        return len(self.stocks)
                
    #--------------------------------------------------------------------------

    def add_stock(self,stock):
        """
        Add a stock to the portfolio (and keep the stocks sorted by starting date)
        """        
        start_date = self._start_date(stock)
        idx = bisect.bisect_left(self.start_dates,start_date)
        
        self.start_dates[idx+1:idx+1] = [start_date]
        self.stocks[idx+1:idx+1] = [stock]

    #--------------------------------------------------------------------------

    def stocks_with_data(self,nb_returns,with_quotes=False):
         """
         Return a list of the stocks for which there is at least 'nb_returns'
         historical returns available (ie at least 'nb_returns'+1 daily records),
         and the associated quotes if required
         """
         idx = len(self.stocks)-1
         
         while idx>=0:
             prices,_ = DataLoader.read_prices_attributes(self.stocks[idx])
             
             if len(prices) >= (nb_returns+1):
                 break;
             else:
                 idx -= 1
                 
         stocks = self.stocks[0:idx+1]
   
         if with_quotes:
             quotes = Portfolio.agreggate_quotes(stocks=stocks,start_date=self.start_dates[0])
             return stocks,quotes
         else:
             return stocks
    
    
    
    #--------------------------------------------------------------------------
    
    @staticmethod
    def agreggate_quotes(stocks,start_date=DataLoader.START_DATE,end_date=DataLoader.END_DATE,align=True):
        """
        Return a pandas Dataframe (one stock per column)
        No check provided for ensuring consistent currency between stocks
        """
        stock_prices = {}

        for stock in stocks:
            p,_ = DataLoader.read_prices_attributes(stock)
            stock_prices[stock] = p[start_date:end_date]
            
        stock_prices = pd.DataFrame(data=stock_prices)
        
        if align:
            stock_prices = stock_prices.fillna(method='ffill')
            # Remaining NaN (first ones) are dealt with using backward propagation
            stock_prices = stock_prices.fillna(method='bfill')
            
        return stock_prices

    
    ###########################################################################
    # Internal functions    
    ########################################################################### 
    
    def _start_date(self,stock):
        """
        Return the first date for the timeseries associated to the stock as a
        Datetime object
        """
        _,a = DataLoader.read_prices_attributes(symbol=stock)
        start_date = pd.to_datetime(a.start_date,coerce=True)
        
        if start_date is pd.NaT:
            raise warnings.warn("Starting date for stock {} ({}) is invalid".format(stock,a.start_date))
            
        if start_date<DataLoader.START_DATE: 
            start_date = pd.to_datetime(DataLoader.START_DATE)
            
        return start_date
            
    #--------------------------------------------------------------------------
    
    def _sort_by_start_date(self):
        """
        Initialize self.start_dates with a list of pandas' datetime objects representing
        the starting dates for the records of the stocks in the portfolio
        """
        start_dates = self.start_dates
        stocks = self.stocks
        
        # Raise an error if a date could not be parsed by pandas.to_datetime
        for stock in stocks:
            start_dates.append(self._start_date(stock))
            
        # Sort form the oldest to the newest starting dates
        idx_sort = np.argsort(np.array(start_dates))
        start_dates = list(np.array(start_dates)[idx_sort])
        stocks = list(np.array(stocks)[idx_sort])
            
        return stocks,start_dates

    #--------------------------------------------------------------------------
        
    def _check_last_date(self):
        """
        """
        for stock in self.stocks:
            p,_ = DataLoader.read_prices_attributes(stock)
            last_date = p.last_valid_index().to_datetime()
            
            if last_date != DataLoader.END_DATE:
                warnings.warn("Last date of {} is different: {} and {}".format(stock,last_date,DataLoader.END_DATE))
        
    ###########################################################################
    # Fonctions to create predefined portfolios
    ###########################################################################

    @staticmethod
    def create_index_portfolio(index_name):
        """
        Create a porfolio with all the constituents of a given index
        """
        return Portfolio(symbols=DataLoader.read_index_components(index_name))