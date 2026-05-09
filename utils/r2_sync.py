"""Cloudflare R2 sync — S3-compatible upload with presigned URLs.

Users never touch S3 credentials. The API gateway generates presigned PUT URLs
that the client uses to upload directly to R2.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger("rosclaw.r2")


def _get_r2_client() -> Any:
    """Lazy-load boto3 S3 client for R2."""
    import boto3
    endpoint = os.environ.get("R2_ENDPOINT")
    access_key = os.environ.get("R2_ACCESS_KEY_ID")
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")
    if not all([endpoint, access_key, secret_key]):
        raise RuntimeError("R2 credentials not configured. Set R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY.")
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )


def generate_presigned_upload_url(key: str, file_size: int, expiry: int = 3600) -> str:
    """Generate a presigned PUT upload URL (valid for 1 hour by default).

    Args:
        key: Object key in R2 (e.g. "uploads/test-wiki.tar.gz").
        file_size: Expected file size in bytes (for validation hints).
        expiry: URL expiry time in seconds.

    Returns:
        Presigned PUT URL string.
    """
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
