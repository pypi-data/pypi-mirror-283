from collections import UserList


class EnumTuple(tuple):
    """
    Tuple that automatically contains the values.
    Allows easy comparisons of tuples with Enum and non-enum values.
    """

    @classmethod
    def extract_value(cls, item):
        if hasattr(item, "value"):
            return item.value
        if isinstance(item, tuple):
            return tuple(cls.extract_value(sub_item) for sub_item in item)
        return item

    def __new__(cls, *args):
        processed_args = tuple(cls.extract_value(arg) for arg in args)
        return super().__new__(cls, processed_args)

    def __contains__(self, item) -> bool:
        item = self.extract_value(item)
        return super().__contains__(item)


class EnumList(UserList):
    """
    List that automatically contains the values.
    Allows easy comparisons of list with Enum and non-enum values.
    """

    @classmethod
    def extract_value(cls, item):
        if hasattr(item, "value"):
            return item.value
        if isinstance(item, (tuple, list)):
            return type(item)(cls.extract_value(sub_item) for sub_item in item)
        return item

    def __init__(self, initlist=None):
        if initlist is None:
            initlist = []
        processed_list = [self.extract_value(item) for item in initlist]
        super().__init__(processed_list)

    def __setitem__(self, i, item):
        processed_item = self.extract_value(item)
        super().__setitem__(i, processed_item)

    def append(self, item):
        processed_item = self.extract_value(item)
        super().append(processed_item)

    def insert(self, i, item):
        processed_item = self.extract_value(item)
        super().insert(i, processed_item)

    def __contains__(self, item) -> bool:
        item = self.extract_value(item)
        return super().__contains__(item)
