"""
.. _fatigue_single_edge_notched_tension_test_isotropic:

Fatigue: Single edge notched tension test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A well-known benchmark simulation in fracture mechanics is performed, relying on the simulation conducted by [Carrara]_. This simulation considers an isotropic formulation.

The model consists of a square plate with a notch located halfway up, extending from the left to the center, as shown in the figure below. The bottom part is fixed in all directions, while the upper part can slide vertically. A vertical displacement is applied at the top. The geometry and boundary conditions are depicted in the figure. We discretize the model with triangular elements, refining the areas (element size h) where crack evolution is expected. The element size h must be sufficiently small to avoid mesh dependencies.

A cyclic tensile test is conducted. A symmetric cyclic load is applied with a displacement amplitude of $\Delta u = 4 \times 10^{-3} mm$. The results are presented in terms of the accumulation of the fatigue history variable $\alpha$ versus the number of cycles N (fatigue life curves).

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
   


+----------+---------+--------+
|          | VALUE   | UNITS  |
+==========+=========+========+
| E        | 210     | kN/mm2 |
+----------+---------+--------+
| nu       | 0.3     | [-]    |
+----------+---------+--------+
| Gc       | 0.0027  | kN/mm2 |
+----------+---------+--------+
| l        | 0.004   | mm     |
+----------+---------+--------+
| alpha_n  | 0.05625 | kN/mm2 |
+----------+---------+--------+

.. [Carrara] A framework to model the fatigue behavior of brittle materials based on a variational phase-field approach. P. Carrara, M. Ambati, R. Alessi, L. De Lorenzis. https://doi.org/10.1016/j.cma.2019.112731.

"""

print(1)
# ###############################################################################
# # Import necessary libraries
# # --------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# import pyvista as pv
# import dolfinx
# import mpi4py 
# import petsc4py
# import os


# ###############################################################################
# # Import from phasefieldx package
# # -------------------------------
# from phasefieldx.Element.Phase_Field_Fracture.Input import Input
# from phasefieldx.Element.Phase_Field_Fracture.solver.solver import solve
# from phasefieldx.Boundary.boundary_conditions import bc_xy, bc_y, get_ds_bound_from_marker
# from phasefieldx.PostProcessing.ReferenceResult import AllResults




# ###############################################################################
# # Parameters definition

# Data = Input(E=210.0,    # young modulus
#              nu=0.3,     # poisson
#              Gc=0.0027,  # critical energy release rate
#              l=0.004,    # lenght scale parameter
#              degradation="isotropic",  # "isotropic" "anisotropic"
#              split_energy="no",        # "spectral" "deviatoric"
#              degradation_function="quadratic",
#              irreversibility="miehe",  # "miehe"
#              fatigue=True,
#              fatigue_degradation_function="asymptotic",
#              fatigue_val=0.05625,
#              k=0.0,
#              min_stagger_iter=2,
#              max_stagger_iter=500,
#              stagger_error_tol=1e-8,
#              save_solution_xdmf=False,
#              save_solution_vtu=True,
#              results_folder_name="1800_Single_Edge_Notched_Tension_Test")

# # ey= np.sqrt(Data.Gc/(2*Data.l*Data.E))
# # Data.fatigue_val =   0.05625 # 0.5*ey*Data.E*ey 


# ###############################################################################
# # Mesh Definition
# # ---------------
# msh_file = os.path.join("mesh", "mesh.msh")
# gdim = 2
# gmsh_model_rank = 0
# mesh_comm = mpi4py.MPI.COMM_WORLD

# msh, cell_markers, facet_markers = dolfinx.io.gmshio.read_from_msh(msh_file, mesh_comm, gmsh_model_rank, gdim)

# fdim = msh.topology.dim - 1

# bottom_facet_marker = facet_markers.find(9)
# top_facet_marker    = facet_markers.find(10)
# right_facet_marker  = facet_markers.find(11)
# left_facet_marker   = facet_markers.find(12)

# ds_bottom = get_ds_bound_from_marker(bottom_facet_marker, msh, fdim)
# ds_top = get_ds_bound_from_marker(top_facet_marker, msh, fdim)
# ds_right = get_ds_bound_from_marker(right_facet_marker, msh, fdim)
# ds_left = get_ds_bound_from_marker(left_facet_marker, msh, fdim)

# ds_list = np.array([
#                    [ds_bottom, "bottom"],
#                    [ds_top,    "top"]
#                    ])


