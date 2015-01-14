# -*- coding: utf-8 -*-

import os.path
import cPickle as pickle
import datetime
import warnings

import pandas as pd
import pandas.io.data as webData

from stock_attributes import StockAttributes


"""
Load only symbols for which we have everything (attributes, prices,...) so as to ease after treatment of data



"""


class DataLoader: 
    # Using Yahoo Finance as the stocks data provider
    DATA_SOURCE = "yahoo"
    # Starting date for historical prices
    START_DATE = datetime.datetime(1990, 1, 1)
    # Last date for historical prices
    END_DATE = datetime.datetime(2014, 10, 30)
    # Path for saving the .csv files
    PATH_PREFIX = "/home/jonathan/Programmation/Python/Projet_statsFinance/Stocks data/"
    
    @staticmethod
    def predefined_index_components_path(index_name):
        """        
        Predefined helpful paths
        """
        return DataLoader.PATH_PREFIX + "Lists of symbols/" + index_name
    

    @staticmethod
    def symbols():
        """
        Return the list of symbols already retrieved
        """
        
        if os.path.isfile(DataLoader.PATH_PREFIX+"Symbols"):
            symbols = pickle.load(open(DataLoader.PATH_PREFIX+"Symbols","r"))
        else:
            symbols = []  
            
        return symbols
         
    @staticmethod
    def read_symbols_from_file(path):
        """
        Read symbols stored in a file such that there is one symbole per line
        """        
        
        symbols = []
        
        with open(path,"r") as sym_file:
            for symbol in iter(sym_file):
                symbols.append(symbol[:-1]) # Last character in '\n'
                
        return symbols
        
        
    @staticmethod
    def get_historical_prices(symbol,save=False):
        """
        Get historical adjusted close prices from the data provider and save it
        """
        
        ts = webData.DataReader(symbol, DataLoader.DATA_SOURCE, DataLoader.START_DATE, DataLoader.END_DATE)
        ts = ts['Adj Close']
        ts.name = "Price"
        
        if save:
             # Save prices in the Prices folder
            path_price =  DataLoader.PATH_PREFIX + "Prices/" + symbol + ".csv"
            ts.to_csv(path=path_price,header=True)    
        else:
            return ts
            
            
    @staticmethod
    def get_attributes(symbol,save=False):
        """
        Fetch stock's attributes from the web and save it
        """
        
        # Fetch attributes and save it in the Attributes folder
        stock_attributes = StockAttributes.get_stock_attributes(symbol)
        
        if save:
            DataLoader.save_attributes(symbol=symbol,attributes=stock_attributes)
        else:
            return stock_attributes
            
            
    @staticmethod
    def save_attribute(symbol,attributes):
        """
        Save attributes for a given stock in the Attributes folder
        """
        
        path_attr = DataLoader.PATH_PREFIX + "Attributes/" + symbol
        pickle.dump(attributes,open(path_attr,"w"))
    

        
    @staticmethod
    def save_symbol(symbol=None,symbols=None):
        """
        Save a single symbol or a list/set/tuple of symbols in the Symbols file
        (where there dumped as a set)
        """
        
        s = set(DataLoader.symbols());

        if symbols is not None:
            s = s.union(set(symbols))
 
        if symbol is not None:
            s.add(symbol)
  
        if (symbols is not None) or (symbol is not None):
            pickle.dump(s,open(DataLoader.PATH_PREFIX+"Symbols","w"))
            
                


    @staticmethod
    def save_stock_data(symbol,erase=False,prices=True,attributes=True):
        
        # Look for the name among the symbols already fetched and does nothing
        # if already retrieved
        symbols = DataLoader.symbols();
        
        if not erase:
            if symbol in symbols:
                return
      
        # If new symbol:
        
        if prices:
            # Fetch and save historical prices
            DataLoader.get_historical_prices(symbol,save=True)
        
        if attributes:
            # Fetch attributes and save it in the Attributes folder
            DataLoader.get_attributes(symbol,save=True)
        
        # Add the symbol to the list in the Symbols file
        if prices or attributes:
            DataLoader.save_symbol(symbols=symbols,symbol=symbol)
            
        
        
    @staticmethod
    def save_listOf_stocks(path,erase=False,prices=True,attributes=True):
        
        # List of the symbols to fetch from the web
        symbols = DataLoader.read_symbols_from_file(path)
        # To store the symbols we fail to fetch from the web        
        errors_list = {}
        
        for symbol in symbols:
            print(symbol)
            
            try:
                DataLoader.save_stock_data(symbol,erase=erase,prices=prices,attributes=attributes)
                print("--Successfully saved")
            except Exception as e:
                print("-------------------------------")
                print("--Error occured:" + e.message)
                print("-------------------------------")                    
                
                errors_list[symbol] = e.message
                
        return errors_list
        
        
        
    @staticmethod
    def load_prices(symbol):
        
        if not symbol in DataLoader.symbols():
            warnings.warn("Symbol not found. No price retrieved")
            return None
    
        return pd.read_csv(DataLoader.PATH_PREFIX+"Prices/"+symbol+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
    

    @staticmethod
    def load_attributes(symbol):
        
        if not symbol in DataLoader.symbols():
            warnings.warn("Symbol not found. Attributes not retrieved")
            return None
                                          
        return pickle.load(open(DataLoader.PATH_PREFIX+"Attributes/"+symbol,"r"))
        
    
    @staticmethod
    def load_prices_attributes(symbol):
        # Return prices,attributes
        return DataLoader.load_prices(symbol),DataLoader.load_attributes(symbol)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

     