import re
import numpy as np
import matplotlib.pyplot as plt
import sys
import subprocess

def extract_pressure_gradient(line):
    # match = re.search(r"(pressure gradient = )(-?\d+.\d+)", line)
    match = re.search(r"(pressure gradient = )(-?\d+\.?\d*(e[+-]?\d+)?)", line)
    return float(match.group(2)) if match else None

def process_log_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f, open(output_file, 'a') as out_f:
            time = None
            gradP = np.array([])
            pressure_gradients = []

            for line in f:
                if line.startswith("Time ="):
                    time = int(line.split("=")[1])
                elif line.startswith("Pressure gradient source:"):
                    pressure_gradients.append(extract_pressure_gradient(line))
                if len(pressure_gradients) == 2:
                    out_f.write(f"{time}\t{pressure_gradients[1]}\n")
                    gradP = np.append(gradP, pressure_gradients[1])
                    pressure_gradients = []
    except:
        with open("log.simpleFoam", 'r') as f, open(output_file, 'a') as out_f:
            time = None
            gradP = np.array([])
            pressure_gradients = []

            for line in f:
                if line.startswith("Time ="):
                    time = int(line.split("=")[1])
                elif line.startswith("Pressure gradient source:"):
                    pressure_gradients.append(extract_pressure_gradient(line))
                if len(pressure_gradients) == 2:
                    out_f.write(f"{time}\t{pressure_gradients[1]}\n")
                    gradP = np.append(gradP, pressure_gradients[1])
                    pressure_gradients = []
    return gradP

def plot_gradP(yy):
    xx = np.arange(1, len(yy)+1)
    
    ymin = yy[-200:].min() - yy[-200:].min()*0.005
    ymax = yy[-200:].max() + yy[-200:].min()*0.005

    # Crea il grafico
    plt.plot(xx, yy)

    # Etichetta gli assi e imposta il titolo
    plt.xlabel('Time')
    plt.ylabel('gradP')
    plt.ylim(ymin, ymax)
    plt.grid()

    # Mostra il grafico
    plt.show()

def fixedJump(gradP,LL, runCommand):  
    '''
    Update the p file with fixed jump if necessary, and run the Allrun-dp 
    '''
    filepath = '0.dp/p'
    dp = gradP*LL
    
    dp_line = "\t\tjump\tuniform\t" + "{:.4e}".format(dp) + ";\n"
    
    # Update the 0/p BC file
    with open(filepath, 'r') as file:
        lines = file.readlines()
    with open(filepath, 'w') as file:
        # Search for the jump word
        for line in lines:
            if "jump" in line:
                file.write(dp_line)
            else:
                file.write(line)
                
    # Run the simulation
    subprocess.call(runCommand,shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python gradP.py <bool sourceU> <bool plotta>")
        sys.exit(1)
    sourceU = eval(sys.argv[1])
    plotta = eval(sys.argv[2])

    LL = 0.01 # m
    input_file = "log.simpleFoamRun"
    output_file = "gradp.dat"

    if sourceU:
        # If the simulation has been run with a momentum source
        f = open(output_file, "w")
        f.write("Time   gradP \n")
        f.close()
        gradP = process_log_file(input_file, output_file)

        # Compute the percentage standard deviation 
        gradp_avg = np.mean(gradP[-500:])
        gradp_std = np.std(gradP[-500:])/gradp_avg*100 
    if plotta:
        plot_gradP(gradP)