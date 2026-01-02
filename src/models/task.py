from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    priority: Optional[str] = None  # 'high', 'medium', 'low'
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None # 'daily', 'weekly', etc.

    def __post_init__(self):
        if self.priority and self.priority not in ['high', 'medium', 'low']:
            raise ValueError("Priority must be 'high', 'medium', or 'low'")
        if self.due_date and not isinstance(self.due_date, datetime):
            raise TypeError("due_date must be a datetime object")
