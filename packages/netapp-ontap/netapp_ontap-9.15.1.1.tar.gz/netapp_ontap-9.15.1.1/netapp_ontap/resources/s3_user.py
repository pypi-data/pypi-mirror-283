r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 user account is created on the S3 server. Buckets that are created for the server are associated with that user (as the owner of the buckets).
The creation of the user account involves generating a pair of keys "access" and "secret".
These keys are shared with clients (by the administrator out of band) who want to access the S3 server. The access_key is sent in the request and it identifies the user performing the operation. The client or server never send the secret_key over the wire.
Only the access_key can be retrieved from a GET operation. The secret_key along with the access_key is returned from a POST operation and from a PATCH operation if the administrator needs to regenerate the keys.
If the user is part of active-directory, the user name takes the format "user@fully_qualified_domain_name".
## Examples
### Retrieving S3 user configurations for a particular SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(S3User.get_collection("db2ec036-8375-11e9-99e1-0050568e3ed9", fields="*"))
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    S3User(
        {
            "key_expiry_time": "2023-11-13T23:28:03+05:30",
            "name": "user-1",
            "key_time_to_live": "PT3H5M",
            "comment": "S3 user",
            "access_key": "(token)",
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/db2ec036-8375-11e9-99e1-0050568e3ed9"
                    }
                },
                "uuid": "db2ec036-8375-11e9-99e1-0050568e3ed9",
            },
        }
    ),
    S3User(
        {
            "name": "user-2",
            "comment": "s3-user",
            "access_key": "(token)",
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/db2ec036-8375-11e9-99e1-0050568e3ed9"
                    }
                },
                "uuid": "db2ec036-8375-11e9-99e1-0050568e3ed9",
            },
        }
    ),
]

```
</div>
</div>

### Retrieving the user configuration of a specific S3 user
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9", name="user-1")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3User(
    {
        "key_expiry_time": "2023-02-20T10:04:31+00:00",
        "name": "user-1",
        "key_time_to_live": "P6DT1H5M",
        "comment": "s3-user",
        "access_key": "(token)",
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/db2ec036-8375-11e9-99e1-0050568e3ed9"}
            },
            "uuid": "db2ec036-8375-11e9-99e1-0050568e3ed9",
        },
    }
)

```
</div>
</div>

### Creating an S3 user configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9")
    resource.name = "user-1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3User({"name": "user-1", "access_key": "(token)"})

```
</div>
</div>

### Creating an S3 user configuration with key expiration configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9")
    resource.comment = "S3 user3"
    resource.key_time_to_live = "P6DT1H5M"
    resource.name = "user-3"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3User(
    {
        "key_expiry_time": "2023-06-16T12:08:38+00:00",
        "name": "user-3",
        "access_key": "(token)",
    }
)

```
</div>
</div>

### Creating an S3 user configuration with a key expiration configuration and where the user is part of Active directory.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9")
    resource.comment = "S3 user3"
    resource.key_time_to_live = "P6DT1H5M"
    resource.name = "user-3@domain1.com"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
S3User(
    {
        "key_expiry_time": "2023-06-16T12:08:38+00:00",
        "name": "user-3@domain1.com",
        "access_key": "(token)",
    }
)

```
</div>
</div>

### Regenerating first key for a specific S3 user for the specified SVM

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9", name="user-2")
    resource.patch(hydrate=True, regenerate_keys=True)

```


### Regenerating keys and setting new expiry configuration for a specific S3 user for the specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9", name="user-2")
    resource.key_time_to_live = "PT6H3M"
    resource.patch(hydrate=True, regenerate_keys=True)

```


### Deleting first key for a specific S3 user for a specified SVM

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("db2ec036-8375-11e9-99e1-0050568e3ed9", name="user-2")
    resource.patch(hydrate=True, delete_keys=True)

```


### Deleting the specified S3 user configuration for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3User

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3User("03ce5c36-f269-11e8-8852-0050568e5298", name="user-2")
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


