import json
import logging
import platform
import subprocess


class Sync:
    """
    Class Sync

    Description
    -----------

    Transfers files to Amazon S3

    DataSync incurs cost
        https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#create-s3-location-s3-requests
    """

    def __init__(self, restart: bool, profile: str):
        """

        """

        self.__restart: bool = restart
        self.__shell = False if platform.system().lower() == 'windows' else True
        self.__profile = profile

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self, source: str, destination: str, metadata: dict):
        """

        :param source: The local directory
        :param destination: The Amazon S3 destination
        :param metadata: The metadata dictionary
        :return:
        """

        if self.__restart:
            action = 'sync'
        else:
            action = 'cp'

        cheat = '"epoch_ms"="The milliseconds unix epoch time when the measure was recorded",' + \
                '"measure"="The unit of measure of the pollutant under measure",' + \
                '"timestamp"="The timestamp of the measure",' + \
                '"date"="The date the measure was recorded",' + \
                '"sequence_id"="The identification code of the sequence this record is part of."'

        self.__logger.info(f"""aws s3 {action} {source} {destination} """ +
                           f"""--metadata '{json.dumps(metadata)}' --profile {self.__profile}""")

        message = subprocess.run(f"""aws s3 {action} {source} {destination} """ +
                                 f"""--metadata {cheat} --profile {self.__profile}""",
                                 shell=self.__shell, capture_output=True)
        self.__logger.info(message)