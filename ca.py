# Cellular Automata
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import random
import math

#functions
def plotDraw(frame, title):
    plt.imshow(frame)#, cmap='plasma')
    plt.title('Frame ' + str(title))
    plt.show()

def grid2array(grid):
    frame = np.zeros([len(grid), len(grid[0])])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
           frame[i,j] = grid[i][j].grainNum
           j = j +1
        i = i+1
    return frame

def listCount(listx):
    counts = []
    for i in range(len(listx)):
        counts.append(listx.count(listx[i]))
    return listx[counts.index(max(counts))]

def neighbourAcquisition(grid, neighbours, nCols, nRows):
    for i in range(1,nRows-1):
        for j in range(1,nCols-1):
            if neighbours == 'vn':
                grid[i][j].neighVN = [ grid[i][j+1].grainNum, grid[i][j-1].grainNum, grid[i+1][j].grainNum, grid[i-1][j].grainNum ]
            else:
                if random.randint(0,1) == 0:    
                    grid[i][j].neighVN = [ grid[i][j+1].grainNum, grid[i][j-1].grainNum, grid[i+1][j].grainNum, grid[i-1][j].grainNum, grid[i-1][j-1].grainNum, grid[i+1][j+1].grainNum ] 
                else:
                    grid[i][j].neighVN = [ grid[i][j+1].grainNum, grid[i][j-1].grainNum, grid[i+1][j].grainNum, grid[i-1][j].grainNum, grid[i-1][j+1].grainNum, grid[i+1][j-1].grainNum ] 
            grid[i][j].neighVN = [i for i in grid[i][j].neighVN if i != 0]
    return grid

def nucleiDistribution(grid, nucleation, nRows, nCols, nuclNum):
    if nucleation == 'random': 
        for i in range(1,nuclNum+1):
            grid[random.randint(1,nRows-2)][random.randint(1,nCols-2)].grainNum = i
    else:
        nucleiIds = list(range(1, nuclNumCol*nuclNumRow+1))
        random.shuffle(nucleiIds)
        spaceRow = int(nRows / nuclNumRow)
        spaceCol = int(nCols / nuclNumCol)
        locRow = int(spaceRow / 2)
        k = 0
        for i in range(1, nuclNumRow+1):
            locCol = int(spaceCol / 2)
            for j in range(1, nuclNumCol+1):  
                grid[locRow][locCol].grainNum = nucleiIds[k]
                locCol = locCol + spaceCol
                k = k + 1
            locRow = locRow + spaceRow
    return grid

def grainRemove(old, n, nRows, nCols):
    newold = np.zeros([nRows, nCols])
    for i in range(1,nRows-1):
        for j in range(1,nCols-1):
            if old[i,j] == n:
                newold[i,j] = n
    return newold

def growthCA(grid, nRows, nCols, neighbours):
    gridRepr = np.zeros([nRows, nCols])
    z = 0
    while gridRepr.size - np.count_nonzero(gridRepr) - (2*nRows+2*nCols-4) != 0:
        
        grid = neighbourAcquisition(grid, neighbours, nCols, nRows)

        #Transition
        for i in range(1,nRows-1):
            for j in range(1,nCols-1):
                if grid[i][j].grainNum == 0 and sum(grid[i][j].neighVN) != 0:
                    newGrain = listCount(grid[i][j].neighVN)
                    grid[i][j].grainNum = newGrain

        gridRepr = grid2array(grid)
        plotDraw(gridRepr, z)
        z = z + 1
                   
    return grid

