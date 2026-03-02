"""External football data API client (Football-Data.org v4)."""

from typing import Any

import httpx

from app.config import settings


class FootballDataClient:
    """Async client for the Football-Data.org REST API (v4).

    All requests include the ``X-Auth-Token`` header required by the API.
    """

    def __init__(self) -> None:
        self._base_url: str = settings.FOOTBALL_DATA_BASE_URL
        self._headers: dict[str, str] = {
            "X-Auth-Token": settings.FOOTBALL_DATA_API_KEY,
        }

    async def _request(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a GET request and return the parsed JSON response.

        Raises:
            httpx.HTTPStatusError: If the response status code indicates an error.
        """
        async with httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=30.0,
        ) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()

    async def get_competitions(self) -> dict[str, Any]:
        """Fetch all available competitions."""
        return await self._request("/competitions")

    async def get_matches(
        self,
        competition_id: int,
        *,
        matchday: int | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        """Fetch matches for a given competition.

        Args:
            competition_id: Football-Data.org competition identifier.
            matchday: Optional matchday filter.
            status: Optional status filter (e.g. ``LIVE``, ``FINISHED``, ``SCHEDULED``).
        """
        params: dict[str, Any] = {}
        if matchday is not None:
            params["matchday"] = matchday
        if status is not None:
            params["status"] = status
        return await self._request(f"/competitions/{competition_id}/matches", params=params or None)

    async def get_teams(self, competition_id: int) -> dict[str, Any]:
        """Fetch all teams registered in a competition."""
        return await self._request(f"/competitions/{competition_id}/teams")

    async def get_standings(self, competition_id: int) -> dict[str, Any]:
        """Fetch current standings / group tables for a competition."""
        return await self._request(f"/competitions/{competition_id}/standings")

    async def get_match_detail(self, match_id: int) -> dict[str, Any]:
        """Fetch details for a single match."""
        return await self._request(f"/matches/{match_id}")

    async def get_team_detail(self, team_id: int) -> dict[str, Any]:
        """Fetch details for a single team, including squad information."""
        return await self._request(f"/teams/{team_id}")
