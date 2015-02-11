# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:03:07 2015

@author: rbanderson

inputs:
predicts = This should be a list of arrays containing the predictions from the submodels
ranges = this should be a list of two-element arrays, each containing the max and min of a range where a certain type of blending should occur
blends = this is a list of three element arrays, one per composition range. 
        The first element in each array is an index into predicts and indicates which prediction to use as the refernece for choosing submodels.
        The second element and third elements are indices into predicts, indicating which two sets of predictions should be blended over the given range.
        If no blending is desired, the second and third elements should both be the prediction that you want to use for the range.

"""
import numpy



def submodels_blend(predicts,ranges,blends):
    blended=numpy.zeros_like(predicts[0])
    for i in range(len(ranges)): #loop over each composition range
        for j in range(len(predicts)): #loop over each spectrum
            if isinstance(blends[i][0],int): #if only one reference prediction is provided, simply check if the spectrum is in range for that prediction
                inrange=(predicts[blends[i][0]][j]>ranges[i][0])&(predicts[blends[i][0]][j]<ranges[i][1])
            if isinstance(blends[i][0],list): #if more than one reference is provided, check if the spectrum is in range for all
                inrange_temp=numpy.array(len(blends[i][0]),dtype='bool')
                for k in blends[i][0]:
                    inrange_temp[k]=(predicts[blends[i][0][k]][j]>ranges[i][0])&(predicts[blends[i][0][k]][j]<ranges[i][1])
                inrange=numpy.all(inrange_temp)
                    
            if inrange: 
                weight1=1-(predicts[blends[i][0]][j]-ranges[0])/(ranges[i][1]-ranges[i][0])
                weight2=(predicts[blends[i][0]][j]-ranges[0])/(ranges[i][1]-ranges[i][0])
                blended[j]=weight1*predicts[blends[i][1]][j]+weight2*predicts[blends[i][2]][j]
    return blended
        








#
#
#
#def submodels_blend2(refpredicts,predicts_A,predicts_B,blendrange):
#    blended=numpy.zeros_like(predicts_A)
#    for i in range(len(blended)):
#        print refpredicts[i]
#        if refpredicts[i]<blendrange[0]:
#            blended[i]=predicts_A[i]
#        else:
#            if refpredicts[i]>blendrange[1]:
#                blended[i]=predicts_B[i]
#            else:
#                A_weight=1-(refpredicts[i]-blendrange[0])/(blendrange[1]-blendrange[0])
#                B_weight=(refpredicts[i]-blendrange[0])/(blendrange[1]-blendrange[0])
#                blended[i]=(A_weight*predicts_A[i]+B_weight*predicts_B[i])
#            
#    return blended
#    
#def submodels_blend3(refpredicts,predicts_A,predicts_B,predicts_C,blendrangeAB,blendrangeBC):
#    blended=numpy.zeros_like(predicts_A)
#    for i in range(len(blended)):
#        print refpredicts[i]
#        if refpredicts[i]<blendrange[0]:
#            blended[i]=predicts_A[i]
#        else:
#            if refpredicts[i]>blendrange[1]:
#                blended[i]=predicts_B[i]
#            else:
#                A_weight=1-(refpredicts[i]-blendrange[0])/(blendrange[1]-blendrange[0])
#                B_weight=(refpredicts[i]-blendrange[0])/(blendrange[1]-blendrange[0])
#                blended[i]=(A_weight*predicts_A[i]+B_weight*predicts_B[i])
#            
#    return blended