def growthMC(grid, nRows, nCols, iterMC):
    coordList = []
    for i in range(1, nRows-1):
        for j in range(1, nCols-1):
            coordList.append([i, j])
    random.shuffle(coordList)
    z = 0
    for c in range(1, iterMC):
        grid = neighbourAcquisition(grid, neighbours, nCols, nRows)  
        for k in range((nRows-2)*(nCols-2)): 
            #grid = neighbourAcquisition(grid, neighbours, nCols, nRows) 
            grid[coordList[k][0]][coordList[k][1]].energyCalc()
            tempEnergy = grid[coordList[k][0]][coordList[k][1]].energy
            tempGrain = grid[coordList[k][0]][coordList[k][1]].grainNum
            grid[coordList[k][0]][coordList[k][1]].grainNum = random.choice(grid[coordList[k][0]][coordList[k][1]].neighVN)
            grid[coordList[k][0]][coordList[k][1]].energyCalc()
            deltaEnergy = grid[coordList[k][0]][coordList[k][1]].energy - tempEnergy
            
            if deltaEnergy > 0:
                probability = math.exp(-deltaEnergy/kt)
                if random.random() > probability:
                    grid[coordList[k][0]][coordList[k][1]].grainNum = tempGrain
            
        gridRepr = grid2array(grid)
        plotDraw(gridRepr, z)
        z = z + 1
    return grid


#calsses
class Cell:
    neighVN = []
    neighR  = []
    grainNum = 0
    energy = 0
    def __init__(self, xPos, yPos, iD):
        self.xPos = xPos
        self.yPos = yPos
        self.iD = iD
    def energyCalc(self):
        neighQ = list([i for i in self.neighVN if i != self.grainNum])
        self.energy = len(neighQ)


        
#settings
nRows = 500
nCols = 500
nuclNum = 200
#first phase nuceli number
nuclNum2 = 500 #second phase nuclei number
nuclNumRow = 3
nuclNumCol = 3 #theese two vars are used only when the 'even' option was chose
nucleation = 'random' #random/even
nucleation2 = 'random'
neighbours = 'vn' #random/vn
neighbours2 = 'random'
kt = 0.5#kt factor used for MC mathod <0.1, 6>
iterMC = 20 #number of interatios of MC mathod grain growth
oldGrainsNumb = 15

#grid generate

grid = []
    
#loop generating the list of the cells (grid)
iDnum = 0
for i in range(nRows):
    row = []
    for j in range(nCols):
        row.append(Cell(i, j, iDnum))
        iDnum = iDnum + 1
    grid.append(row)



#grain growth procedures
#distribution of nuclei
grid = nucleiDistribution(grid, nucleation, nRows, nCols, nuclNum)
#grain growth by the Cellular Automata
oldGrains = grid2array(growthCA(grid, nRows, nCols, neighbours))
#saving the random grains from the first CA
oldGrainsSet = []
for i in range(1, oldGrainsNumb+1):
    newGrain = grainRemove(oldGrains, i, nRows, nCols)
    oldGrainsSet.append(newGrain)
   
#newOldGrains = grainRemove(oldGrains, 10, nRows, nCols)    
plotDraw(oldGrains, 'Old Grains')
sumGrains = sum(oldGrainsSet)
plotDraw(sumGrains, 'Old Grains')
plt.imsave('FirstPhase.png', oldGrains)

#generation of the secong phase
#loop generating the list of the cells (grid)
grid2 = []
iDnum = 0
for i in range(nRows):
    row = []
    for j in range(nCols):
        row.append(Cell(i, j, iDnum))
        iDnum = iDnum + 1
    grid2.append(row)

grid2 = nucleiDistribution(grid2, nucleation2, nRows, nCols, nuclNum2)
#grain growth by the Cellular Automata
grid2 = growthCA(grid2, nRows, nCols, neighbours2)
#grain growth by Monte Carlo
grid2 = growthMC(grid2, nRows, nCols, iterMC)
gridRepr2 = grid2array(grid2)

#phases merging
for i in range(1, nRows-1):
    for j in range(1, nCols):
        if sumGrains[i, j] !=0:
            gridRepr2[i,j] = nuclNum2+80
            
plotDraw(gridRepr2, 'Merged phases')
plt.imsave('MergedPhases.png', gridRepr2)



    

    




