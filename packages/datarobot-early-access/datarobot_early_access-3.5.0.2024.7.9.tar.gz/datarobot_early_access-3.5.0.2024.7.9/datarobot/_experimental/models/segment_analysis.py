#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from typing import cast, List, Optional

from datarobot import Deployment
from datarobot.enums import DEPLOYMENT_MONITORING_TYPE


class SegmentAnalysis(Deployment):
    """A class representing a segment analysis of a deployment.

    .. versionadded:: v3.5

    Parameters
    ----------
    Deployment: datarobot.Deployment
        The deployment object.

    """

    def get_segment_attributes(
        self, monitoringType: Optional[str] = DEPLOYMENT_MONITORING_TYPE.SERVICE_HEALTH
    ) -> List[str]:
        """Get a list of segment attributes for this deployment.

        .. versionadded:: v3.5

        Parameters
        ----------
        monitoringType: str, Optional

        Returns
        -------
        list(str)

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            segment_attributes = deployment.get_segment_attributes(DEPLOYMENT_MONITORING_TYPE.SERVICE_HEALTH)
        """
        path = f"{self._path}{self.id}/segmentAttributes/"
        params = {"monitoringType": monitoringType}
        return cast(List[str], self._client.get(path, params=params).json()["data"])

    def get_segment_values(
        self,
        segmentAttribute: Optional[str] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
        search: Optional[str] = None,
    ) -> List[str]:
        """Get a list of segment values for this deployment.

        .. versionadded:: v3.5

        Parameters
        ----------
        segmentAttribute: str, Optional
            Represents the different ways that prediction requests can be viewed.
        limit: int, Optional
            The maximum number of values to return.
        offset: int, Optional
            The starting point of the values to be returned.
        search: str, Optional
            A string to filter the values.

        Returns
        -------
        list(str)

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            segment_values = deployment.get_segment_values(segmentAttribute='DataRobot-Consumer')
        """
        path = f"{self._path}{self.id}/segmentValues/"
        params = {
            "segmentAttribute": segmentAttribute,
            "limit": limit,
            "offset": offset,
            "search": search,
        }
        return cast(List[str], self._client.get(path, params=params).json()["data"])
