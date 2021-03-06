# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:17:56 2017

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
import lightprobe

probe = lightprobe.load("data/uffizi.png");

# point on sphere to r3 room
def s2tor3( omega) :
    r3 = np.zeros( 3)
    r3[0] = np.sin( omega[0]) * np.cos( omega[1])
    r3[1] = np.sin( omega[0]) * np.sin( omega[1])
    r3[2] = np.cos( omega[0])
    return r3

# points on sphere to r3
def s2tor3array( omega) :
    r3 = np.zeros( [omega.shape[0], 3])
    r3[:,0] = np.sin( omega[:,0]) * np.cos( omega[:,1])
    r3[:,1] = np.sin( omega[:,0]) * np.sin( omega[:,1])
    r3[:,2] = np.cos( omega[:,0])
    return r3
                       
def getCosineDistributedPointH2() :
    #see course notes for where this formula comes from    
    omega = np.random.rand(2)
    omega[0] = np.arcsin(np.sqrt(omega[0]))
    omega[1] *= 2*np.pi
    return omega

def Phong(wi, wo, normal, alpha = 30):
    #lightin = -s2tor3(wi)
    lightout = s2tor3(wo)
    #normalvec = s2tor3(normal)
    #lightin, lightout, normal are all normalized direction vectors
    #lightreflectance = lightin - 2*np.dot(lightin, normalvec)*normalvec
    lightreflectance = s2tor3(wi + [0.0, np.pi]) # just rotate ingoing 180 degree
    phong = np.power(np.dot(lightreflectance, lightout), alpha)
    return  phong * (alpha+1)/(2*np.pi)

def cosineImportanceSampling(Ns, K, roh, lightout, normal, alpha):
    #want to compute integral for different numbers N of sample points
    integrals = np.zeros([Ns.size, K])
    errors = np.zeros(Ns.size)
    varis = np.zeros([Ns.size])              
    for idx in range(Ns.size):
        N = Ns[idx]
        #variance definition = mean(abs(x - x.mean())**2)
        variance = 0
        #compute K time the integral with N random cosine distributed points via monte carlo
        for j in range(K):
            omega = np.array([getCosineDistributedPointH2() for i in range(N)])
            integrals[idx, j] = np.sum(roh(omega[i, :], lightout, normal, alpha) * lightprobe.value(probe, omega[i,:])*np.max([0.0, np.cos(omega[i, 0])])/(np.max([0.0, np.cos(omega[i, 0])])/np.pi) for i in range(N))
        integrals[idx, :] *= 1/N
        #get mean error for all integrals in K
        errors[idx] = np.sum(integrals[idx, :] - 492.3)/K
        #compute variance for the K integrals
        variance = np.var(integrals[idx,:])
        varis[idx] = variance
        print("var = ", variance)
    return [integrals, varis, errors]

#try for multiple degree in theta
for i in range(np.int32(90/15) + 1):
    integrals = cosineImportanceSampling(np.array([2**15]), 10, Phong, np.array([i/12 * np.pi, 0]), np.array([0, 0]), 31)[0]
    print("for lightout ",i * 15, " degree in theta: ",np.mean(integrals))

















