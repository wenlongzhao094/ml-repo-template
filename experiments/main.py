import argparse, random, os
from loguru import logger
import wandb
import numpy as np
import torch

def setup(args):
    random.seed(args.seed)
    os.environ["PYTHONHASHSEED"] = str(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    # Setup logging and checkpointing

    # Setup data

    # Setup model and loss

    # Setup evaluation metric

    # Setup training: optimizer, scheduler, validation performance tracker, early stopper, looper

    # Setup testing: looper, prediction saving


def train(args):
    # simulate training
    for epoch in range(2, args.epochs):
        valid_loss = 2 ** -epoch
        valid_acc = 1 - 2 ** -epoch

        logger.info(f"Epoch {epoch}: valid_loss {valid_loss}, valid_acc {valid_acc}.")
        if args.wandb:
            wandb.log({"epoch": epoch, "valid_loss": valid_loss, "valid_acc": valid_acc})


def test(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_id", type=str, required=True, help="experiment identifier")
    parser.add_argument("--sweep_id", type=str, required=True, help="sweep identifier")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--seed", type=int, default=None, help="random seed")

    # input and output
    parser.add_argument("--train_dataset", type=str, default=None, help="Path to training data")
    parser.add_argument("--valid_dataset", type=str, default=None, help="Path to validation data")
    parser.add_argument("--test_dataset", type=str, default=None, help="Path to testing data")
    parser.add_argument("--ckpt_load_from", type=str, default=None, help="path to load a model checkpoint")
    parser.add_argument(
        "--output_dir", type=str, default="outputs", help="directory to save configs, checkpoints, and predictions"
    )
    parser.add_argument("--wandb", action="store_true", help="whether to use wandb to track the experiment")
    parser.add_argument("--wandb_account", type=str, default=None)
    parser.add_argument("--wandb_project", type=str, default=None)

    # training
    parser.add_argument("--epochs", type=int, default=20, help="number of epochs to train")
    parser.add_argument(
        "--batch_size", type=int, default=None,
        help="batch size to process in parallel, effective training batch size is this batch_size * n_grad_acc_steps",
    )
    parser.add_argument("--n_grad_acc_steps", type=int, default=1, help="number of gradient accumulation steps")
    parser.add_argument("--learning_rate", type=float, default=1e-2, help="learning rate")
    parser.add_argument("--lr_scheduler", type=str, default=None)
    parser.add_argument(
        "--valid_interval_epochs", type=int, default=1, help="run validation every this number of training epochs."
    )
    parser.add_argument(
        "--early_stop_patience", type=int, default=None,
        help="how many validation with no improvement to wait before early stop; no early stop if None",
    )
    args = parser.parse_args()

    if args.device == "cuda":
        assert torch.cuda.is_available(), "Cuda unavailable, please set device to cpu"

    if not args.seed:
        args.seed = random.randint(0, 2 ** 16)

    if args.wandb:
        assert args.wandb_project is not None and args.wandb_account is not None
        wandb.init(project=args.wandb_project, entity=args.wandb_account, config=args)
    else:
        args.wandb_project, args.wandb_account = None, None

    setup(args)
    logger.info(args)

    train(args)
    test(args)

    # [optional] finish the wandb run, necessary in notebooks
    if args.wandb:
        wandb.finish()

if __name__ == "__main__":
    main()
