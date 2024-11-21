import models

class TaskParser:
    def __init__(self, task_notion: dict) -> None:
        self.task_notion = task_notion
    
    
    def get_title(self) -> str | None:
        title_list = self.get_value_or_none(
            self.task_notion,
            ["Name", "title"]
        )
        if len(title_list) == 0:
            return None
        title_object = title_list[0]
        title = self.get_value_or_none(
            title_object,
            ['plain_text']
        )
        return title
    
    
    def get_category_title(self) -> str | None:
        title = self.get_value_or_none(
            self.task_notion, 
            ("Tasks", "select", "name")
        )
        return title
        
    def get_description(self) -> str | None:
        return None
    
    def get_deadline(self) -> str | None:
        deadline = self.get_value_or_none(
            self.task_notion, 
            ("due", "date", "start")
        )
        return deadline
        
    
    def get_priority(self) -> models.Priority | None:
        urgent_flag = self.get_value_or_none(
            self.task_notion,
            ['Urgent', 'checkbox']
        )
        if urgent_flag:
            return models.Priority.high
        return models.Priority.low
    
    def get_approximate_time(self) -> int | None:
        approximate_time = self.get_value_or_none(
            self.task_notion,
            ["Aproximate time", 'number']
        )
        if approximate_time is not None:
            approximate_time = int(approximate_time)
        return approximate_time
    
    @staticmethod
    def get_value_or_none(d, keys_tuple):
        for key in keys_tuple:
            if d is None:
                return None
            if key not in keys_tuple:
                return None
            
            d = d[key]
        return d
