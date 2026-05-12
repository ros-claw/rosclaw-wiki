"""R2 (Cloudflare) sync utilities for ROSClaw Wiki batch pipeline."""

import os
from pathlib import Path

import boto3
from botocore.config import Config


def _get_r2_client():
    """Return an S3 client configured for Cloudflare R2."""
    endpoint = os.environ["R2_ENDPOINT"]
    access_key = os.environ["R2_ACCESS_KEY_ID"]
    secret_key = os.environ["R2_SECRET_ACCESS_KEY"]

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
    )
    return s3


def generate_presigned_download_url(r2_key: str, expiry: int = 3600) -> str:
    """Generate a presigned URL for downloading an object from R2."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": r2_key},
        ExpiresIn=expiry,
    )
    return url


def list_submissions(r2_prefix: str = "submissions") -> list[str]:
    """List submission tarballs in the R2 bucket."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=r2_prefix)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    return keys
