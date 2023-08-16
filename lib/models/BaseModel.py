class BaseModel:
    _raw_name: str = "base_model"
    _node_name: str = "base_model"

    def __init__(self, json_item) -> None:
        object_attributes = [
            attribute
            for attribute in self.__annotations__.keys()
            if attribute[0] != "_"
        ]

        for attribute in object_attributes:
            setattr(self, attribute, json_item[attribute])

    def to_cypher(self):
        cypher_string = ""
        model_items = list(enumerate(self.__dict__.items()))

        for index, (key, value) in model_items:
            if type(value) == str:
                value = '"{}"'.format(value.replace('"', "'"))

            formatted_key = key.replace("'", "")
            cypher_string += (
                f"{formatted_key}: {value}{', ' if index < len(model_items) -1 else ''}"
            )

        return "{" + cypher_string + "}"

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__dict__}
