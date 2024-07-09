"""Google DV360 API Integration.."""

import datetime
from typing import Any, Dict, List, Tuple, cast
import pytz
from targeting_platform.platform import LocationFormats, Platform, ALL_WEEK
from typing_extensions import override
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import h3

from targeting_platform.utils_common import flatten_concatenation, generate_batches


class PlatformDV360(Platform):
    """Implementation of Google DV360 Activation Platfrom."""

    ACCESS_ROLES = {"ADMIN", "ADMIN_PARTNER_CLIENT", "STANDARD", "STANDARD_PARTNER_CLIENT"}
    STATUS_MAPPING: Dict[str, str] = {
        "ENTITY_STATUS_ACTIVE": "Active",
        "ENTITY_STATUS_PAUSED": "Paused",
        "ENTITY_STATUS_ARCHIVED": "Archived",
        "ENTITY_STATUS_DRAFT": "Draft",
        "ENTITY_STATUS_UNSPECIFIED": "Unknown",
        "ENTITY_STATUS_SCHEDULED_FOR_DELETION": "Deleted",
    }
    CHANNELS_MAPPING: Dict[str, str] = {
        "LINE_ITEM_TYPE_UNSPECIFIED": "Display",
        "LINE_ITEM_TYPE_DISPLAY_DEFAULT": "Display",
        "LINE_ITEM_TYPE_DISPLAY_MOBILE_APP_INSTALL": "Display",
        "LINE_ITEM_TYPE_VIDEO_DEFAULT": "Video",
        "LINE_ITEM_TYPE_VIDEO_MOBILE_APP_INSTALL": "Video",
        "LINE_ITEM_TYPE_DISPLAY_MOBILE_APP_INVENTORY": "Display",
        "LINE_ITEM_TYPE_VIDEO_MOBILE_APP_INVENTORY": "Video",
        "LINE_ITEM_TYPE_AUDIO_DEFAULT": "Audio",
        "LINE_ITEM_TYPE_VIDEO_OVER_THE_TOP": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_ACTION": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_NON_SKIPPABLE": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_VIDEO_SEQUENCE": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_AUDIO": "Audio",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_REACH": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_SIMPLE": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_NON_SKIPPABLE_OVER_THE_TOP": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_REACH_OVER_THE_TOP": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_SIMPLE_OVER_THE_TOP": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_TARGET_FREQUENCY": "Video",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_VIEW": "Video",
        "LINE_ITEM_TYPE_DISPLAY_OUT_OF_HOME": "Display",
        "LINE_ITEM_TYPE_VIDEO_OUT_OF_HOME": "Video",
    }
    YOUTUBE_LINEITEM_TYPES = [
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_ACTION",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_NON_SKIPPABLE",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_VIDEO_SEQUENCE",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_AUDIO",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_REACH",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_SIMPLE",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_NON_SKIPPABLE_OVER_THE_TOP",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_REACH_OVER_THE_TOP",
        "LINE_ITEM_TYPE_YOUTUBE_AND_PARTNERS_SIMPLE_OVER_THE_TOP",
    ]
    _TARGETING_TYPES = ["TARGETING_TYPE_DAY_AND_TIME", "TARGETING_TYPE_POI"]
    _FILTER_TRAGETING_OPTIONS = 'targetingType="TARGETING_TYPE_DAY_AND_TIME" OR targetingType="TARGETING_TYPE_POI"'
    _MAX_LOCATION_PER_PLACEMENT: int = 10000
    _MAX_LOCATION_RADIUS: int = 800  # km
    _CHUNK_SIZE: int = 5000
    _CACHE_TTL: int = 3600  # Seconds
    _RETRIES: int = 10

    _API_NAME = "displayvideo"
    _DEFAULT_API_VERSION = "v3"
    _API_URL = "https://displayvideo.googleapis.com/"
    _service: Any = None

    @override
    def _set_credentials(self, credentials: Any) -> None:
        """Set platfrom credentials.

        Args:
        ----
            credentials (Any): Provided credentials. Service account information.

        """
        try:
            self._credentials = ServiceAccountCredentials.from_service_account_info(credentials)
        except Exception:
            pass

    @override
    def _is_credentials(self) -> bool:
        """Check if credential is valid and reissue token (or other credentials) if needed.

        Returns
        -------
            bool: if can connect

        """
        if not self._credentials:
            return False
        if self._service is None:
            self._service = build(
                self._API_NAME,
                self._DEFAULT_API_VERSION,
                discoveryServiceUrl=f"{self._API_URL}/$discovery/rest?version={self._DEFAULT_API_VERSION}",
                credentials=self._credentials,
                num_retries=3,
                cache_discovery=False,
            )
        return self._service is not None

    def _get_advertizer(
        self,
        advertizer_id: str,
        is_force_update: bool = False,
    ) -> Dict[str, Any]:
        """Get advertiser information.

        Args:
        ----
            advertizer_id (str): advertizer id
            is_force_update (bool, optional): Force update even if cache is exists. Defaults to False.

        Returns:
        -------
            dict: Advertiser

        """
        if self._is_credentials():
            advertiser: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="dv360_advertiser", advertizer_id=advertizer_id)
            if advertiser is None or is_force_update:
                request = self._service.advertisers().get(advertiserId=advertizer_id)
                advertiser = request.execute(num_retries=self._RETRIES)
                self._cache.set_cache(
                    name="dv360_advertiser",
                    value=advertiser,
                    ttl=self._CACHE_TTL,
                    advertizer_id=advertizer_id,
                )

        return advertiser if advertiser else {}

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
        if self._is_credentials() and self._credentials:
            result: list[Any] = []
            try:
                response = self._service.users().list(filter=f'email:"{self._credentials.service_account_email}"').execute(num_retries=self._RETRIES)
                roles = set(
                    [
                        role.get("userRole", "")
                        for user in response.get("users", [])
                        for role in user.get("assignedUserRoles", [])
                        if role.get("userRole", "") and role.get("advertiserId", "") == "" or role.get("advertiserId", "") == first_level_id
                    ]
                )
                result = list(roles & self.ACCESS_ROLES)
                if result:
                    result = [self._get_advertizer(first_level_id)]
            except HttpError:
                return False
            return bool(result)
        return False

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
            first_level_id (str): id for main platfrom identificator to get catalog for.
            second_level_ids (List[str] | None, optional): list of second level elements to get (campaigns e.g.). Defaults to None.
            only_placements (bool, optional): Return only placement in response. Defaults to False.
            no_placements (bool, optional): Does not return placements in response. Defaults to False.
            is_force_update (bool, optional): Force update even if cache is exists. Defaults to False.

        Returns:
        -------
            Dict[str, Any]: platfrom catalog. Structure {"second_level_items":[{"third_level_items":[{"placements":[]}]}]}.

        """
        response: Dict[str, Any] = {"second_level_items": []}

        def __to_utc_date(tz: Any, date_string: str) -> str:
            return cast(str, tz.localize(datetime.datetime.fromisoformat(date_string)).astimezone(pytz.timezone("UTC")).date().isoformat()) if date_string else ""

        def __get_lineitem_budget(lineitem: Dict[str, Any], budget_type_only: str | None = None) -> int:
            lineitem_budget = lineitem.get("budget", {})
            budget = 0
            if budget_type_only is None or lineitem_budget.get("budgetAllocationType", "") == budget_type_only:
                budget = int(lineitem_budget.get("maxAmount", 0))

            return budget

        if self._is_credentials():
            filters = [((" OR ".join([f'campaignId="{campaignId}"' for campaignId in second_level_ids if campaignId])) if second_level_ids else None)]
            if not no_placements:
                lineitems: List[Any] | None = None if is_force_update else self._cache.get_cache(name="dv360_lineitems", first_level_id=first_level_id, filter=filters[0])
                if lineitems is None or is_force_update:
                    lineitems = [(self._service.advertisers().lineItems().list(advertiserId=first_level_id, filter=filters[0], pageSize=200).execute(num_retries=self._RETRIES))]
                    # Get all lineitems
                    nextPageToken: str = lineitems[-1].get("nextPageToken", "")
                    while nextPageToken:
                        lineitems.append(
                            (
                                self._service.advertisers()
                                .lineItems()
                                .list(
                                    advertiserId=first_level_id,
                                    filters=filters[0],
                                    pageSize=200,
                                    pageToken=nextPageToken,
                                )
                                .execute(num_retries=self._RETRIES)
                            )
                        )
                        nextPageToken = lineitems[-1].get("nextPageToken", "")
                    self._cache.set_cache(name="dv360_lineitems", value=lineitems, ttl=self._CACHE_TTL, first_level_id=first_level_id, filter=filters[0])

            advertizer = self._get_advertizer(advertizer_id=first_level_id, is_force_update=is_force_update)
            currency = advertizer.get("generalConfig", {}).get("currencyCode", "")
            tz_string = advertizer.get("generalConfig", {}).get("timeZone", "")
            tz_advertizer = pytz.timezone(tz_string if tz_string else "UTC")

            if only_placements and not no_placements:
                # Only lineitems as dict
                response = {
                    "placements": {
                        item["lineItemId"]: {
                            "id": item["lineItemId"],
                            "name": item["displayName"],
                            "status": self.STATUS_MAPPING[item["entityStatus"]],
                            "budget": f"{currency} {(__get_lineitem_budget(item) / 1000000):.2f}",
                            "channel": self.CHANNELS_MAPPING.get(item["lineItemType"], item["lineItemType"]),
                            "start_date": __to_utc_date(
                                tz_advertizer,
                                f"""{item["flight"]["dateRange"]["startDate"]["year"]}-{item["flight"]["dateRange"]["startDate"]["month"]:0>2}-{item["flight"]["dateRange"]["startDate"]["day"]:0>2}T00:00:00"""  # noqa: E501
                                if item["flight"]["dateRange"].get("startDate", {})
                                else "",
                            ),
                            "end_date": __to_utc_date(
                                tz_advertizer,
                                f"""{item["flight"]["dateRange"]["endDate"]["year"]}-{item["flight"]["dateRange"]["endDate"]["month"]:0>2}-{item["flight"]["dateRange"]["endDate"]["day"]:0>2}T23:59:59"""  # noqa: E501
                                if item["flight"]["dateRange"].get("endDate", {})
                                else "",
                            ),
                        }
                        for items in (lineitems if lineitems else [])
                        for item in items.get("lineItems", [])
                    }
                }
            else:
                # Prepare intermediate dictionary (need to take names later)
                campaigns_dict: Dict[str, Any] = {}
                if not no_placements:
                    for items in lineitems if lineitems else []:
                        for item in items.get("lineItems", []):
                            if item["campaignId"] not in campaigns_dict:
                                campaigns_dict[item["campaignId"]] = {}
                            if item["insertionOrderId"] not in campaigns_dict[item["campaignId"]]:
                                campaigns_dict[item["campaignId"]][item["insertionOrderId"]] = []
                            campaigns_dict[item["campaignId"]][item["insertionOrderId"]].append(
                                {
                                    "id": item["lineItemId"],
                                    "name": item["displayName"],
                                    "status": self.STATUS_MAPPING[item["entityStatus"]],
                                    "budget": f"{currency} {(__get_lineitem_budget(item) / 1000000):.2f}",
                                    "channel": self.CHANNELS_MAPPING.get(item["lineItemType"], item["lineItemType"]),
                                    "start_date": __to_utc_date(
                                        tz_advertizer,
                                        f"""{item["flight"]["dateRange"]["startDate"]["year"]}-{item["flight"]["dateRange"]["startDate"]["month"]:0>2}-{item["flight"]["dateRange"]["startDate"]["day"]:0>2}T00:00:00"""  # noqa: E501
                                        if item["flight"]["dateRange"].get("startDate", {})
                                        else "",
                                    ),
                                    "end_date": __to_utc_date(
                                        tz_advertizer,
                                        f"""{item["flight"]["dateRange"]["endDate"]["year"]}-{item["flight"]["dateRange"]["endDate"]["month"]:0>2}-{item["flight"]["dateRange"]["endDate"]["day"]:0>2}T23:59:59"""  # noqa: E501
                                        if item["flight"]["dateRange"].get("endDate", {})
                                        else "",
                                    ),
                                    "is_duplicate": (item["integrationDetails"].get("integrationCode", "") == self._integration_code),
                                    "is_youtube": item["lineItemType"] in self.YOUTUBE_LINEITEM_TYPES,
                                }
                            )
                # All insertion orders and then all campaings
                # It is fatser to get all in one request and then filter
                insertion_orders: List[Any] | None = (
                    None if is_force_update else self._cache.get_cache(name="dv360_insertion_orders", first_level_id=first_level_id, second_level_ids=list(campaigns_dict.keys()))
                )
                if insertion_orders is None or is_force_update:
                    insertion_orders = (
                        self._service.advertisers()
                        .insertionOrders()
                        .list(
                            advertiserId=first_level_id,
                            filter=(" OR ".join([f'campaignId="{campaignId}"' for campaignId in campaigns_dict.keys()]) if campaigns_dict else ""),
                        )
                        .execute(num_retries=self._RETRIES)
                        .get("insertionOrders", [])
                    )
                    self._cache.set_cache(
                        name="dv360_insertion_orders",
                        value=insertion_orders,
                        ttl=self._CACHE_TTL,
                        first_level_id=first_level_id,
                        second_level_ids=list(campaigns_dict.keys()),
                    )
                campaigns: List[Any] | None = (
                    None if is_force_update else self._cache.get_cache(name="dv360_campaigns", first_level_id=first_level_id, second_level_ids=second_level_ids)
                )
                if campaigns is None or is_force_update:
                    campaigns = (
                        self._service.advertisers()
                        .campaigns()
                        .list(
                            advertiserId=first_level_id,
                            filter=filters[0],
                        )
                        .execute(num_retries=self._RETRIES)
                        .get("campaigns", [])
                    )
                    self._cache.set_cache(
                        name="dv360_campaigns",
                        value=campaigns,
                        ttl=self._CACHE_TTL,
                        first_level_id=first_level_id,
                        second_level_ids=list(campaigns_dict.keys()),
                    )
                response = {
                    "second_level_items": [
                        {
                            "id": campaing["campaignId"],
                            "name": campaing["displayName"],
                            "status": self.STATUS_MAPPING[campaing["entityStatus"]],
                            "start_date": __to_utc_date(
                                tz_advertizer,
                                f"""{campaing["campaignFlight"]["plannedDates"]["startDate"]["year"]}-{campaing["campaignFlight"]["plannedDates"]["startDate"]["month"]:0>2}-{campaing["campaignFlight"]["plannedDates"]["startDate"]["day"]:0>2}T00:00:00"""  # noqa: E501
                                if campaing["campaignFlight"]["plannedDates"].get("startDate", {})
                                else "",
                            ),
                            "end_date": __to_utc_date(
                                tz_advertizer,
                                f"""{campaing["campaignFlight"]["plannedDates"]["endDate"]["year"]}-{campaing["campaignFlight"]["plannedDates"]["endDate"]["month"]:0>2}-{campaing["campaignFlight"]["plannedDates"]["endDate"]["day"]:0>2}T23:59:59"""  # noqa: E501
                                if campaing["campaignFlight"]["plannedDates"].get("endDate", {})
                                else "",
                            ),
                            "third_level_items": [
                                {
                                    "id": insertion_order["insertionOrderId"],
                                    "name": insertion_order["displayName"],
                                    "status": self.STATUS_MAPPING[insertion_order["entityStatus"]],
                                    "placements": ([] if no_placements else campaigns_dict[campaing["campaignId"]][insertion_order["insertionOrderId"]]),
                                }
                                for insertion_order in (insertion_orders if insertion_orders else [])
                                if insertion_order["campaignId"] == campaing["campaignId"]
                                and (no_placements or insertion_order["insertionOrderId"] in campaigns_dict[campaing["campaignId"]])
                            ],
                        }
                        for campaing in (campaigns if campaigns else [])
                        if no_placements or campaing["campaignId"] in campaigns_dict
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
        response: Dict[str, List[Dict[str, Any]]] = {"placements": []}
        if self._is_credentials():
            filters = [
                f'campaignId="{second_level_id}"' if second_level_id else "",
                f'insertionOrderId="{third_level_id}"' if third_level_id else "",
            ]
            result = (
                self._service.advertisers()
                .lineItems()
                .list(
                    advertiserId=first_level_id,
                    filter=" AND ".join([f for f in filters if f]),
                )
                .execute(num_retries=self._RETRIES)
            )
            response = {"placements": result.get("lineItems", [])}
        return response

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
        response: Dict[str, Any] = {}
        if self._is_credentials():
            response = (
                self._service.advertisers()
                .lineItems()
                .get(
                    advertiserId=first_level_id,
                    lineItemId=placement_id,
                )
                .execute(num_retries=self._RETRIES)
            )
        return response

    @override
    def duplicate_placement(self, first_level_id: str, placement_id: str, suffixes: List[str]) -> List[str]:
        """Duplicate placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_id (str): placement id to duplicate.
            suffixes (list): suffixes for placement display names. Number of suffixes will produce number of dublicates.

        Returns:
        -------
            list: list of created placement ids.

        """
        result: List[str] = []
        if self._is_credentials() and len(suffixes) > 0:
            original_lineitem = self.get_placement(first_level_id=first_level_id, placement_id=placement_id)
            original_name = original_lineitem.get("displayName", "")
            original_flight = original_lineitem.get("flight", "")
            if original_flight and "flightDateType" in original_flight and "dateRange" in original_flight:
                original_flight["flightDateType"] = "LINE_ITEM_FLIGHT_DATE_TYPE_CUSTOM"
                today = datetime.date.today()
                if (
                    "startDate" in original_flight["dateRange"]
                    and datetime.date(
                        original_flight["dateRange"]["startDate"]["year"],
                        original_flight["dateRange"]["startDate"]["month"],
                        original_flight["dateRange"]["startDate"]["day"],
                    )
                    < today
                ):
                    # Set start date to current date
                    original_flight["dateRange"]["startDate"] = {
                        "year": today.year,
                        "month": today.month,
                        "day": today.day,
                    }
                if (
                    "endDate" in original_flight["dateRange"]
                    and datetime.date(
                        original_flight["dateRange"]["endDate"]["year"],
                        original_flight["dateRange"]["endDate"]["month"],
                        original_flight["dateRange"]["endDate"]["day"],
                    )
                    < today
                ):
                    # Set end date to current date
                    original_flight["dateRange"]["endDate"] = {
                        "year": today.year,
                        "month": today.month,
                        "day": today.day,
                    }
            result = [
                self._service.advertisers()
                .lineItems()
                .duplicate(
                    advertiserId=first_level_id,
                    lineItemId=placement_id,
                    body={
                        "targetDisplayName": f"{original_name}{suffix}",
                    },
                )
                .execute(num_retries=self._RETRIES)
                .get("duplicateLineItemId", "")
                for suffix in suffixes
            ]
            [
                self._service.advertisers()
                .lineItems()
                .patch(
                    advertiserId=first_level_id,
                    lineItemId=duplicated_lineitem_id,
                    updateMask="flight,integrationDetails,displayName",
                    body={
                        "flight": original_flight,
                        "integrationDetails": {
                            "integrationCode": self._integration_code,
                            "details": f"{suffixes[i]}",
                        },
                        "displayName": f"{original_name}{suffixes[i]}",
                    },
                )
                .execute(num_retries=self._RETRIES)
                for i, duplicated_lineitem_id in enumerate(result)
            ]
        return result

    @override
    def delete_placement(self, first_level_id: str, placement_ids: List[str]) -> List[str]:
        """Delete placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to delete.

        Returns:
        -------
            list: list of deleted placement ids.

        """
        result: List[str] = []
        if self._is_credentials():
            for lineitem_id in placement_ids:
                self._service.advertisers().lineItems().patch(
                    advertiserId=first_level_id,
                    lineItemId=lineitem_id,
                    updateMask="entityStatus",
                    body={"entityStatus": "ENTITY_STATUS_ARCHIVED"},
                ).execute(num_retries=self._RETRIES)
                self._service.advertisers().lineItems().delete(
                    advertiserId=first_level_id,
                    lineItemId=lineitem_id,
                ).execute(num_retries=self._RETRIES)
                result.append(lineitem_id)

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
            for lineitem_id in placement_ids:
                self._service.advertisers().lineItems().patch(
                    advertiserId=first_level_id,
                    lineItemId=lineitem_id,
                    updateMask="entityStatus",
                    body={"entityStatus": "ENTITY_STATUS_PAUSED"},
                ).execute(num_retries=self._RETRIES)

        return result

    def _get_targeting_options(self, first_level_id: str, placement_ids: List[str]) -> Dict[str, List[Any]]:
        local_response: Dict[str, List[Any]] = {}
        if self._is_credentials():
            response = (
                self._service.advertisers()
                .lineItems()
                .bulkListAssignedTargetingOptions(
                    advertiserId=first_level_id,
                    lineItemIds=placement_ids,
                    pageSize=self._CHUNK_SIZE,
                    filter=self._FILTER_TRAGETING_OPTIONS,
                )
                .execute(num_retries=self._RETRIES)
            )
            for lineitem_info in response.get("lineItemAssignedTargetingOptions", []):
                if lineitem_info["lineItemId"] not in local_response:
                    local_response[lineitem_info["lineItemId"]] = []
                local_response[lineitem_info["lineItemId"]].append(lineitem_info.get("assignedTargetingOption", {}))

            nextPageToken: str = response.get("nextPageToken", "")
            while nextPageToken:
                response = (
                    self._service.advertisers()
                    .lineItems()
                    .bulkListAssignedTargetingOptions(
                        advertiserId=first_level_id,
                        lineItemIds=placement_ids,
                        pageSize=self._CHUNK_SIZE,
                        pageToken=nextPageToken,
                        filter=self._FILTER_TRAGETING_OPTIONS,
                    )
                    .execute(num_retries=self._RETRIES)
                )
                for lineitem_info in response.get("lineItemAssignedTargetingOptions", []):
                    local_response[lineitem_info["lineItemId"]].append(lineitem_info.get("assignedTargetingOption", {}))
                nextPageToken = response.get("nextPageToken", "")

        return local_response

    @override
    def clear_placement(self, first_level_id: str, placement_ids: List[str]) -> List[str]:
        """Clear placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to cleare.

        Returns:
        -------
            list: list of cleared placement ids.

        """
        for placement_id in placement_ids:
            placement = self.get_placement(first_level_id=first_level_id, placement_id=placement_id)
            if placement["lineItemType"] in self.YOUTUBE_LINEITEM_TYPES:
                # TODO: SDF
                pass
            else:
                local_response = self._get_targeting_options(first_level_id=first_level_id, placement_ids=[placement_id])
                while local_response:
                    response = (
                        self._service.advertisers()
                        .lineItems()
                        .bulkEditAssignedTargetingOptions(
                            advertiserId=first_level_id,
                            body={
                                "lineItemIds": [placement_id],
                                "deleteRequests": [
                                    {
                                        "targetingType": targeting_type,
                                        "assignedTargetingOptionIds": list(
                                            set(
                                                [
                                                    options["assignedTargetingOptionId"]
                                                    for options in local_response.get(placement_id, [])
                                                    if options["targetingType"] == targeting_type
                                                ]
                                            )
                                        )[: self._CHUNK_SIZE],
                                    }
                                    for targeting_type in self._TARGETING_TYPES
                                ],
                            },
                        )
                        .execute(num_retries=self._RETRIES)
                    )
                    local_response = self._get_targeting_options(first_level_id=first_level_id, placement_ids=[placement_id]) if response.get("updatedLineItemIds", []) else {}
        return placement_ids

    @override
    def set_targeting_options(
        self,
        first_level_id: str,
        placement_ids: List[str],
        locations: List[List[str] | List[Tuple[float, float, float]]],
        periods: List[List[Tuple[str, Tuple[int, int]]]],
        format: LocationFormats = LocationFormats.h3,
        is_set_in_each_placement: bool = True,
    ) -> Tuple[List[str], List[str]]:
        """Set targeting into placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to pause.
            locations (List[List[str] | List[Tuple[float, float, float]]]): list of locations either H3 list or list of (latitude,longitude,radius).
            periods (List[List[Tuple[str, Tuple[int, int]]]]): time periods in format (day_of_week,(start_hour, end_hour)). end_hour is not included.
            format (LocationFormats, optional): format of locations. Default: LocationFormats.h3
            is_set_in_each_placement (bool, optional): set the same locations and periods to all placements.
                Locations and periods should have the same size as placement_ids. Defaults to True.

        Returns:
        -------
            Tuple[List[str], List[str]]: list of updated placement ids, list of created placement dublicates ids.

        """
        # TODO: SDF
        duplicate_ids: List[str] = []
        local_placement_ids: List[str] = []
        if self._is_credentials():
            # TODO: Move to super class
            if is_set_in_each_placement:
                full_periods = sorted(set(flatten_concatenation(periods)))
                full_locations = sorted(set(flatten_concatenation(locations)))
                local_periods = [full_periods for _ in placement_ids]
                local_locations = [full_locations for _ in placement_ids]
            else:
                local_periods = periods
                local_locations = locations

            # Depends on number of elements in locations create duplicates
            locations_to_set: List[Any] = []
            periods_to_set: List[Any] = []

            is_youtube = False
            for placement_id in placement_ids:
                placement = self.get_placement(first_level_id=first_level_id, placement_id=placement_id)
                if placement["lineItemType"] in self.YOUTUBE_LINEITEM_TYPES:
                    is_youtube = True
                    break
            if is_youtube:
                # TODO: SDF
                local_placement_ids = placement_ids
            else:
                for i, lineitem_id in enumerate(placement_ids):
                    max_locations = self.get_locations_max()
                    local_placement_ids.append(lineitem_id)
                    if len(local_locations[i]) > max_locations:
                        splitted_locations = [location for location in generate_batches(local_locations[i], max_locations)]
                        duplicated_lineitem_ids = self.duplicate_placement(
                            first_level_id=first_level_id, placement_id=lineitem_id, suffixes=[f" - # {j}" for j in range(len(splitted_locations) - 1)]
                        )
                        duplicate_ids.extend(duplicated_lineitem_ids)
                        local_placement_ids.extend(duplicated_lineitem_ids)
                        periods_to_set.append(local_periods[i])
                        for _ in duplicated_lineitem_ids:
                            periods_to_set.append(local_periods[i])
                        for location in splitted_locations:
                            locations_to_set.append(location)
                    else:
                        locations_to_set.append(local_locations[i])
                        periods_to_set.append(local_periods[i])

                if periods_to_set:
                    # Date Time options is not big - can be handelded with one request
                    [
                        (
                            self._service.advertisers()
                            .lineItems()
                            .bulkEditAssignedTargetingOptions(
                                advertiserId=first_level_id,
                                body={
                                    "lineItemIds": [placement_id],
                                    "createRequests": [
                                        {
                                            "targetingType": "TARGETING_TYPE_DAY_AND_TIME",
                                            "assignedTargetingOptions": PlatformDV360.to_format_periods(periods=periods_to_set[i]),
                                        }
                                    ],
                                },
                            )
                            .execute(num_retries=self._RETRIES)
                        )
                        for i, placement_id in enumerate(local_placement_ids)
                    ]
                    # Validation of response have no sense as complex hierarhy of responses (error if repeat to set the same value e.g.).
                    # If you want to validate set options - use get_targeting_options method.
                if locations_to_set:
                    [
                        (
                            self._service.advertisers()
                            .lineItems()
                            .bulkEditAssignedTargetingOptions(
                                advertiserId=first_level_id,
                                body={
                                    "lineItemIds": [placement_id],
                                    "createRequests": [
                                        {
                                            "targetingType": "TARGETING_TYPE_POI",
                                            "assignedTargetingOptions": PlatformDV360.to_format_locations(locations=batch_locations, format=format),
                                        }
                                    ],
                                },
                            )
                            .execute(num_retries=self._RETRIES)
                        )
                        for i, placement_id in enumerate(local_placement_ids)
                        for batch_locations in generate_batches(locations_to_set[i], self._CHUNK_SIZE)
                    ]
                    # Validation of response have no sense as complex hierarhy of responses (error if repeat to set the same value e.g.).
                    # If you want to validate set options - use get_targeting_options method.
        return local_placement_ids, duplicate_ids

    @override
    def get_targeting_options(
        self, first_level_id: str, placement_ids: List[str], format: LocationFormats = LocationFormats.h3
    ) -> List[Tuple[List[str] | List[Tuple[float, float, float]], List[Tuple[str, Tuple[int, int]]]]]:
        """Get targeting for placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to pause.
            format (LocationFormats, optional): format of locations. Default: LocationFormats.h3

        Returns:
        -------
            List[Tuple[List[str] | List[Tuple[float, float, float]]], List[Tuple[str, Tuple[int, int]]]]]: per each placement - list of locations, list of periods.

        """
        result: List[Tuple[List[str] | List[Tuple[float, float, float]], List[Tuple[str, Tuple[int, int]]]]] = []
        local_response = self._get_targeting_options(first_level_id=first_level_id, placement_ids=placement_ids)

        for lineitem_id in placement_ids:
            response = local_response.get(lineitem_id, [])
            result.append(
                (
                    PlatformDV360.from_format_locations(locations=[v for v in response if v["targetingType"] == "TARGETING_TYPE_POI"], format=format),
                    PlatformDV360.from_format_periods(periods=[v for v in response if v["targetingType"] == "TARGETING_TYPE_DAY_AND_TIME"]),
                )
            )
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
                "dayAndTimeDetails": {
                    "dayOfWeek": day_of_week,
                    "startHour": min(max(start_hour, 0), 23),
                    "endHour": max(min(end_hour, 24), 1),
                    "timeZoneResolution": "TIME_ZONE_RESOLUTION_ADVERTISER",
                }
            }
            for day_of_week, (start_hour, end_hour) in periods
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
        return [
            (
                period["dayAndTimeDetails"]["dayOfWeek"],
                (
                    period["dayAndTimeDetails"].get("startHour", 0),
                    period["dayAndTimeDetails"]["endHour"],
                ),
            )
            for period in periods
        ]

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
                    lats = f"{round(lat, 6):.6f}".split(".")
                    lngs = f"{round(lng, 6):.6f}".split(".")
                    result.append(
                        {
                            "poiDetails": {
                                "targetingOptionId": f"{lats[0]}{lats[1]:06};{lngs[0]}{lngs[1]:06}",
                                "proximityRadiusAmount": min(round(LocationFormats.edge_length(str(cell), unit="km"), 3), PlatformDV360._MAX_LOCATION_RADIUS),
                                "proximityRadiusUnit": "DISTANCE_UNIT_KILOMETERS",
                            }
                        }
                    )
                except Exception:
                    pass
        else:
            for cell in locations:
                lat, lng, radius = tuple(cell)
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    lats = f"{round(lat, 6):.6f}".split(".")
                    lngs = f"{round(lng, 6):.6f}".split(".")
                    result.append(
                        {
                            "poiDetails": {
                                "targetingOptionId": f"{lats[0]}{lats[1]:06};{lngs[0]}{lngs[1]:06}",
                                "proximityRadiusAmount": min(float(str(radius)), PlatformDV360._MAX_LOCATION_RADIUS),
                                "proximityRadiusUnit": "DISTANCE_UNIT_KILOMETERS",
                            }
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
        result: List[Any] = [
            (
                int(cell["poiDetails"]["targetingOptionId"].split(";")[0]) / 1000000,
                int(cell["poiDetails"]["targetingOptionId"].split(";")[1]) / 1000000,
                cell["poiDetails"]["proximityRadiusAmount"] * (1.60934 if cell["poiDetails"]["proximityRadiusUnit"] == "DISTANCE_UNIT_MILES" else 1.0),
            )
            for cell in locations
        ]
        return Platform.location_to_h3(result) if format == LocationFormats.h3 else result
