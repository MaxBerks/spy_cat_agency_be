from pydantic import BaseModel, Field
from typing import List, Optional

# ---------- Cats ----------
class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int = Field(ge=0)
    breed: str
    salary: float = Field(gt=0)

class SpyCatCreate(SpyCatBase):
    pass  #TODO breed validation via TheCatAPI

class SpyCatUpdate(BaseModel):
    salary: float = Field(gt=0)

class SpyCatResponse(SpyCatBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Targets ----------
class TargetBase(BaseModel):
    name: str
    country: str
    notes: str = ""
    is_complete: bool = False

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None

class TargetResponse(TargetBase):
    id: int
    mission_id: int
    class Config:
        from_attributes = True

# ---------- Missions ----------
class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(min_length=1, max_length=3)
    cat_id: Optional[int] = None  

class MissionUpdate(BaseModel):
    cat_id: Optional[int] = None

class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int] = None
    is_complete: bool
    targets: List[TargetResponse]
    class Config:
        from_attributes = True

class MissionAssign(BaseModel):
    cat_id: int