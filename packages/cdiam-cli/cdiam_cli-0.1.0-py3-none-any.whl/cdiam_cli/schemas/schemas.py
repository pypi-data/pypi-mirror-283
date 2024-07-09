from pydantic import BaseModel
from typing import Literal, Optional
from sqlmodel import (
    Field,
    SQLModel,
    ForeignKeyConstraint,
    Column,
    DateTime,
    func,
    Relationship,
    UniqueConstraint,
    BigInteger,
)
import sqlalchemy as sa
from pydantic import validator, BaseModel
from datetime import datetime
from typing import Union, Callable, ClassVar, Optional, List, Dict, Any
import json


class ProjectSettings(BaseModel):
    class Config:
        orm_mode = True

    cpdb: List[str] = []
    enrichment: List[str] = []

    @staticmethod
    def encode_settings(settings: Union[Dict[str, Any], "ProjectSettings"]) -> str:
        return ProjectSettings.parse_obj(settings).json()

    @staticmethod
    def decode_setting(settings: str) -> "ProjectSettings":
        if settings is None:
            settings = "{}"
        return ProjectSettings.parse_obj(json.loads(settings))


class ProjectBase(SQLModel):
    name: str = Field(max_length=128, nullable=False)


class Project(ProjectBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "project"
    id: str = Field(
        max_length=128, nullable=False, primary_key=True, index=True, unique=True
    )
    tombstone: Optional[bool] = Field(
        default=False,
        nullable=False,
        description="Deleted marker of the project. True = deleted",
    )
    time_created: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="Time added",
    )
    is_public: bool = Field(
        default=False,
        nullable=False,
        description="If the project is public",
    )
    delete_date: Optional[datetime] = Field(
        default=None, sa_column=Column(sa.DateTime(timezone=True), nullable=True)
    )
    settings: Optional[str] = Field(
        default=None,
        max_length=10240,
        nullable=True,
    )
    storage_used: int = Field(
        sa_column=Column(BigInteger),
        nullable=True,
        description="Non-zero expression values",
    )
    created_by: str = Field(
        max_length=128,
        nullable=False,
        index=True,
        foreign_key="user.email",
    )

    @validator("settings")
    def validate_settings(cls, v: str):
        if v == "nan":
            v = "{}"
        if v is None:
            v = "{}"
        return ProjectSettings.encode_settings(ProjectSettings.decode_setting(v))

    @validator("tombstone")
    def validate_tombstone(cls, v):
        if not v:
            return False
        return v


class ParamsRequestGetTaskStatus(BaseModel):
    """
    Represents the parameters for a request to get the status of an analysis task.

    :param api: The API endpoint being called, which should be "get_task_status".
    :param task_id: The unique identifier of the analysis task.
    """

    api: Literal["get_task_status"]
    task_id: str


class TaskStatus(BaseModel):
    status: str = "UNKNOWN"


class AnalysisResultBase(SQLModel):
    result_id: str = Field(
        max_length=128,
        nullable=False,
        primary_key=True,
        description="ID of the analysis",
    )
    data_id: str = Field(max_length=128, nullable=False, description="ID of the data")
    analysis: int = Field(
        nullable=False,
        foreign_key="analysis_catalog.id",
        description="Reference to the analysis",
    )
    task_id: str = Field(
        max_length=128,
        nullable=False,
        sa_column_kwargs={"server_default": ""},
        description="ID of task in celery",
    )
    args: str = Field(
        max_length=10240,
        default="{}",
        nullable=False,
        description="Args of the analysis",
        sa_column_kwargs={"server_default": "{}"},
    )
    project_id: str = Field(
        max_length=128,
        nullable=False,
        description="ID of project this analysis belong to",
    )
    user_email: Optional[str] = Field(max_length=256, nullable=True)


class AnalysisCatalogBase(SQLModel):
    name: str = Field(nullable=False, description="Name of the analysis")
    description: Optional[str] = Field(
        max_length=4096, description="Detailed information about this analysis"
    )


class AnalysisCatalog(AnalysisCatalogBase, table=True):
    """
    This table stores available analyses type
    that the App supports.
    """

    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "analysis_catalog"
    id: int = Field(primary_key=True)
    time_created: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="Time added",
    )
    time_modified: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
        description="Time modified",
    )
    """A list of all analysis results of this type"""
    results: List["AnalysisResult"] = Relationship(back_populates="analysis_orm")

    __table_args__ = (UniqueConstraint("name", name="_name_analysis_uc"),)


class AnalysisResultRead(AnalysisResultBase):
    """
    A response model of an anlysis result
    """

    time_created: datetime
    time_modified: datetime
    task: Optional[TaskStatus]
    result_data_status: Optional[str]


class AnalysisResult(AnalysisResultBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "analysis_result"
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id"], ["project.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    """
    This table stores all analyses that had been produced for a data 
    The analysis reference points to the description of the analysis.
    The result_id reference points to the detail result of the analysis
    """
    time_created: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="Time added",
    )
    time_modified: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
        description="Time modified",
    )
    """An object of the analysis type"""
    analysis_orm: AnalysisCatalog = Relationship(back_populates="results")
