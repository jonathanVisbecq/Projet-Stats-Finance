# -*- coding: utf-8 -*-

import pandas as pd

from dataloader import DataLoader
from global_data import interest_rates_currency


class RiskFreeRate:
    
    def __init__(self,risk_free_rate,currency):
        self.risk_free_rate = risk_free_rate
        self.currency = currency
        
    
    def get_first_date(self,as_string=False):
        """
        Return the starting date(as datetime.date object)
        """
        first_date = self.risk_free_rate.index[0].date()
        
        if as_string:
            first_date = first_date.isoformat()[0:10]
        
        return first_date
        
        
    def get_last_date(self,as_string=False):
        """
        Return the last date (as datetime.date object)
        """
        last_date = self.risk_free_rate.index[0].date()
        
        if as_string:        
            last_date = last_date.isoformat()[0:10]
        
        return last_date
        

    
    ###########################################################################
    # Predefined risk free rates
    ###########################################################################
    
    @staticmethod
    def create_rates(name):
        """
        """                 
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/"+name+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency=interest_rates_currency[name])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        