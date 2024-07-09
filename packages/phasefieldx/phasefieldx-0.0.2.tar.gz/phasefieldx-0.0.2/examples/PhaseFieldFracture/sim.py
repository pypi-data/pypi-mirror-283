"""
.. _ref_1711:

Single edge notched tension test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A well-known benchmark simulation in fracture mechanics is performed, for which we rely on the simulation done by [Miehe]_. This simulation consider an anisotropic formulation with spectral energy decomposition, although we have repeated the simulations with isotropic formulation.

The model consists of a square plate, with a notch located halfway up, which runs from the left to the centre of it, as shown in the next figure. The bottom part is fixed in all directions, while the upper can slide vertically. A vertical displacement is applied at the top in steps of :math:`\Delta U`. The geometry and boundary conditions are shown in. We discretize the model with triangular elements as [Miehe]_, refining the areas (h element size) where crack evolution is expected .The element size h must be small enough to avoid mesh dependencies. 

.. code-block::

   #           u/\/\/\/\/\/\       
   #            ||||||||||||  
   #            *----------*  
   #            |          | 
   #            | a=0.5    |
   #            |---       |
   #            |          |
   #            |          | 
   #            *----------*
   #            /_\/_\/_\/_\       
   #     |Y    /////////////
   #     |                
   #      ---X           
   #  Z /  
   

+----+---------+--------+
|    | VALUE   | UNITS  |
+====+=========+========+
| E  | 210     | kN/mm2 |
+----+---------+--------+
| nu | 0.3     | [-]    |
+----+---------+--------+
| Gc | 0.0027  | kN/mm2 |
+----+---------+--------+
| l  | 0.015   | mm     |
+----+---------+--------+

.. [Miehe] A phase field model for rate-independent crack propagation: Robust algorithmic implementation based on operator splits, https://doi.org/10.1016/j.cma.2010.04.011.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import dolfinx
import mpi4py 
import petsc4py


from phasefieldx.Element.Phase_Field_Fracture.solver.solver import solve
from phasefieldx.Element.Phase_Field_Fracture.Input import Input
from phasefieldx.Boundary.boundary_conditions import bc_xy, bc_y, get_ds_bound_from_marker
from phasefieldx.Loading.loading_functions import loading_Txy
from phasefieldx.PostProcessing.ReferenceResult import AllResults


current_script_dir = '../../examples/PhaseFieldFracture'
###############################################################################
# Parameters definition

Data = Input(
                 E = 210.0,   # young modulus
                 nu = 0.3,    # poisson
                 Gc = 0.0027, # critical energy release rate
                 l = 0.015,     # lenght scale parameter
                 degradation = "isotropic", # "isotropic" "anisotropic"
                 split_energy = "no",       # "spectral" "deviatoric"
                 degradation_function = "quadratic",
                 irreversibility = "miehe", # "miehe"
                 fatigue = False,
                 fatigue_degradation_function = "asymptotic",
                 fatigue_val = 0.05625,
                 k = 0.0,
                 min_stagger_iter = 2,
                 max_stagger_iter = 500,
                 stagger_error_tol = 1e-8,
                 save_solution_xdmf = False,
                 save_solution_vtu = True,
                 result_folder_name = "SIM")


###############################################################################
# Mesh definition
msh_file = "mesh/mesh.msh"
gdim = 2
gmsh_model_rank = 0
mesh_comm = mpi4py.MPI.COMM_WORLD

msh, cell_markers, facet_markers = dolfinx.io.gmshio.read_from_msh(msh_file, mesh_comm, gmsh_model_rank, gdim)

fdim = msh.topology.dim - 1

bottom_facet_marker = facet_markers.find(9)
top_facet_marker    = facet_markers.find(10)
right_facet_marker  = facet_markers.find(11)
left_facet_marker   = facet_markers.find(12)


ds_bottom = get_ds_bound_from_marker(bottom_facet_marker, msh, fdim)
ds_top = get_ds_bound_from_marker(top_facet_marker, msh, fdim)
ds_right = get_ds_bound_from_marker(right_facet_marker, msh, fdim)
ds_left = get_ds_bound_from_marker(left_facet_marker, msh, fdim)

ds_list = np.array([
                   [ds_bottom, "bottom"],
                   [ds_top,    "top"]
                   ])

###############################################################################
# Function Space definition 
V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))


###############################################################################
# Boundary Conditions *********************************************************

###############################################################################
# Boundary Conditions four displacement field
bc_bottom = bc_xy(bottom_facet_marker, V_u, fdim)
bc_top    = bc_y(top_facet_marker, V_u, fdim)
bcs_list_u = [bc_top, bc_bottom]

def update_boundary_conditions(bcs, time):
    dt0 = 10**-4
    if time <= 50:
        val = dt0 * time
    else:
        val = 50*dt0 + dt0/10 * (time - 50)

    bcs[0].g.value[...] = petsc4py.PETSc.ScalarType(val)
    return 0, val, 0


T_list_u = None 
def update_loading(T_list_u, time):
    return 0, 0, 0

###############################################################################
# Boundary Conditions four phase field
bcs_list_phi=[]


###############################################################################
# Call the solver
T = dolfinx.fem.Constant(msh, petsc4py.PETSc.ScalarType((0.0, 0.0)))
f = dolfinx.fem.Constant(msh, petsc4py.PETSc.ScalarType((0.0, 0.0)))

final_time = 150
solve(os.getcwd(), 
      Data,
      msh, 
      final_time, 
      V_u, 
      V_phi,
      bcs_list_u, 
      bcs_list_phi, 
      update_boundary_conditions,
      f, 
      T_list_u,
      update_loading,  
      ds_list)
    

###############################################################################
# Load results
example_path = os.path.join(current_script_dir, Data.result_folder_name)
S = AllResults(example_path)
S.set_label('simulation')
S.set_color('b')

###############################################################################
# Plot displacement "u"
import pyvista as pv
file_vtu = pv.read(example_path+"/paraview-solutions_vtu/phasefieldx_p0_000149.vtu")
file_vtu.plot(scalars='phi', cpos='xy', show_scalar_bar=True, show_edges=False)

###############################################################################
# Plot solutions
Miehe  = np.loadtxt("reference_solutions/miehe_solution.csv")

displacement = S.dof_files["top.dof"]["Uy"]


###############################################################################
# Plot displacement vs W fracture energy
fig, energyW = plt.subplots() 

energyW.plot(displacement, S.energy_files['total.energy']["W"], 'b-', linewidth=2.0, label='W')
energyW.plot(displacement, S.energy_files['total.energy']["W_phi"], 'y-', linewidth=2.0, label='Wphi')
energyW.plot(displacement, S.energy_files['total.energy']["W_gradphi"], 'g-', linewidth=2.0, label='Wgraphi')

energyW.grid(color='k', linestyle='-', linewidth=0.3)
energyW.set_xlabel('displacement - u $[mm]$' )  
energyW.set_ylabel('Energy')
energyW.legend() 




###############################################################################
# Reaction forces
fig, ax_reaction = plt.subplots() 

ax_reaction.plot(Miehe[:, 0], Miehe[:, 1],    'g-', linewidth=2.0, label='Miehe')
ax_reaction.plot(displacement, S.reaction_files['bottom.reaction']["Ry"], 'k.', linewidth=2.0, label='FenicsX')


ax_reaction.grid(color='k', linestyle='-', linewidth=0.3)
ax_reaction.set_xlabel('displacement - u $[mm]$' )  
ax_reaction.set_ylabel('reaction force - F $[kN]$')    
ax_reaction.set_title('Reaction')   
ax_reaction.legend() 

###############################################################################
# Convergence
# fig, ax_convergence = plt.subplots() 

# ax_convergence.plot(displacement, result.convergence_files["phasefieldx.conv"].stagger_iter, 'k.', linewidth=2.0, label='Stagger iterations')

# ax_convergence.grid(color='k', linestyle='-', linewidth=0.3)
# ax_convergence.set_xlabel('displacement - u $[mm]$' )  
# ax_convergence.set_ylabel('stagger iterations - []')    
# ax_convergence.set_title('Stagger iterations')   
# ax_convergence.legend() 

plt.show()