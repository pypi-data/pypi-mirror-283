r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to manage transfers on an existing SnapMirror relationship.</br>
You can initiate SnapMirror operations such as "initialize", "update", "restore-transfer", and "abort" using this API on asynchronous SnapMirror relationship. On a synchronous SnapMirror relationship, you can initiate SnapMirror "initialize" operation. The GET for this API reports the status of both active transfers and transfers that have terminated within the past 24 hours.<br>For the restore relationships, the POST on transfers API triggers "restore-transfer". Successful completion of "restore" also deletes the restore relationship. If the "restore" fails, DELETE on relationships must be called to delete the restore relationship.<br/>
A transfer on an asynchronous SnapMirror relationship with Application Consistency Group endpoints expands the destination Application Consistency Group endpoint if the source Application Consistency Group endpoint is already expanded.<br/>"""

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


__all__ = ["SnapmirrorTransfer", "SnapmirrorTransferSchema"]
__pdoc__ = {
    "SnapmirrorTransferSchema.resource": False,
    "SnapmirrorTransferSchema.opts": False,
    "SnapmirrorTransfer.snapmirror_transfer_show": False,
    "SnapmirrorTransfer.snapmirror_transfer_create": False,
    "SnapmirrorTransfer.snapmirror_transfer_modify": False,
    "SnapmirrorTransfer.snapmirror_transfer_delete": False,
}


class SnapmirrorTransferSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorTransfer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapmirror_transfer."""

    bytes_transferred = Size(
        data_key="bytes_transferred",
        allow_none=True,
    )
    r""" Bytes transferred"""

    checkpoint_size = Size(
        data_key="checkpoint_size",
        allow_none=True,
    )
    r""" Amount of data transferred in bytes as recorded in the restart checkpoint."""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" End time of the transfer.

Example: 2020-12-03T02:36:19.000+0000"""

    error_info = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_error_info.SnapmirrorTransferErrorInfoSchema", data_key="error_info", unknown=EXCLUDE, allow_none=True)
    r""" The error_info field of the snapmirror_transfer."""

    files = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_files.SnapmirrorTransferFilesSchema", unknown=EXCLUDE, allow_none=True), data_key="files", allow_none=True)
    r""" This is supported for transfer of restore relationship only. This specifies the list of files or LUNs to be restored. Can contain up to eight files or LUNs."""

    last_updated_time = ImpreciseDateTime(
        data_key="last_updated_time",
        allow_none=True,
    )
    r""" Last updated time of the bytes transferred in an active transfer.

Example: 2023-09-15T23:58:39.000+0000"""

    network_compression_ratio = marshmallow_fields.Str(
        data_key="network_compression_ratio",
        allow_none=True,
    )
    r""" Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.

Example: 61"""

    on_demand_attrs = marshmallow_fields.Str(
        data_key="on_demand_attrs",
        validate=enum_validation(['off', 'read_write_with_user_data_pull']),
        allow_none=True,
    )
    r""" Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.

Valid choices:

