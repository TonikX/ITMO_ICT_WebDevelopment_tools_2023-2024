from sqlmodel import SQLModel, Field


# Associative table
class ScheduleTaskDefault(SQLModel):
    schedule_id: int | None = Field(default=None, foreign_key="schedule.id", primary_key=True)
    task_id: int | None = Field(default=None, foreign_key="task.id", primary_key=True)
