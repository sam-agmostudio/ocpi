from py_ocpi.modules.versions.enums import VersionNumber


class Adapter:
    @classmethod
    def location_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Location schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Location: The object data in proper OCPI schema
        """

    @classmethod
    def session_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Session schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Session: The object data in proper OCPI schema
        """

    @classmethod
    def charging_preference_adapter(cls, data: dict,
                                    version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI ChargingPreference schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            ChargingPreference: The object data in proper OCPI schema
        """

    @classmethod
    def credentials_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Credential schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Credential: The object data in proper OCPI schema
        """

    @classmethod
    def cdr_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI CDR schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            CDR: The object data in proper OCPI schema
        """

    @classmethod
    def commands_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Command schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Command: The object data in proper OCPI schema
        """

    @classmethod
    def token_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Token schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Token: The object data in proper OCPI schema
        """
