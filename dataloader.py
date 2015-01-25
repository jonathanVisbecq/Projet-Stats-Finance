# -*- coding: utf-8 -*-

import os.path
import cPickle as pickle
import datetime
import warnings

import pandas as pd
import pandas.io.data as webData

from stock_attributes import StockAttributes



class DataLoader: 
    # Path for saving the .csv files
    PATH_PREFIX = "/home/jonathan/Programmation/Python/Projet_statsFinance/Stocks data/"
    
    # Starting date for historical prices
    START_DATE = datetime.datetime(1990, 1, 1)
    # Last date for historical prices
    END_DATE = datetime.datetime(2014, 12, 31)
    
    
    
    ###########################################################################
    # Functions to get stock data from the internet
    ###########################################################################
    
    @staticmethod
    def fetch_stock_data(symbol,erase=False,prices=True,attributes=True):
        """
        Fetch prices time series and/or attributes for a stock (or anything 
        with a symbol on yahoo finance)
        """
        # Look for the name among the symbols already fetched and does nothing
        # if already retrieved
        symbols = DataLoader.symbols();
        
        if not erase:
            if symbol in symbols:
                return
      
        # If new symbol:
        
        if prices:
            # Fetch and save historical prices
            DataLoader.fetch_historical_prices(symbol,save=True)
        
        if attributes:
            # Fetch attributes and save it in the Attributes folder
            DataLoader.fetch_attributes(symbol,save=True)
        
        # Add the symbol to the list in the Symbols file
        if prices or attributes:
            DataLoader.save_symbol(symbols=symbols,symbol=symbol)
            
    #--------------------------------------------------------------------------
            
    @staticmethod
    def fetch_listOf_stocks(list_of_symbols,erase=False,prices=True,attributes=True):
        """
        Fetch stocks with symbols specified in 'list_of_symbols'
        """
        # To store the symbols we failed to retrieve
        errors_list = {}
        
        for symbol in list_of_symbols:
            print(symbol)
            
            try:
                DataLoader.fetch_stock_data(symbol,erase=erase,prices=prices,attributes=attributes)
                print("--Successfully saved")
            except Exception as e:
                print("-------------------------------")
                print("--Error occured:" + e.message)
                print("-------------------------------")                    
                
                errors_list[symbol] = e.message
                
        return errors_list
        
    #--------------------------------------------------------------------------
   
    @staticmethod
    def fetch_historical_prices(symbol,save=False,source="yahoo"):
        """
        Get historical adjusted close prices from the data provider and save it
        """
        
        prices = webData.DataReader(symbol, source, DataLoader.START_DATE, DataLoader.END_DATE)
        prices = prices['Adj Close']

        prices.name = "Price"
        
        if save: # Save prices in the Prices folder
            DataLoader.save_historical_prices(symbol,prices)
        else:
            return prices

    #--------------------------------------------------------------------------

    @staticmethod
    def fetch_attributes(symbol,save=False):
        """
        Fetch stock's attributes from the web and save it
        """
        
        # Fetch attributes and save it in the 'Attributes' folder
        stock_attributes = StockAttributes.get_stock_attributes(symbol)
        
        if save:
            DataLoader.save_attributes(symbol=symbol,attributes=stock_attributes)
        else:
            return stock_attributes
            
            
    ###########################################################################
    # Functions to fetch interest rates data from the internet
    ###########################################################################
    
    @staticmethod
    def fetch_historical_interest_rates(name,save=False):
        """
        """
        symbols = {"LIBOR ON USD":"USDONTD156N",
                   "LIBOR ON EUR":"EURONTD156N",
                   "LIBOR ON GBP":"GBPONTD156N",
                   "FED FUNDS RATES":"DFF"}        
        
        rates = webData.DataReader(symbols[name], "fred", DataLoader.START_DATE, DataLoader.END_DATE)
        rates.name = name
        
        if save:
            DataLoader.save_historical_interest_rates(name,rates)
        else:
            return rates

    ###########################################################################
    # Functions to save data
    ###########################################################################

    @staticmethod
    def save_historical_prices(symbol,prices):
        """
        """
        path_price =  DataLoader.PATH_PREFIX + "Prices/" + symbol + ".csv"
        prices.to_csv(path=path_price,header=True)    

    #--------------------------------------------------------------------------

    @staticmethod
    def save_historical_interest_rates(name,rates):
        """
        """
        path_rates =  DataLoader.PATH_PREFIX + "Rates/" + name + ".csv"
        rates.to_csv(path_or_buf=path_rates,header=True)


    #--------------------------------------------------------------------------
            
    @staticmethod
    def save_attributes(symbol,attributes):
        """
        """
        path_attr = DataLoader.PATH_PREFIX + "Attributes/" + symbol
        pickle.dump(attributes,open(path_attr,"w"))

    #--------------------------------------------------------------------------

    @staticmethod
    def save_symbol(symbol=None,symbols=None):
        """
        Save a single symbol or a list/set/tuple of symbols in the Symbols file
        (where they are stored as a set object)
        """
        
        s = set(DataLoader.symbols());

        if symbols is not None:
            s = s.union(set(symbols))
 
        if symbol is not None:
            s.add(symbol)
  
        if (symbols is not None) or (symbol is not None):
            pickle.dump(s,open(DataLoader.PATH_PREFIX+"Symbols","w"))
            
    #--------------------------------------------------------------------------
            
    @staticmethod            
    def save_results(results,study_type,results_type,erase=False,params=None):    
        """
        Save results and parameters from a study
        """
        # File for storing the results for a study
        path_results = DataLoader.PATH_PREFIX+"Results/"+study_type+"/"+results_type+"/Results"
        # File for storing the parameters for a study
        path_params = DataLoader.PATH_PREFIX+"Results/"+study_type+"/"+results_type+"/Params"
        
        if os.path.exists(path_results) and not erase:
            raise Exception("Result file already exists for this study")
        else:        
            pickle.dump(results,open(path_results,"w"))
           
        if params is not None:   
            if os.path.exists(path_params) and not erase:
                raise Exception("Result file already exists for this study")
            else:        
                pickle.dump(params,open(path_params,"w"))
            
    ###########################################################################
    # Functions to read data that has already been saved
    ###########################################################################
            
    @staticmethod
    def symbols():
        """
        Return the list of symbols already retrieved
        """
        if os.path.isfile(DataLoader.PATH_PREFIX+"Symbols"):
            symbols = pickle.load(open(DataLoader.PATH_PREFIX+"Symbols","r"))
        else:
            symbols = set()  
            
        return symbols        
            
    #--------------------------------------------------------------------------

    @staticmethod
    def read_symbols_from_file(path):
        """
        Read symbols stored in a file such that there is one symbole per line
        """        
        symbols = []
        
        with open(path,"r") as sym_file:
            for symbol in iter(sym_file):
                symbols.append(symbol[:-1]) # Last character is the newline '\n'
                
        return symbols
        
    #--------------------------------------------------------------------------

    @staticmethod
    def read_prices_attributes(symbol):
        """
        """
        if not symbol in DataLoader.symbols():
            warnings.warn("Symbol not found in list of symbols. ")
        
        prices = pd.read_csv(DataLoader.PATH_PREFIX+"Prices/"+symbol+".csv",index_col=0,parse_dates=True,header=0,squeeze=True)
        attributes =  pickle.load(open(DataLoader.PATH_PREFIX+"Attributes/"+symbol,"r"))       
            
        return prices,attributes
        
    #--------------------------------------------------------------------------

    @staticmethod
    def read_index_components(index_name):
        """
        """
        return DataLoader.read_symbols_from_file(DataLoader.PATH_PREFIX + "Lists of symbols/" + index_name)
    
    #--------------------------------------------------------------------------
    
    @staticmethod
    def read_results(study_type,results_type):
        """
        Returns results,parameters for a given study
        """    
        # Path to the results
        path_results = DataLoader.PATH_PREFIX+"Results/"+study_type+"/"+results_type+"/Results"
        # Path the parameters 
        path_params = DataLoader.PATH_PREFIX+"Results/"+study_type+"/"+results_type+"/Params"
        
        if not os.path.exists(path_results):
            raise Exception("File {} does not exist".format(path_results))
        else:        
            results = pickle.load(open(path_results,"r"))
       
        if not os.path.exists(path_params):
            raise Exception("File {} does not exist".format(path_params))
        else:        
            params = pickle.load(open(path_params,"r"))
            
        return results,params