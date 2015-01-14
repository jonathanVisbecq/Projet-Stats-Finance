# -*- coding: utf-8 -*-

import pandas as pd

from dataloader import DataLoader


class RiskFreeRate:
    
    def __init__(self,risk_free_rate,currency):
        self.risk_free_rate = risk_free_rate
        self.currency = currency
        
    
    def get_first_date(self):
        """
        Return the starting date for the time series of rates as a string
        """
        first_date = self.risk_free_rate[0:1].index[0].date()
        first_date = first_date.isoformat()[0:10]
        
        return first_date
        

    
    #--------------------------------------------------------------------------
    # Predefined risk free rates
    #--------------------------------------------------------------------------
    
    @staticmethod
    def create_fed_funds_rate():
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/Fed Funds Rate.csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency="USD")
        
    @staticmethod
    def create_LIBOR_overnight_USD():
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/LIBOR Overnight USD.csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency="USD")
        
    @staticmethod
    def create_sonia_rate():
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/SONIA lending.csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency="GBp")
        
    @staticmethod
    def create_eonia_rate():
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/EONIA lending.csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency="EUR")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        