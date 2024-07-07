from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvalidScopesT")


@_attrs_define
class InvalidScopesT:
    """Not authorised to access this scope

    Example:
        {'id': '123e4567-e89b-12d3-a456-426614174000', 'message': 'Not authorized to perform this action'}

    Attributes:
        message (str): Message of error Example: Not authorized to perform this action.
        id (Union[Unset, str]): ID of involved resource Example: 123e4567-e89b-12d3-a456-426614174000.
    """

    message: str
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        id = d.pop("id", UNSET)

        invalid_scopes_t = cls(
            message=message,
            id=id,
        )

        invalid_scopes_t.additional_properties = d
        return invalid_scopes_t

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
