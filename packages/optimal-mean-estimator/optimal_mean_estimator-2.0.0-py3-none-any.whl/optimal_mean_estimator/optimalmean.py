#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Jun  9 01:35:07 2024

@author: Bennjamin Schulz

Copyright (c) <2024> <Benjamin Schulz>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to 
use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software,and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:
    
The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.


This module is a python implementation of the optimal subgaussian mean estimator
from

J. C. H. Lee and P. Valiant, "Optimal Sub-Gaussian Mean Estimation in  R" 
2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS),
Denver, CO, USA, 2022, pp. 672-683, doi: 10.1109/FOCS52979.2021.00071.
https://arxiv.org/abs/2011.08384




The implementation consists of a function mean that computes
the optimal mean estimator for numpy arrays.
it expects a numpy array a, a confidence parameter delta and its other 
arguments match the behavior of the numpy.mean function whose documentation is
given here:
https://numpy.org/doc/stable/reference/generated/numpy.mean.html

The computed mean estimator is by default a numpy f64 value if the array is of
integer type. Otherwise, the result is of the same type as the array, which is 
also similar as the numpy mean function.

The estimator is computed to fulfill the equation 

P(|mu-mean|<epsilon)>=1-delta

by default, delta=0.05.

The module also has a function 

mean_flattened

This function works in the same way as optimal_mean_estimator, but it works
only for flattened arrays, and it also has no optional out parameter