# ###############################################################################
# # Function Space Definition
# # -------------------------
# # Define function spaces for displacement and phase-field using Lagrange elements.
# V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
# V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))


# ###############################################################################
# # Boundary Conditions
# # -------------------
# # Apply boundary conditions: bottom nodes fixed in both directions, top nodes can slide vertically.
# bc_bottom = bc_xy(bottom_facet_marker, V_u, fdim)
# bc_top    = bc_y(top_facet_marker, V_u, fdim)
# bcs_list_u = [bc_top, bc_bottom]

# amplitude = 0.002
# f = 1/8
# w= 2*np.pi*f

# def update_boundary_conditions(bcs, time):
#     val =2/np.pi * amplitude  * np.arcsin(np.sin(w * time))
#     bcs[0].g.value[...] = petsc4py.PETSc.ScalarType(val)
#     return 0, val, 0

# #dt = 1
# #t = np.arange(0, 8*200+1, 1)
# #f = 1/8
# #w= 2*np.pi*f
# #amplitude = 0.002
# #values = 2/np.pi * amplitude  * np.arcsin( np.sin(w * t) )
# #steps=t

# #def update_boundary_conditions(bcs, step):
# #    bcs[0].g.value[1] = petsc4py.PETSc.ScalarType(values[step])
# #    return 0, values[step]

# T_list_u = None 
# update_loading = None

# ###############################################################################
# # Boundary Conditions four phase field
# bcs_list_phi=[]

# ###############################################################################
# # Call the Solver
# # ---------------
# # The problem is solved. The solver will handle the mesh, boundary conditions,
# # and the given parameters to compute the solution.

# dt = 1.0
# final_time = 8*200+1

# # solve(Data,
# #       msh, 
# #       final_time,
# #       V_u,
# #       V_phi,
# #       bcs_list_u,
# #       bcs_list_phi,
# #       update_boundary_conditions,
# #       f, 
# #       T_list_u,
# #       update_loading, 
# #       ds_list,
# #       dt,
# #       path=None)


# ###############################################################################
# # Load results
# # ------------
# # Once the simulation finishes, the results are loaded from the results folder.
# # The AllResults class takes the folder path as an argument and stores all
# # the results, including logs, energy, convergence, and DOF files.
# # Note that it is possible to load results from other results folders to compare results.
# # It is also possible to define a custom label and color to automate plot labels.
# S = AllResults(Data.results_folder_name)
# S.set_label('Simulation')
# S.set_color('b')


# ###############################################################################
# # Plot solutions
# cycles = S.dof_files["top.dof"]["#step"]*f

# displacement = S.dof_files["top.dof"]["Uy"]


# Lorenzis_solution_gamma = np.loadtxt(os.path.join("reference_solutions", "isotropic.csv"))
# fig, ax_r = plt.subplots() 
# ax_r.plot(Lorenzis_solution_gamma[:, 0], Lorenzis_solution_gamma[:, 1], 'b-', linewidth=2.0,  label = 'Lorenzis Isotropic')
# #ax_r.plot(Lorenzis_spec[:, 0], Lorenzis_spec[:, 1], 'r-', linewidth=2.0, label = 'Lorenzis Spectral')
# ax_r.plot(cycles, S.energy_files["total.energy"]["gamma"], 'r.', linewidth=2.0, label='gamma')
# # ax_r.plot(cycles, S.energy_files["total.energy"].gamma_phi, 'g.', linewidth=2.0, label='gamma_phi')
# # ax_r.plot(cycles, S.energy_files["total.energy"].gamma_gradphi, 'y.', linewidth=2.0, label='gamma_gradphi')

# ax_r.grid(color='k', linestyle='-', linewidth=0.3)
# ax_r.set_xlabel('cycles' )  
# ax_r.set_ylabel('crack')    
# ax_r.set_title('crack')   
# ax_r.legend()

# # ###############################################################################
# # # Gamma
# # fig, ax_gamma = plt.subplots() 

# # ax_gamma.plot(cycles, result.energy_files["total.energy"].gamma, 'k.', linewidth=2.0, label='gamma')
# # ax_gamma.plot(cycles, result.energy_files["total.energy"].gamma_phi, 'r.', linewidth=2.0, label='gamma_phi')
# # ax_gamma.plot(cycles, result.energy_files["total.energy"].gamma_gradphi, 'b.', linewidth=2.0, label='gamma_gradphi')

