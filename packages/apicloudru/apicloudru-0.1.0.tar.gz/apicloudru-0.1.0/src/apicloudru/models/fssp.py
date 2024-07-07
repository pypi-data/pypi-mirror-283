from typing import Optional, List
from pydantic import BaseModel

from src.apicloudru.models.base import CommonInfo, Inquiry


class FSSPRecord(BaseModel):
    debtor_name: str
    debtor_address: str
    debtor_dob: str
    process_title: str
    process_date: str
    recIspDoc: str
    stopIP: str
    subject: str
    sum: str
    document_organization: str
    document_type: str
    officer_name: str
    officer_phones: Optional[List[List[str]]]


class FSSPPhysicalSearch(CommonInfo):
    countAll: Optional[str] = 0
    pagesAll: Optional[int] = 0
    totalLoadedPage: Optional[str] = 0
    onlyActual: Optional[bool]
    records: Optional[List[FSSPRecord]] = None
    inquiry: Inquiry
