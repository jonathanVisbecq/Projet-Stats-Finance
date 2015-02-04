# -*- coding: utf-8 -*-

import urllib2
import simplejson

class StockAttributes:
    
    def __init__(self,name="",symbol="",currency="",sector="",industry="",shares_outstanding=0,float_shares=0,start_date=""):
        # - name of the company without qualifiers (Inc., Ltd., SA, ...)
        self.name = name        
        # - listed symbol of the stock
        self.symbol = symbol        
        # - currency used for the price series
        self.currency = currency
        # - sector (arbitrarily defined or from the data provider)
        self.sector = sector
        # - industry (arbitrarily defined or from the data provider)
        self.industry = industry
        # - number of shares outstanding
        self.shares_outstanding = shares_outstanding
        # - float shares
        self.float_shares = float_shares
        # - first date issuing stocks
        self.start_date = start_date
        
    def print_info(self):
        print("-------------------------------------------------------------")
        print("Name")
        print("    " + self.name)
        print("Symbol")
        print("    " + self.symbol)
        print("Currency")
        print("    " + self.currency)
        print("Sector")
        print("    " + self.sector)
        print("Industry")
        print("    " + self.industry)
        print("Shares outstanding")
        print("    " + self.shares_outstanding)          
        print("Float shares")
        print("    " + self.float_shares)
        print("Starting date")
        print("    " + self.start_date)
        print("-------------------------------------------------------------")
    
    
    
    @staticmethod
    def get_stock_attributes(symbol):
        # Get name, currency
        url_prefix = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%3D\'"
        url_suffix = "\'%0A%09%09&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
        url_str =  url_prefix + symbol + url_suffix
        
        json = urllib2.urlopen(url_str).read()
        data = simplejson.loads(json)

        name = data["query"]["results"]["quote"]["Name"]
        currency = data["query"]["results"]["quote"]["Currency"]
        
        # Get sector, industry, start_date        
        url_prefix = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.stocks%20where%20symbol%3D%22"
        url_suffix = "%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
        url_str = url_prefix + symbol + url_suffix
        
        json = urllib2.urlopen(url_str).read()
        stock_info = simplejson.loads(json)
        
        if stock_info['query']['results']['stock'].has_key("Sector"):    
            sector = stock_info['query']['results']['stock']["Sector"]
        else:
            print("--Sector missing")
            sector = " "
            
        if stock_info['query']['results']['stock'].has_key("Industry"):
            industry = stock_info['query']['results']['stock']["Industry"]
        else:
            print("--Industry missing")
            industry = " "

        if stock_info['query']['results']['stock'].has_key("start"):    
            start_date = stock_info['query']['results']['stock']["start"]
        else:
            print("--Starting date missing")
            start_date = " "
        
        # Number of shares outstanding    
        url_prefix = "http://finance.yahoo.com/d/quotes.csv?s="
        url_suffix = "&f=j2"
        urlStr =  url_prefix + symbol + url_suffix

        result = urllib2.urlopen(urlStr).read()
        
        if len(result)>4:
            shares_outstanding = result[:-2]
        else:
            raise RuntimeError("Shares outstanding missing")
            
        # Float shares 
        url_prefix = "http://finance.yahoo.com/d/quotes.csv?s="
        url_suffix = "&f=f6"
        urlStr =  url_prefix + symbol + url_suffix

        result = urllib2.urlopen(urlStr).read()
        
        if len(result)>4:
            float_shares = result[:-2]
        else:
            raise RuntimeError("Float shares missing")
            
            
        return StockAttributes(name=name,symbol=symbol,currency=currency,sector=sector,industry=industry,shares_outstanding=shares_outstanding,float_shares=float_shares,start_date=start_date)