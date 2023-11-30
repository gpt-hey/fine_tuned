class Remindme:
    def __init__(self):
        self.references = "remind"
    def is_matched(self, text):
        return "@remindme" in text.lower()
    def execute_action(self, text):
        # TODO add action to execute
        return text.replace("@remindme", "")
