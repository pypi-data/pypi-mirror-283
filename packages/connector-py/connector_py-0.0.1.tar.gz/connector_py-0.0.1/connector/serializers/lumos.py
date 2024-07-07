from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    MOCK_CONNECTOR_RESOURCE_1 = "MOCK_CONNECTOR_RESOURCE_1"
    GITHUB_REPOSITORY = "GITHUB_REPOSITORY"
    GITHUB_TEAM = "GITHUB_TEAM"


class EntitlementType(str, Enum):
    MOCK_CONNECTOR_ENTITLEMENT_1 = "MOCK_CONNECTOR_ENTITLEMENT_1"
    GITHUB_REPOSITORY_ROLE = "GITHUB_REPOSITORY_ROLE"
    GITHUB_TEAM_ROLE = "GITHUB_TEAM_ROLE"


class FoundAccountData(BaseModel):
    integration_specific_id: str
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    username: Optional[str] = None
    user_status: Optional[str] = None


class FoundResourceData(BaseModel):
    integration_specific_id: str
    label: str
    resource_type: ResourceType
    extra_data: Optional[Dict[str, str]] = None


class FoundEntitlementData(BaseModel):
    integration_specific_id: str
    integration_specific_resource_id: str
    is_assignable: bool
    label: str
    entitlement_type: EntitlementType
    extra_data: Optional[Dict[str, str]] = None


class FoundEntitlementAssociation(BaseModel):
    integration_specific_entitlement_id: str
    account: FoundAccountData
    integration_specific_resource_id: str


Response = TypeVar("Response")


class ResponseWrapper(BaseModel, Generic[Response]):
    response: Response
    errors: list[str]
    raw_data: dict[str, Any] | None


class BaseArgs(BaseModel):
    include_raw_data: bool = Field(default=False)


class ListAccountsArgsBase(BaseArgs):
    pass


class ListAccountsResp(ResponseWrapper[list[FoundAccountData]]):
    pass


class ValidateCredentialsArgsBase(BaseArgs):
    pass


class ValidateCredentialsResp(ResponseWrapper[bool]):
    pass


class GetAccountArgsBase(BaseArgs):
    pass


class GetAccountResp(ResponseWrapper[FoundAccountData]):
    pass


class ListResourcesArgsBase(BaseArgs):
    resource_types: List[ResourceType]


class ListResourcesResp(ResponseWrapper[dict[ResourceType, list[FoundResourceData]]]):
    pass


class GetResourceArgsBase(BaseArgs):
    integration_specific_id: str


class GetResourceResp(ResponseWrapper[FoundResourceData]):
    pass


class ListEntitlementsArgsBase(BaseArgs):
    resource_integration_specific_ids: List[str]


class ListEntitlementsResp(ResponseWrapper[list[FoundEntitlementData]]):
    pass


class FindEntitlementAssociationsArgsBase(BaseArgs):
    accounts: List[FoundAccountData]
    resources: List[FoundResourceData]
    entitlements: List[FoundEntitlementData]


class FindEntitlementAssociationsResp(ResponseWrapper[list[FoundEntitlementAssociation]]):
    pass


class AssignEntitlementArgsBase(BaseArgs):
    account: FoundAccountData
    entitlement: FoundEntitlementData


class AssignEntitlementResp(ResponseWrapper[bool]):
    pass


class UnassignEntitlementArgsBase(BaseArgs):
    account: FoundAccountData
    entitlement: FoundEntitlementData


class UnassignEntitlementResp(ResponseWrapper[bool]):
    pass
