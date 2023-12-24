"""
This is the data type Sequence
"""
import typing


class Sequence(typing.NamedTuple):
    """
    The Sequence class
    """

    sequence_id: int
    unit_of_measure: str
    station_id: int
    pollutant_id: int