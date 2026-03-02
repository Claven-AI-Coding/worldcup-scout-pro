"""Wallpaper generation service -- AI-powered wallpaper creation."""

import logging
from typing import Any

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

# Style definitions with prompt modifiers.
STYLE_PROMPTS: dict[str, dict[str, str]] = {
    "cyberpunk": {
        "label": "赛博朋克",
        "modifier": (
            "cyberpunk style, neon lights, futuristic cityscape background, "
            "glowing edges, dark atmosphere with vibrant neon colors, "
            "high-tech and sci-fi aesthetic, cinematic lighting"
        ),
    },
    "ink": {
        "label": "水墨",
        "modifier": (
            "traditional Chinese ink wash painting style, sumi-e, "
            "minimalist brush strokes, black ink on white paper, "
            "elegant and flowing, subtle gradients, artistic splashes"
        ),
    },
    "comic": {
        "label": "漫画",
        "modifier": (
            "comic book style, bold outlines, halftone dots, "
            "vibrant pop-art colors, dynamic action pose, "
            "speech bubbles optional, manga-inspired aesthetic"
        ),
    },
    "minimal": {
        "label": "极简",
        "modifier": (
            "minimalist design, clean lines, flat colors, "
            "geometric shapes, limited color palette, "
            "modern graphic design, negative space, elegant simplicity"
        ),
    },
}


def generate_wallpaper_prompt(
    team_name: str,
    player_name: str | None = None,
    style: str = "cyberpunk",
) -> str:
    """Build a DALL-E / Stable Diffusion prompt for a World Cup wallpaper.

    Args:
        team_name: Name of the national team.
        player_name: Optional player name to feature.
        style: One of ``cyberpunk``, ``ink``, ``comic``, ``minimal``.

    Returns:
        A descriptive prompt string.
    """
    style_info = STYLE_PROMPTS.get(style, STYLE_PROMPTS["cyberpunk"])
    modifier = style_info["modifier"]

    subject = f"the {team_name} national football team"
    if player_name:
        subject = f"{player_name} from {team_name} national football team"

    prompt = (
        f"A stunning World Cup 2026 wallpaper featuring {subject}. "
        f"The artwork should incorporate the team's national colors and crest motif. "
        f"Style: {modifier}. "
        "High resolution, 16:9 aspect ratio, suitable as a phone or desktop wallpaper. "
        "No text or watermarks."
    )
    return prompt


async def generate_wallpaper_image(
    prompt: str,
    style: str = "cyberpunk",
) -> dict[str, Any]:
    """Generate a wallpaper image using OpenAI DALL-E API.

    Args:
        prompt: The image generation prompt.
        style: Style key used for quality and size settings.

    Returns:
        A dict containing ``url`` (image URL) and ``revised_prompt`` from the API.

    Raises:
        Exception: If the API call fails.
    """
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Adjust quality / style based on wallpaper type.
    dalle_style = "natural" if style == "ink" else "vivid"

    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            style=dalle_style,
            n=1,
        )

        image_data = response.data[0]
        result = {
            "url": image_data.url,
            "revised_prompt": image_data.revised_prompt,
        }
        logger.info("Wallpaper generated successfully: %s", result["url"][:80])
        return result

    except Exception:
        logger.exception("Failed to generate wallpaper via DALL-E")
        raise
