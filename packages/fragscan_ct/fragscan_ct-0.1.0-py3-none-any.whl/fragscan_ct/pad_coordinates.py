def pad_coordinates(start, end, pad_size):
    """
    The function pads the given coordinates with the specified pad size.

    :param start: The starting coordinate of the range
    :param end: The `end` parameter represents the end coordinate value
    :param pad_size: The pad_size parameter is the amount by which the coordinates should be padded
    :return: the padded start and end coordinates.
    """
    padded_start = max(start - pad_size, 0)
    padded_end = end + pad_size
    return padded_start, padded_end