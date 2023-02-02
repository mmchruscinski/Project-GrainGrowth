import numpy as np
from matplotlib import pyplot as plt

#functions


#calsses
class Cell:
    neighVN = []
    neighM  = []
    grainNum = 0
    def __init__(self, xPos, yPos, iD):
        self.xPos = xPos
        self.yPos = yPos
        self.iD = iD
        print('Cell created at ' + str(xPos) + ' , ' + str(yPos))
        
#settings
nRows = 5
nCols = 5


#generowanie siatk
gridRepr = np.zeros([nRows, nCols])
plt.imshow(gridRepr)
plt.show()

grid = []



iDnum = 0
#loop generating the list of the cells
for i in range(nRows):
    for j in range(nCols):
        grid.append(Cell(i, j, iDnum))
        gridRepr[i,j] = grid[iDnum].grainNum
        iDnum = iDnum + 1
        
#loop generating the list of the cells
for i in range(nRows):
    row = []
    for j in range(nCols):
        row.append(Cell(i, j, iDnum))
        iDnum = iDnum +1
    grid.append(row)



# for i in range(nRows):
#     for j in range(nCols):
#         grid[iDnum].neighVN = [ iDnum-1, iDnum+1, iDnum-nCols, iDnum+nCols ]
#         iDnum = iDnum + 1

#loop setting the neighbourhood
iDnum = 1
print('Grain loop')
for i in range(1, nRows-1):
    for j in range(1, nCols-1):
        grid[iDnum].neighVN = [ grid[iDnum-1].grainNum, grid[iDnum+1].grainNum, grid[iDnum-nCols].grainNum, grid[iDnum+nCols].grainNum ]
        grid[iDnum].grainNum = 1
        print("Cell " + str(iDnum) + ' ziarno ' + str(grid[iDnum].grainNum))
        iDnum = iDnum + 1

iDnum = 0  
for i in range(nRows):
    for j in range(nCols):
        gridRepr[i,j] = grid[iDnum].grainNum
        iDnum = iDnum + 1
        


# for obj in grid:
#     print(obj.iD)
#     print(obj.grainNum)
#     print(obj.neighVN)
    
    
    
print(gridRepr)
plt.imshow(gridRepr)
plt.show()
    



