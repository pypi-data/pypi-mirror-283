from typing import Union, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field


class Template(SQLModel, table=True):
    name: str = Field(default='unnamed')
    type: str = Field(...)
    content: Optional[str] = Field(None)
    # ctime: Optional[datetime]
    # utime: Optional[datetime]
    creator: int = Field(...)
    id: Optional[int] = Field(None, primary_key=True)

class Templates(SQLModel):
    data: list[Template]
    count: int


class Router(SQLModel, table=True):
    name: str = Field(default='unnamed')
    node_ids: str = Field(...)
    edge_ids: Optional[str] = Field(None)
    # ctime: Optional[datetime]
    # utime: Optional[datetime]
    id: Optional[int] = Field(None, primary_key=True)

class Routers(SQLModel):
    data: list[Router]
    count: int


class Node(SQLModel, table=True):
    name: str = Field(default='unnamed')
    description: str = Field(...)
    system_template_ids: str = Field(...)
    user_template_ids: str = Field(...)
    tool_names: Optional[str] = Field(None)
    chat_limit: int = Field(...)
    goal: Optional[str] = Field(None)
    # ctime: Optional[datetime]
    # utime: Optional[datetime]
    id: Optional[int] = Field(None, primary_key=True)

class Nodes(SQLModel):
    data: list[Node]
    count: int


class Edge(SQLModel, table=True):
    start_id: int = Field(...)
    end_id: int = Field(...)
    goal: str = Field(...)
    weight: float = Field(...)
    # ctime: Optional[datetime]
    # utime: Optional[datetime]
    id: Optional[int] = Field(None, primary_key=True)

class Edges(SQLModel):
    data: list[Edge]
    count: int


class Chat(SQLModel, table=True):
    uid: int = Field(...)
    router_id: int = Field(...)
    whole_conversation_text: str = Field(...)
    whole_conversation_voice: str = Field(...)
    # ctime: Optional[datetime]
    # utime: Optional[datetime]
    id: Optional[int] = Field(None, primary_key=True)

class Chats(SQLModel):
    data: list[Chat]
    count: int