## Contents of this folder
- Python entry point of an experiment, e.g., `main.py`.
- Bash script to launch a single experiment without reporting to wandb, e.g., `launch.sh`. 
  - This could be useful during debugging.
- `slurm_wandb_agent.py` that submits jobs to slurm, where each job launches a wandb agent. The agent performs a few runs for a wandb hyperparameter sweep and logs outputs to wandb.
  - Configuration files for the sweeps: `sweep_config*`. 
  - These are useful once the code is bug-free and we start to run hyperparameter searches.

## Debug your code
1. Request an interactive session with GPU access. For example:
    ```
    srun  --partition gpu --gres=gpu:1 -c 2 --mem=40GB -t 0-04:00:00 --pty /bin/bash
    ```
    This will allow a single GPU, 2 CPUs, and 40GB memory on the compute node for 4 hours.

2. Activate your conda environment.
   ```
   module load miniconda/22.11.1-1
   conda activate <env_name>
   ```

3. Config the hyperparameters in `launch.sh` and run `bash launch.sh` in the interaction session on a GPU.

## Use wandb to launch a hyperparameter sweep
### Setup
1. Create a wandb account. 
2. Run `wandb login` on the command line; config `wandb/settings`.
3. Add the wandb account and project name as default arguments in `slurm_wandb_agent.py`.

More details are in the documentation: https://docs.wandb.ai/quickstart.

### Launch a sweep
1. Activate your conda environment.
   ```
   module load miniconda/22.11.1-1
   conda activate <env_name>
   ```
2. Create a yaml file to config a hyperparameter sweep, e.g. `sweep_config_experiment_1/exp1_sweep1.yaml`. More details are in the documentation: https://docs.wandb.ai/guides/sweeps/define-sweep-configuration.

3. Let wandb create a sweep based on the config. Note down the returned `SWEEP_ID`. This sweep can now be seen in the wandb web UI also.
    ```
    wandb sweep <sweep_configs>/<sweep>.yaml
    ```

4. Submit jobs to slurm; slurm can assign GPU access to the jobs. Each job launches a wandb agent that performs one or more runs sequentially for the hyperparameter sweep and logs outputs to wandb. For example:
    ```
    python slurm_wandb_agent.py --sweep_id SWEEP_ID \
    --partition gypsum-titanx --exclude gypsum-gpu122,gypsum-gpu124 \
    --n_agents 2 --n_runs 10 --n_gpus 1
    ```
    This will result in 2x10=20 runs in the sweep, i.e. 20 sets of hyperparameters will be tried.