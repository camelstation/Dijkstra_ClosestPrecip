## Dijkstra's algorithm for computing the closest precipitating grid cell

A fast routine to return a 2D array of distance to closest precipitating grid cell.

* Input: a 2D array of precip
* Output: a 2D array of distance to closest precipitating grid cell (measured by number of grid cells)

I have used it for super-resolution exercises (e.g., see https://arxiv.org/abs/2012.01233) but it could be used for many applications.

## How to use

Read in a 2D precipitation array and modify it such that: 
* Wet cells (with precip) = 0
* Dry cells (without precip) = 1

The output of this program is a 2D array with the same dimensions as the input file. Values in the 
array indicate the number of grid cells to the closest wet cell.

We use the convolve function to search for the closest precipitating cell from the perspective of each dry cell (aka: the target cell).
The convolve function searches outwards from each dry cell and requires a kernel with a given search radius, e.g:

```
[1 1 1]  [1 1 1 1 1]
[1 0 1]  [1 0 0 0 1]
[1 1 1]  [1 0 0 0 1]
         [1 0 0 0 1]
         [1 1 1 1 1]
```

The 1's are effectively the search area, expanding over time. 

With the target cell centered, the convolve function sums up the value in the **Precip** array 
co-located with the 1's in the kernel. If the sum of the convolve output is less than the total 
number of 1's in the kernel, it indicates a wet cell has been found and the distance to nearest wet cell 
can then be computed for the **Distance** array. This distance is computed for all dry cells simultaneously; 
the search diameter thus continues for the remaining dry cells.

Note: In this code, I create an artificial precip array of [9x9]. You should write code to input your own 2D precip array and modify it so the wet cells = 0 and dry cells = 1. I have run it with precip arrays from globally-gridded obs (e.g., CHIRPS) and numerical model output (e.g., WRF) and it's pretty fast  
