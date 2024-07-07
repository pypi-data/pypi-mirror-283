#-------------------------------------------------------------------------------------#
#  Benchmarking suite for non-linear optimization algorithms                          #
#                                                                                     #
#  Author: Ahmed H. Bayoumy                                                           #
#  email: ahmed.bayoumy@mail.mcgill.ca                                                #
#                                                                                     #
#  This program is free software: you can redistribute it and/or modify it under the  #
#  terms of the GNU Lesser General Public License as published by the Free Software   #
#  Foundation, either version 3 of the License, or (at your option) any later         #
#  version.                                                                           #
#                                                                                     #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY    #
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A    #
#  PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.   #
#                                                                                     #
#  You should have received a copy of the GNU Lesser General Public License along     #
#  with this program. If not, see <http://www.gnu.org/licenses/>.                     #
#                                                                                     #
#  You can find information on OMADS at                                               #
#  https://github.com/Ahmed-Bayoumy/NOBM                                              #
# ------------------------------------------------------------------------------------#

from DMDO import *
import math
import numpy as np
from numpy import cos, exp, pi, sin, sqrt
import copy
from typing import List

user =USER



def Sellar_A1(x):
  return x[0] + x[1]**2 + x[2] - 0.2*x[3]

def Sellar_A2(x):
  return x[0] + x[1] + np.sqrt(x[2]) 

def Sellar_opt1(x, y):
  return [x[0]**2 + x[2] + y[0] + np.exp(-x[3]), [3.16-y[0]]]

def Sellar_opt2(x, y):
  return [0., [y[0]-24.]]

