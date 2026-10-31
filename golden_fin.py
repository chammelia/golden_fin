import numpy as np

# T_b = T_c - q_f*k*A_b / h_b
# print(T_b)


# Alyssa's Code:

import numpy as np
import matplotlib.pyplot as plt

T_inf = 20+273.15       # 20C


k = 317                 # conductivity of gold, W/m K
N = 26                  # number of fins
w_f = 24/1000           # width of the fin mm  
t_f = .25/1000          # thickness of the fin mm
l_f = 26/1000           # height (length) of the fin mm         

# dimensions of the base
h_b = 1/1000
w_b = 24/1000
l_b = 26/1000

q = 25                  # W 
h =                   # convection coefficient, W/m^2 K 

P = 2*w_f + 2 * t_f     # Perimeter
A_c = w_f * t_f         # Area of the cross section 

m = (2*h/(k*t_f))**0.5          
m2 = (h*P/(k*A_c))**0.5         # another way to calculate m, same result (approximately)


L_c = l_f + t_f/2               # Corrected length condition for rectangular fin

# Areas:
A_f = 2*w_f*L_c                 # x2 because both sides?
A_b = w_b*l_b                   # I think you have to take out the part of the fins
A_t = N*A_f + A_b                 # Total area

# Efficiencies:
n_f = np.tanh(m*L_c)/(m*L_c)    # Efficiency for 1 fin with corrected length for adiabatic tip
n_o = 1-N*A_f*(1-n_f)/A_t       # Efficiency overall for N fins 

# Resistances:
R_t = 1/(n_o*h*A_t)            
R_cond = h_b/(k*w_b*l_b)

T_b = R_t*q + T_inf

T = q*(R_cond+R_t) + T_inf


e = q/(h*A_b*(T_b - T_inf))         # Efficiency (In the eqn I have, this area is A_c,b the cross section of the bas)

print(f"T(h={h})= {T-273.15} for fin height {l_f}")
print(f"Efficiency at h={h}: {e}")

e = []
h_array = np.linspace(1, 400000, 5000)          # I think this array should have smaller h values closer together
h_threshold = []


for i in h_array:
    m = (2*i/(k*t_f))**0.5          # calculate m for each h value
    
    n_f = np.tanh(m*L_c)/(m*L_c)
    n_o = 1-N*A_f*(1-n_f)/A_t
    
    R_t = 1/(n_o*i*A_t)    
    T_b = R_t*q+T_inf
    
    epsilon = q/(i*A_b*(T_b-T_inf))
    e.append(epsilon)
    if epsilon < 2:                     # Don't we want this to be greater???        
        h_threshold.append(i)

        
if h_threshold:
    print(f"Effectiveness > 2 when h < {min(h_threshold)} W/(K*m^2)")
else:
    print("Effectiveness never drops below 2 in the evaluated range.")   



fig, ax = plt.subplots()
ax.plot(h_array, e)
ax.set_xlabel("h (W/(K*m^2))")
ax.set_ylabel("Fin Effectiveness")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.title(f"Efficiency of a fin of height {l_f*1000} mm")
plt.savefig("efficiency_graph.png")
