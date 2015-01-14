# -*- coding: utf-8 -*-

import numpy as np

from dataloader import DataLoader
from portfolio import Portfolio

class Market:
    
    def __init__(self,portfolio,market_index):
        
        # Prevent building a market with no stocks
        if portfolio.nb_stocks()==0:
            raise RuntimeError("Porfolio must contain at least one stock")
        
        # Portfolio of stocks consituting the market
        self.portfolio = portfolio
        # Index representing the performance of the market. If market_index is provided,
        # it is used as a the representing index.
        self.market_index = market_index
        
    def get_first_date(self):
        """
        Return the starting date for the index series 
        """
        first_date = self.market_index[0:1].index[0].date()
        first_date = first_date.isoformat()[0:10]
        
        return first_date
        
                
    #--------------------------------------------------------------------------
    # Predefined markets
    #--------------------------------------------------------------------------
    
    @staticmethod
    def create_index_market(index_name):
        """
        Create a market based on an index: the portfolio is constituted by all the stocks
        contributing to the index, and the mark_index series is the index
        """
        portfolio = Portfolio.create_index_portfolio(index_name=index_name)
        market_index = DataLoader.load_prices(symbol=index_name)
        
        return Market(portfolio=portfolio,market_index=market_index)
             

            
            
            
            
            
            
            
            

