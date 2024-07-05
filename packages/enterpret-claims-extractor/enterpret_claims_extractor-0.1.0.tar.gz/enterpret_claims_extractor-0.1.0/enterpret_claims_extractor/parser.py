# To ingest the records from Given Data
class Content:
    def __init__(self, dict):
        self.id = dict["ID"]
        self.url = dict["URL"]
        self.type = dict["Type"]
        self.timestamp = dict["CreatedAt"]
        self.source = dict["Source"]
        self.content = dict["Content"]
        self.summary = dict["Summary"]
        self.reason = dict["Reasons"]
