class ObjectNotExist(Exception):
    def __init__(self, model_name: str):
        self.model = model_name


class ObjectWithGivenAttrExist(Exception):
    def __init__(self, model_name: str, attr_name: str):
        self.model = model_name
        self.attr = attr_name


class ObjectNotExistInBody(Exception):
    def __init__(self, model_name: str):
        self.model = model_name
