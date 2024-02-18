### Contents of this folder
- Python entry point of an experiment, e.g., `main.py`.
- Bash script to launch a single experiment without reporting to wandb, e.g., `launch.sh`. This could be useful during debugging.
- Configurations for a hyperparameter sweep via wandb, e.g., `sweep_config*`. These are useful once the code is bug-free and we start to run hyperparameter searches.

### Debug your code
1. Request an interactive session with GPU access. 
E.g. `srun  --partition gpu --gres=gpu:1 -c 2 --mem=40GB -t 0-04:00:00 --pty /bin/bash`. This will allow a single GPU, 2 CPUs, and 40GB memory on the compute node for 4 hours.
2. Activate your conda environment.
   ```
   module load miniconda/22.11.1-1
   conda activate <env_name>
   ```
3. Config the hyperparameters in `launch.sh` and run `bash launch.sh` in the interaction session on a GPU.

### Use wandb to launch a hyperparameter sweep
Create a wandb account. Run `wandb login` on the command line; config `wandb/settings`. Documentation here: https://docs.wandb.ai/quickstart.

1. Create a yaml file to config a hyperparameter sweep: https://docs.wandb.ai/guides/sweeps/define-sweep-configuration. E.g. `sweep_config_experiment_1/exp1_sweep1.yaml`.
2. Run `wandb sweep <experiment_dir>/<config>.yaml` to ask wandb to create a sweep based on the config. Note down the SWEEP_ID that wandb returns.
   This sweep can now be seen in the wandb web UI also.
3. Submit slurm jobs in order that slurm give each job GPU access.
   Each job should launch a wandb agent to perform one or more runs sequentially for the hyperparameter sweep and log outputs to wandb. For example:
   `python slurm_wandb_agent.py
   --wandb_account ACCOUNT_NAME --wandb_project PROJECT_NAME --sweep SWEEP_ID
   --nagents 2 --nruns 10 --partition PARTITION`
   This will result in 2x10=20 runs in the sweep, i.e. 20 sets of hyperparameters will be tried.