import json

import pandas as pd


class Logger:
    def __init__(self, host):
        self.host = host
        self.records = []

    def log(self):
        """Log data by directly accessing host attributes."""
        state_info = {
            attr: getattr(self.host, attr)
            for attr in dir(self.host)
            if not callable(getattr(self.host, attr)) and not attr.startswith("__") and attr != "logger"
        }
        self.records.append(json.dumps(state_info))

    def toPandas(self):
        """Convert the logged records to a Pandas DataFrame."""
        return pd.DataFrame([json.loads(record) for record in self.records])