#-----------------#
# Written by Campbell Watson, IBM Research, Yorktown Heghts, NY, USA
# July 2 2019
#-----------------#

import numpy as np
from scipy.ndimage.interpolation import shift
from scipy.ndimage import convolve
import copy


# ------------HOW TO USE--------------
# Read in a 2D Precipitation Array
# Modify 2D array so that: 
#   Wet cells (with precip) = 0
#   Dry cells (without precip) = 1
#
# The output of this program is a 2D array with the same dimensions as the input file. Values in the 
# array indicate the number of grid cells to the closest wet cell

# We search for a precipitating cell using the convolve function, which searches outwards from each dry cell
# (known as the target cell). The convolve function requires a kernel with a given search radius, as follows:
#
# [1 1 1]  [1 1 1 1 1]
# [1 0 1]  [1 0 0 0 1]
# [1 1 1]  [1 0 0 0 1]
#          [1 0 0 0 1]
#          [1 1 1 1 1]
#
# The 1's are effectively the search area, expanding over time. There is code below to create this 
# kernel with a given radius
#
# With the target cell centered, the convolve function sums up the value in the Precip array 
# co-located with the 1's in the kernel. If the sum of the convolve output is less than the total 
# number of 1's in the kernel it indicates a wet cell has been found and a distance to nearest wet cell 
# can then be given to the Distance array. The search diameter thus continues for the remaining dry cells

#----------------
# Note: Here I am creating artificial precip array (9x9).
# You should write code to input your own 2D precip array and modify it so the wet cells = 0 and dry cells = 1

# Initialize 2D array with 1's (without Precip)
Precip = np.zeros((9,9)) + 1

# Add some 0s to pretend some cells are wet
Precip[0,2] = 0 
Precip[2,4] = 0
Precip[1,7] = 0
Precip[7,3] = 0
Precip[8,1] = 0
#----------------

# Print the 2D wet/dry array
print '-----PRECIP'
print Precip

# Create a 2D array with the same dimensions to store the distance to closest cell with precip. 
# This array is initialized with zeros because this is the minimum possible distance.
Distance = np.zeros_like(Precip)

# Obtain an index of i/j points of dry cells
DryIndex = np.where(Precip == 1)

# Assign all cells in the DryIndex to have distance=1 (since they are at least 1 cell away from 
# a wet cell)
for jdx in range(len(DryIndex[0])):
    Distance[DryIndex[0][jdx], DryIndex[1][jdx]] = 1

# Create a list of search diameters. They must increase by 2 so the box edge is always one cell 
# further away from the center (see example kernels above).
Diameters = range(1,max(Precip.shape)+2,2)

# Loop through search diameters
for count, Diameter in enumerate(Diameters):
    print 'Diameter of search box:', Diameter

    # Define kernel with 1's around edge of the 2D array
    kernel = np.zeros((Diameter+2,Diameter+2))
    kernel[0,:] = 1
    kernel[:,0] = 1
    kernel[-1,:] = 1
    kernel[:,-1] = 1

    # Compute the sum of the surrounding cells in the Precip array 
    # Note: wet cell = 0, dry cell = 1
    # When the search box extends outside of 2D array, these points are given a 1 (cval)
    SumTarget = convolve(Precip, kernel, mode='constant', cval=1)
    print '---SumTarget'
    print SumTarget

    # We can break out of this loop early if all cells are accounted for
    TargetIndex = np.where(Distance == count+1)
    if len(TargetIndex[0]) == 0:
        'No more searching required. Breaking out of loop'
        break

#    # Loop through the remaining dry cells and if convolve sum is less than the 
#    # number of 1s in the kernel, then we know a wet cell is in this ring and we can mark that in the 
#    # distance array
#   
#    for jdx in range(len(TargetIndex[0])):
#        if SumTarget[TargetIndex[0][jdx],TargetIndex[1][jdx]] == np.sum(kernel):
#            Distance[TargetIndex[0][jdx],TargetIndex[1][jdx]] = count+2

    # If the convolve total = kernal total then no precip is found in the convolve box and distance 
    # can be increased.Create a temporary array to store these new distance values
    Distance_Temp = np.zeros_like(Precip)
    Distance_Temp[SumTarget == np.sum(kernel)] = count+2
 
    # However, the above function replaces all values where where the convolve total = kernal total, 
    # even if the target cell already has a smaller distance allocated. So we need to replace these
    # distances with their original values
    for c in range(count+1):
        print '---c', c
        Distance_Temp[Distance == c] = c

    # Now update the final Distance array with distances computed in the temporary array above
    Distance[Distance_Temp == count+2] = count+2
    print '---Distance'
    print Distance
   


# COMPLETE!
print '---PRECIP'
print Precip

print '---Distance'
print Distance
