import random
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot as plt
from matplotlib import cm
from celluloid import Camera
from IPython.display import HTML, display

def single_particle(t):
	positions=[]
	x=0
	for i in range(t+1):
		positions.append(x)
		x += random.choice((-1,1))
	return np.array(positions)

def simulate(n_gen, n_part):

	sim = []
	for particle in range(n_part):
		sim.append(single_particle(n_gen))
	sim = np.array(sim)
	return sim

def plot_table(sim):
	n_particules, duree = sim.shape

	display_times = np.int32(np.linspace(0,duree-1,3))

	columns = [f't={t}' for t in range(duree)]
	index = [f'x_{i+1}' for i in range(n_particules)]

	return DataFrame(sim, index=index, columns=columns).T.iloc[display_times]

def plot_sim(sim, variable):

	if variable not in [1,2]:
		print('ERREUR: la variable y doit être égale a 1 ou 2.')

	else:
		n_particules, duree = sim.shape
		T = np.arange(sim.shape[1])

		nbins = np.int32(np.floor(duree/2))
		if nbins > 25:
		    nbins = 25
		tp = np.int32(np.linspace(0, duree, nbins))

		fig, (ax0, ax1) = plt.subplots(figsize=[13,6], ncols=2, gridspec_kw={'wspace':0.3})
		fig.patch.set_facecolor('white')
		fig.text(0.5, 0.97, f'{n_particules} particules, durée: {duree-1}', ha='center', va='top', size=30)
		cam = Camera(fig)

		ylim = 1.1*np.abs(sim.max()) * np.array([-1,1])
		ax0.set_facecolor('0.95')
		ax0.set_xlabel(r'Temps $t$ (secondes)', size=20)
		ax0.set_ylabel(r'Position $x$', size=20)
		ax0.set_ylim(ylim)

		ax1.set_facecolor('0.95')
		ax1.set_xlabel(r'Temps $t$ (secondes)', size=20)

		c = [cm.viridis(i) for i in np.linspace(0, 1, n_particules)]

		if variable == 1:
		    ax1.set_ylabel(r'Moyenne $\overline{x}$', size=20)
		    ax1.set_ylim(ylim)
		    values = np.apply_along_axis(lambda x: np.mean(x), 0, sim)
		    def add_baseline():
		        ax1.axhline(0, lw=0.5, c='k')

		if variable == 2:
		    ax1.set_ylabel(r'Variance $\overline{x^2}$', size=20)
		    values = np.apply_along_axis(lambda x: np.mean(x**2), 0, sim)
		    def add_baseline():
		        ax1.plot([0,duree], [0, duree], lw=0.5, c='k')

		for t in tp:
		    for i, x in enumerate(sim):
		        ax0.plot(T[:t], x[:t], alpha=0.5, lw=1, c=c[i])

		    add_baseline()
		    ax1.plot(T[:t], values[:t], c='k')

		    cam.snap()

		animation = cam.animate()

		display(HTML(animation.to_jshtml()))
		plt.close()
