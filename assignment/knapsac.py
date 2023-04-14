import numpy as np

def total_valu_size(packing, valus, sizes, max_size):
  """
  Returns the total value and size of a specified packing, where a packing is a list of 1s and 0s indicating whether an
  item is included in the knapsack or not. If the size of the packing exceeds the maximum allowed size, the total value
  is set to 0.

  Parameters:
  packing (list): A list of 1s and 0s indicating whether an item is included in the knapsack or not
  valus (list): A list of values for each item
  sizes (list): A list of sizes for each item
  max_size (float): The maximum size of the knapsack

  Returns:
  tuple: A tuple containing the total value and size of the specified packing

  """
  # total value and size of a specified packing
  v = 0.0  # total valu of packing
  s = 0.0  # total size of packing
  n = len(packing)# number of items in the packing
  # iterate over each item in the packing
  for item in range(n):
    if packing[item] == 1:
       # if the item is packed, add its value and size to the totals
      v += valus[item]
      s += sizes[item]

  # if the total size exceeds the maximum allowed size, the packing is invalid   
  if s  > max_size:  # too big to fit in knapsack
    v = 0.0

  return (v, s) # return a tuple containing the total value and size of the packing

def adjacent(packing, rnd):
  """
  Generates an adjacent packing by flipping the value of a randomly chosen item in the packing (i.e., if an item is
  included in the knapsack, it is removed; if it is not included, it is added).
  
  Parameters:
  packing (list): A list of 1s and 0s indicating whether an item is included in the knapsack or not
  rnd (numpy.random.Generator): A random number generator
  
  Returns:
  list: A new packing that is adjacent to the original packing
  
  """ 
  # Initialize variables
  n = len(packing) # number of items in the packing  
  # make a copy of the current packing
  result = np.copy(packing)   
  
  i = rnd.randint(n) # pick a random index i between 0 and n-1
  # if the item at index i is not in the packing
  # add it to the packing
  if result[i] == 0:          
    result[i] = 1     
    # if the item at index i is in the packing 
    #  # remove it from the packing      
  elif result[i] == 1:        
    result[i] = 0           
  return result # return the modified packing

def solve(n_items, rnd, valus, sizes, max_size, max_iter, start_temperature, alpha):
  """
  Solves the knapsack problem using simulated annealing.

  Parameters:
  n_items (int): The number of items to be included in the knapsack
  rnd (numpy.random.Generator): A random number generator object
  valus (list): A list of values for each item in the knapsack
  sizes (list): A list of sizes for each item in the knapsack
  max_size (float): The maximum size of the knapsack
  max_iter (int): The maximum number of iterations for the simulated annealing algorithm
  start_temperature (float): The starting temperature for the simulated annealing algorithm
  alpha (float): The cooling rate for the simulated annealing algorithm

  Returns:
  list: A list of 1s and 0s indicating which items should be included in the knapsack

  """
  
  # Initialize the current temperature to the starting temperature and set the initial packing to include all items.
  curr_temperature = start_temperature
  curr_packing = np.ones(n_items, dtype=np.int64)
  print("Initial guess: ")
  print(curr_packing)

  # Calculate the value and size of the current packing using the `total_valu_size()` function.
  (curr_valu, curr_size) = total_valu_size(curr_packing, valus, sizes, max_size)

  # Set the initial iteration to zero and calculate the iteration interval for printing updates.
  iteration = 0
  interval = (int)(max_iter / 10)

  # Run the simulated annealing algorithm until the maximum number of iterations is reached.
  while iteration < max_iter:
    # Generate an adjacent packing by calling the `adjacent()` function.
    adj_packing = adjacent(curr_packing, rnd)
    (adj_v, _) = total_valu_size(adj_packing, valus, sizes, max_size)

    # If the adjacent packing is better, accept it.
    if adj_v  > curr_valu:
      curr_packing = adj_packing
      curr_valu = adj_v

    # If the adjacent packing is worse, accept it with a certain probability based on the temperature.
    else:
      accept_p = np.exp( (adj_v - curr_valu ) / curr_temperature ) 
      p = rnd.random()
      if p < accept_p:
        curr_packing = adj_packing
        curr_valu = adj_v 

    # Print out an update every `interval` iterations.
    if iteration % interval == 0:
      print("iter = %6d : curr value = %7.0f : curr temp = %10.2f " % (iteration, curr_valu, curr_temperature))

    # Decrease the temperature by the cooling rate `alpha` and increment the iteration counter.
    curr_temperature *= alpha
    iteration += 1

  # Return the final packing of the knapsack.
  return curr_packing
    

def main():
  print("\nBegin knapsack simulated annealing demo ")
  print("Goal is to maximize value subject \
    to max size constraint ")

  valus = np.array([79, 32, 47, 18, 26, 85, 33, 40, 45, 59])
  sizes = np.array([85, 26, 48, 21, 22, 95, 43, 45, 55, 52])
  max_size = 101

  print("\nItem values: ")
  print(valus)
  print("\nItem sizes: ")
  print(sizes)
  print("\nMax total size = %d " % max_size)

  rnd = np.random.RandomState(5)  # 3 .98 = 117,100
  max_iter = 1000
  start_temperature = 10000.0
  alpha = 0.98

  print("\nSettings: ")
  print("max_iter = %d " % max_iter)
  print("start_temperature = %0.1f " \
    % start_temperature)
  print("alpha = %0.2f " % alpha)

  print("\nStarting solve() ")
  packing = solve(10, rnd, valus, sizes, 
    max_size, max_iter, start_temperature, alpha)
  print("Finished solve() ")

  print("\nBest packing found: ")
  print(packing)
  (v,s) = \
    total_valu_size(packing, valus, sizes, max_size)
  print("\nTotal value of packing = %0.1f " % v)
  print("Total size  of packing = %0.1f " % s)

  print("\nEnd demo ")

if __name__ == "__main__":
  main()