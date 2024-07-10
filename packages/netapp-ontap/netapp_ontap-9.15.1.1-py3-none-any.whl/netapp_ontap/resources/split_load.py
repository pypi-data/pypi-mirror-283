r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    RECLINE_INSTALLED = False
    import recline
    from recline.arg_types.choices import Choices
    from recline.commands import ReclineCommandError
    from netapp_ontap.resource_table import ResourceTable
    RECLINE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SplitLoad", "SplitLoadSchema"]
__pdoc__ = {
    "SplitLoadSchema.resource": False,
    "SplitLoadSchema.opts": False,
    "SplitLoad.split_load_show": False,
    "SplitLoad.split_load_create": False,
    "SplitLoad.split_load_modify": False,
    "SplitLoad.split_load_delete": False,
}


class SplitLoadSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SplitLoad object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the split_load."""

    load = marshmallow_fields.Nested("netapp_ontap.models.split_load_load.SplitLoadLoadSchema", data_key="load", unknown=EXCLUDE, allow_none=True)
    r""" The load field of the split_load."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the split_load."""

    @property
    def resource(self):
        return SplitLoad

    gettable_fields = [
        "links",
        "load",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """links,load,node.links,node.name,node.uuid,"""

    patchable_fields = [
        "load",
    ]
    """load,"""

    postable_fields = [
        "load",
    ]
    """load,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SplitLoad.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("SplitLoad modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SplitLoad(Resource):
    """Allows interaction with SplitLoad objects on the host"""

    _schema = SplitLoadSchema
    _path = "/api/storage/file/clone/split-loads"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the clone split load of a node.
### Related Ontap Commands
* `volume file clone split load show`
### Retrieving file clone split load related information
The GET operation can be used to retrieve information about clone split load data. Split load data is the data currently undergoing the split. There is a limit on split load data. This API communicates how much data is undergoing split and how much can still be processed.
```
# The API:
/api/storage/file/clone/split-loads
# The call:
curl -X GET "https://<mgmt_ip>/api/storage/file/clone/split-loads" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "node": {
        "uuid": "158d592f-a829-11eb-a47b-005056bb46d7",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/158d592f-a829-11eb-a47b-005056bb46d7"
          }
        }
      },
      "load": {
        "maximum": 35184372088832,
        "current": 0,
        "token_reserved": 0,
        "allowable": 35184372088832
      },
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-loads/158d592f-a829-11eb-a47b-005056bb46d7"
        }
      }
    },
    {
      "node": {
        "uuid": "9686b8d1-a828-11eb-80d8-005056bbe7b6",
        "name": "node2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/9686b8d1-a828-11eb-80d8-005056bbe7b6"
          }
        }
      },
      "load": {
        "maximum": 35184372088832,
        "current": 0,
        "token_reserved": 0,
        "allowable": 35184372088832
      },
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-loads/9686b8d1-a828-11eb-80d8-005056bbe7b6"
        }
      }
    }
  ],
  "num_records": 2,
  "_links":
    "self": {
      "href": "/api/storage/file/clone/split-loads"
    }
  }
}
```
### Learn More
* [`DOC /storage/file/clone`]
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="split load show")
        def split_load_show(
            fields: List[Choices.define(["*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SplitLoad resources

            Args:
            """

            kwargs = {}
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SplitLoad.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SplitLoad resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent SplitLoad resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SplitLoad"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the maximum split load.
### Related Ontap command
* `volume file clone split load modify`
### Learn More
* [`DOC /storage/file/clone`]
```
# The call:
curl -X PATCH "https://<mgmt_IP>/api/storage/file/clone/split-loads/9686b8d1-a828-11eb-80d8-005056bbe7b6" -d '{"load": {"maximum": "16TB" } }'
# The response to successful patch is empty body
```
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the clone split load of a node.
### Related Ontap Commands
* `volume file clone split load show`
### Retrieving file clone split load related information
The GET operation can be used to retrieve information about clone split load data. Split load data is the data currently undergoing the split. There is a limit on split load data. This API communicates how much data is undergoing split and how much can still be processed.
```
# The API:
/api/storage/file/clone/split-loads
# The call:
curl -X GET "https://<mgmt_ip>/api/storage/file/clone/split-loads" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "node": {
        "uuid": "158d592f-a829-11eb-a47b-005056bb46d7",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/158d592f-a829-11eb-a47b-005056bb46d7"
          }
        }
      },
      "load": {
        "maximum": 35184372088832,
        "current": 0,
        "token_reserved": 0,
        "allowable": 35184372088832
      },
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-loads/158d592f-a829-11eb-a47b-005056bb46d7"
        }
      }
    },
    {
      "node": {
        "uuid": "9686b8d1-a828-11eb-80d8-005056bbe7b6",
        "name": "node2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/9686b8d1-a828-11eb-80d8-005056bbe7b6"
          }
        }
      },
      "load": {
        "maximum": 35184372088832,
        "current": 0,
        "token_reserved": 0,
        "allowable": 35184372088832
      },
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-loads/9686b8d1-a828-11eb-80d8-005056bbe7b6"
        }
      }
    }
  ],
  "num_records": 2,
  "_links":
    "self": {
      "href": "/api/storage/file/clone/split-loads"
    }
  }
}
```
### Learn More
* [`DOC /storage/file/clone`]
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieve the volume file clone split load.
### Related ONTAP command
* `volume file clone split load show`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the maximum split load.
### Related Ontap command
* `volume file clone split load modify`
### Learn More
* [`DOC /storage/file/clone`]
```
# The call:
curl -X PATCH "https://<mgmt_IP>/api/storage/file/clone/split-loads/9686b8d1-a828-11eb-80d8-005056bbe7b6" -d '{"load": {"maximum": "16TB" } }'
# The response to successful patch is empty body
```
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="split load modify")
        async def split_load_modify(
        ) -> ResourceTable:
            """Modify an instance of a SplitLoad resource

            Args:
            """

            kwargs = {}
            changes = {}


            if hasattr(SplitLoad, "find"):
                resource = SplitLoad.find(
                    **kwargs
                )
            else:
                resource = SplitLoad()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify SplitLoad: %s" % err)



