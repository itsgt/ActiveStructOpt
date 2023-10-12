from bayes_opt import BayesianOptimization
import numpy as np

def bayesian_optimization(optfunc, args, exp, starting_structure, N, nrandom = 10):
  def construct_structure(**kwargs):
    structure = starting_structure.copy()
    x = list(kwargs.values())
    for i in range(len(structure)):
      structure.sites[0].coords = structure.lattice.get_cartesian_coords(
          x[(3 * i):(3 * i + 3)])
    return structure

  def msefunc(**kwargs):
    th = optfunc(construct_structure(**kwargs), **(args))
    mse = np.mean((th - exp) ** 2)
    return -mse

  pbounds = {}
  for i in range(len(starting_structure)):
    for j in range(3):
      pbounds['x' + str(i + 1) + str(j + 1)] = (0, 1)
  
  optimizer = BayesianOptimization(
      f = msefunc,
      pbounds = pbounds,
      random_state = 1,
      verbose = 0,
  )

  optimizer.maximize(init_points = nrandom, n_iter = N - nrandom)

  structures = [construct_structure(**iter['params']) for iter in optimizer.res]
  mses = [-iter['target'] for iter in optimizer.res]
  return structures, mses