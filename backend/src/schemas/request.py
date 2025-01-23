from typing import Optional
from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    projectId: int
    projectName: str
    startDate: str
    endDate: str
    feedbackScore: Optional[int]
    manageName: str
    requestName: str
    status: int
