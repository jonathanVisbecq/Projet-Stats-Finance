# -*- coding: utf-8 -*-


import pandas as pd

from dataloader import DataLoader
from global_data import index_currency


class Market:
    
    def __init__(self,market_index,currency):
        
        # Index representing the performance of the market
        self.market_index = market_index
        # Currency used for the index
        self.currency = currency
        
    #--------------------------------------------------------------------------

    def get_first_date(self,as_string=False):
        """
        Return the starting date (as datetime.date object)
        """
        first_date = self.market_index.index[0].date()
        
        if as_string:
            first_date = first_date.isoformat()[0:10]
        
        return first_date
        
        
    #--------------------------------------------------------------------------
        
    def get_last_date(self,as_string=False):
        """
        Return the last date (as datetime.date object)
        """
        last_date = self.market_index.index[0].date()
        
        if as_string:        
            last_date = last_date.isoformat()[0:10]
        
        return last_date        
                
    ###########################################################################
    # Functions to create predefined market indices
    ###########################################################################
    
    @staticmethod
    def create_index_market(index_name):
        """
        Create a market index
        """
                   
        market_index = pd.read_csv(DataLoader.PATH_PREFIX+"Prices/"+index_name+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        
        return Market(market_index=market_index,currency=index_currency[index_name])
             

            
            
            
            
            
            
            
            

