from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LoginPayload")


@_attrs_define
class LoginPayload:
    """
    Attributes:
        username (str):  Example: string.
        password (str):  Example: string.
        id_client (Union[Unset, str]):  Example: string.
    """

    username: str
    password: str
    id_client: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        password = self.password

        id_client = self.id_client

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
            }
        )
        if id_client is not UNSET:
            field_dict["idClient"] = id_client

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        id_client = d.pop("idClient", UNSET)

        login_payload = cls(
            username=username,
            password=password,
            id_client=id_client,
        )

        login_payload.additional_properties = d
        return login_payload

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
