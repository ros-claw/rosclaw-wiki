"""Cloudflare R2 sync — S3-compatible object storage for ROSClaw Wiki batch pipeline.

NOTE: This file is kept in sync with utils/r2_sync.py. Both contain the same
implementation because Docker's PYTHONPATH order puts /app/utils before /app,
so the container imports utils/r2_sync.py, while local scripts run from the
project root and import this file. Update BOTH files when changing R2 logic.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger("rosclaw.r2")


def _get_r2_client() -> Any:
    """Lazy-load boto3 S3 client for Cloudflare R2."""
    import boto3
    from botocore.config import Config

    endpoint = os.environ.get("R2_ENDPOINT")
    access_key = os.environ.get("R2_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")
    if not all([endpoint, access_key, secret_key]):
        raise RuntimeError(
            "R2 credentials not configured. Set R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY."
        )
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def generate_presigned_upload_url(key: str, file_size: int, expiry: int = 3600) -> str:
    """Generate a presigned PUT upload URL (default 1 hour validity)."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    return s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentLength": file_size,
        },
        ExpiresIn=expiry,
    )


def generate_presigned_download_url(key: str, expiry: int = 3600) -> str:
    """Generate a presigned GET download URL."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiry,
    )


def head_object(key: str) -> dict[str, Any] | None:
    """Check if an object exists in R2 and return metadata."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    try:
        return s3.head_object(Bucket=bucket, Key=key)
    except Exception as exc:
        logger.warning("R2 head_object failed for %s: %s", key, exc)
        return None


def list_submissions(r2_prefix: str = "submissions") -> list[str]:
    """List submission object keys in the R2 bucket under the given prefix."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=r2_prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]


def delete_object(key: str) -> bool:
    """Delete an object from the R2 bucket. Returns True on success."""
    s3 = _get_r2_client()
    bucket = os.environ.get("R2_BUCKET", "rosclaw-wiki")
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        return True
    except Exception as exc:
        logger.warning("R2 delete_object failed for %s: %s", key, exc)
        return False
