import json


class BaseModel:
    def to_cypher(self):
        cypher_string = ""
        model_items = list(enumerate(self.__dict__.items()))

        for index, (key, value) in model_items:
            if type(value) == str:
                value = f"'{value}'"

            formatted_key = key.replace("'", "")
            cypher_string += (
                f"{formatted_key}: {value}{', ' if index < len(model_items) -1 else ''}"
            )

        print(cypher_string)
        return "{" + cypher_string + "}"
