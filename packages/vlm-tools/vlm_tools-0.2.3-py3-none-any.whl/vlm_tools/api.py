import os
from functools import lru_cache
from typing import Any, Dict

import requests
from PIL import Image

from vlm_tools.constants import VLM_BASE_URL
from vlm_tools.utils import encode_image


@lru_cache
def get_key() -> str:
    VLM_API_KEY = os.getenv("VLM_API_KEY", None)
    if VLM_API_KEY is None:
        raise ValueError("VLM_API_KEY is not set, please set your API key in your environment variable `VLM_API_KEY`.")
    return VLM_API_KEY


def vlm(image: Image.Image, domain: str, metadata: Dict[str, Any] = None):
    """Send an image to the VLM API."""
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": get_key(),
    }
    addiitonal_kwargs = {}
    if metadata is not None:
        addiitonal_kwargs["metadata"] = metadata
    data = {
        "model": "vlm-1",
        "domain": domain,
        "image": encode_image(image),
        **addiitonal_kwargs,
    }
    response = requests.post(f"{VLM_BASE_URL}/image/generate", headers=headers, json=data)
    response.raise_for_status()
    return response.json()