* off
* read_write_with_user_data_pull"""

    options = marshmallow_fields.List(marshmallow_fields.Dict, data_key="options", allow_none=True)
    r""" Options for snapmirror transfer."""

    relationship = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_relationship.SnapmirrorTransferRelationshipSchema", data_key="relationship", unknown=EXCLUDE, allow_none=True)
    r""" The relationship field of the snapmirror_transfer."""

    snapshot = marshmallow_fields.Str(
        data_key="snapshot",
        allow_none=True,
    )
    r""" Name of Snapshot copy being transferred."""

    source_snapshot = marshmallow_fields.Str(
        data_key="source_snapshot",
        allow_none=True,
    )
    r""" Specifies the Snapshot copy on the source to be transferred to the destination."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['aborted', 'failed', 'hard_aborted', 'queued', 'success', 'transferring']),
        allow_none=True,
    )
    r""" Status of the transfer. Set PATCH state to "aborted" to abort the transfer. Set PATCH state to "hard_aborted" to abort the transfer and discard the restart checkpoint. To find "queued" transfers refer to relationships GET API.

Valid choices:

* aborted
* failed
* hard_aborted
* queued
* success
* transferring"""

    storage_efficiency_enabled = marshmallow_fields.Boolean(
        data_key="storage_efficiency_enabled",
        allow_none=True,
    )
    r""" This is supported for transfer of restore relationship only. Set this property to "false" to turn off storage efficiency for data transferred over the wire and written to the destination."""

    throttle = Size(
        data_key="throttle",
        allow_none=True,
    )
    r""" Throttle, in KBs per second. This "throttle" overrides the "throttle" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited."""

    total_duration = marshmallow_fields.Str(
        data_key="total_duration",
        allow_none=True,
    )
    r""" Elapsed transfer time.

Example: PT28M41S"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the SnapMirror transfer.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SnapmirrorTransfer

    gettable_fields = [
        "links",
        "bytes_transferred",
        "checkpoint_size",
        "end_time",
        "error_info",
        "last_updated_time",
        "network_compression_ratio",
        "on_demand_attrs",
        "relationship",
        "snapshot",
        "state",
        "throttle",
        "total_duration",
        "uuid",
    ]
    """links,bytes_transferred,checkpoint_size,end_time,error_info,last_updated_time,network_compression_ratio,on_demand_attrs,relationship,snapshot,state,throttle,total_duration,uuid,"""

    patchable_fields = [
        "on_demand_attrs",
        "state",
    ]
    """on_demand_attrs,state,"""

    postable_fields = [
        "files",
        "on_demand_attrs",
        "options",
        "source_snapshot",
        "storage_efficiency_enabled",
        "throttle",
    ]
    """files,on_demand_attrs,options,source_snapshot,storage_efficiency_enabled,throttle,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SnapmirrorTransfer.get_collection(fields=field)]
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
            raise NetAppRestError("SnapmirrorTransfer modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SnapmirrorTransfer(Resource):
    r""" SnapMirror transfer information """

    _schema = SnapmirrorTransferSchema
    _path = "/api/snapmirror/relationships/{relationship[uuid]}/transfers"
    _keys = ["relationship.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of ongoing SnapMirror transfers for the specified relationship.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers"
```
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
<br/>
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="snapmirror transfer show")
        def snapmirror_transfer_show(
            relationship_uuid,
            bytes_transferred: Choices.define(_get_field_list("bytes_transferred"), cache_choices=True, inexact=True)=None,
            checkpoint_size: Choices.define(_get_field_list("checkpoint_size"), cache_choices=True, inexact=True)=None,
            end_time: Choices.define(_get_field_list("end_time"), cache_choices=True, inexact=True)=None,
            last_updated_time: Choices.define(_get_field_list("last_updated_time"), cache_choices=True, inexact=True)=None,
            network_compression_ratio: Choices.define(_get_field_list("network_compression_ratio"), cache_choices=True, inexact=True)=None,
            on_demand_attrs: Choices.define(_get_field_list("on_demand_attrs"), cache_choices=True, inexact=True)=None,
            options: Choices.define(_get_field_list("options"), cache_choices=True, inexact=True)=None,
            snapshot: Choices.define(_get_field_list("snapshot"), cache_choices=True, inexact=True)=None,
            source_snapshot: Choices.define(_get_field_list("source_snapshot"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            storage_efficiency_enabled: Choices.define(_get_field_list("storage_efficiency_enabled"), cache_choices=True, inexact=True)=None,
            throttle: Choices.define(_get_field_list("throttle"), cache_choices=True, inexact=True)=None,
            total_duration: Choices.define(_get_field_list("total_duration"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["bytes_transferred", "checkpoint_size", "end_time", "last_updated_time", "network_compression_ratio", "on_demand_attrs", "options", "snapshot", "source_snapshot", "state", "storage_efficiency_enabled", "throttle", "total_duration", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SnapmirrorTransfer resources

            Args:
                bytes_transferred: Bytes transferred
                checkpoint_size: Amount of data transferred in bytes as recorded in the restart checkpoint.
                end_time: End time of the transfer.
                last_updated_time: Last updated time of the bytes transferred in an active transfer.
                network_compression_ratio: Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.
                on_demand_attrs: Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.
                options: Options for snapmirror transfer.
                snapshot: Name of Snapshot copy being transferred.
                source_snapshot: Specifies the Snapshot copy on the source to be transferred to the destination.
                state: Status of the transfer. Set PATCH state to \"aborted\" to abort the transfer. Set PATCH state to \"hard_aborted\" to abort the transfer and discard the restart checkpoint. To find \"queued\" transfers refer to relationships GET API.
                storage_efficiency_enabled: This is supported for transfer of restore relationship only. Set this property to \"false\" to turn off storage efficiency for data transferred over the wire and written to the destination.
                throttle: Throttle, in KBs per second. This \"throttle\" overrides the \"throttle\" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited.
                total_duration: Elapsed transfer time.
                uuid: Unique identifier of the SnapMirror transfer.
            """

            kwargs = {}
            if bytes_transferred is not None:
                kwargs["bytes_transferred"] = bytes_transferred
            if checkpoint_size is not None:
                kwargs["checkpoint_size"] = checkpoint_size
            if end_time is not None:
                kwargs["end_time"] = end_time
            if last_updated_time is not None:
                kwargs["last_updated_time"] = last_updated_time
            if network_compression_ratio is not None:
                kwargs["network_compression_ratio"] = network_compression_ratio
            if on_demand_attrs is not None:
                kwargs["on_demand_attrs"] = on_demand_attrs
            if options is not None:
                kwargs["options"] = options
            if snapshot is not None:
                kwargs["snapshot"] = snapshot
            if source_snapshot is not None:
                kwargs["source_snapshot"] = source_snapshot
            if state is not None:
                kwargs["state"] = state
            if storage_efficiency_enabled is not None:
                kwargs["storage_efficiency_enabled"] = storage_efficiency_enabled
            if throttle is not None:
                kwargs["throttle"] = throttle
            if total_duration is not None:
                kwargs["total_duration"] = total_duration
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SnapmirrorTransfer.get_collection(
                relationship_uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SnapmirrorTransfer resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnapmirrorTransfer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnapmirrorTransfer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts an ongoing SnapMirror transfer. This operation is applicable on asynchronous SnapMirror relationships.
### Related ONTAP commands
* `snapmirror abort`
### Example
<br/>
```
PATCH "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd" '{"state":"aborted"}'
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnapmirrorTransfer"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnapmirrorTransfer"], NetAppResponse]:
        r"""Starts a SnapMirror transfer operation. This API initiates a restore operation if the SnapMirror relationship is of type "restore". Otherwise, it intiates a SnapMirror "initialize" operation or "update" operation based on the current SnapMirror state.
### Default property values
* `storage_efficiency_enabled` - _true_
### Related ONTAP commands
* `snapmirror update`
* `snapmirror initialize`
* `snapmirror restore`

### Examples
The following examples show how to perform SnapMirror "initialize", "update", and "restore" operations.
<br/>
   Perform SnapMirror initialize or update
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{}'
   ```
   <br/>
   Perform SnapMirror initialize, update or restore with throttle value set
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"throttle":"100"}'
   ```
   <br/>
   Perform SnapMirror restore transfer of a file
   <br/>
   ```
   POST "/api/snapmirror/relationships/c8c62a90-0fef-11e9-b09e-0050568e7067/transfers" '{"source_snapshot": "src", "files":[{"source_path": "/a1.txt.0", "destination_path": "/a1-renamed.txt.0"}]}'
   ```
   <br/>
   Performing a SnapMirror initialize or update using a particular Snapshot copy.
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"source_snapshot":"snap1"}'
   ```
   <br/>
   
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of ongoing SnapMirror transfers for the specified relationship.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers"
```
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
<br/>
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the attributes of a specific ongoing SnapMirror transfer.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd"
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Starts a SnapMirror transfer operation. This API initiates a restore operation if the SnapMirror relationship is of type "restore". Otherwise, it intiates a SnapMirror "initialize" operation or "update" operation based on the current SnapMirror state.
### Default property values
* `storage_efficiency_enabled` - _true_
### Related ONTAP commands
* `snapmirror update`
* `snapmirror initialize`
* `snapmirror restore`

### Examples
The following examples show how to perform SnapMirror "initialize", "update", and "restore" operations.
<br/>
   Perform SnapMirror initialize or update
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{}'
   ```
   <br/>
   Perform SnapMirror initialize, update or restore with throttle value set
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"throttle":"100"}'
   ```
   <br/>
   Perform SnapMirror restore transfer of a file
   <br/>
   ```
   POST "/api/snapmirror/relationships/c8c62a90-0fef-11e9-b09e-0050568e7067/transfers" '{"source_snapshot": "src", "files":[{"source_path": "/a1.txt.0", "destination_path": "/a1-renamed.txt.0"}]}'
   ```
   <br/>
   Performing a SnapMirror initialize or update using a particular Snapshot copy.
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"source_snapshot":"snap1"}'
   ```
   <br/>
   
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="snapmirror transfer create")
        async def snapmirror_transfer_create(
            relationship_uuid,
            links: dict = None,
            bytes_transferred: Size = None,
            checkpoint_size: Size = None,
            end_time: datetime = None,
            error_info: dict = None,
            files: dict = None,
            last_updated_time: datetime = None,
            network_compression_ratio: str = None,
            on_demand_attrs: str = None,
            options: dict = None,
            relationship: dict = None,
            snapshot: str = None,
            source_snapshot: str = None,
            state: str = None,
            storage_efficiency_enabled: bool = None,
            throttle: Size = None,
            total_duration: str = None,
            uuid: str = None,
        ) -> ResourceTable:
            """Create an instance of a SnapmirrorTransfer resource

            Args:
                links: 
                bytes_transferred: Bytes transferred
                checkpoint_size: Amount of data transferred in bytes as recorded in the restart checkpoint.
                end_time: End time of the transfer.
                error_info: 
                files: This is supported for transfer of restore relationship only. This specifies the list of files or LUNs to be restored. Can contain up to eight files or LUNs.
                last_updated_time: Last updated time of the bytes transferred in an active transfer.
                network_compression_ratio: Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.
                on_demand_attrs: Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.
                options: Options for snapmirror transfer.
                relationship: 
                snapshot: Name of Snapshot copy being transferred.
                source_snapshot: Specifies the Snapshot copy on the source to be transferred to the destination.
                state: Status of the transfer. Set PATCH state to \"aborted\" to abort the transfer. Set PATCH state to \"hard_aborted\" to abort the transfer and discard the restart checkpoint. To find \"queued\" transfers refer to relationships GET API.
                storage_efficiency_enabled: This is supported for transfer of restore relationship only. Set this property to \"false\" to turn off storage efficiency for data transferred over the wire and written to the destination.
                throttle: Throttle, in KBs per second. This \"throttle\" overrides the \"throttle\" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited.
                total_duration: Elapsed transfer time.
                uuid: Unique identifier of the SnapMirror transfer.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if bytes_transferred is not None:
                kwargs["bytes_transferred"] = bytes_transferred
            if checkpoint_size is not None:
                kwargs["checkpoint_size"] = checkpoint_size
            if end_time is not None:
                kwargs["end_time"] = end_time
            if error_info is not None:
                kwargs["error_info"] = error_info
            if files is not None:
                kwargs["files"] = files
            if last_updated_time is not None:
                kwargs["last_updated_time"] = last_updated_time
            if network_compression_ratio is not None:
                kwargs["network_compression_ratio"] = network_compression_ratio
            if on_demand_attrs is not None:
                kwargs["on_demand_attrs"] = on_demand_attrs
            if options is not None:
                kwargs["options"] = options
            if relationship is not None:
                kwargs["relationship"] = relationship
            if snapshot is not None:
                kwargs["snapshot"] = snapshot
            if source_snapshot is not None:
                kwargs["source_snapshot"] = source_snapshot
            if state is not None:
                kwargs["state"] = state
            if storage_efficiency_enabled is not None:
                kwargs["storage_efficiency_enabled"] = storage_efficiency_enabled
            if throttle is not None:
                kwargs["throttle"] = throttle
            if total_duration is not None:
                kwargs["total_duration"] = total_duration
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = SnapmirrorTransfer(
                relationship_uuid,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create SnapmirrorTransfer: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts an ongoing SnapMirror transfer. This operation is applicable on asynchronous SnapMirror relationships.
### Related ONTAP commands
* `snapmirror abort`
### Example
<br/>
```
PATCH "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd" '{"state":"aborted"}'
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="snapmirror transfer modify")
        async def snapmirror_transfer_modify(
            relationship_uuid,
            bytes_transferred: Size = None,
            query_bytes_transferred: Size = None,
            checkpoint_size: Size = None,
            query_checkpoint_size: Size = None,
            end_time: datetime = None,
            query_end_time: datetime = None,
            last_updated_time: datetime = None,
            query_last_updated_time: datetime = None,
            network_compression_ratio: str = None,
            query_network_compression_ratio: str = None,
            on_demand_attrs: str = None,
            query_on_demand_attrs: str = None,
            options: dict = None,
            query_options: dict = None,
            snapshot: str = None,
            query_snapshot: str = None,
            source_snapshot: str = None,
            query_source_snapshot: str = None,
            state: str = None,
            query_state: str = None,
            storage_efficiency_enabled: bool = None,
            query_storage_efficiency_enabled: bool = None,
            throttle: Size = None,
            query_throttle: Size = None,
            total_duration: str = None,
            query_total_duration: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a SnapmirrorTransfer resource

            Args:
                bytes_transferred: Bytes transferred
                query_bytes_transferred: Bytes transferred
                checkpoint_size: Amount of data transferred in bytes as recorded in the restart checkpoint.
                query_checkpoint_size: Amount of data transferred in bytes as recorded in the restart checkpoint.
                end_time: End time of the transfer.
                query_end_time: End time of the transfer.
                last_updated_time: Last updated time of the bytes transferred in an active transfer.
                query_last_updated_time: Last updated time of the bytes transferred in an active transfer.
                network_compression_ratio: Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.
                query_network_compression_ratio: Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.
                on_demand_attrs: Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.
                query_on_demand_attrs: Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.
                options: Options for snapmirror transfer.
                query_options: Options for snapmirror transfer.
                snapshot: Name of Snapshot copy being transferred.
                query_snapshot: Name of Snapshot copy being transferred.
                source_snapshot: Specifies the Snapshot copy on the source to be transferred to the destination.
                query_source_snapshot: Specifies the Snapshot copy on the source to be transferred to the destination.
                state: Status of the transfer. Set PATCH state to \"aborted\" to abort the transfer. Set PATCH state to \"hard_aborted\" to abort the transfer and discard the restart checkpoint. To find \"queued\" transfers refer to relationships GET API.
                query_state: Status of the transfer. Set PATCH state to \"aborted\" to abort the transfer. Set PATCH state to \"hard_aborted\" to abort the transfer and discard the restart checkpoint. To find \"queued\" transfers refer to relationships GET API.
                storage_efficiency_enabled: This is supported for transfer of restore relationship only. Set this property to \"false\" to turn off storage efficiency for data transferred over the wire and written to the destination.
                query_storage_efficiency_enabled: This is supported for transfer of restore relationship only. Set this property to \"false\" to turn off storage efficiency for data transferred over the wire and written to the destination.
                throttle: Throttle, in KBs per second. This \"throttle\" overrides the \"throttle\" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited.
                query_throttle: Throttle, in KBs per second. This \"throttle\" overrides the \"throttle\" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited.
                total_duration: Elapsed transfer time.
                query_total_duration: Elapsed transfer time.
                uuid: Unique identifier of the SnapMirror transfer.
                query_uuid: Unique identifier of the SnapMirror transfer.
            """

            kwargs = {}
            changes = {}
            if query_bytes_transferred is not None:
                kwargs["bytes_transferred"] = query_bytes_transferred
            if query_checkpoint_size is not None:
                kwargs["checkpoint_size"] = query_checkpoint_size
            if query_end_time is not None:
                kwargs["end_time"] = query_end_time
            if query_last_updated_time is not None:
                kwargs["last_updated_time"] = query_last_updated_time
            if query_network_compression_ratio is not None:
                kwargs["network_compression_ratio"] = query_network_compression_ratio
            if query_on_demand_attrs is not None:
                kwargs["on_demand_attrs"] = query_on_demand_attrs
            if query_options is not None:
                kwargs["options"] = query_options
            if query_snapshot is not None:
                kwargs["snapshot"] = query_snapshot
            if query_source_snapshot is not None:
                kwargs["source_snapshot"] = query_source_snapshot
            if query_state is not None:
                kwargs["state"] = query_state
            if query_storage_efficiency_enabled is not None:
                kwargs["storage_efficiency_enabled"] = query_storage_efficiency_enabled
            if query_throttle is not None:
                kwargs["throttle"] = query_throttle
            if query_total_duration is not None:
                kwargs["total_duration"] = query_total_duration
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if bytes_transferred is not None:
                changes["bytes_transferred"] = bytes_transferred
            if checkpoint_size is not None:
                changes["checkpoint_size"] = checkpoint_size
            if end_time is not None:
                changes["end_time"] = end_time
            if last_updated_time is not None:
                changes["last_updated_time"] = last_updated_time
            if network_compression_ratio is not None:
                changes["network_compression_ratio"] = network_compression_ratio
            if on_demand_attrs is not None:
                changes["on_demand_attrs"] = on_demand_attrs
            if options is not None:
                changes["options"] = options
            if snapshot is not None:
                changes["snapshot"] = snapshot
            if source_snapshot is not None:
                changes["source_snapshot"] = source_snapshot
            if state is not None:
                changes["state"] = state
            if storage_efficiency_enabled is not None:
                changes["storage_efficiency_enabled"] = storage_efficiency_enabled
            if throttle is not None:
                changes["throttle"] = throttle
            if total_duration is not None:
                changes["total_duration"] = total_duration
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(SnapmirrorTransfer, "find"):
                resource = SnapmirrorTransfer.find(
                    relationship_uuid,
                    **kwargs
                )
            else:
                resource = SnapmirrorTransfer(relationship_uuid,)
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify SnapmirrorTransfer: %s" % err)



