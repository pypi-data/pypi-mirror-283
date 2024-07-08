import numpy as np

from aviary._utils.exceptions import AviaryUserError
from aviary._utils.types import (
    Coordinate,
    CoordinatesSet,
)


def validate_bounding_box(
    x_min: Coordinate,
    y_min: Coordinate,
    x_max: Coordinate,
    y_max: Coordinate,
) -> None:
    if x_min >= x_max:
        message = (
            'Invalid bounding box! '
            'x_min must be less than x_max.'
        )
        raise AviaryUserError(message)

    if y_min >= y_max:
        message = (
            'Invalid bounding box! '
            'y_min must be less than y_max.'
        )
        raise AviaryUserError(message)


def validate_coordinates_set(
    coordinates: CoordinatesSet,
) -> None:
    """Validates `coordinates`.

    Parameters:
        coordinates: coordinates (x_min, y_min) of each tile

    Raises:
        AviaryUserError: Invalid coordinates (`coordinates` is not an array of shape (n, 2) and data type int32)
    """
    conditions = [
        coordinates.ndim != 2,
        coordinates.shape[1] != 2,
        coordinates.dtype != np.int32,
    ]

    if any(conditions):
        message = (
            'Invalid coordinates! '
            'coordinates must be an array of shape (n, 2) and data type int32.'
        )
        raise AviaryUserError(message)
