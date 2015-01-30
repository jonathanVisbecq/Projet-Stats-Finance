# -*- coding: utf-8 -*-

import pandas as pd

import global_data
from market import Market
from portfolio import Portfolio
from risk_free_rate import RiskFreeRate
from dataloader import DataLoader

def align_series(stock_prices,index,rates,start_date,end_date):
    """
    Return series (stock prices, index, rfr) aligned with respect to stocks
    start_date and end_date must be consistent with the actual timstamps
    
    Stocks are assumed to be already aligned with each other
    """
    
    # Select data between start_date and end_date, assuming these are
    # consitent dates for the records
    stock_prices = stock_prices[start_date:end_date]
    index = index[start_date:end_date]
    rates = rates[start_date:end_date]
    
    # Missing values are dealt with by forward propagation, after they have
    # been aligned on the first stock series
    _,index = stock_prices[stock_prices.columns[0]].align(index,join='left')
    index = index.fillna(method='ffill')
    _,rates = stock_prices[stock_prices.columns[0]].align(rates,join='left')
    rates = rates.fillna(method='ffill')
        
    # Remaining NaN (first ones) are dealt with using backward propagation
    index = index.fillna(method='bfill')
    rates = rates.fillna(method='bfill')
    
    return stock_prices,index,rates
    

def capm_betas(pr,mr):
    """
    Compute the beta(s) & alpha(s) for all provided stocks using pandas' ols method
    
    /!\ Totally un-optimized 
    """ 
    betas = {}
    alphas = {}
    models = {}
    for stock,stock_prices in pr.iteritems():
         model = pd.ols(y=stock_prices,x={'Index':mr})
         models[stock],betas[stock],alphas[stock] = model,model.beta['Index'],model.beta['intercept']
             
    return models,betas,alphas
    

if __name__=="__main__":
    
    # To store the parameters
    params = {}
    
    ## Acquisition of the data
    params["index_name"] = "SP500"
    params["min_nb_returns_stocks"] = 5000

    market = Market.create_index_market(params["index_name"])
    rates = RiskFreeRate.create_rates(global_data.default_rates[global_data.index_currency[params["index_name"]]])
    portfolio = Portfolio.create_index_portfolio(params["index_name"])
    
    stocks = portfolio.stocks_with_data(nb_returns=params["min_nb_returns_stocks"])
    quotes = Portfolio.agreggate_quotes(stocks.stocks,start_date=stocks.start_dates[-1])
    
    # Determine first date
    params["start_date"] = max(stocks.start_dates[-1].date(),rates.get_first_date(),market.get_first_date())
    params["end_date"] = DataLoader.END_DATE

    # Align series
    p,m,r = align_series(stock_prices=quotes,
                         index=market.market_index,
                         rates=rates.risk_free_rate,
                         start_date=params["start_date"],
                         end_date=params["end_date"])
    
    # Lag rates by one day (for day t, the rate is that offered at t-1)
    # and convert to relative change
    r = r.shift(periods=1) / 100.
    
    # Convert to percent change with the previous day and substract risk free rate
    pr = p.pct_change()[1:].sub(r,axis=0)
    mr = m.pct_change()[1:].sub(r,axis=0)

    ## Compute betas,alphas
    models,betas,alphas =capm_betas(pr,mr)
    
    # Real number of observations used
    params["nb_returns"] = models[models.keys()[0]].nobs
    
    ## Saving the data
    m_sum = dict([(key,val.summary_as_matrix) for key,val in models.iteritems()])
    
    DataLoader.save_results(results=m_sum,
                   study_type="CAPM",
                   results_type="Regression",
                   erase=True,
                   params=params)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    