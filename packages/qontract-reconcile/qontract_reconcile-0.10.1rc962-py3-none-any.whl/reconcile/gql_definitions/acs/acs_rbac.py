"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)


DEFINITION = """
query AcsRbac  {
  acs_rbacs: users_v1 {
    org_username
    roles {
      name
      oidc_permissions {
        name
        description
        service
        ... on OidcPermissionAcs_v1 {
          permission_set
          clusters {
            name
          }
          namespaces {
            name
            cluster {
              name
            }
          }
        }
      }
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class OidcPermissionV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    description: str = Field(..., alias="description")
    service: str = Field(..., alias="service")


class ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class NamespaceV1_ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class NamespaceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    cluster: NamespaceV1_ClusterV1 = Field(..., alias="cluster")


class OidcPermissionAcsV1(OidcPermissionV1):
    permission_set: str = Field(..., alias="permission_set")
    clusters: Optional[list[ClusterV1]] = Field(..., alias="clusters")
    namespaces: Optional[list[NamespaceV1]] = Field(..., alias="namespaces")


class RoleV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    oidc_permissions: Optional[list[Union[OidcPermissionAcsV1, OidcPermissionV1]]] = Field(..., alias="oidc_permissions")


class UserV1(ConfiguredBaseModel):
    org_username: str = Field(..., alias="org_username")
    roles: Optional[list[RoleV1]] = Field(..., alias="roles")


class AcsRbacQueryData(ConfiguredBaseModel):
    acs_rbacs: Optional[list[UserV1]] = Field(..., alias="acs_rbacs")


def query(query_func: Callable, **kwargs: Any) -> AcsRbacQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        AcsRbacQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return AcsRbacQueryData(**raw_data)
