# -*- coding: utf-8 -*-

import pandas as pd

from dataloader import DataLoader


class RiskFreeRate:
    
    def __init__(self,risk_free_rate,currency):
        self.risk_free_rate = risk_free_rate
        self.currency = currency
        
    
    def get_first_date(self):
        """
        Return the starting date 
        """
        first_date = self.risk_free_rate[0:1].index[0].date()
        first_date = first_date.isoformat()[0:10]
        
        return first_date
        
        
    def get_last_date(self):
        """
        Return the last date 
        """
        last_date = self.risk_free_rate[-1:].index[0].date()
        last_date = last_date.isoformat()[0:10]
        
        return last_date
        

    
    ###########################################################################
    # Predefined risk free rates
    ###########################################################################
    
    @staticmethod
    def create_rates(name):

        currency = {"LIBOR ON USD":"USD",
                   "LIBOR ON EUR":"EUR",
                   "LIBOR ON GBP":"GBP",
                   "FED FUNDS RATES":"USD"}   
                            
        risk_free_rate = pd.read_csv(DataLoader.PATH_PREFIX+"Rates/"+name+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        
        return RiskFreeRate(risk_free_rate=risk_free_rate,currency=currency[name])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        