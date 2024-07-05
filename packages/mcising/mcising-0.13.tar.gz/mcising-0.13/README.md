# mcising

mcising is a Python package for generating Ising model data using Metropolis algorithm. It works for square lattices, and for nearest neighbor and next nearest neighbor interactions. The Monte-Carlo method it uses, has the cool-down approach to avoid semi stable states.

## Installation

You can install the package using pip:

`pip install mcising`

## Usage

You can generate Ising model data from the command line:

`generate_ising_data <seed> <lattice_size> <num_configs> <j1> <j2> [--T_init <T_init>] [--T_final <T_final>] [--T_step <T_step>] [--sweep_steps <sweep_steps>] [--thermalization_scans <thermalization_scans>] [--calculate_correlation]`

`seed`: the random seed for reproducibility

`lattice_size`: the system size L of the square lattice LxL

`num_configs`: number of configurations to be saved per temperature

`j1` and `j2`: the interaction strengths, `j1` for nearest neighbor and `j2` for next nearest neighbor

`T_init` and `T_final`: initial and final temperatures, initial being higher

`T_step`: the step in between each temperature point

`sweep_steps`: number of Monte-Carlo sweeps per step

`thermalization_scans`: number of sweeps on each temperature step to ensure thermalization

`calculate_correlation`: option to select if correlation function and correlation length should be calculated, since they are time consuming.

An example usage:

```console
generate_ising_data 42 10 100 1.0 0.5 --T_init 4.0 --T_final 0.1 --T_step 0.05 --sweep_steps 10 --thermalization_scans 5 --calculate_correlation
```

An example of the output console:

```
..1 / 11 samples saved.
2 / 11 samples saved.
3 / 11 samples saved.
4 / 11 samples saved.
5 / 11 samples saved.
6 / 11 samples saved.
7 / 11 samples saved.
8 / 11 samples saved.
9 / 11 samples saved.
10 / 11 samples saved.
11 / 11 samples saved.
For temperature= 1.0, MC simulation executed in: 0.43 seconds
.1 / 11 samples saved.
2 / 11 samples saved.
3 / 11 samples saved.
4 / 11 samples saved.
5 / 11 samples saved.
6 / 11 samples saved.
7 / 11 samples saved.
8 / 11 samples saved.
9 / 11 samples saved.
10 / 11 samples saved.
11 / 11 samples saved.
For temperature= 1.0, MC simulation executed in: 0.18 seconds
```

Example output png files:

<img src="mcising/imgs/SQ_L_30_J1_1.000_J2_0.650_h_0.000_T_4.000_s_1149_n_0.png" width="100">
<img src="mcising/imgs/SQ_L_30_J1_1.000_J2_0.000_h_0.000_T_2.350_s_3985_n_0.png" width="100">
<img src="mcising/imgs/SQ_L_30_J1_1.000_J2_0.000_h_0.000_T_0.100_s_8394_n_1000.png" width="100">

Structure of the saved pickle files:

```
data_sample = {
    'configuration': np.ndarray,  # The lattice configuration (2D array of spins)
    'energy': float,              # The energy of the configuration
    'magnetization': float,       # The magnetization of the configuration
    'correlation_length': float,  # The correlation length (if calculated)
    'correlation_function': np.ndarray,  # The correlation function values (if calculated)
    'distances': np.ndarray       # The distances corresponding to the correlation function values (if calculated)
}
```

### Detailed Description of Each Key

- **configuration**: A 2D NumPy array representing the lattice configuration, where each element is a spin (-1 or 1).

  - Type: `np.ndarray`
  - Shape: `(lattice_size, lattice_size)`

- **energy**: A float representing the energy of the current lattice configuration.

  - Type: `float`

- **magnetization**: A float representing the net magnetization of the current lattice configuration.

  - Type: `float`

- **correlation_length**: A float representing the correlation length of the lattice. This is only present if correlation calculations are enabled.

  - Type: `float`
  - Note: This key is `None` if correlation calculations are not performed.

- **correlation_function**: A 1D NumPy array representing the values of the correlation function. This is only present if correlation calculations are enabled.

  - Type: `np.ndarray`
  - Shape: `(num_distances,)`
  - Note: This key is `None` if correlation calculations are not performed.

- **distances**: A 1D NumPy array representing the distances corresponding to the correlation function values. This is only present if correlation calculations are enabled.
  - Type: `np.ndarray`
  - Shape: `(num_distances,)`
  - Note: This key is `None` if correlation calculations are not performed.

## Licence

This project is licensed under the MIT License.
