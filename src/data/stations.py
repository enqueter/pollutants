"""Module stations.py"""
import logging

import pandas as pd

import src.functions.objects

class Stations:
    """
    Class Stations
    Reads-in the Scottish Air Quality Agency's inventory of telemetric devices
    """

    def __init__(self):
        """
        Constructor
        """

        self.__url = 'https://www.scottishairquality.scot/sos-scotland/api/v1/stations'

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __structure(blob: dict) -> pd.DataFrame:

        try:
            return pd.json_normalize(data=blob, max_level=2)
        except ImportError as err:
            raise Exception(err) from err

    def exc(self):
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        dictionary: dict = objects.api(url=self.__url)
        self.__logger.info(dictionary)

        data: pd.DataFrame = self.__structure(blob=dictionary)
        self.__logger.info(data)

        coordinates = pd.DataFrame(data=data['geometry.coordinates'].to_list(), columns=['longitude', 'latitude', 'height'])
        data = data.copy().drop(columns='geometry.coordinates').join(coordinates, how='left')
        self.__logger.info(data)