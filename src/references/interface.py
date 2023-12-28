"""Module interface.py"""
import logging

import pandas as pd

import src.elements.parameters
import src.elements.service
import src.references.registry
import src.references.stations
import src.references.substances
import src.s3.unload
import src.s3.upload


class Interface:
    """
    Class Interface

    Rebuild, or retrieve the Amazon S3 data?  The Amazon S3 aspect is upcoming.
    """

    def __init__(self, service: src.elements.service.Service, restart: bool = False):
        """

        :param service:
        :param restart:
        """

        self.__restart = restart
        self.__service = service

        # Amazon S3 Settings & Interactions Instances
        self.__parameters: src.elements.parameters.Parameters = self.__service.parameters
        self.__unload = src.s3.unload.Unload(service=self.__service)
        self.__upload = src.s3.upload.Upload(service=self.__service)

    def __stations(self) -> pd.DataFrame:
        """

        :return:
        """

        key_name = f'{self.__parameters.references_}stations.csv'

        if self.__restart:
            data: pd.DataFrame
            metadata: dict
            data, metadata = src.references.stations.Stations().exc()
            self.__upload.bytes(data=data, metadata=metadata, key_name=key_name)
        else:
            chunk = self.__unload.exc(key_name=key_name)
            data = pd.read_csv(chunk)

        return data

    def __substances(self) -> pd.DataFrame:

        key_name = f'{self.__parameters.references_}substances.csv'

        if self.__restart:
            data: pd.DataFrame
            metadata: dict
            data, metadata = src.references.substances.Substances().exc()
            self.__upload.bytes(data=data, metadata=metadata, key_name=key_name)
        else:
            chunk = self.__unload.exc(key_name=key_name)
            data = pd.read_csv(chunk)

        return data

    def __registry(self) -> pd.DataFrame:

        key_name = f'{self.__parameters.references_}registry.csv'

        if self.__restart:
            data: pd.DataFrame
            metadata: dict
            data, metadata = src.references.registry.Registry().exc()
            self.__upload.bytes(data=data, metadata=metadata, key_name=key_name)
        else:
            chunk = self.__unload.exc(key_name=key_name)
            data = pd.read_csv(chunk)

        return data

    def exc(self) -> None:
        """

        :return:
        """

        registry = self.__registry()
        stations = self.__stations()
        substances = self.__substances().copy()[['pollutant_id', 'substance', 'notation']]

        frame = registry.merge(stations, how='left', on='station_id')
        frame = frame.copy().merge(substances, how='left', on='pollutant_id')

        logging.log(level=logging.INFO, msg=frame)
