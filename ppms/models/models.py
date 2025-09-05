from pydantic import (
    BaseModel,
    Field,
    TypeAdapter,
    field_serializer,
    AliasChoices,
    ValidationInfo,
    AliasPath,
    model_validator
)
from typing import List, Optional, Any
from enum import Enum

class User(BaseModel):
    id: int
    name: str
    fullName: str = Field(validation_alias=AliasChoices('fullName', 'label'))
    firstName: str
    lastName: str
    login: str
    active: bool
    ext: bool

class UserDetail(User):
    email: str
    phone: str
    notes: str
    unitId: int
    unitName: str
    userBcode: str
    userAccountAffiliation: str
    isUserBcodePending: bool
    isUserBcodeActive: bool
    isUserBcodeValid: bool
    isUserBcodeExpirationDatePassed: bool
    isUserBcodeStartDatePassed: bool
    unitBcode: str
    isUnitBcodePending: bool
    pendingBcode: str
    usercustom1value: str
    usercustom2value: str
    usercustom3value: str
    usercustom4value: str
    usercustom5value: str
    usercustom6value: str
    usercustom7value: str
    usercustom8value: str
    usercustom1name: str
    usercustom2name: str
    usercustom3name: str
    usercustom4name: str
    usercustom5name: str
    usercustom6name: str
    usercustom7name: str
    usercustom8name: str
    usercustom1mand: bool
    usercustom2mand: bool
    usercustom3mand: bool
    usercustom4mand: bool
    usercustom5mand: bool
    usercustom6mand: bool
    usercustom7mand: bool
    usercustom8mand: bool
    bcodepattern: str
    Passwd: str
    affiliation: int
    mustChPwd: bool
    mustChBcode: bool
    canBeDeleted: bool
    pfInstitution: str
    unitDepartment: str
    adddepttoname: bool
    newusernoautologin: bool
    ORCID: str
    PubMedQuery: str
    skipOrcidQuestion: bool

class PublicationLinkType(str, Enum):
    AUTHOR = 'A'
    GROUP = 'G'
    FACILITY = 'F'
    SERVICE = 'S'
    STAFF = 'U'

class PublicationLink(BaseModel):
    pubid: Optional[int] = None
    id: int
    type: PublicationLinkType
    name: Optional[str] = None

class CrossrefResponse(BaseModel):
    title: str = Field(validation_alias=AliasPath("message", "title", 0))
    journal: str = Field(validation_alias=AliasPath("message", "container-title", 0))
    volume: Optional[str] = Field(validation_alias=AliasPath("message", "volume"), default='')
    yearpub: int = Field(validation_alias=AliasPath("message", "published", "date-parts", 0, 0))
    monthpub: int = Field(validation_alias=AliasPath("message", "published", "date-parts", 0, 1))

class EntrezResponse(BaseModel):
    pubmedid: str = Field(validation_alias=AliasPath("esearchresult", "idlist", 0))

class Publication(BaseModel):
    pubid: Optional[int] = Field(validation_alias="id", default = 0)
    title: Optional[str] = ''
    journal: Optional[str] = ''
    yearpub: Optional[int] = Field(validation_alias="year", default = None)
    monthpub: Optional[int] = Field(validation_alias="month", default = None)
    volume: Optional[str] = ''
    pubmedid: Optional[str] = Field(validation_alias="pubMedId", default = None)
    doi: Optional[str] = Field(validation_alias=AliasChoices('DOI', 'doi'), default='')
    links: Optional[List[PublicationLink]] = Field(exclude=True, default = [])
    validated: Optional[bool] = True

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(by_alias=True, **kwargs)
    
    def model_dump_json(self, **kwargs: Any) -> str:
        return super().model_dump_json(by_alias=True, **kwargs)

    @model_validator(mode='after')
    def get_crossref(self, info: ValidationInfo):
        if (info.context == None) or not (info.context.get('skip_external')):
            res = req.get(f"https://api.crossref.org/works/{self.doi}")
            validated = CrossrefResponse.model_validate_json(res.text)
    
            self.title = validated.title
            self.journal = validated.journal
            self.yearpub = validated.yearpub
            self.monthpub = validated.monthpub

        return self

    @model_validator(mode='after')
    def get_pmid(self, info: ValidationInfo = {}):
        if (info.context == None) or not (info.context.get('skip_external')):
            res = req.get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?=&db=pubmed&retmode=json&term={self.doi}[doi]")
            validated = EntrezResponse.model_validate_json(res.text)
    
            self.pubmedid = validated.pubmedid

        return self

    @field_serializer('validated')
    def serialize_validated(self, validated: bool, _info):
        return str(validated).lower()