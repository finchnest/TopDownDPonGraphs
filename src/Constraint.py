from RelationalOp import RelationalOp

class Constraint():
    def __init__(self, key: str, value: str, relationalOp: RelationalOp):
        self.key = key
        self.value = value
        self.relationalOp = relationalOp
