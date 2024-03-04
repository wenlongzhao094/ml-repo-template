## Contents of this folder
- Python entry point of an experiment, e.g., `main.py`.
- Bash script to call the python entry script and launch an experiment without reporting to wandb, e.g., `launch.sh`. 
  - This could be useful during debugging.
- `slurm_wandb_agent.py` that submits jobs to slurm, where each job launches a wandb agent. The agent performs a few runs for a wandb hyperparameter sweep and logs outputs to wandb.
  - Configuration files for the sweeps: `*.yaml`. 
  - This is useful once the code is bug-free and we start to run hyperparameter searches.

## Single Run
1. Optionally, use a [tmux session](https://tmuxcheatsheet.com/) so that the run won't get killed if the terminal connection is accidentally closed.
2. Request an interactive session with GPU access. For example:
    ```
    srun --pty --partition gpu-preempt --constraint 2080ti --gres=gpu:1 -c 2 --mem=30GB -t 0-08:00:00 /bin/bash
    ```
    This will allow a single 2080ti GPU, 2 CPUs, and 30GB memory on the compute node for 8 hours.

3. Activate the conda environment installed for this project (see the main README of this repo).
   ```
   module load miniconda/22.11.1-1
   conda activate <env_name>
   ```

4. Config the hyperparameters in `launch.sh` and run it in the srun session with GPU access.
   ```
   bash launch.sh
   ```

## Using wandb to launch a hyperparameter sweep
### Setup
1. Create a wandb account. 
2. Run `wandb login` on the command line; config `wandb/settings`.
3. Add the wandb account and project name as default arguments in `slurm_wandb_agent.py` and `main.py`.

More details are in the documentation: https://docs.wandb.ai/quickstart.

### Launch a sweep
1. Activate your conda environment.
   ```
   module load miniconda/22.11.1-1
   conda activate <env_name>
   ```
2. Create a yaml file `<experiment_id>/<sweep_id>.yaml` to config a hyperparameter sweep. More details are in the documentation: https://docs.wandb.ai/guides/sweeps/define-sweep-configuration.

3. Let wandb create a sweep based on the config.
    ```
    wandb sweep <experiment_id>/<sweep_id>.yaml
    ```
   Note down the returned `SWEEP_ID`. This sweep can now be seen in the wandb web UI also.
4. Submit jobs to slurm, each job launching a wandb agent that performs one or more runs sequentially for the created hyperparameter sweep and logs outputs to wandb. Slurm will assign GPU access to each job. For example:
    ```
    python slurm_wandb_agent.py \
    --sweep_id SWEEP_ID \
    --partition gpu-preempt --constraint 2080ti \
    --n_jobs 2 --n_gpus 1 --n_cpus_per_task 2 --time 1-00:00 --mem 30GB --n_runs 10
    ```
    This requests 2 slurm jobs, each launching a wandb agent to use a 2080ti GPU to sequentially perform 10 runs.
    Thus we have 2x10=20 runs for the sweep, i.e., 20 sets of hyperparameters will be tried.