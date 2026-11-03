import numpy as np

# T_b = T_c - q_f*k*A_b / h_b
# print(T_b)


# Alyssa's Code:

import numpy as np
import matplotlib.pyplot as plt

T_inf = 20 + 273.15       # 20C


k = 317                 # conductivity of gold, W/m K
N = 13 * 12              # number of fins
D = 1/1000               # diameter (m)
l_f = 10/1000           # height (length) of the fin mm         

# dimensions of the base
h_b = 1/1000            # 1 mm thick
w_b = 24/1000
l_b = 26/1000

q = 25                  # W 
h = 319.25                # W / m K       # WE CHOSE THIS

L_c = l_f + D/4               # Corrected length condition for rectangular fin

# Areas:
A_f = L_c * np.pi * D
A = w_b * l_b                 # Area of the base without any fins
A_b = A - np.pi*D**2/4 * N        # remove the part with the fins
A_t = N*A_f + A_b                 # Total area

m = np.sqrt(4*h/(k*D))

# Efficiencies:
n_f = np.tanh(m*L_c)/(m*L_c)    # Efficiency for 1 fin with corrected length for adiabatic tip
n_o = 1-N*A_f*(1-n_f)/A_t       # Efficiency overall for N fins 

# Resistances:
R_t_o = 1/(n_o*h*A_t)            
R_cond = h_b/(k*A)
R_tot = R_cond + R_t_o

T_b = R_t_o*q + T_inf

e = q/(h*A*(T_b - T_inf))         # Efficiency (overall, Dr. Iverson also said we can just do it for one fin if we want)

print(f"T(h={h}) = {T_b-273.15} C for fin height {l_f*1000}mm")
print(f"Effectiveness at h={h}: {e}")

e = []
h_array = np.linspace(h, 4000)          
h_threshold = []


for i in h_array:
    m = (4*i/(k*D))**0.5          # calculate m for each h value
    
    n_f = np.tanh(m*L_c)/(m*L_c)
    n_o = 1-N*A_f*(1-n_f)/A_t
    
    R_tot = 1/(n_o*i*A_t) + R_cond   
    T_b = R_tot*q+T_inf
    
    epsilon = q/(i*A*(T_b-T_inf))
    e.append(epsilon)
    if epsilon > 2:                           
        h_threshold.append(i)

        
if h_threshold:
    print("Effectiveness never drops below 2 in the evaluated range.")   



fig, ax = plt.subplots()
ax.plot(h_array, e)
ax.set_xlabel("h (W/(K*m^2))")
ax.set_ylabel("Fin Effectiveness")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# plt.title(f"Effectiveness of fins of height {l_f*1000} mm for varying h values")
plt.savefig("effectiveness_graph.png")



# From section 7.6, calculating the fluid conditions
def h(k, V, nu, Pr, m, C1):
    Pr_s = .69837               # at T = 85 C
    
    Re_D = V*D/nu
    print(f"Re_D = {Re_D}")
    C2 = 0.98
    Nu = C1 * Re_D**m * Pr**(0.36) * (Pr/Pr_s)**0.25            # eqn 7.58
    return C2 * Nu * k / D


# Selecting V and then air at room temp:
V = 20              # m/s
# Properties of air at T_f = 52.5 C (Tinf + Ts)/2
Pr = .703409
k = .0281981
nu = 1.847039e-5
m = .4                   # 
C1 = .8
print(f"h = {h(k, V, nu, Pr, m, C1)}")

# Notes: We choose V to be higher rather than increasing the number of fins (and making them smaller) 
# because this is more reasonable from a manufacturing viewpoint
# This causes our T_b to be really low, great for chip computing power



