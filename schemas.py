"""
Database Schemas for The Sanctuary of Nature

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from typing import Optional, List
from pydantic import BaseModel, Field

class Host(BaseModel):
    name: str = Field(..., description="Host or facilitator name")
    bio: Optional[str] = Field(None, description="Short bio")
    specialties: List[str] = Field(default_factory=list, description="Modalities: meditation, breathwork, yoga, sound, etc.")
    website: Optional[str] = None
    location: Optional[str] = Field(None, description="Primary base location of the host")

class Location(BaseModel):
    title: str = Field(..., description="Sanctuary name or place title")
    region: str = Field(..., description="Country/Region")
    nature_type: str = Field(..., description="desert | forest | mountain | ocean | jungle | mixed")
    description: Optional[str] = None
    image_url: Optional[str] = None

class Retreat(BaseModel):
    title: str
    description: Optional[str] = None
    host_name: str = Field(..., description="Name of the host facilitating")
    location_title: str = Field(..., description="Name of the location/sanctuary")
    nature_type: str = Field(..., description="desert | forest | mountain | ocean | jungle | mixed")
    focus: List[str] = Field(default_factory=list, description="e.g., meditation, detox, silence, ayurvedic, eco-building")
    duration_days: int = Field(..., ge=1, le=60)
    price_usd: float = Field(..., ge=0)
    start_date: Optional[str] = Field(None, description="ISO date string")
    image_url: Optional[str] = None

class Message(BaseModel):
    author: str = Field(..., description="Name or nickname")
    content: str = Field(..., description="Community message")
    topic: Optional[str] = Field(None, description="general | requests | offerings | rideshare | Q&A")

class Preference(BaseModel):
    energy: Optional[str] = Field(None, description="calm | transformative | adventurous | restorative")
    preferred_nature: Optional[str] = Field(None, description="desert | forest | mountain | ocean | jungle | mixed")
    budget: Optional[float] = Field(None, description="Approx budget in USD")
    duration: Optional[int] = Field(None, description="Preferred days")
    goals: Optional[str] = Field(None, description="Free text: meditate deeper, release stress, connect to nature...")
