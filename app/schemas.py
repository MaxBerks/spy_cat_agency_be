from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Set
import httpx
import os

# ---------- Cats ----------
CAT_API_URL = "https://api.thecatapi.com/v1/breeds"
CAT_API_KEY = os.getenv("CAT_API_KEY", None)
_VALID_BREEDS_CACHE: Optional[Set[str]] = None

def fetch_breeds() -> Optional[Set[str]]:
    headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}
    try: 
        r = httpx.get(CAT_API_URL, headers=headers, timeout=8.0)
        if r.status_code == 200:
            return {b["name"].lower() for b in r.json()}
        return None
    except Exception:
        return None

class SpyCatCreate(SpyCatBase):
    @field_validator("breed")
    @classmethod
    def validate_breed(cls, v: str):
        global _VALID_BREEDS_CACHE
        
        if _VALID_BREEDS_CACHE is None:
            _VALID_BREEDS_CACHE = fetch_breeds()
        
        if not _VALID_BREEDS_CACHE:
            return v
        
        if v.lower() not in _VALID_BREEDS_CACHE:
            raise ValueError(f"Invalid breed: {v}")
        return v

class SpyCatUpdate(BaseModel):
    salary: float = Field(gt=0)


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