__all__ = ["S3User", "S3UserSchema"]
__pdoc__ = {
    "S3UserSchema.resource": False,
    "S3UserSchema.opts": False,
    "S3User.s3_user_show": False,
    "S3User.s3_user_create": False,
    "S3User.s3_user_modify": False,
    "S3User.s3_user_delete": False,
}


class S3UserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3User object"""

    access_key = marshmallow_fields.Str(
        data_key="access_key",
        allow_none=True,
    )
    r""" Specifies the access key for the user.

Example: HJAKU28M3SXTE2UXUACV"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the user being created or modified.

Example: S3 user"""

    key_expiry_time = ImpreciseDateTime(
        data_key="key_expiry_time",
        allow_none=True,
    )
    r""" Specifies the date and time after which keys expire and are no longer valid.

Example: 2024-01-01T00:00:00.000+0000"""

    key_time_to_live = marshmallow_fields.Str(
        data_key="key_time_to_live",
        allow_none=True,
    )
    r""" Indicates the time period from when this parameter is specified:

* when creating or modifying a user or
* when the user keys were last regenerated, after which the user keys expire and are no longer valid.
* Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds.
* If the value specified is '0' seconds, then the keys won't expire.


Example: PT6H3M"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=64),
        allow_none=True,
    )
    r""" Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, "_", "+", "=", ",", ".","@", and "-".

Example: user-1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_user."""

    @property
    def resource(self):
        return S3User

    gettable_fields = [
        "access_key",
        "comment",
        "key_expiry_time",
        "key_time_to_live",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """access_key,comment,key_expiry_time,key_time_to_live,name,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "comment",
        "key_time_to_live",
    ]
    """comment,key_time_to_live,"""

    postable_fields = [
        "comment",
        "key_time_to_live",
        "name",
    ]
    """comment,key_time_to_live,name,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in S3User.get_collection(fields=field)]
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
            raise NetAppRestError("S3User modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class S3User(Resource):
    r""" This is a container of S3 users. """

    _schema = S3UserSchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/users"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 user's SVM configuration.
### Related ONTAP commands
* `vserver object-store-server user show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 user show")
        def s3_user_show(
            svm_uuid,
            access_key: Choices.define(_get_field_list("access_key"), cache_choices=True, inexact=True)=None,
            comment: Choices.define(_get_field_list("comment"), cache_choices=True, inexact=True)=None,
            key_expiry_time: Choices.define(_get_field_list("key_expiry_time"), cache_choices=True, inexact=True)=None,
            key_time_to_live: Choices.define(_get_field_list("key_time_to_live"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["access_key", "comment", "key_expiry_time", "key_time_to_live", "name", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of S3User resources

            Args:
                access_key: Specifies the access key for the user.
                comment: Can contain any additional information about the user being created or modified.
                key_expiry_time: Specifies the date and time after which keys expire and are no longer valid.
                key_time_to_live: Indicates the time period from when this parameter is specified: * when creating or modifying a user or * when the user keys were last regenerated, after which the user keys expire and are no longer valid. * Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds. * If the value specified is '0' seconds, then the keys won't expire. 
                name: Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, \"_\", \"+\", \"=\", \",\", \".\",\"@\", and \"-\".
            """

            kwargs = {}
            if access_key is not None:
                kwargs["access_key"] = access_key
            if comment is not None:
                kwargs["comment"] = comment
            if key_expiry_time is not None:
                kwargs["key_expiry_time"] = key_expiry_time
            if key_time_to_live is not None:
                kwargs["key_time_to_live"] = key_time_to_live
            if name is not None:
                kwargs["name"] = name
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return S3User.get_collection(
                svm_uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all S3User resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3User resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3User"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 user configuration of an SVM.
### Important notes
- User access_key and secret_key pair can be regenerated using the PATCH operation.
- User access_key and secret_key is returned in a PATCH operation if the "regenerate_keys" field is specified as true.
- If "regenerate_keys" is true and user keys have expiry configuration, then "key_expiry_time" is also returned as part of response.
- User access_key and secret_key pair can be deleted using the PATCH operation.
### Recommended optional properties
* `regenerate_keys` - Specifies if secret_key and access_key need to be regenerated.
* `delete_keys` - Specifies if secret_key and access_key need to be deleted.
* `comment` - Any information related to the S3 user.
### Related ONTAP commands
* `vserver object-store-server user show`
* `vserver object-store-server user regenerate-keys`
* `vserver object-store-server user delete-keys`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3User"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3User"], NetAppResponse]:
        r"""Creates the S3 user configuration.
### Important notes
- Each SVM can have one or more user configurations.
- If the user is a member of Active directory, the user name takes the format "user@FQDN". For example, "user1@domain1.com".
- If user creation is successful, a user access_key and secret_key is returned as part of the response.
- If user keys have expiry configuration, then "key_expiry_time" is also returned as part of the response.
### Required properties
* `svm.uuid` - Existing SVM in which to create the user configuration.
* `name` - User name that is to be created.
### Default property values
* `comment` - ""
### Related ONTAP commands
* `vserver object-store-server user create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["S3User"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 user configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server user delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 user's SVM configuration.
### Related ONTAP commands
* `vserver object-store-server user show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 user configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server user show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
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
        r"""Creates the S3 user configuration.
### Important notes
- Each SVM can have one or more user configurations.
- If the user is a member of Active directory, the user name takes the format "user@FQDN". For example, "user1@domain1.com".
- If user creation is successful, a user access_key and secret_key is returned as part of the response.
- If user keys have expiry configuration, then "key_expiry_time" is also returned as part of the response.
### Required properties
* `svm.uuid` - Existing SVM in which to create the user configuration.
* `name` - User name that is to be created.
### Default property values
* `comment` - ""
### Related ONTAP commands
* `vserver object-store-server user create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 user create")
        async def s3_user_create(
            svm_uuid,
            access_key: str = None,
            comment: str = None,
            key_expiry_time: datetime = None,
            key_time_to_live: str = None,
            name: str = None,
            svm: dict = None,
        ) -> ResourceTable:
            """Create an instance of a S3User resource

            Args:
                access_key: Specifies the access key for the user.
                comment: Can contain any additional information about the user being created or modified.
                key_expiry_time: Specifies the date and time after which keys expire and are no longer valid.
                key_time_to_live: Indicates the time period from when this parameter is specified: * when creating or modifying a user or * when the user keys were last regenerated, after which the user keys expire and are no longer valid. * Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds. * If the value specified is '0' seconds, then the keys won't expire. 
                name: Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, \"_\", \"+\", \"=\", \",\", \".\",\"@\", and \"-\".
                svm: 
            """

            kwargs = {}
            if access_key is not None:
                kwargs["access_key"] = access_key
            if comment is not None:
                kwargs["comment"] = comment
            if key_expiry_time is not None:
                kwargs["key_expiry_time"] = key_expiry_time
            if key_time_to_live is not None:
                kwargs["key_time_to_live"] = key_time_to_live
            if name is not None:
                kwargs["name"] = name
            if svm is not None:
                kwargs["svm"] = svm

            resource = S3User(
                svm_uuid,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create S3User: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 user configuration of an SVM.
### Important notes
- User access_key and secret_key pair can be regenerated using the PATCH operation.
- User access_key and secret_key is returned in a PATCH operation if the "regenerate_keys" field is specified as true.
- If "regenerate_keys" is true and user keys have expiry configuration, then "key_expiry_time" is also returned as part of response.
- User access_key and secret_key pair can be deleted using the PATCH operation.
### Recommended optional properties
* `regenerate_keys` - Specifies if secret_key and access_key need to be regenerated.
* `delete_keys` - Specifies if secret_key and access_key need to be deleted.
* `comment` - Any information related to the S3 user.
### Related ONTAP commands
* `vserver object-store-server user show`
* `vserver object-store-server user regenerate-keys`
* `vserver object-store-server user delete-keys`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 user modify")
        async def s3_user_modify(
            svm_uuid,
            access_key: str = None,
            query_access_key: str = None,
            comment: str = None,
            query_comment: str = None,
            key_expiry_time: datetime = None,
            query_key_expiry_time: datetime = None,
            key_time_to_live: str = None,
            query_key_time_to_live: str = None,
            name: str = None,
            query_name: str = None,
        ) -> ResourceTable:
            """Modify an instance of a S3User resource

            Args:
                access_key: Specifies the access key for the user.
                query_access_key: Specifies the access key for the user.
                comment: Can contain any additional information about the user being created or modified.
                query_comment: Can contain any additional information about the user being created or modified.
                key_expiry_time: Specifies the date and time after which keys expire and are no longer valid.
                query_key_expiry_time: Specifies the date and time after which keys expire and are no longer valid.
                key_time_to_live: Indicates the time period from when this parameter is specified: * when creating or modifying a user or * when the user keys were last regenerated, after which the user keys expire and are no longer valid. * Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds. * If the value specified is '0' seconds, then the keys won't expire. 
                query_key_time_to_live: Indicates the time period from when this parameter is specified: * when creating or modifying a user or * when the user keys were last regenerated, after which the user keys expire and are no longer valid. * Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds. * If the value specified is '0' seconds, then the keys won't expire. 
                name: Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, \"_\", \"+\", \"=\", \",\", \".\",\"@\", and \"-\".
                query_name: Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, \"_\", \"+\", \"=\", \",\", \".\",\"@\", and \"-\".
            """

            kwargs = {}
            changes = {}
            if query_access_key is not None:
                kwargs["access_key"] = query_access_key
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_key_expiry_time is not None:
                kwargs["key_expiry_time"] = query_key_expiry_time
            if query_key_time_to_live is not None:
                kwargs["key_time_to_live"] = query_key_time_to_live
            if query_name is not None:
                kwargs["name"] = query_name

            if access_key is not None:
                changes["access_key"] = access_key
            if comment is not None:
                changes["comment"] = comment
            if key_expiry_time is not None:
                changes["key_expiry_time"] = key_expiry_time
            if key_time_to_live is not None:
                changes["key_time_to_live"] = key_time_to_live
            if name is not None:
                changes["name"] = name

            if hasattr(S3User, "find"):
                resource = S3User.find(
                    svm_uuid,
                    **kwargs
                )
            else:
                resource = S3User(svm_uuid,)
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify S3User: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 user configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server user delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/users`](#docs-object-store-protocols_s3_services_{svm.uuid}_users)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 user delete")
        async def s3_user_delete(
            svm_uuid,
            access_key: str = None,
            comment: str = None,
            key_expiry_time: datetime = None,
            key_time_to_live: str = None,
            name: str = None,
        ) -> None:
            """Delete an instance of a S3User resource

            Args:
                access_key: Specifies the access key for the user.
                comment: Can contain any additional information about the user being created or modified.
                key_expiry_time: Specifies the date and time after which keys expire and are no longer valid.
                key_time_to_live: Indicates the time period from when this parameter is specified: * when creating or modifying a user or * when the user keys were last regenerated, after which the user keys expire and are no longer valid. * Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds. * If the value specified is '0' seconds, then the keys won't expire. 
                name: Specifies the name of the user. A user name length can range from 1 to 64 characters and can only contain the following combination of characters 0-9, A-Z, a-z, \"_\", \"+\", \"=\", \",\", \".\",\"@\", and \"-\".
            """

            kwargs = {}
            if access_key is not None:
                kwargs["access_key"] = access_key
            if comment is not None:
                kwargs["comment"] = comment
            if key_expiry_time is not None:
                kwargs["key_expiry_time"] = key_expiry_time
            if key_time_to_live is not None:
                kwargs["key_time_to_live"] = key_time_to_live
            if name is not None:
                kwargs["name"] = name

            if hasattr(S3User, "find"):
                resource = S3User.find(
                    svm_uuid,
                    **kwargs
                )
            else:
                resource = S3User(svm_uuid,)
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete S3User: %s" % err)