# # ax_gamma.grid(color='k', linestyle='-', linewidth=0.3)
# # ax_gamma.set_xlabel('displacement - u $[mm]$' )  
# # ax_gamma.set_ylabel('Gamma')    
# # ax_gamma.set_title('Gamma')   
# # ax_gamma.legend() 

# # ###############################################################################
# # # Energy
# # fig, ax_EW = plt.subplots() 

# # #ax_EW.plot(cycles, result.energy_files["total.energy"].EW, 'g-', linewidth=2.0, label='E+W')
# # ax_EW.plot(cycles, result.energy_files["total.energy"].W, 'k.', linewidth=2.0, label='W')
# # #ax_EW.plot(cycles, result.energy_files["total.energy"].E, 'y.', linewidth=2.0, label='E')

# # ax_EW.grid(color='k', linestyle='-', linewidth=0.3)
# # ax_EW.set_xlabel('displacement - u $[mm]$' )  
# # ax_EW.set_ylabel('energy')    
# # ax_EW.set_title('ENERGY')   
# # ax_EW.legend() 


# # ###############################################################################
# # # Reaction forces
# # fig, ax_reaction = plt.subplots() 
# # ax_reaction.plot(cycles, result.reaction_files["top.reaction"].y, 'k.', linewidth=2.0, label='FenicsX')

# # ax_reaction.grid(color='k', linestyle='-', linewidth=0.3)
# # ax_reaction.set_xlabel('cycles -  $[-]$' )  
# # ax_reaction.set_ylabel('reaction force - F $[kN]$')    
# # ax_reaction.set_title('Reaction')   
# # ax_reaction.legend() 

# # # Reaction forces
# # fig, ax_reactionu = plt.subplots() 
# # ax_reactionu.plot(displacement, result.reaction_files["top.reaction"].y, 'k.', linewidth=2.0, label='FenicsX')

# # ax_reactionu.grid(color='k', linestyle='-', linewidth=0.3)
# # ax_reactionu.set_xlabel('displacement - u $[mm]$' )  
# # ax_reactionu.set_ylabel('reaction force - F $[kN]$')    
# # ax_reactionu.set_title('Reaction')   
# # ax_reactionu.legend() 

# ###############################################################################
# # Convergence
# fig, ax_convergence = plt.subplots() 

# ax_convergence.plot(cycles, S.convergence_files["phasefieldx.conv"]["stagger"], 'k.', linewidth=2.0, label='Stagger iterations')

# ax_convergence.grid(color='k', linestyle='-', linewidth=0.3)
# ax_convergence.set_xlabel('displacement - u $[mm]$' )  
# ax_convergence.set_ylabel('stagger iterations - []')    
# ax_convergence.set_title('Stagger iterations')   
# ax_convergence.legend() 


# ###############################################################################
# # Cycles- uy
# fig, ax = plt.subplots() 
# ax.plot(cycles[0:2*8+1], S.dof_files["top.dof"]["Uy"][0:2*8+1], '-')
# ax.grid(color='k', linestyle='-', linewidth=0.3)
# ax.set_xlabel('cycles' )   
# ax.set_ylabel('displacement')    
# ax.set_title('Steps')   
# ax.legend() 

# ###############################################################################
# # alpha_acum
# Lorenzis_solution = np.loadtxt(os.path.join("reference_solutions", "isotropic_alpha.csv"))

# fig, ax_alpha = plt.subplots() 

# ax_alpha.plot(Lorenzis_solution[:,0], Lorenzis_solution[:,1], 'b-', linewidth=2.0, label='De Lorenzis')
# # ax_alpha.plot(cycles, S.energy_files["total.energy"]["alpha_acum"], 'r.', linewidth=2.0, label = S.label)

# aux2= max(S.energy_files["total.energy"]["alpha_acum"][:3*8]) 
# ax_alpha.plot(cycles[:3*8], S.energy_files["total.energy"]["alpha_acum"][:3*8]/aux2*max(Lorenzis_solution[:,1]), 'r.', linewidth=2.0, label='alpha')

# ax_alpha.grid(color='k', linestyle='-', linewidth=0.3)
# ax_alpha.set_xlabel('cycles' )  
# ax_alpha.set_ylabel(r'$\bar{\alpha}$')    
# ax_alpha.set_title(r'alpha bar vs number of cycles')   
# ax_alpha.legend()


# plt.show()
