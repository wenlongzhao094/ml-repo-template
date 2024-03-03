"""
wandb sweep <sweep_configs>/<sweep>.yaml  # log the generated SWEEP_ID
python slurm_wandb_agent.py --sweep_id SWEEP_ID \
--partition gypsum-titanx --exclude gypsum-gpu122,gypsum-gpu124 \
--n_agents 2 --n_runs 10 --n_gpus 1
"""

import argparse, os, json

parser = argparse.ArgumentParser(description="Launch a slurm job to run a wandb agent")
parser.add_argument("--wandb_account", type=str, default="wandb_account_name") # TODO: set the default
parser.add_argument("--wandb_project", type=str, default="wandb_project_name") # TODO: set the default
parser.add_argument("--sweep_id", type=str, required=True, help="sweep id created by wandb")
parser.add_argument("--partition", type=str, required=True, help="gpu partition name")
parser.add_argument("--constraint", type=str, default=None, help="constraint on the assigned GPU")
parser.add_argument("--exclude", type=str, default=None, help="comma-separated nodes to exclude, e.g. node001,node010")
parser.add_argument("--n_agents", type=int, default=1, help="number of agents for the sweep")
parser.add_argument("--n_runs", type=int, default=10, help="number of runs per agent")
parser.add_argument("--n_gpus", type=int, default=1, help="number of gpus per agent")
parser.add_argument("--n_cpus", type=int, default=None, help="number of cpus per agent")
parser.add_argument("--mem", type=str, default="30GB", help="memory to request on the computation node per agent")
parser.add_argument(
    "--slurm_dir", type=str, default="slurm",
    help="directory to store slurm input and output files in"
)
parser.add_argument(
    "--srun_filename", type=str, default="srun.sh",
    help="filename of srun script to create and launch",
)
parser.add_argument(
    "--sbatch_filename", type=str, default="sbatch.sh",
    help="filename of sbatch script to create and launch",
)
args = parser.parse_args()

os.makedirs(args.slurm_dir, exist_ok=True)
with open(os.path.join(args.slurm_dir, ".gitignore"), "w") as f:
    f.write("*\n!.gitignore")

sweep_dir = os.path.join(args.slurm_dir, args.sweep_id)
os.makedirs(sweep_dir, exist_ok=True)
sbatch_file_path = os.path.join(sweep_dir, args.sbatch_filename)
srun_file_path = os.path.join(sweep_dir, args.srun_filename)

# In general, the sbatch file doesn't change much, but the srun file
with open(sbatch_file_path, "w") as f:
    f.write(
        "\n".join(
            (
                "#!/bin/bash",
                f"#SBATCH --job-name={args.sweep_id}",
                f"#SBATCH --array=1-{args.n_agents}" if args.n_agents > 1 else "",
                f"#SBATCH --gres=gpu:{args.n_gpus}",
                f"#SBATCH --partition={args.partition}",
                f"#SBATCH --constraint={args.constraint}" if args.constraint else "",
                f"#SBATCH --exclude={args.exclude}" if args.exclude else "",
                f"#SBATCH --cpus-per-task={args.n_cpus}" if args.n_cpus else "",
                f"#SBATCH --mem={args.mem}",
                f"#SBATCH --output={sweep_dir}/%A-%a.out"
                if args.n_agents > 1
                else f"#SBATCH --output={sweep_dir}/%A.out",

                f"srun {srun_file_path}",
            )
        )
    )
os.system(f"chmod +x {sbatch_file_path}")

with open(srun_file_path, "w") as f:
    f.write(
        "\n".join(
            (
                "#!/bin/bash",
                "export NO_PROGRESS_BAR=true",
                "hostname",
                f"wandb agent --count {args.n_runs} {args.wandb_account}/{args.wandb_project}/{args.sweep_id}"
                if args.n_runs
                else f"wandb agent {args.wandb_account}/{args.wandb_project}/{args.sweep_id}",
            )
        )
    )
os.system(f"chmod +x {srun_file_path}")

os.system(f"sbatch {sbatch_file_path}")
