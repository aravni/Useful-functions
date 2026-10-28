#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for finding roots of functions.
"""

__author__ = "Aljaž Ravnikar"
__date__ = "15.11.2024"

import numpy as np

def secant(fun, x0, x1, N=10, tol=1e-3):
    """Secant method for finding roots of a function."""
    x_n = x0
    x_new= x1
    xtol = 1
    i=0
    x = np.zeros(N+2)
    koef=np.zeros(N)
    x[0]=x0
    x[1]=x1
    while i < N and xtol > tol:
        x_old=x_n
        x_n=x_new
        f_old=fun(x_old)
        f_n=fun(x_n)

        k = (f_n-f_old) / (x_n-x_old) #sekantna
        #k = df/dx #newtonova -> odvod!
        x_new = x_n - 1/k*f_n

        #če nas zanima le ničla je to nepotrebno!
        x[i+2] = x_new
        koef[i]= k

        xtol = abs(x_n-x_new)
        i+=1
    if xtol < tol:
        x=np.trim_zeros(x)
        koef=np.trim_zeros(koef)
        print(f'Tolerance xtol = {xtol:1E} reached in N = {i} iterations.')
    return x_new, x, koef

def bisect(fun, x1,x2, i,Nmax, roots, interval=False):
    """Bisection method for finding roots of a function."""
    if i<Nmax:
        i+=1
        x3=(x1+x2)/2 #razpolovimo
        f1=fun(x1)
        f2=fun(x2)
        f3=fun(x3)
        if ((f3<0 and f1>0) or (f3>0 and f1<0)):
            bisect(fun,x1,x3, i,Nmax, roots, interval)
        if ((f3<0 and f2>0) or (f3>0 and f2<0)):
            bisect(fun,x3,x2, i,Nmax, roots, interval)
    else:
        if interval: roots.append([x1,x2]) # interval ničle
        else: roots.append((x1+x2)/2) #nova ocena ničle

def incr(fun, xmin,xmax, N, roots=[]):
    """Incremental method for finding roots of a function."""
    x = np.linspace(xmin,xmax,N)
    for i in range(N-1):
        x1 = x[i]
        x2 = x[i+1]
        f1 = fun(x1)
        f2 = fun(x2)
        if (f1<0 and f2>0) or (f1>0 and f2<0): roots.append([x1,x2])
    return roots

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.style.use('aljaz')
    a=np.linspace(0,1,11)
    print(a[:len(a)//2-1:-1],a[:len(a)//2+1], a)

    def f(x):
        return np.log(x)
        # return x**3

    x=np.linspace(0.001,1,500)
    y=f(x)

    f0, xs, k = secant(f, x0=0.1, x1=0.2, N=100, tol=1e-3)

    plt.plot(f0, f(f0),'o')
    plt.plot(x,y)
    plt.plot(xs, f(xs), '.')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.title(f'$N={len(k)}$')
    plt.show()

    # sekantna
    for i in range(len(k)):
        plt.clf()
        plt.plot(x,y,'b-')
        plt.plot(xs[i],f(xs[i]),'k.')
        plt.plot(xs[i+1],f(xs[i+1]), 'k.')
        plt.plot(xs[i+2],f(xs[i+2]), 'kx', markersize=10)

        xmin=min([xs[i],xs[i+1],xs[i+2]])*0.9
        xmax=max([xs[i],xs[i+1],xs[i+2]])*1.1
        xi = np.linspace(xmin,xmax,100)
        yi = k[i]*xi + (f(xs[i]) - k[i]*xs[i])
        plt.plot(xi, yi, 'r-', lw=0.7)
        plt.vlines(xs[i+2], ymin=0, ymax=f(xs[i+2]), color='k',ls='--',lw=0.7)

        plt.axhline(0,c='gray',ls='-',lw=0.9)
        plt.axvline(0,c='gray',ls='-',lw=0.9)
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.title(f'$i={i+1}$')
        plt.show()