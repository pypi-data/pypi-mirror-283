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


__all__ = ["KeyServer", "KeyServerSchema"]
__pdoc__ = {
    "KeyServerSchema.resource": False,
    "KeyServerSchema.opts": False,
    "KeyServer.key_server_show": False,
    "KeyServer.key_server_create": False,
    "KeyServer.key_server_modify": False,
    "KeyServer.key_server_delete": False,
}


class KeyServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the key_server."""

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.key_server_state_array.KeyServerStateArraySchema", data_key="connectivity", unknown=EXCLUDE, allow_none=True)
    r""" The connectivity field of the key_server."""

    create_remove_timeout = Size(
        data_key="create_remove_timeout",
        validate=integer_validation(minimum=-1, maximum=60),
        allow_none=True,
    )
    r""" The key server timeout for create and remove operations.
-1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response.


Example: 60"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Password credentials for connecting with the key server. This is not audited.

Example: password"""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.key_server_no_records.KeyServerNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of key servers specified to add multiple key servers to a key manager in a single API call. Valid in POST only and not valid if `server` is provided."""

    secondary_key_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="secondary_key_servers", allow_none=True)
    r""" A list of the secondary key servers associated with the primary key server.

Example: ["secondary1.com","10.1.2.3"]"""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.

Example: keyserver1.com:5698"""

    timeout = Size(
        data_key="timeout",
        validate=integer_validation(minimum=-1, maximum=60),
        allow_none=True,
    )
    r""" I/O timeout in seconds for communicating with the key server.
-1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response.


Example: 60"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" KMIP username credentials for connecting with the key server.

