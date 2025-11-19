clc
clear
close all

%% GEOMETRICAL PARAMETERS
V_fluid = 4.99981e-07; %[m^3]
A_wet = 0.000309139; %[m^2]
phi = 0.5; %0<phi<1
surface_to_volume = A_wet / V_fluid;
D_hyd = 4*V_fluid/A_wet;

%% PHYSICAL PARAMETERS
rho = 998.2; %[kg/m^3]
mu = 0.001002; % evaluated @20 °C [Pa*s]
%% VELOCITY COMPUTATION
Re = 5;
U_s = Re*mu*phi / (D_hyd*rho);
U_p = Re*mu / (D_hyd*rho);
