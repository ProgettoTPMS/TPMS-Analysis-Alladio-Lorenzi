clc
clear
close all

%% GEOMETRICAL PARAMETERS
Lc = 0.01; %[m]
V_fluid = 4.99981e-07; %[m^3]
A_wet = 0.000309139; %[m^2]
phi = 0.5; %0<phi<1
surface_to_volume = A_wet / V_fluid;
D_hyd = 4*V_fluid/A_wet;

%% PHYSICAL PARAMETERS
rho = 998.2; %[kg/m^3]
mu = 1.002e-3; % evaluated @20 °C [Pa*s]

%% VELOCITY COMPUTATION
Re = [5, 10, 50, 100];
U_s = zeros(4,0);
U_p = zeros(4,0);

for ii = 1:length(Re)
    U_s(ii) = Re(ii)*mu*phi / (D_hyd*rho);
    U_p(ii) = Re(ii)*mu / (D_hyd*rho);
end

%% RESULTS
cinematic_gradp = [1.75012e-03;3.67846e-03;2.85524e-02;7.18076e-02];
gradp = cinematic_gradp .* rho;

%% DARCY-FORCHHEIMER CORRELATION
krel = 2.2e-3;
Cf = 0.31;
kk = krel * Lc^2;
vett_Us = (1e-4:1e-6:2e-2)';
darcy_gradp = - (- (mu/kk)*vett_Us - (rho*Cf/sqrt(kk))*vett_Us.^2);

%% PLOT
loglog(vett_Us,darcy_gradp,LineWidth=3, Color="r", LineStyle="--")
hold on
loglog(U_s, gradp, 'bd', 'MarkerFaceColor', 'b', 'MarkerSize', 8)
grid minor
title('Pressure gradient vs Superficial velocity - Gyroid 50% porosity, water @20°C','FontSize',24)
xlabel('Us [m/s]', 'FontSize', 18)
ylabel('\Deltap/L [Pa/m]', 'FontSize', 18)
set(gca,'Fontsize',20)
legend('Darcy-Forchheimer','CFD','Location','northwest','FontSize',18)
