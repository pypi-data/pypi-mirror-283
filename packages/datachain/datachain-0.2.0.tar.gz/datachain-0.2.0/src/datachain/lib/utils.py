class DataChainError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DataChainParamsError(DataChainError):
    def __init__(self, message):
        super().__init__(message)
