r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunLunMaps", "LunLunMapsSchema"]
__pdoc__ = {
    "LunLunMapsSchema.resource": False,
    "LunLunMapsSchema.opts": False,
    "LunLunMaps": False,
}


class LunLunMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunLunMaps object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_lun_maps. """

    igroup = marshmallow_fields.Nested("netapp_ontap.models.lun_lun_maps_igroup.LunLunMapsIgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The igroup field of the lun_lun_maps. """

    logical_unit_number = Size(data_key="logical_unit_number", allow_none=True)
    r""" The logical unit number assigned to the LUN for initiators in the initiator group. """

    @property
    def resource(self):
        return LunLunMaps

    gettable_fields = [
        "links",
        "igroup",
        "logical_unit_number",
    ]
    """links,igroup,logical_unit_number,"""

    patchable_fields = [
        "igroup",
    ]
    """igroup,"""

    postable_fields = [
        "igroup",
    ]
    """igroup,"""


class LunLunMaps(Resource):

    _schema = LunLunMapsSchema
