#!/usr/bin/python3

import numpy as np
import sys
from scipy.spatial import KDTree
import pandas as pd

def extract_Vflow(Vflow_file):
    '''
        Process the surfaceFieldValue file of the volume flow rate.
        Take the last 200 lines and compute the mean and the standard deviation
    '''
    # Read all lines from the dat file
    with open(Vflow_file, 'r') as file:
        lines = file.readlines()

    # Extract only last 200 lines
    processLines = lines[-200:]
    latestTime = processLines[-1].split()[0]
    Vflow = np.array([])
    # Split the two columns of the file
    for line in processLines:
        columns = line.split()
        Vflow = np.append(Vflow, -float(columns[1]))

    # Compute mean and standard deviation of vflow
    Vflow_avg = np.mean(Vflow)
    Vflow_std = np.std(Vflow)/Vflow_avg*100
    
    return Vflow_avg, Vflow_std, latestTime

def extract_gradp(gradp_file, LL):
    '''
        Process the gradp.dat file for the pressure gradient.
        Take the last 200 lines and compute the mean and the standard deviation
        Check that the standard deviation is lower than 1%, otherwise use fixedJumpAMI
    '''
    with open(gradp_file, 'r') as f:
        data = np.loadtxt(f, skiprows=1)  # Adjust skiprows as needed
        # time, gradp = data[:, 0], data[:, 1]
    gradp = data[-500:,1]
    gradp_avg = np.mean(gradp)
    gradp_std = np.std(gradp)/gradp_avg*100

    return gradp_avg, gradp_std

def extract_Tm(Tm_file):
    '''
        Process the surfaceFieldValue file of the mean bulk Temperature.
        Take the last 50 lines and compute the mean and the standard deviation
    '''
    # Read all lines from the dat file
    with open(Tm_file, 'r') as file:
        lines = file.readlines()

    # Extract only last 50 lines
    processLines = lines[-10:]
    Tm = np.array([])
    # Split the two columns of the file
    for line in processLines:
        columns = line.split()
        Tm = np.append(Tm, float(columns[1]))

    # Compute mean and standard deviation of Tm
    Tm_avg = np.mean(Tm)
    Tm_std = np.std(Tm)/Tm_avg*100
    
    return Tm_avg

def extract_Tw(transportProp):
    Tw = 0.0
    with open(transportProp, 'r') as file:
        lines = file.readlines().split()
        for line in lines:
            if "Tw" in line:
                Tw = float(line.split()[1])
    return Tw

def extract_SST(sstFile):
    with open(sstFile, 'r') as file:
        # lines = file.readlines().split()
        line = file.readlines()[-1]
        sst_str = line.split('(')[-1].strip(')\n')
        sst = np.array([float(x) for x in sst_str.split()])
    return sst

def get_dp():
    '''
        Get the imposed pressure drop from the 0/p file, when imposing fixedJump AMI
    '''
    filepath = '0/p'
    # Open the p BC file
    with open(filepath, 'r') as file:
        lines = file.readlines()
    dp = 0.
    # Search for the jump word
    for line in lines:
        if "jump" in line:
            dp = float(line.split()[2].replace(';',''))
            break
    return dp

def get_Tbulk_out(file_Tbulk, nLine):
    # Read all lines from the dat file
    with open(file_Tbulk, 'r') as file:
        lines = file.readlines()
    Tbulk_out = float(lines[nLine].split()[1])
    return Tbulk_out
    
def getMeshInfo(info_file):
    '''
        Get the mesh info from the dat file produced using the function object system/infoTPMS
    '''
    with open(info_file, 'r') as file:
        line = file.readlines()[-1].split()
    volCube = line[1]
    Aw = line[2]
    volFluid = line[3] 
    return Aw, volCube, volFluid
    
def extract_qwall(qwall_file):
    '''
        Process myWallHeatFlux.dat.
        Take the last 100 lines and compute the mean and the standard deviation of qwall/(rho cp) [W/m2 / (kg/m3 J/kg/K)]
    '''
    # Read all lines from the dat file
    with open(qwall_file, 'r') as file:
        lines = file.readlines()

    # Extract only last 100 lines
    processLines = lines[-10:]
    qwall = np.array([])
    Qwall = np.array([])
    # Split the four columns of the file
    for line in processLines:
        columns = line.split()
        qwall = np.append(qwall, float(columns[2]))
        Qwall = np.append(Qwall, float(columns[3]))

    # Compute mean and standard deviation of vflow
    qwall_avg = np.mean(qwall)
    qwall_std = np.std(qwall)/qwall_avg*100
    Qwall_avg = np.mean(Qwall)
    
    return qwall, qwall_avg, qwall_std, Qwall_avg