Example: username"""

    @property
    def resource(self):
        return KeyServer

    gettable_fields = [
        "links",
        "connectivity",
        "create_remove_timeout",
        "secondary_key_servers",
        "server",
        "timeout",
        "username",
    ]
    """links,connectivity,create_remove_timeout,secondary_key_servers,server,timeout,username,"""

    patchable_fields = [
        "create_remove_timeout",
        "password",
        "secondary_key_servers",
        "timeout",
        "username",
    ]
    """create_remove_timeout,password,secondary_key_servers,timeout,username,"""

    postable_fields = [
        "records",
        "server",
    ]
    """records,server,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in KeyServer.get_collection(fields=field)]
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
            raise NetAppRestError("KeyServer modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class KeyServer(Resource):
    """Allows interaction with KeyServer objects on the host"""

    _schema = KeyServerSchema
    _path = "/api/security/key-managers/{security_key_manager[uuid]}/key-servers"
    _keys = ["security_key_manager.uuid", "server"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="key server show")
        def key_server_show(
            uuid,
            create_remove_timeout: Choices.define(_get_field_list("create_remove_timeout"), cache_choices=True, inexact=True)=None,
            password: Choices.define(_get_field_list("password"), cache_choices=True, inexact=True)=None,
            secondary_key_servers: Choices.define(_get_field_list("secondary_key_servers"), cache_choices=True, inexact=True)=None,
            server: Choices.define(_get_field_list("server"), cache_choices=True, inexact=True)=None,
            timeout: Choices.define(_get_field_list("timeout"), cache_choices=True, inexact=True)=None,
            username: Choices.define(_get_field_list("username"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["create_remove_timeout", "password", "secondary_key_servers", "server", "timeout", "username", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of KeyServer resources

            Args:
                create_remove_timeout: The key server timeout for create and remove operations. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                password: Password credentials for connecting with the key server. This is not audited.
                secondary_key_servers: A list of the secondary key servers associated with the primary key server.
                server: External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.
                timeout: I/O timeout in seconds for communicating with the key server. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                username: KMIP username credentials for connecting with the key server.
            """

            kwargs = {}
            if create_remove_timeout is not None:
                kwargs["create_remove_timeout"] = create_remove_timeout
            if password is not None:
                kwargs["password"] = password
            if secondary_key_servers is not None:
                kwargs["secondary_key_servers"] = secondary_key_servers
            if server is not None:
                kwargs["server"] = server
            if timeout is not None:
                kwargs["timeout"] = timeout
            if username is not None:
                kwargs["username"] = username
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return KeyServer.get_collection(
                uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all KeyServer resources that match the provided query"""
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
        """Returns a list of RawResources that represent KeyServer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["KeyServer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a primary key server.
### Related ONTAP commands
* `security key-manager external modify-server`
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["KeyServer"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["KeyServer"], NetAppResponse]:
        r"""Adds primary key servers to a configured external key manager.
### Required properties
* `uuid` - UUID of the external key manager.
* `server` - Primary Key server name.
### Related ONTAP commands
* `security key-manager external add-servers`
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
        records: Iterable["KeyServer"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a primary key server.
### Optional parameters:
* `force` - Bypass Out of Quorum checks when deleting a primary key server. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
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
        r"""Adds primary key servers to a configured external key manager.
### Required properties
* `uuid` - UUID of the external key manager.
* `server` - Primary Key server name.
### Related ONTAP commands
* `security key-manager external add-servers`
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="key server create")
        async def key_server_create(
            uuid,
            links: dict = None,
            connectivity: dict = None,
            create_remove_timeout: Size = None,
            password: str = None,
            records: dict = None,
            secondary_key_servers: dict = None,
            server: str = None,
            timeout: Size = None,
            username: str = None,
        ) -> ResourceTable:
            """Create an instance of a KeyServer resource

            Args:
                links: 
                connectivity: 
                create_remove_timeout: The key server timeout for create and remove operations. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                password: Password credentials for connecting with the key server. This is not audited.
                records: An array of key servers specified to add multiple key servers to a key manager in a single API call. Valid in POST only and not valid if `server` is provided. 
                secondary_key_servers: A list of the secondary key servers associated with the primary key server.
                server: External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.
                timeout: I/O timeout in seconds for communicating with the key server. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                username: KMIP username credentials for connecting with the key server.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if connectivity is not None:
                kwargs["connectivity"] = connectivity
            if create_remove_timeout is not None:
                kwargs["create_remove_timeout"] = create_remove_timeout
            if password is not None:
                kwargs["password"] = password
            if records is not None:
                kwargs["records"] = records
            if secondary_key_servers is not None:
                kwargs["secondary_key_servers"] = secondary_key_servers
            if server is not None:
                kwargs["server"] = server
            if timeout is not None:
                kwargs["timeout"] = timeout
            if username is not None:
                kwargs["username"] = username

            resource = KeyServer(
                uuid,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create KeyServer: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a primary key server.
### Related ONTAP commands
* `security key-manager external modify-server`
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="key server modify")
        async def key_server_modify(
            uuid,
            create_remove_timeout: Size = None,
            query_create_remove_timeout: Size = None,
            password: str = None,
            query_password: str = None,
            secondary_key_servers: dict = None,
            query_secondary_key_servers: dict = None,
            server: str = None,
            query_server: str = None,
            timeout: Size = None,
            query_timeout: Size = None,
            username: str = None,
            query_username: str = None,
        ) -> ResourceTable:
            """Modify an instance of a KeyServer resource

            Args:
                create_remove_timeout: The key server timeout for create and remove operations. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                query_create_remove_timeout: The key server timeout for create and remove operations. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                password: Password credentials for connecting with the key server. This is not audited.
                query_password: Password credentials for connecting with the key server. This is not audited.
                secondary_key_servers: A list of the secondary key servers associated with the primary key server.
                query_secondary_key_servers: A list of the secondary key servers associated with the primary key server.
                server: External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.
                query_server: External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.
                timeout: I/O timeout in seconds for communicating with the key server. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                query_timeout: I/O timeout in seconds for communicating with the key server. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                username: KMIP username credentials for connecting with the key server.
                query_username: KMIP username credentials for connecting with the key server.
            """

            kwargs = {}
            changes = {}
            if query_create_remove_timeout is not None:
                kwargs["create_remove_timeout"] = query_create_remove_timeout
            if query_password is not None:
                kwargs["password"] = query_password
            if query_secondary_key_servers is not None:
                kwargs["secondary_key_servers"] = query_secondary_key_servers
            if query_server is not None:
                kwargs["server"] = query_server
            if query_timeout is not None:
                kwargs["timeout"] = query_timeout
            if query_username is not None:
                kwargs["username"] = query_username

            if create_remove_timeout is not None:
                changes["create_remove_timeout"] = create_remove_timeout
            if password is not None:
                changes["password"] = password
            if secondary_key_servers is not None:
                changes["secondary_key_servers"] = secondary_key_servers
            if server is not None:
                changes["server"] = server
            if timeout is not None:
                changes["timeout"] = timeout
            if username is not None:
                changes["username"] = username

            if hasattr(KeyServer, "find"):
                resource = KeyServer.find(
                    uuid,
                    **kwargs
                )
            else:
                resource = KeyServer(uuid,)
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify KeyServer: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a primary key server.
### Optional parameters:
* `force` - Bypass Out of Quorum checks when deleting a primary key server. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="key server delete")
        async def key_server_delete(
            uuid,
            create_remove_timeout: Size = None,
            password: str = None,
            secondary_key_servers: dict = None,
            server: str = None,
            timeout: Size = None,
            username: str = None,
        ) -> None:
            """Delete an instance of a KeyServer resource

            Args:
                create_remove_timeout: The key server timeout for create and remove operations. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                password: Password credentials for connecting with the key server. This is not audited.
                secondary_key_servers: A list of the secondary key servers associated with the primary key server.
                server: External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.
                timeout: I/O timeout in seconds for communicating with the key server. -1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response. 
                username: KMIP username credentials for connecting with the key server.
            """

            kwargs = {}
            if create_remove_timeout is not None:
                kwargs["create_remove_timeout"] = create_remove_timeout
            if password is not None:
                kwargs["password"] = password
            if secondary_key_servers is not None:
                kwargs["secondary_key_servers"] = secondary_key_servers
            if server is not None:
                kwargs["server"] = server
            if timeout is not None:
                kwargs["timeout"] = timeout
            if username is not None:
                kwargs["username"] = username

            if hasattr(KeyServer, "find"):
                resource = KeyServer.find(
                    uuid,
                    **kwargs
                )
            else:
                resource = KeyServer(uuid,)
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete KeyServer: %s" % err)


