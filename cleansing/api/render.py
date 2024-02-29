import json
import pandas as pd
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if pd.isnull(obj):
            return None
        return super().default(obj)

# Usage in your API view
