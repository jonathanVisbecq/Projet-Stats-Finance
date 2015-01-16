# -*- coding: utf-8 -*-


import pandas as pd

from dataloader import DataLoader


class Market:
    
    def __init__(self,market_index):
        
        # Index representing the performance of the market
        self.market_index = market_index
        
    def starting_date(self):
        """
        Return the starting date for the index series 
        """
        return self.market_index.index[0]

        
                
    #--------------------------------------------------------------------------
    # Predefined markets
    #--------------------------------------------------------------------------
    
    @staticmethod
    def create_index_market(index_name):
        """
        Create a market index
        """
        market_index = pd.read_csv(DataLoader.PATH_PREFIX+"Prices/"+index_name+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        return Market(market_index=market_index)
             

            
            
            
            
            
            
            
            

