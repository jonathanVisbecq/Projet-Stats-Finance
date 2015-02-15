# -*- coding: utf-8 -*-

import pandas as pd

import global_data
from market import Market
from portfolio import Portfolio
from dataloader import DataLoader
from sklearn.decomposition import PCA
from stock_attributes import StockAttributes

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

def get_moments(index_name,start_date,end_date):
    """
    give the expectation and covariance matrix
    
    """
    index = Portfolio.create_index_portfolio(index_name)
    data = Portfolio.agreggate_quotes(index.stocks,start_date,end_date)
    X = np.array(data)
    returns = X[1:,:] / X[:-1,:]
    mean = np.mean(returns, axis=0)
    Y = np.dot((returns - mean).transpose(),(returns - mean))
    return mean,Y/returns.shape[0], returns, X
    
def markowitz_portfolio(mean, cov, lamda, returns,rate=0):
    nb_days = returns.shape[0] 
    nb_stocks = returns.shape[1] 
    a = np.zeros((nb_days,nb_stocks))    
    for k in range(nb_days):
        #print k
        a[k,:] = np.dot(np.dot(np.diag(prices[k,:]),cov**(-1)),mean-rate)/lamda
    return a
    
def get_lambda(mean,rate,cov, sigma):
    X= np.sqrt(((mean-rate)[np.newaxis,:]*(cov**(-1))*(mean-rate)[:,np.newaxis]).sum())
    return X/sigma
def clean_matrix(cov,Q):
    N = cov.shape[0]
    var = np.zeros(N)
    for k in range(N):    
        var[k] = sqrt(cov[k,k])
    corr = cov / (var[:,np.newaxis]*var[np.newaxis,:])
    eigen_values , eigen_vectors = linalg.eigh(corr)
    lamda_plus = 1 + np.sqrt(Q)
    boolean = (eigen_values> lamda_plus)
    Eclean = (boolean[np.newaxis,np.newaxis,:] * eigen_values[np.newaxis,np.newaxis,:] * eigen_vectors[:,np.newaxis,:] * eigen_vectors[np.newaxis,:,:]).sum(axis=2)
    corr_clean = Eclean + (N-(boolean*eigen_values).sum()) * np.identity(N)
    cov_clean = corr_clean * (var[:,np.newaxis]*var[np.newaxis,:])
    return cov_clean, corr, corr_clean

def get_gain(a,rate,investment,prices,again = 0):
    nb_days = a.shape[0]
    nb_stocks = a.shape[1] 
    initial_wealth = investment
    gain = np.zeros((nb_days))    
    for k in range(nb_days):
        a_0 = initial_wealth - (a[k,:]*prices[k,:]).sum()
        gain[k] = (a[k,:]*prices[k+1,:]).sum() + (1+rate) * a_0
        if again == 0:
            initial_wealth = gain[k]
    return gain
    
if __name__=="__main__":
    
    index_name = "CAC40"
    start_date = "2014-01-01"
    end_date = "2014-12-31"
    mean, cov , returns, prices = get_moments(index_name,start_date,end_date)
    cov_clean, corr, corr_clean = clean_matrix(cov,prices.shape[1]*1./prices.shape[0])
    sigma = 0.01
    lamda = get_lambda(mean,0,cov_clean, sigma)
    a = markowitz_portfolio(mean, cov_clean, lamda, returns,0)