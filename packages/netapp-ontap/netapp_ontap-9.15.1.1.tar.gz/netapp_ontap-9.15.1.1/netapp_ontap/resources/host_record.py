r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Displays the IP address of the specified hostname and vice-versa.
## Retrieving the host table entries
The host-record GET endpoint to retrieve the hostname for a given Ip address and vice-versa.
## Examples
### Retrieving the hostname for a given IP address.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import HostRecord

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = HostRecord(
        host="127.0.0.1", **{"svm.uuid": "77e23bd4-a8fe-11eb-99e0-0050568e14ff"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
HostRecord(
    {
        "source": "Files",
        "hostname": "localhost",
        "ipv4_addresses": ["127.0.0.1"],
        "svm": {"name": "svm1", "uuid": "77e23bd4-a8fe-11eb-99e0-0050568e14ff"},
        "host": "127.0.0.1",
    }
)

```
</div>
</div>

---
### Retrieving the Ip address for a given hostname.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import HostRecord

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = HostRecord(
        host="localhost", **{"svm.uuid": "77e23bd4-a8fe-11eb-99e0-0050568e14ff"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
HostRecord(
    {
        "ipv6_addresses": ["::1"],
        "source": "Files",
        "hostname": "localhost",
        "ipv4_addresses": ["127.0.0.1"],
        "svm": {"name": "svm1", "uuid": "77e23bd4-a8fe-11eb-99e0-0050568e14ff"},
        "canonical_name": "localhost",
        "host": "localhost",
    }
)

```
</div>
</div>

---"""

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


__all__ = ["HostRecord", "HostRecordSchema"]
__pdoc__ = {
    "HostRecordSchema.resource": False,
    "HostRecordSchema.opts": False,
    "HostRecord.host_record_show": False,
    "HostRecord.host_record_create": False,
    "HostRecord.host_record_modify": False,
    "HostRecord.host_record_delete": False,
}


class HostRecordSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the HostRecord object"""

    canonical_name = marshmallow_fields.Str(
        data_key="canonical_name",
        allow_none=True,
    )
    r""" Canonical name of the host.


Example: localhost"""

    host = marshmallow_fields.Str(
        data_key="host",
        allow_none=True,
    )
    r""" IP address or hostname.


Example: localhost"""

    hostname = marshmallow_fields.Str(
        data_key="hostname",
        allow_none=True,
    )
    r""" Hostname.


Example: localhost"""

    ipv4_addresses = marshmallow_fields.List(marshmallow_fields.Str, data_key="ipv4_addresses", allow_none=True)
    r""" List of IPv4 addresses.


Example: ["127.0.0.1"]"""

    ipv6_addresses = marshmallow_fields.List(marshmallow_fields.Str, data_key="ipv6_addresses", allow_none=True)
    r""" List of IPv6 addresses.


Example: ["::1"]"""

    source = marshmallow_fields.Str(
        data_key="source",
        allow_none=True,
    )
    r""" Source used for lookup.


Example: Files"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the host_record."""

    @property
    def resource(self):
        return HostRecord

    gettable_fields = [
        "canonical_name",
        "host",
        "hostname",
        "ipv4_addresses",
        "ipv6_addresses",
        "source",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """canonical_name,host,hostname,ipv4_addresses,ipv6_addresses,source,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "host",
        "source",
        "svm.name",
        "svm.uuid",
    ]
    """host,source,svm.name,svm.uuid,"""

    postable_fields = [
        "host",
        "source",
        "svm.name",
        "svm.uuid",
    ]
    """host,source,svm.name,svm.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in HostRecord.get_collection(fields=field)]
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
            raise NetAppRestError("HostRecord modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class HostRecord(Resource):
    """Allows interaction with HostRecord objects on the host"""

    _schema = HostRecordSchema
    _path = "/api/name-services/host-record"
    _keys = ["svm.uuid", "host"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the IP address of the specified hostname and vice-versa.
### Related ONTAP commands
* `vserver services name-service getxxbyyy getnameinfo`
* `vserver services name-service getxxbyyy getaddrinfo`

### Learn more
* [`DOC /name-services/host-record/{svm.uuid}/{host}`](#docs-name-services-name-services_host-record_{svm.uuid}_{host})"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="host record show")
        def host_record_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single HostRecord resource

            Args:
                canonical_name: Canonical name of the host. 
                host: IP address or hostname. 
                hostname: Hostname. 
                ipv4_addresses: List of IPv4 addresses. 
                ipv6_addresses: List of IPv6 addresses. 
                source: Source used for lookup. 
            """

            kwargs = {}
            if canonical_name is not None:
                kwargs["canonical_name"] = canonical_name
            if host is not None:
                kwargs["host"] = host
            if hostname is not None:
                kwargs["hostname"] = hostname
            if ipv4_addresses is not None:
                kwargs["ipv4_addresses"] = ipv4_addresses
            if ipv6_addresses is not None:
                kwargs["ipv6_addresses"] = ipv6_addresses
            if source is not None:
                kwargs["source"] = source
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = HostRecord(
                **kwargs
            )
            resource.get()
            return [resource]





