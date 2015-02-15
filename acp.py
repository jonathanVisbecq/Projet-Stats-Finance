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


def plot_eigenValues(eigen_values,nb=None):
    """
    Make an historam out of the 'nb' first eigenvalues from the PCA
    
    """
    # Sort the eigenvalues
    eigen_values = sp.sort(eigen_values)
    
    # Keep only the first eigenvalues
    if nb is not None:
        eigen_values = eigen_values[0:nb]
    
    # Plot the bars histogram
    plt.bar(left=eigen_values,
            height=np.ones(len(eigen_values)),
            width=0)
    
    plt.xlabel("Eigenvalues",
               fontsize="large")

def acp_factors(index_name,start_date,end_date):
    """
    makes an acp over a given index between start_date and end_date 
    returns the eigen values and eigen vectors
    
    """
    
    #create the portfolio
    index = Portfolio.create_index_portfolio(index_name)
    data = Portfolio.agreggate_quotes(index.stocks,start_date,end_date)
    pca = PCA(n_components=40)
    X = np.array(data)
    #X = as_float_array(X, copy=self.copy)
    # Center data
    mean = np.mean(X, axis=0)
    Y = abs(X - mean)**2
    std = np.sqrt(np.mean(Y,axis = 0))
    X -= mean
    X = X / std
    transformed_data = pca.fit(X).transform(X)
    eigenValues = pca.explained_variance_
    eigenVectors = pca.components_
    
    return eigenValues, eigenVectors, transformed_data, mean

def get_attributes(index_name):
    index = Portfolio.create_index_portfolio(index_name)
    l= [];
    for stock in index.stocks:
        l.append(DataLoader.read_attributes(stock))
    return l

def get_sectors(lis):
    l=[];
    for stock in lis:
        l.append(stock.sector)
    return list(set(l)) 
    
def divid_sectors(lis,vector,n):
    N = vector.size
    sectors = get_sectors(lis)
    nb_sectors = len(sectors)
    l = [[] for k in range(nb_sectors)]
    for k in range(n):
        ind = sectors.index(lis[k].sector)
        l[ind].append(vector[k])
    return l

def divid_stocks(lis,transformed_data):
    N = len(transformed_data)
    sectors = get_sectors(lis)
    nb_sectors = len(sectors)
    l = [[] for k in range(nb_sectors)]
    for k in range(N):
        ind = sectors.index(lis[k].sector)
        l[ind].append(transformed_data[k])
    return l

if __name__=="__main__":
    
    index_name = "DJIA"
    result = acp_factors(index_name,"2014-01-01","2014-12-31")
    eigen_values = result[0]
    transformed_data = result[2]
    plot_eigenValues(eigen_values,nb=500)
    plt.plot(transformed_data[:,0],np.zeros(transformed_data[:,0].size),"ro")
    print transformed_data
    n = 10
    lis = get_attributes(index_name)
    
    