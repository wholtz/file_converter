#!/usr/bin/env python3

from typing import Optional

import pandas as pd
"""
For each file processed, collect the errors and warnings into a panda dataframe with columns:

filename
field_num: int - zero-indexed. Use index == number of field for non-field specific errors
level: str - one of 'warning' or 'error'
description: str
"""

LEVELS = ['error', 'warning']

class ValidationResults:
    """Store and output results of MS file validation"""
    def __init__(self, num_fields: int):
        self.num_fields = num_fields
        self.data = pd.DataFrame({"file_name":[], "field_num": [], "level": [], "description": [])

    def add(self, file_name: str, field_num: int, level: str, description: str):
        assert level in LEVELS
        assert 0 <= field_num <= self.num_fields
        self.data.append({"file_name": file_name, "field_num": field_num, "level": level, "description": description})

    def get_field_summary(self, field_num: Optional[int]) -> pd.DataFrame:
        return [self.data.loc[self.data["field_num"] == field_num &&
                              self.data["level"] == level].groupby("description")
                for level in LEVELS]

    @property
    def summary(self) -> List[Dict[str, str]]:
        return [self.get_field_summary(idx) for idx in range(self.num_fields+1)]

    @property
    def summary_table(self) -> str:
        pass  # TODO

    def count(self, file_name: Optional[str], field_num: Optional[int], level: Optional[str], description: Optional[str]) -> int:
        subset = self.data
        query = {"file_name": file_name, "field_num": field_num, "level": level, "description": description}
        for k, v in query.items():
            if v is not None:
                subset = subset[subset[k] == v]
        return len(subset)

    @property
    def error_count(self):
        return self.count(level="error")

    @property
    def warning_count((self):
        return self.count(level="warning")
