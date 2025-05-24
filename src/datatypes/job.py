from typing import TypedDict


class Job(TypedDict):
    title: str
    logoPath: str | None
    logoPathV3: str | None
    jobId: str
    currency: str
    footerPlaceholderLabel: str
    footerPlaceholderColor: str
    companyName: str
    isSaved: bool
    tagsAndSkills: list[str]
    placeholders: list[str]
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
