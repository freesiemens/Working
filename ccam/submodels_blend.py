# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 16:03:07 2015

@author: rbanderson

inputs:
predicts = This should be a list of arrays containing the predictions from the submodels
ranges = this should be a list of two-element arrays, each containing the max and min of a range where a certain type of blending should occur
inrange = This is a list of index arrays indicating the predictions that must fall within each desired range. If an array in this list has more than one element, then
    for each spectrum, all of the predictions indicated must be in the range for a value to be assigned to the blended output for that spectrum.
refpredict = list of indices indicating which of the predicts should be used to determine the weighting when blending.
toblend = List of two-element arrays indicating the two sets of predictions to be blended in a given composition range.

blends = this is a list of three element arrays, one per composition range. 
        The first element in each array is an index into predicts and indicates which prediction to use as the refernece for choosing submodels.
        The second element and third elements are indices into predicts, indicating which two sets of predictions should be blended over the given range.
        If no blending is desired, the second and third elements should both be the prediction that you want to use for the range.

"""
import numpy



def submodels_blend(predicts,ranges,inrange,refpredict,toblend):
    blended=numpy.zeros_like(predicts[0])
    for i in range(len(ranges)): #loop over each composition range
        for j in range(len(predicts[0])): #loop over each spectrum

            if isinstance(inrange[i],int): #if only one reference prediction is provided, simply check if the spectrum is in range for that prediction
                inrangecheck=(predicts[inrange[i]][j]>ranges[i][0])&(predicts[inrange[i]][j]<ranges[i][1])
            if isinstance(inrange[i],list): #if more than one reference is provided, check if the spectrum is in range for all
                inrange_temp=numpy.zeros(len(inrange[i]),dtype='bool')
                for k in range(len(inrange[i])):
                    inrange_temp[k]=(predicts[inrange[i][k]][j]>ranges[i][0])&(predicts[inrange[i][k]][j]<ranges[i][1])
                inrangecheck=numpy.all(inrange_temp)
                    
            if inrangecheck: 
                weight1=1-(predicts[refpredict[i]][j]-ranges[i][0])/(ranges[i][1]-ranges[i][0])
                weight2=(predicts[refpredict[i]][j]-ranges[i][0])/(ranges[i][1]-ranges[i][0])
                blended[j]=weight1*predicts[toblend[i][0]][j]+weight2*predicts[toblend[i][1]][j]

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