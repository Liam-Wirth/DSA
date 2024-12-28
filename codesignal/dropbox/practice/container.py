class Container:
    """
    A container of integers that should support
    addition, removal, and search for the median integer
    """
    def __init__(self):
        self.data = []

    def add(self, value: int) -> None:
        """
        Adds the specified value to the container

        :param value: int
        """
        self.data.append(value)

    def delete(self, value: int) -> bool:
        """
        Attempts to delete one item of the specified value from the container

        :param value: int
        :return: True, if the value has been deleted, or
                 False, otherwise.
        """
        try:
            self.data.remove(value)
            return True
        except ValueError:
            return False

    def get_median(self) -> int:
        """
        Finds the container's median integer value, which is
        the middle integer when the all integers are sorted in order.
        If the sorted array has an even length,
        the leftmost integer between the two middle 
        integers should be considered as the median.

        :return: The median if the array is not empty, or
        :raise:  a runtime exception, otherwise.
        """
        if len(self.data) == 0:
            raise RuntimeError("Container is Empty")
        else:
            sorted_data = sorted(self.data)  # Sort the data
            n = len(sorted_data)
            return sorted_data[(n - 1) // 2]

