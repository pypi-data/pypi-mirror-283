from datetime import date, datetime, time

from pydantic import BaseModel


class ReachBaseModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        original_dict = super().model_dump(*args, **kwargs)
        for key, value in original_dict.items():
            if isinstance(value, datetime):
                original_dict[key] = value.isoformat()
            elif isinstance(value, date):
                original_dict[key] = value.isoformat()
            elif isinstance(value, time):
                original_dict[key] = value.strftime("%H:%M:%S")
        return original_dict
