"""
.. _ref_1715:

One Element tension Isotropic force controlled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import dolfinx
import mpi4py 
import petsc4py

sys.path.append("../../src")

from Element.Phase_Field_Fracture.solver.solver_dolfiny_arc_force import solve
from Element.Phase_Field_Fracture.ClassInput import SimulationPhaseFieldFracture
from Boundary.boundary_conditions import bc_xy, bc_y, get_ds_bound_from_marker
from Loading.loading_functions import loading_Txy
from PostProcessing.ReferenceResult import AllResults

current_script_dir = '../../examples/17_Fracture'
###############################################################################
# Parameters definition

Data = SimulationPhaseFieldFracture(
                 E = 210.0,   # young modulus
                 nu = 0.3,    # poisson
                 Gc = 0.005,  # critical energy release rate
                 l = 0.1,     # lenght scale parameter
                 degradation = "isotropic", # "isotropic" "anisotropic"
                 split_energy = "no",       # "spectral" "deviatoric"
                 degradation_function = "quadratic",
                 irreversibility = "miehe", # "miehe"
                 fatigue = False,
                 fatigue_degradation_function = "asymptotic",
                 fatigue_val = 0.05625,
                 k = 0.0,
                 min_stagger_iter = 2,
                 max_stagger_iter = 5,
                 stagger_error_tol = 1e-8,
                 save_solution_xdmf = False,
                 save_solution_vtu = True,
                 result_folder_name = "1715_One_element_arc_lenght")



###############################################################################
# Mesh definition

msh = dolfinx.mesh.create_rectangle(mpi4py.MPI.COMM_WORLD,
                                    [np.array([0, 0]),
                                     np.array([1, 1])],
                                     [1, 1],
                                     cell_type=dolfinx.mesh.CellType.quadrilateral)

def bottom(x):
    return np.isclose(x[1], 0)

def top(x):
    return np.isclose(x[1], 1)

fdim = msh.topology.dim - 1

bottom_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, bottom) 
top_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, top)         

ds_bottom = get_ds_bound_from_marker(top_facet_marker, msh , fdim)
ds_top = get_ds_bound_from_marker(top_facet_marker, msh , fdim)

ds_list = np.array([
                   [ds_top,    "top"],
                   [ds_bottom, "bottom"],
                   ])

###############################################################################
# Function Space definition 
V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))


###############################################################################
# Boundary Conditions
bc_bottom = bc_xy(bottom_facet_marker, V_u, fdim)

bcs_list_u = [bc_bottom]


def update_boundary_conditions(bcs, time):
    if time <= 50:
        val =   0.0003*time 
    elif time <= 100:
        val =  -0.0003*(time-50) + 0.015
    else:
        val =  0.0003*(time-100)
    
    bcs[0].g.value[1] = petsc4py.PETSc.ScalarType(val)
    return 0, val, 0

    
bcs_list_phi=[]

###############################################################################
# External 
T_top = loading_Txy(V_u, msh, ds_top)

T_list_u = [[T_top,  ds_top]]

def update_loading(T_list_u, time):
    val = 0.003*time
    T_list_u[0][0].value[1] = petsc4py.PETSc.ScalarType(val)
    return 0, val, 0

f = None

###############################################################################
# Call the solver
final_time = 100
dt = 1.0
solve(os.getcwd(),
      Data,
      msh, 
      final_time,
      V_u,
      V_phi,
      bcs_list_u,
      bcs_list_phi,
      None,
      f, 
      T_list_u,
      None, 
      ds_list,
      dt)
    

###############################################################################
# Load results
example_path = os.path.join(current_script_dir, Data.result_folder_name)
S = AllResults(example_path)
S.set_label('simulation')
S.set_color('b')

###############################################################################
# Plot phase-field $\phi$
#S.paraview.data[0].plot(scalars='f', component=0, cpos='xy', show_scalar_bar=True,show_edges=True)
import pyvista as pv
# pN = pv.read("/Users/miguelcastillon/Programs/Fenicsx-Codes/examples/17_Fracture/1700_General/paraview-solutions_vtu/fenicsx000199.pvtu")
# pN.plot(scalars='phi', component=0, cpos='xy', show_scalar_bar=True,show_edges=True)
###############################################################################
# Vetical displacement
displacement = S.dof_files["top.dof"]["Uy"]
force = S.reaction_files["bottom.reaction"]["Ry"]

psi_t     = 0.5 * displacement **2 * (Data.lambda_+2*Data.mu)
sigma_t   = displacement  * (Data.lambda_+2*Data.mu)
phi_t     = 2 * psi_t/(Data.Gc/Data.l+2*psi_t)
g_sigma_t = (1-phi_t)**2 * sigma_t 



###############################################################################
# Plot time vs reaction force
fig, ax = plt.subplots() 

ax.plot(force, S.color+'.', linewidth=2.0, label=S.label)

ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('time')    
ax.set_ylabel('displacement - u $[mm]$' )  

ax.legend() 


###############################################################################
# Plot displacement vs reaction force
fig, ax = plt.subplots() 

ax.plot(displacement, S.reaction_files['top.reaction']["Ry"], S.color+'.', linewidth=2.0, label=S.label)
ax.plot(displacement, g_sigma_t , 'k-', linewidth=2.0, label="Teory")


ax.grid(color='k', linestyle='-', linewidth=0.3)
ax.set_xlabel('displacement - u $[mm]$' )  
ax.set_ylabel('reaction force - F $[kN]$')    
ax.legend() 


###############################################################################
# Plot displacement vs energy
fig, energy = plt.subplots() 

energy.plot( S.energy_files['total.energy']["EplusW"], 'k-', linewidth=2.0, label='EW')
energy.plot( S.energy_files['total.energy']["E"], 'r-', linewidth=2.0, label='E')
energy.plot( S.energy_files['total.energy']["W"], 'b-', linewidth=2.0, label='W')

energy.legend() 
energy.grid(color='k', linestyle='-', linewidth=0.3)
energy.set_xlabel('displacement - u $[mm]$' )  
energy.set_ylabel('Energy')


###############################################################################
# Plot displacement vs W fracture energy
fig, energyW = plt.subplots() 

energyW.plot( S.energy_files['total.energy']["W"], 'b-', linewidth=2.0, label='W')
energyW.plot( S.energy_files['total.energy']["W_phi"], 'y-', linewidth=2.0, label='Wphi')
energyW.plot( S.energy_files['total.energy']["W_gradphi"], 'g-', linewidth=2.0, label='Wgraphi')

energyW.grid(color='k', linestyle='-', linewidth=0.3)
energyW.set_xlabel('displacement - u $[mm]$' )  
energyW.set_ylabel('Energy')
energyW.legend() 


plt.show()

# fenics-basix              0.6.0           py310ha23aa8a_0    conda-forge
# fenics-dolfinx            0.6.0           py310h9047b3e_100    conda-forge
# fenics-ffcx               0.6.0              pyh56297ac_0    conda-forge
# fenics-libbasix           0.6.0                h7396341_0    conda-forge
# fenics-libdolfinx         0.6.0              h245ff80_100    conda-forge
# fenics-ufcx               0.6.0                h56297ac_0    conda-forge
# fenics-ufl 