def printResults_rotated(Aw, volCube, volFluid, VflowIn, VflowTop, gradp_avg, gradp_std, qwall_avg, To, Tbottom, sst, nameOutput):
    '''
        Take Aw, volFluid and volTot from infoTPMS.dat and write them with the hydraulic results in a unique file
    '''
    VIn_e="{:.5e}".format(VflowIn)
    VTop_e="{:2.2f}".format(VflowTop)
    p_avg_e="{:.5e}".format(gradp_avg)
    p_std_e="{:2.2f}".format(gradp_std)
    q_avg_e="{:.5e}".format(qwall_avg)
    q_std_e="{:2.2f}".format(qwall_std)
    To_e="{:.5e}".format(To)
    Tbottom_e="{:.5e}".format(Tbottom)
    sstY_e="{:.5e}".format(sst[1])
    sstZ_e="{:.5e}".format(sst[2])

    spaz = '\t'
    outResults = Aw + spaz + volCube + spaz + volFluid + spaz + \
                 VIn_e + spaz + VTop_e + spaz + \
                 p_avg_e + spaz + p_std_e + spaz + \
                 q_avg_e + spaz + q_std_e + spaz + \
                 To_e + spaz + Tbottom_e + spaz + \
                 sstY_e + spaz + sstZ_e + '\n'   
    fileOutput = open(nameOutput,'w')
    fileOutput.write("Aw\tvolCube\tvolF\tVIn\tVBottom\tgradp_avg\tgradp_std\tqwall_avg\tqwall_std\tTb_o\tTb_b\tsstY\tsstZ\n")
    fileOutput.write(outResults)
    fileOutput.close()

def printResultsQw(Aw, volCube, volFluid, Vflow_avg, gradp_avg, Ti, To, Tw, TbVol, ssty, nameOut):
    '''
        Take Aw, volFluid and volTot from infoTPMS.dat and write them with the hydraulic results in a unique file
    '''

    V_avg_e="{:.5e}".format(Vflow_avg)
    p_avg_e="{:.5e}".format(gradp_avg)
    Ti_e="{:.5e}".format(Ti)
    To_e="{:.5e}".format(To)
    Tw_e="{:.5e}".format(Tw)
    TbVol_e="{:.5e}".format(TbVol)
    sst_e="{:.4e}".format(ssty)

    spaz = '\t'
    outResults = Aw + spaz + volCube + spaz + volFluid + spaz + \
                 V_avg_e + spaz + p_avg_e  + spaz + \
                 Ti_e + spaz + To_e + spaz + \
                 Tw_e + spaz + TbVol_e + spaz + sst_e + '\n'   
    fileOutput = open(nameOut,'w')
    fileOutput.write("Aw\tvolCube\tvolFluid\tVflow_avg\tgradp_avg\tTi\tTo\tTw\tTbV\tSST\n")
    fileOutput.write(outResults)
    fileOutput.close()

if __name__ == "__main__":    

    LL = 0.01 # m

    Vflow_file = "postProcessing/inlet_Vflow/0/surfaceFieldValue.dat"
    Vflow_avg, Vflow_std, latestTime = extract_Vflow(Vflow_file)
    
    gradp_file = "gradp.dat"
    gradp_avg, gradp_std = extract_gradp(gradp_file, LL)

    info_file  = "infoTPMS.dat"
    Aw, volCube, volFluid = getMeshInfo(info_file)
    volCube = f"{0.01**3:.2e}"
    por = float(volFluid)/(0.01**3)

    To_file = f"postProcessing/Tbulk2/{latestTime}/surfaceFieldValue.dat"
    Ti_file = f"postProcessing/Tbulk1/{latestTime}/surfaceFieldValue.dat"
    Tw_file = f"postProcessing/Tw/{latestTime}/surfaceFieldValue.dat"
    Tm_file = f"postProcessing/Tm/{latestTime}/volFieldValue.dat"
    To = get_Tbulk_out(To_file,6)
    Ti = get_Tbulk_out(Ti_file,6)
    Tw = get_Tbulk_out(Tw_file,5)
    TbVol = extract_Tm(Tm_file)

    # Tbottom = get_Tbulk_out(Tbottom_file)
    sstFile = "postProcessing/myWallStress/0/myWallShearStress.dat"
    sst = extract_SST(sstFile)
    
    nameOutput = "results.dat"
    printResultsQw(Aw, volCube, volFluid,Vflow_avg, gradp_avg, Ti, To, Tw, TbVol, sst[1], nameOutput)    
    
    
    




