import argparse, wandb

def main():
    parser = argparse.ArgumentParser()
    # environment parameters and metadata
    parser.add_argument("--wandb_account", type=str, default=None)
    parser.add_argument("--wandb_project", type=str, default=None)
    parser.add_argument(
        "--exp_idx", type=str, required=True, help="experiment index, e.g. exp1"
    )
    parser.add_argument(
        "--sweep_idx", type=str, default="local", help="sweep index, e.g. sweep1.1"
    )
    args = parser.parse_args()

    if args.wandb:
        wandb.log({
            "epoch": 0,
            "train_loss": 0.1,
            "valid_loss": 0.1,
        })

if __name__ == "__main__":
    main()