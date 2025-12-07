#!/usr/bin/python3

import numpy as np


def process_file():
    '''
        Process the surfaceFieldValue file of the mass flow rate.
        Take the last 200 lines and compute the man and the standard deviation
    '''
    # Read all lines from the dat file
    file_path = 'postProcessing/inlet_Vflow/0/surfaceFieldValue.dat'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract only last 200 lines
    processLines = lines[-100:]

    # Initialize step (-) and Vflow 
    step = np.array([])
    Vflow = np.array([])

    # Split the two columns of the file
    for line in processLines:
        columns = line.split()
        step = np.append(step, float(columns[0]))
        Vflow = np.append(Vflow, -float(columns[1]))


    # Compute mean and standard deviation of vflow
    Vflow_avg = np.mean(Vflow)
    Vflow_std = np.std(Vflow)
    
    return Vflow_avg, Vflow_std

def getMeshInfo():
    '''
        Get the mesh info from the dat file produced using the function object system/infoTPMS
    '''
    filepath = 'infoTPMS.dat'
    # Open the dat file
    with open(filepath, 'r') as file:
        line = file.readlines()[-1].split()
    volCube = float(line[1])
    Aw = float(line[2])
    volFluid = float(line[3]) 
    return Aw, volCube, volFluid
    
    
def printResults(Aw, volCube, volFluid, Vflow_avg, Vflow_std):
    '''
        Take Aw, volFluid and volTot from infoTPMS.dat and compute Reynolds number
    '''
    
    # nu = 8.566E-07
    nu = 5e-7
    Dh = 4*volFluid/Aw
    Us = Vflow_avg/(0.01**2)
    por = volFluid/volCube
    Re = Us*Dh/nu/por
    
    print(f"Us = {Us:.2e}")
    print(f"Dh = {Dh:.2e}")
    print(f"Re = {Re:.2e}")
 
    
if __name__ == "__main__":    
    
    Vflow_avg, Vflow_std = process_file()
    Aw, volCube, volFluid = getMeshInfo()
    printResults(Aw, volCube, volFluid, Vflow_avg, Vflow_std)
            
    # plotMflowRate(step, mflow)
    
    
    




