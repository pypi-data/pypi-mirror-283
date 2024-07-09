import json
from itertools import islice
from pathlib import Path

import requests
import typer
from loguru import logger
from PIL import Image
from tqdm import tqdm

from vlm_tools.api import get_key, vlm
from vlm_tools.constants import VLM_BASE_URL, VLM_ENDPOINT_URL

app = typer.Typer()


@app.command("submit-image")
def submit_image(path: Path, domain: str):
    """Submit an image to the VLM API."""
    typer.echo(f"Submitting image at path={path} to domain={domain}.")
    if not path.exists():
        raise ValueError(f"Path={path} does not exist.")
    if path.suffix not in [".jpg", ".jpeg", ".png"]:
        raise ValueError(f"Path={path} is not a valid image file.")

    image = Image.open(path)
    response = vlm(image, domain)
    logger.info("Response")
    logger.info("\n" + json.dumps(response, indent=2))


@app.command("submit-video")
def submit_video(path: Path, domain: str, max_frames: int = 10):
    """Submit a video in a streaming fashion to the VLM API."""
    from vlm_tools.video import VideoItertools, VideoReader

    typer.echo(f"Submitting video at path={path} to domain={domain}.")
    if not path.exists():
        raise ValueError(f"Path={path} does not exist.")
    if path.suffix not in [".mp4", ".avi", ".mov"]:
        raise ValueError(f"Path={path} is not a valid video file.")

    v_itertools = VideoItertools()
    video = VideoReader(path)
    stream = v_itertools.islice(video, similarity_threshold=0.9)
    n = len(video)
    for _idx, img in tqdm(enumerate(islice(stream, max_frames)), desc="Processing frames"):
        img = Image.fromarray(img).convert("RGB")
        response = vlm(img, domain)
        logger.info("\n" + json.dumps(response, indent=2))
    logger.info(f"video={path}, nframes={n}, processed={_idx+1}, sampling_rate={(_idx + 1) * 100. / n:.2f}%")


@app.command("submit-pdf")
def submit_pdf(path: Path, domain: str):
    """Submit a PDF to the VLM API."""
    typer.echo(f"Submitting PDF at path={path} to domain={domain}.")
    if not path.exists():
        raise ValueError(f"Path={path} does not exist.")
    if path.suffix not in [
        ".pdf",
    ]:
        raise ValueError(f"Path={path} is not a valid PDF file.")

    headers = {"X-Api-Key": get_key()}
    logger.debug(f"Uploading PDF [path={path}]")
    response = requests.post(f"{VLM_BASE_URL}/files", files={"file": path.open("rb")}, headers=headers)
    logger.debug(f"Uploaded file [response={response.json()}]")

    logger.debug("Confirm file upload...")
    r = response.json()
    response = requests.get(f"{VLM_BASE_URL}/files/{r['id']}", headers=headers)
    assert response.status_code == 200, f"Response failed: {response.text}"
    logger.debug(f"Referenced file [response={response.json()}]")

    logger.debug(f"Process PDF [path={path}]...")
    json_data = {
        "file_id": r["id"],
        "model": "vlm-1",
        "domain": domain,
    }

    headers = {"Content-Type": "application/json", "X-Api-Key": get_key()}
    response = requests.post(f"{VLM_ENDPOINT_URL}/document/generate", headers=headers, json=json_data)
    assert response.status_code == 201, f"Response failed: {response.text}"
    logger.info("Response")
    logger.info("\n" + json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    app()
