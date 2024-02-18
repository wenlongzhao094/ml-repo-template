import argparse, os, json

parser = argparse.ArgumentParser(description="Launch a slurm job to run a wandb agent")
parser.add_argument("--wandb_account", type=str)
parser.add_argument("--wandb_project", type=str)
parser.add_argument("--sweep_id", type=str, default=None, help="sweep id created by wandb")
parser.add_argument("--nagents", type=int, default=1, help="number of agents per sweep")
parser.add_argument("--nruns", type=int, default=10, help="number of runs per agent")
parser.add_argument("--ngpus", type=int, default=1, help="number of gpus per agent")
parser.add_argument("--partition", type=str, default=None, help="gpu partition name")
parser.add_argument("--exclude", type=str, default=None, help="gpu nodes to exclude, e.g. node001,node002")
parser.add_argument("--ncpus", type=int, default=None, help="number of cpus per agent")
parser.add_argument(
    "--slurm_dir", 
    type=str, 
    default="slurm", 
    help="directory to store slurm input and output files in"
)
parser.add_argument(
    "--srun_filename",
    type=str,
    default="srun.sh",
    help="filename of srun script to create and launch",
)
parser.add_argument(
    "--sbatch_filename",
    type=str,
    default="sbatch.sh",
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
                f"#SBATCH --array=1-{args.nagents}" if args.nagents > 1 else "",
                f"#SBATCH --gres=gpu:{args.ngpus}",
                f"#SBATCH --partition={args.partition}",
                f"#SBATCH --exclude={args.exclude}" if args.exclude else "",
                f"#SBATCH --cpus-per-task={args.ncpus}" if args.ncpus else "",
                "#SBATCH --mem=40G",
                f"#SBATCH --output={sweep_dir}/%A-%a.out"
                if args.nagents > 1
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
                "module load miniconda/22.11.1-1",
                "conda activate <env_name>", # TODO: change conda environment name
                f"wandb agent --count {args.nruns} {args.wandb_account}/{args.wandb_project}/{args.sweep_id}"
                if args.nruns
                else f"wandb agent {args.wandb_account}/{args.wandb_project}/{args.sweep_id}",
            )
        )
    )
os.system(f"chmod +x {srun_file_path}")

os.system(f"sbatch {sbatch_file_path}")
