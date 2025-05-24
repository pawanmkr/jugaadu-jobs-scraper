from typing import TypedDict, List, Optional

class Job(TypedDict):
    title: str
    logoPath: Optional[str]
    logoPathV3: Optional[str]
    jobId: str
    currency: str
    footerPlaceholderLabel: str
    footerPlaceholderColor: str
    companyName: str
    isSaved: bool
    tagsAndSkills: List[str]
    placeholders: List[str]
    companyId: str
    jdURL: str
    staticUrl: str
    jobDescription: str
    showMultipleApply: bool
    groupId: str
    isTopGroup: bool
    createdDate: str
    mode: str
    board: str
    experienceText: str
    saved: bool
