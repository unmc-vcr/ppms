from pydantic import (
    BaseModel,
    Field,
    AliasChoices,
    BeforeValidator,
    PastDatetime
)
from typing import Optional, ClassVar, Annotated, Union

def parse_empty_or_datetime(val: str):
    return None if val == '' else val

past_datetime_or_none = Annotated[Union[PastDatetime, None], BeforeValidator(parse_empty_or_datetime)]


class Group(BaseModel):
    _OBJECT_TYPE: ClassVar[int] = 5
    id: int = Field(validation_alias=AliasChoices('id', 'UnitID'))
    name: str = Field(validation_alias=AliasChoices('name', 'UnitName'))
    head: str = Field(validation_alias=AliasChoices('head', 'Chef'))
    headName: str = Field(validation_alias=AliasChoices('headName', 'ChefName'))
    department: str = Field(validation_alias=AliasChoices('department', 'Department'))
    institution: str
    label: Optional[str] = ""


class GroupDetail(Group):
    bcode: str
    isBcodePending: bool
    isGroupFinancialAccountActive: bool
    isGroupFinancialAccountValid: bool
    isGroupFinancialAccountStartDatePassed: bool
    isGroupFinancialAccountExpirationDatePassed: bool
    unitAccountAffiliation: str
    UserContract: bool
    ContactUserID: int
    MadeByUserID: int
    MadeDate: past_datetime_or_none = None
    Ext: bool
    ExtType: str
    InvoicingAddress: str
    NotInvoiced: bool
    Active: bool
    ChefEmail: str
    fax: str
    admName: str
    admEmail: str
    admUserID: str
    admPhone: str
    updated: bool
    new: bool
    affiliation: int
    groupcustom1name: str
    groupcustom2name: str
    groupcustom3name: str
    groupcustom4name: str
    groupcustom5name: str
    groupcustom6name: str
    groupcustom7name: str
    groupcustom8name: str
    groupcustom1mand: bool
    groupcustom2mand: bool
    groupcustom3mand: bool
    groupcustom4mand: bool
    groupcustom5mand: bool
    groupcustom6mand: bool
    groupcustom7mand: bool
    groupcustom8mand: bool
    custom1: str
    custom2: str
    custom3: str
    custom4: str
    custom5: str
    custom6: str
    custom7: str
    custom8: str
    ORCID: str
    canBeDeleted: bool
    isVirtualInternalAccountTypeOn: bool
    isVirtualExternalAccountTypeOn: bool