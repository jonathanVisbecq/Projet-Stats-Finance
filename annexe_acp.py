# -*- coding: utf-8 -*-

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
    
    
    
    
    
if __name__=="__main__":
    
    eigen_values = [0.2,0.3,0.5,0.55,0.6,0.9]
    
    plot_eigenValues(eigen_values,nb=5)
    
