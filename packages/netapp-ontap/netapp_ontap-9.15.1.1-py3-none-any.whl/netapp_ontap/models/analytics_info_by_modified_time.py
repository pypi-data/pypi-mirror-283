r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsInfoByModifiedTime", "AnalyticsInfoByModifiedTimeSchema"]
__pdoc__ = {
    "AnalyticsInfoByModifiedTimeSchema.resource": False,
    "AnalyticsInfoByModifiedTimeSchema.opts": False,
    "AnalyticsInfoByModifiedTime": False,
}


class AnalyticsInfoByModifiedTimeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsInfoByModifiedTime object"""

    bytes_used = marshmallow_fields.Nested("netapp_ontap.models.analytics_histogram_by_time.AnalyticsHistogramByTimeSchema", unknown=EXCLUDE, data_key="bytes_used", allow_none=True)
    r""" The bytes_used field of the analytics_info_by_modified_time. """

    @property
    def resource(self):
        return AnalyticsInfoByModifiedTime

    gettable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""

    patchable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""

    postable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""


class AnalyticsInfoByModifiedTime(Resource):

    _schema = AnalyticsInfoByModifiedTimeSchema
