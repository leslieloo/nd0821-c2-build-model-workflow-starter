#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    logger.info(f"Downloading {args.input_artifact} from Weights & Biases")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    df = pd.read_csv(artifact_local_path)

    logger.info(f"Filter out data that price column not falls between {args.min_price} and {args.max_price}")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info(f"Convert data column 'last_review' to datetime type")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info(f"Save clean data to clean_sample.csv")
    df.to_csv("clean_sample.csv", index=False)

    logger.info(f"Uploading {args.output_artifact} to Weights & Biases")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )

    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    artifact.wait()

    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input artifact to download",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact to save",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Output artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="A brief description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,
        help="Minimum price accepted from filtering out",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,
        help="Maximum price accepted from filtering out",
        required=True
    )


    args = parser.parse_args()

    go(args)
