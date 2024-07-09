"""The Trade Desk (TTD) API Integration."""

from typing import Any, Dict, List, Tuple, cast
from typing_extensions import override
from targeting_platform.platform import ALL_WEEK, ALL_WEEK_BACK, LocationFormats, Platform
from targeting_platform.utils_common import get_time_periods
import h3


class PlatformTTD(Platform):
    """Implementation of The Trade Desk (TTD) Activation Platfrom."""

    CHANNELS_MAPPING: Dict[str, str] = {
        "Other": "Display",
        "Display": "Display",
        "Video": "Video",
        "Audio": "Audio",
        "Native": "Display",
        "NativeDisplay": "Display",
        "NativeVideo": "Video",
        "TV": "Connected TV",
        "TVPersonal": "Connected TV",
        "OutOfHome": "DOOH",
        "Mixed": "Display",
    }
    _MAX_LOCATION_PER_PLACEMENT: int = 10000
    _MAX_LOCATION_RADIUS: int = 100000  # km
    _CHUNK_SIZE: int = 10000
    _CACHE_TTL: int = 86400  # Seconds

    @override
    def _set_credentials(self, credentials: Any) -> None:
        """Set platfrom credentials.

        Args:
        ----
            credentials (Any): Provided credentials. Format: {"api_url":"","partner_id":"","token":"","login":"","password":""}.

        """
        self._credentials: Dict[str, Any] = credentials
        self._api_headers = {
            "Content-Type": "application/json",
            "TTD-Auth": self._credentials.get("token", ""),
        }
        self._API_URL = self._credentials.get("api_url", "")

    @override
    def _is_credentials(self) -> bool:
        """Check if credential is valid and reissue token if needed.

        Returns
        -------
            bool: if can connect.

        """
        if not self._API_URL or not self._credentials.get("token", ""):
            return False
        response = self._http_session.post(
            f"{self._API_URL}introspectToken",
            headers=self._api_headers,
            timeout=None,
        )
        if response.status_code != 200:
            # Get new token
            if self._credentials:
                response = self._http_session.post(
                    f"{self._API_URL}authentication",
                    json={
                        "Login": self._credentials.get("login", ""),
                        "Password": self._credentials.get("password", ""),
                        "TokenExpirationInMinutes": 1440,
                    },
                    timeout=None,
                )
                if response.status_code == 200:
                    self._api_headers = {
                        "Content-Type": "application/json",
                        "TTD-Auth": response.json().get("Token", ""),
                    }
                else:
                    raise Exception(response.text)
            else:
                return False
        return True

    def _get_advertizer(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get advertiser information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.

        Returns:
        -------
            Dict[str, Any]: Advertiser information.

        """
        partner_id = self._credentials.get("partner_id", "")
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser", partner_id=partner_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/advertiser/query/partner",
                headers=self._api_headers,
                json={
                    "PartnerId": partner_id,
                    "ReturnEntireAdvertiser": True,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("Advertisers", []):
                # There is new data
                new_advertisers = {advertiser["AdvertiserId"]: advertiser for advertiser in result.get("Advertisers", [])}
                if cached_values:
                    cached_values["Advertisers"].update(new_advertisers)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "Advertisers": new_advertisers,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }
            self._cache.set_cache(
                name="ttd_advertiser",
                value=cached_values,
                ttl=self._CACHE_TTL,
                partner_id=partner_id,
            )
        return cast(Dict[str, Any], cached_values.get("Advertisers", {}).get(advertizer_id, {})) if cached_values else {}

    def _get_advertiser_campaigns(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get Campaigns information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.


        Returns:
        -------
            Dict[str, Any]: Campaigns information.

        """
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser_campaigns", advertizer_id=advertizer_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/campaign/query/advertiser",
                headers=self._api_headers,
                json={
                    "AdvertiserId": advertizer_id,
                    "ReturnEntireCampaign": True,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("Campaigns", []):
                # There is new data
                new_campaigns = {campaign["CampaignId"]: campaign for campaign in result.get("Campaigns", [])}
                if cached_values:
                    cached_values["Campaigns"].update(new_campaigns)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "Campaigns": new_campaigns,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }

            self._cache.set_cache(
                name="ttd_advertiser_campaigns",
                value=cached_values,
                ttl=self._CACHE_TTL,
                advertizer_id=advertizer_id,
            )

        return cast(Dict[str, Any], cached_values.get("Campaigns", {})) if cached_values else {}

    def _get_advertiser_adgroups(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get AdGroups information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.


        Returns:
        -------
            Dict[str, Any]: AdGroups information.

        """
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser_adgroups", advertizer_id=advertizer_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/adgroup/query/advertiser",
                headers=self._api_headers,
                json={
                    "AdvertiserId": advertizer_id,
                    "ReturnEntireAdGroup": True,
                    "IncludeTemplates": False,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("AdGroups", []):
                # There is new data
                new_adgroups = {adgroup["AdGroupId"]: adgroup for adgroup in result.get("AdGroups", [])}
                if cached_values:
                    cached_values["AdGroups"].update(new_adgroups)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "AdGroups": new_adgroups,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }

            self._cache.set_cache(
                name="ttd_advertiser_adgroups",
                value=cached_values,
                ttl=self._CACHE_TTL,
                advertizer_id=advertizer_id,
            )

        return cast(Dict[str, Any], cached_values.get("AdGroups", {})) if cached_values else {}

    def _get_adgroup_budget(self, adgroup: Dict[str, Any]) -> float:
        """Get AdGroup budget value.

        Args:
        ----
            adgroup (Dict[str, Any]): adgroup information.

        Returns:
        -------
            float: budget value, 0 if not set.

        """
        return float(adgroup.get("RTBAttributes", {}).get("BudgetSettings", {}).get("Budget", {}).get("Amount", 0))

    @override
    def validate_credentials(self, first_level_id: str) -> bool:
        """Validate connection to the platform.

        For connection credentials from object will be used.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to validate access to.

        Returns:
        -------
            bool: True if platform can be access with current credentials and id

        """
        advertizer = self._get_advertizer(advertizer_id=first_level_id, is_force_update=True)
        return bool(advertizer)

    @override
    def get_catalog(
        self,
        first_level_id: str,
        second_level_ids: List[str] | None = None,
        only_placements: bool = False,
        no_placements: bool = False,
        is_force_update: bool = False,
    ) -> Dict[str, Any]:
        """Return catalog of elements for platfrom.

        Args:
        ----
            first_level_id (str): iadvertiser id.
            second_level_ids (List[str] | None, optional): list of campaign ids. Defaults to None.
            only_placements (bool, optional): Return only placement in response. Defaults to False.
            no_placements (bool, optional): Does not return placements in response. Defaults to False.
            is_force_update (bool, optional): Force update even if cache is exists. Defaults to False.

        Returns:
        -------
            Dict[str, Any]: platfrom catalog. Structure {"second_level_items":[{"third_level_items":[{"placements":[]}]}]}.

        """
        response: Dict[str, Any] = {}

        advertizer = self._get_advertizer(advertizer_id=first_level_id, is_force_update=is_force_update)
        adgroups = self._get_advertiser_adgroups(advertizer_id=first_level_id, is_force_update=is_force_update) if not no_placements else {}

        currency = advertizer.get("CurrencyCode", "")

        if only_placements:
            response = {
                "placements": {
                    item["AdGroupId"]: {
                        "id": item["AdGroupId"],
                        "name": item["AdGroupName"],
                        "status": "Enabled" if item["IsEnabled"] else "Disabled",
                        "budget": f"{currency} {self._get_adgroup_budget(item):.2f}",
                        "channel": self.CHANNELS_MAPPING.get(item["ChannelId"], item["ChannelId"]),
                        "start_date": "",
                        "end_date": "",
                    }
                    for item in adgroups.values()
                    if (not second_level_ids or item["CampaignId"] in second_level_ids) and item["Availability"] != "Archived"
                }
            }
        else:
            campaigns_dict: Dict[str, List[Dict[str, Any]]] = {}
            for item in adgroups.values():
                if (not second_level_ids or item["CampaignId"] in second_level_ids) and item["Availability"] != "Archived":
                    if item["CampaignId"] not in campaigns_dict:
                        campaigns_dict[item["CampaignId"]] = []
                    campaigns_dict[item["CampaignId"]].append(
                        {
                            "id": item["AdGroupId"],
                            "name": item["AdGroupName"],
                            "status": "Enabled" if item["IsEnabled"] else "Disabled",
                            "budget": f"{currency} {self._get_adgroup_budget(item):.2f}",
                            "channel": self.CHANNELS_MAPPING.get(item["ChannelId"], item["ChannelId"]),
                            "is_duplicate": False,
                            "is_youtube": False,
                        }
                    )
            campaigns = self._get_advertiser_campaigns(advertizer_id=first_level_id, is_force_update=is_force_update) if not only_placements else {}
            response = {
                "second_level_items": [
                    {
                        "id": campaign["CampaignId"],
                        "name": campaign["CampaignName"],
                        "status": campaign["Availability"],
                        "start_date": campaign.get("StartDate", "")[:10],
                        "end_date": campaign.get("EndDate", "")[:10],
                        "third_level_items": [
                            {
                                "id": "",
                                "name": "",
                                "status": "",
                                "placements": [
                                    placement
                                    | {
                                        "start_date": campaign.get("StartDate", "")[:10],
                                        "end_date": campaign.get("EndDate", "")[:10],
                                    }
                                    for placement in campaigns_dict.get(campaign["CampaignId"], [])
                                ],
                            }
                        ],
                    }
                    for campaign in campaigns.values()
                    if (not second_level_ids or campaign["CampaignId"] in second_level_ids) and campaign["Availability"] != "Archived"
                ]
            }

        return response

    @override
    def get_all_placements(self, first_level_id: str, second_level_id: str | None = None, third_level_id: str | None = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all placements.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            second_level_id (str | None, optional): list of second level elements to get (campaigns e.g.). Defaults to None.
            third_level_id (str | None, optional): list of third level elements to get (insertion orders e.g.). Defaults to None.

        Returns:
        -------
            Dict[str, List[Dict[str, Any]]]: placements information.

        """
        adgroups = self._get_advertiser_adgroups(advertizer_id=first_level_id, is_force_update=True)
        return {"placements": [item for item in adgroups.values() if not second_level_id or item["CampaignId"] == second_level_id]}

    @override
    def get_placement(self, first_level_id: str, placement_id: str) -> Any:
        """Get placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_id (str): placement id to duplicate.

        Returns:
        -------
            Any: placement object or information.

        """
        result: Dict[str, Any] = {}
        if self._is_credentials():
            response = self._http_session.get(
                f"{self._API_URL}adgroup/{placement_id}",
                headers=self._api_headers,
                timeout=None,
            )
            response.raise_for_status()
            if response.status_code == 200:
                result = response.json()
        return result

    @override
    def pause_placement(self, first_level_id: str, placement_ids: List[str]) -> List[str]:
        """Pause placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to pause.

        Returns:
        -------
            list: list of paused placement ids.

        """
        result: List[str] = []
        if self._is_credentials():
            for adgroup_id in placement_ids:
                response = self._http_session.put(
                    f"{self._API_URL}adgroup",
                    headers=self._api_headers,
                    json={"AdGroupId": adgroup_id, "IsEnabled": False},
                    timeout=None,
                )
                response.raise_for_status()
                if response.status_code == 200:
                    result.append(adgroup_id)

        return result

    @override
    @staticmethod
    def to_format_periods(periods: List[Tuple[str, Tuple[int, int]]]) -> List[Any]:
        """Return datetime periods in platform format.

        Args:
        ----
            periods (List[Tuple[str, Tuple[int, int]]]): periods in format (day_of_week,(start_hour, end_hour)).

        Returns:
        -------
            List[Any]: periods in platform format.

        """
        return [
            {
                "HourOfWeek": hour + ALL_WEEK[day_of_week] * 24,
            }
            for day_of_week, (start_hour, end_hour) in periods
            for hour in range(min(max(start_hour, 0), 23), max(min(end_hour, 24), 1))
            if start_hour < end_hour and day_of_week in ALL_WEEK
        ]

    @override
    @staticmethod
    def from_format_periods(periods: List[Any]) -> List[Tuple[str, Tuple[int, int]]]:
        """Return datetime periods in generic format.

        Args:
        ----
            periods (List[Any]): periods in platfrom format.

        Returns:
        -------
            List[Tuple[str, Tuple[int, int]]]: periods in generic format (day_of_week,(start_hour, end_hour)).

        """
        grouped_days: Dict[str, List[int]] = {}
        for period in periods:
            dow = ALL_WEEK_BACK[period["HourOfWeek"] // 24]
            if dow in grouped_days:
                grouped_days[dow].append(period["HourOfWeek"] % 24)
            else:
                grouped_days[dow] = [period["HourOfWeek"] % 24]

        generic_periods = {k: get_time_periods(v) for k, v in grouped_days.items()}

        return [(k, v_) for k, v in generic_periods.items() for v_ in v]

    @override
    @staticmethod
    def to_format_locations(locations: List[str] | List[Tuple[float, float, float]], format: LocationFormats = LocationFormats.h3) -> List[Any]:
        """Return locations in platform format.

        Args:
        ----
            locations (List[str] | List[Tuple[float, float, float]]): list of locations either H3 list or list of (latitude,longitude,radius).
            format (LocationFormats, optional): format of locations. Default: LocationFormats.h3

        Returns:
        -------
            List[Any]: locations in platform format.

        """
        result: List[Any] = []
        if format == LocationFormats.h3:
            for cell in locations:
                try:
                    lat, lng = h3.h3_to_geo(cell)
                    result.append(
                        {
                            "LatDeg": lat,
                            "LngDeg": lng,
                            "RadMet": min(int(LocationFormats.edge_length(str(cell), unit="m")), PlatformTTD._MAX_LOCATION_RADIUS),
                        }
                    )
                except Exception:
                    pass
        else:
            for cell in locations:
                lat, lng, radius = tuple(cell)
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    result.append(
                        {
                            "LatDeg": lat,
                            "LngDeg": lng,
                            "RadMet": min(float(str(radius)), PlatformTTD._MAX_LOCATION_RADIUS),
                        }
                    )
        return result

    @override
    @staticmethod
    def from_format_locations(locations: List[Any], format: LocationFormats = LocationFormats.h3) -> List[str] | List[Tuple[float, float, float]]:
        """Return location in requested format.

        Args:
        ----
            locations (List[Any]): locations in platfrom format.
            format (LocationFormats, optional): format of locations. Default: LocationFormats.h3

        Returns:
        -------
            List[str] | List[Tuple[float, float, float]]: locations in requested format.

        """
        result: List[Any] = [(cell["LatDeg"], cell["LngDeg"], round(cell["RadMet"] / 1000, 3)) for cell in locations]
        return Platform.location_to_h3(result) if format == LocationFormats.h3 else result
