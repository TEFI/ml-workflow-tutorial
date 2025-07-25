import argparse
from training import train_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--min_samples_split", type=int, default=2)
    parser.add_argument("--min_samples_leaf", type=int, default=1)
    parser.add_argument("--gcs_path", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_model(args)
