# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 13:05:50 2014

@author: rbanderson
"""
def inst_response(uvwave,viswave,vnirwave,uv,vis,vnir,distt=1600,gainfile='llgain_info.sav'):
    from scipy.io.idl import readsav
    import math
    import numpy
    gain=readsav(gainfile,python_dict=True)
    uvgain=gain['alluvdata'][50:2097]
    visgain=gain['allvisdata'][50:2097]
    vnirgain=gain['allvnirdata'][50:2097]
    
    s=uv.shape
    for i in range(s[0]):
        dn=vnir[i,:]
        vnir[i,:]=dn*vnirgain*(distt/(math.pi*54.2*0.1))^2/(numpy.append([vnirwave[1:]],[vnirwave[-1]])-vnirwave)
        vis[i,:]=dn*visgain*(distt/(math.pi*54.2*0.1))^2/(numpy.append([viswave[1:]],[viswave[-1]])-viswave)
        uv[i,:]=dn*uvgain*(distt/(math.pi*54.2*0.1))^2/(numpy.append([uvwave[1:]],[uvwave[-1]])-uvwave)
    return uv,vis,vnir
            
            
            
