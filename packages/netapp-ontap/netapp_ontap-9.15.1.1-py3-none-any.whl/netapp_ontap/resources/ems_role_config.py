r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Manages the EMS role-based configuration of a specific access control role.
##
See the documentation for [/support/ems/role-configs](#docs-support-support_ems_role-configs) for details on the various properties.
## Examples
### Retrieving the EMS role-based configuration of an access control role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsRoleConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsRoleConfig(**{"access_control_role.name": "storage-admin"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
EmsRoleConfig(
    {
        "event_filter": {
            "name": "storage-admin-events",
            "_links": {
                "self": {"href": "/api/support/ems/filters/storage-admin-events"}
            },
        },
        "_links": {"self": {"href": "/api/support/ems/role-configs/storage-admin"}},
        "access_control_role": {
            "name": "storage-admin",
            "_links": {
                "self": {
                    "href": "/api/security/roles/0b2580c8-de36-4213-bfca-88cdaaaf3ae6/storage-admin"
                }
            },
        },
    }
)

```
</div>
</div>

### Updating the EMS role-based configuration of an access control role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsRoleConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsRoleConfig(**{"access_control_role.name": "storage-admin"})
    resource.event_filter = {"name": "new-storage-admin-events"}
    resource.limit_access_to_global_configs = False
    resource.patch()

```

### Removing the EMS role-based configuration of an access control role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsRoleConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsRoleConfig(**{"access_control_role.name": "storage-admin"})
    resource.delete()

```
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


__all__ = ["EmsRoleConfig", "EmsRoleConfigSchema"]
__pdoc__ = {
    "EmsRoleConfigSchema.resource": False,
    "EmsRoleConfigSchema.opts": False,
    "EmsRoleConfig.ems_role_config_show": False,
    "EmsRoleConfig.ems_role_config_create": False,
    "EmsRoleConfig.ems_role_config_modify": False,
    "EmsRoleConfig.ems_role_config_delete": False,
}


class EmsRoleConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsRoleConfig object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_role_config."""

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="access_control_role", unknown=EXCLUDE, allow_none=True)
    r""" The access_control_role field of the ems_role_config."""

    event_filter = marshmallow_fields.Nested("netapp_ontap.resources.ems_filter.EmsFilterSchema", data_key="event_filter", unknown=EXCLUDE, allow_none=True)
    r""" The event_filter field of the ems_role_config."""

    limit_access_to_global_configs = marshmallow_fields.Boolean(
        data_key="limit_access_to_global_configs",
        allow_none=True,
    )
    r""" Indicates whether the access control has limited access to global EMS configurations."""

    @property
    def resource(self):
        return EmsRoleConfig

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "event_filter.links",
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """links,access_control_role.links,access_control_role.name,event_filter.links,event_filter.name,limit_access_to_global_configs,"""

    patchable_fields = [
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """event_filter.name,limit_access_to_global_configs,"""

    postable_fields = [
        "access_control_role.name",
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """access_control_role.name,event_filter.name,limit_access_to_global_configs,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in EmsRoleConfig.get_collection(fields=field)]
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
            raise NetAppRestError("EmsRoleConfig modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class EmsRoleConfig(Resource):
    """Allows interaction with EmsRoleConfig objects on the host"""

    _schema = EmsRoleConfigSchema
    _path = "/api/support/ems/role-configs"
    _keys = ["access_control_role.name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of the EMS role-based configurations.
### Related ONTAP commands
* `event role-config show`

### Learn more
* [`DOC /support/ems/role-configs`](#docs-support-support_ems_role-configs)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems role config show")
        def ems_role_config_show(
            fields: List[Choices.define(["limit_access_to_global_configs", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of EmsRoleConfig resources

            Args:
                limit_access_to_global_configs: Indicates whether the access control has limited access to global EMS configurations.
            """

            kwargs = {}
            if limit_access_to_global_configs is not None:
                kwargs["limit_access_to_global_configs"] = limit_access_to_global_configs
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return EmsRoleConfig.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsRoleConfig resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsRoleConfig resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["EmsRoleConfig"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the EMS role-based configuration of the access control role.
### Recommended optional properties
* `event_filter` - Identifies the event filter.
* `limit_access_to_global_configs` - Indicates whether the access control role has limited access to global EMS configurations.
### Related ONTAP commands
* `event role-config modify`

### Learn more
* [`DOC /support/ems/role-configs/{access_control_role.name}`](#docs-support-support_ems_role-configs_{access_control_role.name})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["EmsRoleConfig"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["EmsRoleConfig"], NetAppResponse]:
        r"""Creates an EMS role-based configuration for an access control role.
### Required properties
* `access_control_role` - Uniquely identifies the access control role.
### Recommended optional properties
* `event_filter` - Identifies the event filter.
* `limit_access_to_global_configs` - Indicates whether the access control role has limited access to global EMS configurations.
### Related ONTAP commands
* `event role-config create`

### Learn more
* [`DOC /support/ems/role-configs`](#docs-support-support_ems_role-configs)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["EmsRoleConfig"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Removes the EMS role-based configuration of the access control role.
### Related ONTAP commands
* `event role-config delete`

### Learn more
* [`DOC /support/ems/role-configs/{access_control_role.name}`](#docs-support-support_ems_role-configs_{access_control_role.name})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of the EMS role-based configurations.
### Related ONTAP commands
* `event role-config show`

### Learn more
* [`DOC /support/ems/role-configs`](#docs-support-support_ems_role-configs)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the EMS role-based configuration of the access control role.
### Related ONTAP commands
* `event role-config show`

### Learn more
* [`DOC /support/ems/role-configs/{access_control_role.name}`](#docs-support-support_ems_role-configs_{access_control_role.name})"""
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
        r"""Creates an EMS role-based configuration for an access control role.
### Required properties
* `access_control_role` - Uniquely identifies the access control role.
### Recommended optional properties
* `event_filter` - Identifies the event filter.
* `limit_access_to_global_configs` - Indicates whether the access control role has limited access to global EMS configurations.
### Related ONTAP commands
* `event role-config create`

### Learn more
* [`DOC /support/ems/role-configs`](#docs-support-support_ems_role-configs)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems role config create")
        async def ems_role_config_create(
        ) -> ResourceTable:
            """Create an instance of a EmsRoleConfig resource

            Args:
                links: 
                access_control_role: 
                event_filter: 
                limit_access_to_global_configs: Indicates whether the access control has limited access to global EMS configurations.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if access_control_role is not None:
                kwargs["access_control_role"] = access_control_role
            if event_filter is not None:
                kwargs["event_filter"] = event_filter
            if limit_access_to_global_configs is not None:
                kwargs["limit_access_to_global_configs"] = limit_access_to_global_configs

            resource = EmsRoleConfig(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create EmsRoleConfig: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the EMS role-based configuration of the access control role.
### Recommended optional properties
* `event_filter` - Identifies the event filter.
* `limit_access_to_global_configs` - Indicates whether the access control role has limited access to global EMS configurations.
### Related ONTAP commands
* `event role-config modify`

### Learn more
* [`DOC /support/ems/role-configs/{access_control_role.name}`](#docs-support-support_ems_role-configs_{access_control_role.name})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems role config modify")
        async def ems_role_config_modify(
        ) -> ResourceTable:
            """Modify an instance of a EmsRoleConfig resource

            Args:
                limit_access_to_global_configs: Indicates whether the access control has limited access to global EMS configurations.
                query_limit_access_to_global_configs: Indicates whether the access control has limited access to global EMS configurations.
            """

            kwargs = {}
            changes = {}
            if query_limit_access_to_global_configs is not None:
                kwargs["limit_access_to_global_configs"] = query_limit_access_to_global_configs

            if limit_access_to_global_configs is not None:
                changes["limit_access_to_global_configs"] = limit_access_to_global_configs

            if hasattr(EmsRoleConfig, "find"):
                resource = EmsRoleConfig.find(
                    **kwargs
                )
            else:
                resource = EmsRoleConfig()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify EmsRoleConfig: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Removes the EMS role-based configuration of the access control role.
### Related ONTAP commands
* `event role-config delete`

### Learn more
* [`DOC /support/ems/role-configs/{access_control_role.name}`](#docs-support-support_ems_role-configs_{access_control_role.name})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="ems role config delete")
        async def ems_role_config_delete(
        ) -> None:
            """Delete an instance of a EmsRoleConfig resource

            Args:
                limit_access_to_global_configs: Indicates whether the access control has limited access to global EMS configurations.
            """

            kwargs = {}
            if limit_access_to_global_configs is not None:
                kwargs["limit_access_to_global_configs"] = limit_access_to_global_configs

            if hasattr(EmsRoleConfig, "find"):
                resource = EmsRoleConfig.find(
                    **kwargs
                )
            else:
                resource = EmsRoleConfig()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete EmsRoleConfig: %s" % err)


