import hiperwalk as hpw
import numpy as np

dim = 21
lat = hpw.Grid(dim, diagonal=True)
center = np.array([dim//2,dim//2])
dtqw = hpw.Coined(lat, shift='persistent', coin='grover')
psi0 = dtqw.state([[0.5, (center, center + (1, 1))],
                  [-0.5, (center, center + (1, -1))],
                  [-0.5, (center, center + (-1, 1))],
                  [0.5, (center, center + (-1, -1))]])
psi_final = dtqw.simulate(time=dim // 2, initial_state=psi0, hpc=None)
prob = dtqw.probability_distribution(psi_final)
hpw.plot_probability_distribution(prob, graph=lat)