"""

import numpy as np
import scipy 
import math
def mean (a,delta=0.01, axis=None,dtype=None,out=None,keepdims=False,where=None, skewness_tolerance=0.988,correctionfactor=None,bagnumber=None, trimarray_if_prime_elements=False):
    """
    Computes the optimal mean estimator of
    
    J. C. H. Lee and P. Valiant, "Optimal Sub-Gaussian Mean Estimation in  R" 
    2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS),
    Denver, CO, USA, 2022, pp. 672-683, doi: 10.1109/FOCS52979.2021.00071.
    https://arxiv.org/abs/2011.08384
    
    
    for numpy arrays.
    
    #Args:
        a: A numpy array whose mean is computed. can by of integer, floating or 
        complex type and have arbitrary axes.
        
        delta: a float value. The computed estimator fulfills
                P(|mu-mean|<epsilon)>=1-delta. The default is 0.001. Note that
                the size of the sample must be larger than ln(1/delta).
        
        axis:  a tuple defining the axes over which the mean is to be computed,
               default isnone
        
        dtype:  numpy type of the computed result. Per default, if a is an 
                integer array, a numpy.f64 is returned, otherwise, unless 
                specified explicitly, the default return is of the same type 
                as the array a.
                Note that if an int type is specified, float64 values are used
                during the computation in order to increase precision.
        
        out:    a numpy array that stores the means.
                If the result is a matrix out must have the same shape
                as the computed result. If the result is a single mean value, the
                output is stored in out[0].
                
        keepdims:   boolean, the default is false. If  set to True, the reduced axes 
                are left in the result as dimensions with size one and the 
                result broadcasts against the input array.
        where:  a boolean numpy array. Elements set to false are discarded from the
                computation
        skewness_tolerance:     a float value, per default 0.988. This is the maximum skewness, 
                    in terms of the adjusted Fisher-Pearson standardized moment coefficient,
                    where the optimized mean is computed. If the absolute value of the skewness
                    of the array exceeds that, then the ordinary mean is returned.
        correctionfactor: a float, per default None. If it is None, then the correctionfactor 
                    is given by 1/3*ln(1/bagnumber)
        bagnumber:      a signed int that should be smaller or equal than the size of a.
                    if it is none, then the bagnumber is given by ln(1/delta)
                    if the element number of a is such that it can not by divided equally into bagnumber bags
                    then the bagnumber used is given by the next largest divisor of the number of elemewnts of a
        trimarray_if_prime_elements:    a boolean, default is false. If it is true, then if a has n elements,
                    and n is prime, a random element is removed from a before the bagnumber is computed. Otherwise,
                    the bagnumber will be the number of elements in the array, which leads to slower computations.                 
            
        
    Returns:
        The computed mean estimator is by default a numpy f64 value if the array is of
        integer type. Otherwise, the result is of the same type as the array, which is 
        also similar as the numpy mean function.

        The estimator is computed to fulfill the equation 

        P(|mu-mean|<epsilon)>=1-delta
    """
    
    """possible type cast for out"""
   
    if dtype is None:
        if np.issubdtype(a.dtype, np.integer): 
            ddtype=np.float64  
        else:
            ddtype=a.dtype       
    else:
        ddtype=dtype
    if out is not None:  out.astype(ddtype)
        
    """if no axes are selected and dims should not be kept,
       then flatten the arraysand compute the mean with respect to the mask where.
       fill the first index of out with the result and return the result too
       if dims should be kept, then set a tuple over all axes explicitely"""
    if axis is None:
        if keepdims==False:  
            if where is not None:                  
                newmean=mean_flattened(a,delta,ddtype,where=where,skewness_tolerance=skewness_tolerance,
                                       correctionfactor=correctionfactor,bagnumber=bagnumber, trimarray_if_prime_elements=trimarray_if_prime_elements)
            else:
                newmean=mean_flattened(a,delta,ddtype,skewness_tolerance=skewness_tolerance,
                                       correctionfactor=correctionfactor,bagnumber=bagnumber, trimarray_if_prime_elements=trimarray_if_prime_elements)
                
            if out is not None:
                out[0]=newmean
            return newmean   
        else:
            axis=tuple(t for t in range(len(a.shape)))
    """create lists of axes for the output array and an axis list from which an index
        is computed that contains the groups over which the mean is calculated.
       this varies for a different keepdims parameter"""        
    newarray=a
    if where is not None:
        newh=where  
     
    shape1list=list(a.shape)
    if keepdims==True:
        shape2list=list(a.shape)
        shape3list=list(a.shape)

            
    for index in sorted(axis,reverse=True):
        newarray=np.moveaxis(newarray,index,-1)
        
        if where is not None: newh=np.moveaxis(newh,index,-1) 
            
        del shape1list[index]   
        
        if keepdims==True:
            shape2list[index]=1
            shape3list[index]=-1
                     
    if keepdims==True: 
        newmean=np.empty(tuple(shape2list),ddtype)  
    else: 
        newmean=np.empty(tuple(shape1list),ddtype)
            
    """with the axes lists one can now create and iterate over indices lists for 
    the result and the    groups over which the mean is computed. 
    This varies for different values of keepdims"""
    for index in np.ndindex(tuple(shape1list)): 
        index2=()
        if keepdims==True: 
            count=0
            for x in shape3list:
                if x==-1: index2+=(0,)
                else:
                    index2=index2+(index[count],)
                    count=count+1
        else:
            index2=index
            
        if where is not None:                   
            newmean[index2]=mean_flattened(newarray[index],delta,dtype=ddtype,where=newh[index],skewness_tolerance=skewness_tolerance,
                                           correctionfactor=correctionfactor,bagnumber=bagnumber, trimarray_if_prime_elements=trimarray_if_prime_elements)
        else:
            newmean[index2]=mean_flattened(newarray[index],delta,dtype=ddtype,skewness_tolerance=skewness_tolerance,
                                           correctionfactor=correctionfactor,bagnumber=bagnumber, trimarray_if_prime_elements=trimarray_if_prime_elements)
    """finally, one can fill the out parameter if not none, and also return the result"""       
    if out is not None:
        for x in np.ndindex(newmean.shape):
            out[x]=newmean[x]
                
    return newmean
        


def _f(alpha, mhelpersq, onethirdloginv):  
    """ computes a helper function whose roots are solved in the mean
        estimator function
        Args:
            alpha: a float,
            mhelpersq: a numpy array
            onethirdloginv: a float
        Returns:
            the float corresponding to
            sum_i  min(alpha*mhelpersq_i, 1)- 1/3 log(1/delta),
            (with the subtracted value given as onethirdloginv)
    """
    array1=alpha*mhelpersq
    array1[array1 > 1.0] = 1.0
    return np.sum(array1)-onethirdloginv



def is_prime(n):
  for i in range(2,int(math.sqrt(n))+1):
    if (n%i) == 0:
      return False
  return True




def mean_flattened(a, delta=0.01,dtype=None,where=None,skewness_tolerance=0.988,correctionfactor=None,bagnumber=None, trimarray_if_prime_elements=False):
    """
    Computes the optimal mean estimator of
    
    J. C. H. Lee and P. Valiant, "Optimal Sub-Gaussian Mean Estimation in  R" 
    2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS),
    Denver, CO, USA, 2022, pp. 672-683, doi: 10.1109/FOCS52979.2021.00071.
    https://arxiv.org/abs/2011.08384
    
    
    for flattened numpy arrays with one axis.
    
    Args:
        a: A numpy array whose mean is computed. can by of integer, floating or 
        complex type and have arbitrary axes.
        
        delta: a float value. per default=0.01. The computed estimator fulfills
                P(|mu-mean|<epsilon)>=1-delta
        
       
        dtype:  numpy type of the computed result. Per default, if a is an 
                integer array, a numpy.f64 is returned, otherwise, unless 
                specified explicitly, the default return is of the same type 
                as the array a.
                Note that if an int type is specified, float64 values are used
                during the computation in order to increase precision.
        
        where: a boolean numpy array. Elements set to false are discarded from the
                computation
        skewness_tolerance: a float value, per default 0.988. This is the maximum skewness, 
                in terms of the adjusted Fisher-Pearson standardized moment coefficient,
                where the optimized mean is computed. If the absolute value of the skewness
                of the array exceeds that, then the ordinary mean is returned.
        correctionfactor: a float, per default None. If it is None, then the correctionfactor 
                is given by 1/3*ln(1/bagnumber)
        bagnumber: a signed int that should be smaller or equal than the size of a.
                if it is none, then the bagnumber is given by ln(1/delta)
                if the element number of a is such that it can not by divided equally into bagnumber bags
                then the bagnumber used is given by the next largest divisor of the number of elemewnts of a
        trimarray_if_prime_elements: a boolean, default is false. If it is true, then if a has n elements,
                and n is prime, a random element is removed from a before the bagnumber is computed. Otherwise,
                the bagnumber will be the number of elements in the array, which leads to slower computations.                 
        
    
    Returns:
        The computed mean estimator is by default a numpy f64 value if the array is of
        integer type. Otherwise, the result is of the same type as the array, which is 
        also similar as the numpy mean function.

        The estimator is computed to fulfill the equation 

        P(|mu-mean|<epsilon)>=1-delta
    """
    
    """We apply the mask if given"""
    
    x_filtered=a.flatten()
    
    if where is not None:
        where=where.flatten()     
        x_filtered=x_filtered[where]
     
    
    
    """cast and return the final result to the desired datatype.
    If no type was specified and the array is an integer,
    cast the result to a float64,  otherwise if no type was specified, set it
    as the type of the supplied array, or, if an output type was set, set the array type
    to this value"""
     
    ddtype=np.float64
     
    if dtype is None:
      if np.issubdtype(x_filtered.dtype, np.integer): 
          ddtype=np.float64  
      else:
          ddtype=x_filtered.dtype 
    else:
       ddtype=dtype
     
        
    """if the array has just one element, then return that in the right type"""
    if x_filtered.size==1:
        return np.array(x_filtered,dtype=ddtype)[0]
    

    
    
    """if the correction factor was not set for the distribution and if the skewness of the input array
    is larger than the given skewtolerance return the ordinary mean"""

    if correctionfactor is None: 
        if np.abs(scipy.stats.skew(x_filtered))>skewness_tolerance: 
           return np.mean(x_filtered,dtype=ddtype)
         
       
         
    """compute the number of bags as in https://arxiv.org/abs/2011.08384 or 
    get it from a specified parameter"""
    if bagnumber is None:
        n_bags=int(np.emath.log(1.0/abs(delta)))
    else:
        n_bags=bagnumber
   
    
    """if there is just one bag, return the ordinary mean"""
    if n_bags<=1: 
        return np.mean(x_filtered,dtype=ddtype)
        
        
    """ if the values were integers, store the intermediate values for the means and corrections
         as float64. if the values were some other format, use this format to store the means. Note that
         the specified argument dtype has no effect on these intermediate values"""
         
    if np.issubdtype(x_filtered.dtype, np.integer): 
        ddtype1=np.float64 
    else:
        ddtype1=x_filtered.dtype
            
        
    """if the number of elements is prime, then if one should not trim the array, use one bag for every element. 
           The alternative is be to trim the data and remove one random value"""
    if is_prime(x_filtered.size):
        if trimarray_if_prime_elements:
            random_index = np.random.randint(0, x_filtered.size)
            x_filtered = np.delete(x_filtered, random_index)           
        else:
            n_bags = x_filtered.size
       
            
    """if the number of bags is larger or equal than the array size, set it to the array size """
    if n_bags > x_filtered.size: 
        n_bags=x_filtered.size

    """set the number of bags such that the elements can at least be evenly distributed
           i.e. one has the same number of elements in each bag"""
    while(x_filtered.size % n_bags!=0):
        n_bags=n_bags+1
               
          
    """compute the median of means in the different, randomly shuffled bags. note that the mean
    is computed with numpy default datatypes, even if int was specified. The type cast is done after the 
    computation"""
    means=np.zeros(n_bags,dtype=ddtype1)    
    ind =  np.tile(np.arange(n_bags), int(x_filtered.size / n_bags))
    np.random.shuffle(ind)
    for bag in range(n_bags):
        means[bag] =np.mean(x_filtered.take(np.where(ind == bag)),dtype=ddtype1) 
       
    medianofmeans=np.median(means)

       
    """if correctionfactor is not specified, set it to 1/3*ln(1/delta), as in 
    https://arxiv.org/abs/2011.08384"""
    
    
    if correctionfactor is None:
        loginvdelta=np.float64(n_bags)
        onethirdloginv=np.float64(loginvdelta/3.0)
    else:
        onethirdloginv=correctionfactor
    
    mhelper=x_filtered-medianofmeans
    mhelpersq=mhelper*mhelper    
    
    """now solve the equation sum_i min(alpha*mhelpersq_i, 1)-correctionfactor=0,
    we use brentq as it is very fast. This solver needs an interval. The border
    where f is smaller than zero is obviously 0, 
    and f gets larger than 0 for alpha
    if there are  1/3 log(1/delta) elements of alpha*mhelpersq_i larger or equal than 1.
    if N is the number of elements in mhelpersq_i and if we set the right border of 
    alpha to 1/ (minimum of mhelpersq_i), then there are
    N elements of alpha*mhelpersq_i larger than 1 and  1/3 log(1/delta) is smaller than N because it is
    ln(N) number of bags which is smaller than N. For simplicity, find the smallest non zero value of mhelpersq_i."""
    
    
    """if the array contains so many zeros that the equation can not be solved, return the
    ordinary mean (the equation has no solutions then)"""
    nonzerosq=mhelpersq[np.nonzero(mhelpersq)]
    if nonzerosq.size<int(onethirdloginv):
        return np.mean(x_filtered,dtype=ddtype)
            
   
    rightinterval=1.0/np.min(nonzerosq)

     
    alpha=scipy.optimize.brentq(_f,a=0.0,b=rightinterval,args=(mhelpersq,onethirdloginv))
   
    
    #compute the correction and add it to the median of means and return the result
    mhelper2=alpha*mhelpersq
    mhelper2[mhelper2 > 1.0] = 1.0
    
    
    mean=np.array([medianofmeans + 1.0/(x_filtered.size) * np.sum(mhelper* (1.0 -  mhelper2))],dtype=ddtype)

    return mean[0]