def Run():
  #  Sellar - Two discipline problem with IDF

  #  Variables grouping and problem setup
  x = {}
  X: List[variableData] = []
  # Define variable names
  N = ["x", "z1", "z2", "y1", "y2", "z1", "z2", "y1", "y2"]
  nx: int = len(N)
  # Subproblem indices: Indices should be non-zero
  J = [1,1,1,1,1,2,2,2,2]
  # Subproblems links
  L = [None, 2, 2, 2, 2, 1, 1, 1, 1]
  # Coupling types
  Ct = [COUPLING_TYPE.UNCOUPLED, 
        COUPLING_TYPE.SHARED, 
        COUPLING_TYPE.SHARED,
        COUPLING_TYPE.FEEDFORWARD, 
        COUPLING_TYPE.FEEDBACK, 
        COUPLING_TYPE.SHARED,
        COUPLING_TYPE.SHARED, 
        COUPLING_TYPE.FEEDBACK,
        COUPLING_TYPE.FEEDFORWARD]
  # Realistic lower bounds
  lb = [0, -10, 0, 3.16, 1.77763888346, -10, 0, 3.16, 1.77763888346]
  # Realistic upper bounds
  ub = [10.,10.,10., 115.2, 24., 10.,10., 115.2, 24.]

  # # Artificial lower bounds
  # lb = [0, -10, 0, 2., 1.5, -10, 0, 2., 1.5]
  # # Artificial upper bounds
  # ub = [10.,10.,10., 50., 50, 10.,10., 50., 50]

  # Bad artificial lower bounds
  # lb = [0, -10, 0, 0., 0., -10, 0, 0., 0.]
  # Bad artificial upper bounds
  # ub = [10.]*9

  # Baseline
  x0 = [0., 5., 5., 8.43, 7.848, 5., 5., 8.43, 7.848]
  # Scaling
  scaling = np.subtract(ub,lb)
  Qscaling = []
  # Create a dictionary for each variable
  for i in range(nx):
    x[f"var{i+1}"] = {"index": i+1,
    "sp_index": J[i],
    f"name": N[i],
    "dim": 1,
    "value": 0.,
    "coupling_type": Ct[i],
    "link": L[i],
    "baseline": x0[i],
    "scaling": scaling[i],
    "lb": lb[i],
    "value": x0[i],
    "ub": ub[i]}
    Qscaling.append(10./scaling[i] if 10./scaling[i] != np.inf and 10./scaling[i] != np.nan else 1.)

  # Instantiate the variableData class for each variable using its according dictionary
  for i in range(nx):
    X.append(variableData(**x[f"var{i+1}"]))


  # Analyses setup; construct disciplinary analyses
  DA1: process = DA(inputs=[X[0], X[1], X[2], X[4]],
  outputs=[X[3]],
  blackbox=Sellar_A1,
  links=2,
  coupling_type=COUPLING_TYPE.FEEDFORWARD
  )

  DA2: process = DA(inputs=[X[5], X[6], X[7]],
  outputs=[X[8]],
  blackbox=Sellar_A2,
  links=1,
  coupling_type=COUPLING_TYPE.FEEDFORWARD
  )

  sp1_MDA: process = MDA(nAnalyses=1, analyses = [DA1], variables=[X[0], X[1], X[2], X[4]], responses=[X[3]])
  sp2_MDA: process = MDA(nAnalyses=1, analyses = [DA2], variables=[X[5], X[6], X[7]], responses=[X[8]])


  # Construct the coordinator
  coord = ADMM(beta = 1.3,
  nsp=2,
  budget = 500,
  index_of_master_SP=1,
  display = True,
  scaling = Qscaling,
  mode = "serial",
  M_update_scheme= w_scheme.MAX,
  store_q_io=True
  )

  # Construct subproblems
  sp1 = SubProblem(nv = 4,
  index = 1,
  vars = [X[0], X[1], X[2], X[4]],
  resps = [X[3]],
  is_main=1,
  analysis= sp1_MDA,
  coordination=coord,
  opt=Sellar_opt1,
  fmin_nop=np.inf,
  budget=10,
  display=False,
  psize = 1.,
  pupdate=PSIZE_UPDATE.LAST,
  freal=3.160,
  solver="scipy")

  sp2 = SubProblem(nv = 3,
  index = 2,
  vars = [X[5], X[6], X[7]],
  resps = [X[8]],
  is_main=0,
  analysis= sp2_MDA,
  coordination=coord,
  opt=Sellar_opt2,
  fmin_nop=np.inf,
  budget=10,
  display=False,
  psize = 1.,
  pupdate=PSIZE_UPDATE.LAST
  )

  MDAO: MDO = MDO(
  Architecture = MDO_ARCHITECTURE.IDF,
  Coordinator = coord,
  subProblems = [sp1, sp2],
  variables = X,
  responses = [X[3], X[8]],
  fmin = np.inf,
  hmin = np.inf,
  display = True,
  inc_stop = 1E-9,
  stop = "Iteration budget exhausted",
  tab_inc = [],
  noprogress_stop = 1000
  )

  # Run the MDO problem
  out = MDAO.run()

  # Print summary output
  print(f'------Run_Summary------')
  print(MDAO.stop)
  print(f'q = {MDAO.Coordinator.q}')
  for i in MDAO.Coordinator.master_vars:
    print(f'{i.name}_{i.sp_index} = {i.value}')

  fmin = 0
  hmax = -np.inf
  for j in range(len(MDAO.subProblems)):
    print(f'SP_{MDAO.subProblems[j].index}: fmin= {MDAO.subProblems[j].MDA_process.getOutputs()}, hmin= {MDAO.subProblems[j].opt([s.value for s in MDAO.subProblems[j].get_design_vars()] , MDAO.subProblems[j].MDA_process.getOutputs())[1]}')
    fmin += sum(MDAO.subProblems[j].MDA_process.getOutputs())
    hmin= MDAO.subProblems[j].opt([s.value for s in MDAO.subProblems[j].get_design_vars()] , MDAO.subProblems[j].MDA_process.getOutputs())[1]
    if max(hmin) > hmax: 
      hmax = max(hmin) 
  print(f'P_main: fmin= {fmin}, hmax= {hmax}')
  print(f'Final obj value of the main problem: \n {fmin}')

