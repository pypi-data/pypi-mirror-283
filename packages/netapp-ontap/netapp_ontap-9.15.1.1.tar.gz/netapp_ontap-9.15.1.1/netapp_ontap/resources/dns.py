r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Displays DNS information and controls the DNS subsytem. DNS domain name and DNS servers are required parameters.
## Retrieving DNS information
The DNS GET endpoint retrieves all of the DNS configurations for all SVMs.
DNS configuration for the cluster is retrieved via [`/api/cluster`](#docs-cluster-cluster).
## Examples
### Retrieving all of the fields for all of the DNS configurations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Dns.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Dns(
        {
            "domains": ["domain.example.com"],
            "servers": ["44.44.44.44"],
            "scope": "cluster",
            "svm": {
                "name": "clust-1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "27eff5d8-22b2-11eb-8038-0050568ed32c",
            },
            "timeout": 2,
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/27eff5d8-22b2-11eb-8038-0050568ed32c"
                }
            },
            "attempts": 1,
        }
    ),
    Dns(
        {
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            "domains": ["domainA.example.com"],
            "dynamic_dns": {
                "use_secure": False,
                "enabled": False,
                "time_to_live": "PT1H",
            },
            "servers": ["10.10.10.10"],
            "scope": "svm",
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            },
            "timeout": 2,
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
                }
            },
            "attempts": 1,
        }
    ),
    Dns(
        {
            "uuid": "19076d35-6e27-11e8-b9b8-005056b41bd1",
            "domains": ["sample.example.com"],
            "dynamic_dns": {
                "use_secure": False,
                "enabled": True,
                "time_to_live": "PT3H",
            },
            "servers": ["11.11.11.11", "22.22.22.22", "33.33.33.33"],
            "scope": "svm",
            "svm": {
                "name": "vs2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/19076d35-6e27-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "19076d35-6e27-11e8-b9b8-005056b41bd1",
            },
            "timeout": 2,
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/19076d35-6e27-11e8-b9b8-005056b41bd1"
                }
            },
            "attempts": 2,
        }
    ),
]

```
</div>
</div>

### Retrieving all DNS configurations whose domain name starts with _dom*_.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Dns.get_collection(domains="dom*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Dns(
        {
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            "domains": ["domainA.example.com"],
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            },
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
                }
            },
        }
    )
]

```
</div>
</div>

### Retrieving the DNS configuration for a specific SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Dns(
    {
        "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        "packet_query_match": True,
        "domains": ["domainA.example.com"],
        "dynamic_dns": {"use_secure": False, "enabled": False, "time_to_live": "P1D"},
        "servers": ["10.10.10.10"],
        "scope": "svm",
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "timeout": 2,
        "tld_query_enabled": True,
        "_links": {
            "self": {
                "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "source_address_match": True,
        "attempts": 1,
    }
)

```
</div>
</div>

### Retrieving the advanced fields "DNS status", "tld_query_enable", "source_address_match", and "packet_query_match" using wildcards **
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.get(fileds="**")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Dns(
    {
        "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        "packet_query_match": True,
        "domains": ["domainA.example.com"],
        "dynamic_dns": {"use_secure": False, "enabled": False, "time_to_live": "P1D"},
        "servers": ["10.10.10.10"],
        "scope": "svm",
        "status": [
            {
                "code": 0,
                "name_server": "10.10.10.10",
                "state": "up",
                "message": "Response time (msec): ",
            }
        ],
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "timeout": 2,
        "tld_query_enabled": True,
        "_links": {
            "self": {
                "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "source_address_match": True,
        "attempts": 1,
    }
)

```
</div>
</div>

### Retrieving the "service_ips" for a specific DNS service name
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.get(fields="**", **{"service.name": "_kpasswd._udp.domainA.example.com"})
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
Dns(
    {
        "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        "packet_query_match": True,
        "domains": ["domainA.example.com"],
        "dynamic_dns": {"use_secure": False, "enabled": False, "time_to_live": "P1D"},
        "service_ips": ["10.10.10.10", "2001:db08:a0b:12f0::1"],
        "servers": ["10.10.10.10"],
        "scope": "svm",
        "status": [
            {
                "code": 0,
                "name_server": "10.10.10.10",
                "state": "up",
                "message": "Response time (msec): 218",
            }
        ],
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "timeout": 2,
        "tld_query_enabled": True,
        "_links": {
            "self": {
                "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1?fields=**"
            }
        },
        "source_address_match": True,
        "attempts": 1,
    }
)

```
</div>
</div>

### Retrieving the "service_ips" for a specific DNS service name with a particular address type (can be ipv4, ipv6 or all)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.get(
        fields="**",
        **{
            "service.name": "_kpasswd._udp.domainA.example.com",
            "service.address_type": "ipv4",
        }
    )
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Dns(
    {
        "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        "packet_query_match": True,
        "domains": ["domainA.example.com"],
        "dynamic_dns": {"use_secure": False, "enabled": False, "time_to_live": "P1D"},
        "service_ips": ["10.10.10.10"],
        "servers": ["10.10.10.10"],
        "scope": "svm",
        "status": [
            {
                "code": 0,
                "name_server": "10.10.10.10",
                "state": "up",
                "message": "Response time (msec): 218",
            }
        ],
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "timeout": 2,
        "tld_query_enabled": True,
        "_links": {
            "self": {
                "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1?fields=**"
            }
        },
        "source_address_match": True,
        "attempts": 1,
    }
)

```
</div>
</div>

## Creating a DNS configuration
The DNS POST endpoint creates a DNS configuration for the specified SVM.
## Examples
### Specifying only the required fields
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.domains = ["domainA.example.com"]
    resource.servers = ["10.10.10.10"]
    resource.post(hydrate=True)
    print(resource)

```

### Specifying the optional fields as well
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.domains = ["domainA.example.com"]
    resource.servers = ["10.10.10.10"]
    resource.timeout = 2
    resource.attempts = 3
    resource.post(hydrate=True)
    print(resource)

```

### Specifying the scope of the SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.domains = ["domainA.example.com"]
    resource.servers = ["10.10.10.10"]
    resource.timeout = 2
    resource.attempts = 3
    resource.scope = "svm"
    resource.post(hydrate=True)
    print(resource)

```

## Updating a DNS configuration
The DNS PATCH endpoint updates the DNS configuration for the specified SVM.
## Examples
### Updating both the DNS domains and servers
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.domains = ["domainA.example.com", "domainB.example.com"]
    resource.servers = ["10.10.10.10", "10.10.10.11"]
    resource.patch()

```

### Updating the DNS servers only
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.servers = ["10.10.10.10"]
    resource.patch()

```

### Updating the optional fields "timeout", "attempts", and "source_address_match"
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.timeout = 2
    resource.attempts = 3
    resource.source_address_match = True
    resource.patch()

```

### Updating the Dynamic DNS related fields
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
    resource.timeout = 2
    resource.attempts = 3
    resource.dynamic_dns.enabled = True
    resource.dynamic_dns.time_to_live = "20h"
    resource.patch()

```

## Deleting a DNS configuration
The DNS DELETE endpoint deletes the DNS configuration for the specified SVM.
## Example
The following example shows a DELETE operation.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(uuid="179d3c85-7053-11e8-b9b8-005056b41bd1")
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


__all__ = ["Dns", "DnsSchema"]
__pdoc__ = {
    "DnsSchema.resource": False,
    "DnsSchema.opts": False,
    "Dns.dns_show": False,
    "Dns.dns_create": False,
    "Dns.dns_modify": False,
    "Dns.dns_delete": False,
}


class DnsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Dns object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the dns."""

    attempts = Size(
        data_key="attempts",
        validate=integer_validation(minimum=1, maximum=4),
        allow_none=True,
    )
    r""" Number of attempts allowed when querying the DNS name servers.


Example: 1"""

    domains = marshmallow_fields.List(marshmallow_fields.Str, data_key="domains", allow_none=True)
    r""" The domains field of the dns."""

    dynamic_dns = marshmallow_fields.Nested("netapp_ontap.models.ddns.DdnsSchema", data_key="dynamic_dns", unknown=EXCLUDE, allow_none=True)
    r""" The dynamic_dns field of the dns."""

    packet_query_match = marshmallow_fields.Boolean(
        data_key="packet_query_match",
        allow_none=True,
    )
    r""" Indicates whether or not the query section of the reply packet is equal to that of the query packet."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for DNS owned by an SVM, otherwise set to "cluster".


Valid choices:

* svm
* cluster"""

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" The servers field of the dns."""

    service_ips = marshmallow_fields.List(marshmallow_fields.Str, data_key="service_ips", allow_none=True)
    r""" List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both.


Example: ["10.224.65.20","2001:db08:a0b:12f0::1"]"""

    skip_config_validation = marshmallow_fields.Boolean(
        data_key="skip_config_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified DNS configuration is disabled."""

    source_address_match = marshmallow_fields.Boolean(
        data_key="source_address_match",
        allow_none=True,
    )
    r""" Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to."""

    status = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.status.StatusSchema", unknown=EXCLUDE, allow_none=True), data_key="status", allow_none=True)
    r""" Status of all the DNS name servers configured for the specified SVM."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the dns."""

    timeout = Size(
        data_key="timeout",
        validate=integer_validation(minimum=1, maximum=5),
        allow_none=True,
    )
    r""" Timeout values for queries to the name servers, in seconds.


Example: 2"""

    tld_query_enabled = marshmallow_fields.Boolean(
        data_key="tld_query_enabled",
        allow_none=True,
    )
    r""" Enable or disable top-level domain (TLD) queries."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of the DNS object.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7"""

    @property
    def resource(self):
        return Dns

    gettable_fields = [
        "links",
        "attempts",
        "domains",
        "dynamic_dns",
        "packet_query_match",
        "scope",
        "servers",
        "service_ips",
        "source_address_match",
        "status",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "timeout",
        "tld_query_enabled",
        "uuid",
    ]
    """links,attempts,domains,dynamic_dns,packet_query_match,scope,servers,service_ips,source_address_match,status,svm.links,svm.name,svm.uuid,timeout,tld_query_enabled,uuid,"""

    patchable_fields = [
        "attempts",
        "domains",
        "dynamic_dns",
        "packet_query_match",
        "servers",
        "skip_config_validation",
        "source_address_match",
        "timeout",
        "tld_query_enabled",
        "uuid",
    ]
    """attempts,domains,dynamic_dns,packet_query_match,servers,skip_config_validation,source_address_match,timeout,tld_query_enabled,uuid,"""

    postable_fields = [
        "attempts",
        "domains",
        "packet_query_match",
        "scope",
        "servers",
        "skip_config_validation",
        "source_address_match",
        "svm.name",
        "svm.uuid",
        "timeout",
        "tld_query_enabled",
        "uuid",
    ]
    """attempts,domains,packet_query_match,scope,servers,skip_config_validation,source_address_match,svm.name,svm.uuid,timeout,tld_query_enabled,uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Dns.get_collection(fields=field)]
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
            raise NetAppRestError("Dns modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Dns(Resource):
    """Allows interaction with Dns objects on the host"""

    _schema = DnsSchema
    _path = "/api/name-services/dns"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the DNS configurations of all SVMs.
Specify 'scope' as 'svm' to retrieve the DNS configuration of all the data SVMs.
Specify 'scope' as 'cluster' to retrieve the DNS configuration of the cluster.
### Advanced properties
* 'tld_query_enabled'
* 'source_address_match'
* 'packet_query_match'
* 'status' property retrieves the status of each name server of the DNS configuration for an SVM.
* 'service_ips' property is displayed only when both service.name and SVM are set.
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
* `vserver services name-service dns dynamic-update show`
* `vserver services access-check dns srv-lookup`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="dns show")
        def dns_show(
            fields: List[Choices.define(["attempts", "domains", "packet_query_match", "scope", "servers", "service_ips", "skip_config_validation", "source_address_match", "timeout", "tld_query_enabled", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Dns resources

            Args:
                attempts: Number of attempts allowed when querying the DNS name servers. 
                domains: 
                packet_query_match: Indicates whether or not the query section of the reply packet is equal to that of the query packet. 
                scope: Set to \"svm\" for DNS owned by an SVM, otherwise set to \"cluster\". 
                servers: 
                service_ips: List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both. 
                skip_config_validation: Indicates whether or not the validation for the specified DNS configuration is disabled. 
                source_address_match: Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to. 
                timeout: Timeout values for queries to the name servers, in seconds. 
                tld_query_enabled: Enable or disable top-level domain (TLD) queries. 
                uuid: UUID of the DNS object. 
            """

            kwargs = {}
            if attempts is not None:
                kwargs["attempts"] = attempts
            if domains is not None:
                kwargs["domains"] = domains
            if packet_query_match is not None:
                kwargs["packet_query_match"] = packet_query_match
            if scope is not None:
                kwargs["scope"] = scope
            if servers is not None:
                kwargs["servers"] = servers
            if service_ips is not None:
                kwargs["service_ips"] = service_ips
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if source_address_match is not None:
                kwargs["source_address_match"] = source_address_match
            if timeout is not None:
                kwargs["timeout"] = timeout
            if tld_query_enabled is not None:
                kwargs["tld_query_enabled"] = tld_query_enabled
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Dns.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Dns resources that match the provided query"""
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
        """Returns a list of RawResources that represent Dns resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Dns"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates DNS domain and server configurations of an SVM.
### Important notes
- Both DNS domains and servers can be modified.
- The domains and servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified for the `servers` field.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>
- The DNS server validation can be skipped by setting the property "skip_config_validation" to "true".
- Dynamic DNS configuration can be modified.
- If both DNS and Dynamic DNS parameters are modified, DNS parameters are updated first followed by Dynamic DNS parameters.
  If updating Dynamic DNS fails, then the updated DNS configuration is not reverted.
#### The following parameters are optional:
- timeout
- attempts
- source_address_match
- packet_query_match
- tld_query_enabled
- skip_config_validation
- dynamic_dns.enabled
- dynamic_dns.use_secure
- dynamic_dns.time_to_live
### Related ONTAP commands
* `vserver services name-service dns modify`
* `vserver services name-service dns dynamic-update modify`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Dns"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Dns"], NetAppResponse]:
        r"""Creates DNS domain and server configurations for an SVM.<br/>
### Important notes
- Each SVM can have only one DNS configuration.
- The domain name and the servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified in the `servers` field.
- Configuring more than one DNS server is recommended to avoid a single point of failure.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
</br> The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>
- The DNS server validation can be skipped by setting the property "skip_config_validation" to "true".
- Scope of the SVM can be specified using the "scope" parameter. "svm" scope refers to data SVMs and "cluster" scope refers to clusters.
#### The following parameters are optional:
- timeout
- attempts
- source_address_match
- packet_query_match
- tld_query_enabled
- skip_config_validation
- scope

### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Dns"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes DNS domain configuration of the specified SVM.
### Related ONTAP commands
* `vserver services name-service dns delete`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the DNS configurations of all SVMs.
Specify 'scope' as 'svm' to retrieve the DNS configuration of all the data SVMs.
Specify 'scope' as 'cluster' to retrieve the DNS configuration of the cluster.
### Advanced properties
* 'tld_query_enabled'
* 'source_address_match'
* 'packet_query_match'
* 'status' property retrieves the status of each name server of the DNS configuration for an SVM.
* 'service_ips' property is displayed only when both service.name and SVM are set.
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
* `vserver services name-service dns dynamic-update show`
* `vserver services access-check dns srv-lookup`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves DNS domain and server configuration of an SVM. By default, both DNS domains and servers are displayed.
### Advanced properties
* 'tld_query_enabled'
* 'source_address_match'
* 'packet_query_match'
* 'status' property retrieves the status of each name server of the DNS configuration for an SVM.
* 'service_ips' property is displayed only when both service.name and SVM are set.
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
* `vserver services name-service dns dynamic-update show`
* `vserver services access-check dns srv-lookup`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
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
        r"""Creates DNS domain and server configurations for an SVM.<br/>
### Important notes
- Each SVM can have only one DNS configuration.
- The domain name and the servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified in the `servers` field.
- Configuring more than one DNS server is recommended to avoid a single point of failure.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
</br> The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>
- The DNS server validation can be skipped by setting the property "skip_config_validation" to "true".
- Scope of the SVM can be specified using the "scope" parameter. "svm" scope refers to data SVMs and "cluster" scope refers to clusters.
#### The following parameters are optional:
- timeout
- attempts
- source_address_match
- packet_query_match
- tld_query_enabled
- skip_config_validation
- scope

### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="dns create")
        async def dns_create(
        ) -> ResourceTable:
            """Create an instance of a Dns resource

            Args:
                links: 
                attempts: Number of attempts allowed when querying the DNS name servers. 
                domains: 
                dynamic_dns: 
                packet_query_match: Indicates whether or not the query section of the reply packet is equal to that of the query packet. 
                scope: Set to \"svm\" for DNS owned by an SVM, otherwise set to \"cluster\". 
                servers: 
                service_ips: List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both. 
                skip_config_validation: Indicates whether or not the validation for the specified DNS configuration is disabled. 
                source_address_match: Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to. 
                status: Status of all the DNS name servers configured for the specified SVM. 
                svm: 
                timeout: Timeout values for queries to the name servers, in seconds. 
                tld_query_enabled: Enable or disable top-level domain (TLD) queries. 
                uuid: UUID of the DNS object. 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if attempts is not None:
                kwargs["attempts"] = attempts
            if domains is not None:
                kwargs["domains"] = domains
            if dynamic_dns is not None:
                kwargs["dynamic_dns"] = dynamic_dns
            if packet_query_match is not None:
                kwargs["packet_query_match"] = packet_query_match
            if scope is not None:
                kwargs["scope"] = scope
            if servers is not None:
                kwargs["servers"] = servers
            if service_ips is not None:
                kwargs["service_ips"] = service_ips
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if source_address_match is not None:
                kwargs["source_address_match"] = source_address_match
            if status is not None:
                kwargs["status"] = status
            if svm is not None:
                kwargs["svm"] = svm
            if timeout is not None:
                kwargs["timeout"] = timeout
            if tld_query_enabled is not None:
                kwargs["tld_query_enabled"] = tld_query_enabled
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = Dns(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create Dns: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates DNS domain and server configurations of an SVM.
### Important notes
- Both DNS domains and servers can be modified.
- The domains and servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified for the `servers` field.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>
- The DNS server validation can be skipped by setting the property "skip_config_validation" to "true".
- Dynamic DNS configuration can be modified.
- If both DNS and Dynamic DNS parameters are modified, DNS parameters are updated first followed by Dynamic DNS parameters.
  If updating Dynamic DNS fails, then the updated DNS configuration is not reverted.
#### The following parameters are optional:
- timeout
- attempts
- source_address_match
- packet_query_match
- tld_query_enabled
- skip_config_validation
- dynamic_dns.enabled
- dynamic_dns.use_secure
- dynamic_dns.time_to_live
### Related ONTAP commands
* `vserver services name-service dns modify`
* `vserver services name-service dns dynamic-update modify`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="dns modify")
        async def dns_modify(
        ) -> ResourceTable:
            """Modify an instance of a Dns resource

            Args:
                attempts: Number of attempts allowed when querying the DNS name servers. 
                query_attempts: Number of attempts allowed when querying the DNS name servers. 
                domains: 
                query_domains: 
                packet_query_match: Indicates whether or not the query section of the reply packet is equal to that of the query packet. 
                query_packet_query_match: Indicates whether or not the query section of the reply packet is equal to that of the query packet. 
                scope: Set to \"svm\" for DNS owned by an SVM, otherwise set to \"cluster\". 
                query_scope: Set to \"svm\" for DNS owned by an SVM, otherwise set to \"cluster\". 
                servers: 
                query_servers: 
                service_ips: List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both. 
                query_service_ips: List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both. 
                skip_config_validation: Indicates whether or not the validation for the specified DNS configuration is disabled. 
                query_skip_config_validation: Indicates whether or not the validation for the specified DNS configuration is disabled. 
                source_address_match: Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to. 
                query_source_address_match: Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to. 
                timeout: Timeout values for queries to the name servers, in seconds. 
                query_timeout: Timeout values for queries to the name servers, in seconds. 
                tld_query_enabled: Enable or disable top-level domain (TLD) queries. 
                query_tld_query_enabled: Enable or disable top-level domain (TLD) queries. 
                uuid: UUID of the DNS object. 
                query_uuid: UUID of the DNS object. 
            """

            kwargs = {}
            changes = {}
            if query_attempts is not None:
                kwargs["attempts"] = query_attempts
            if query_domains is not None:
                kwargs["domains"] = query_domains
            if query_packet_query_match is not None:
                kwargs["packet_query_match"] = query_packet_query_match
            if query_scope is not None:
                kwargs["scope"] = query_scope
            if query_servers is not None:
                kwargs["servers"] = query_servers
            if query_service_ips is not None:
                kwargs["service_ips"] = query_service_ips
            if query_skip_config_validation is not None:
                kwargs["skip_config_validation"] = query_skip_config_validation
            if query_source_address_match is not None:
                kwargs["source_address_match"] = query_source_address_match
            if query_timeout is not None:
                kwargs["timeout"] = query_timeout
            if query_tld_query_enabled is not None:
                kwargs["tld_query_enabled"] = query_tld_query_enabled
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if attempts is not None:
                changes["attempts"] = attempts
            if domains is not None:
                changes["domains"] = domains
            if packet_query_match is not None:
                changes["packet_query_match"] = packet_query_match
            if scope is not None:
                changes["scope"] = scope
            if servers is not None:
                changes["servers"] = servers
            if service_ips is not None:
                changes["service_ips"] = service_ips
            if skip_config_validation is not None:
                changes["skip_config_validation"] = skip_config_validation
            if source_address_match is not None:
                changes["source_address_match"] = source_address_match
            if timeout is not None:
                changes["timeout"] = timeout
            if tld_query_enabled is not None:
                changes["tld_query_enabled"] = tld_query_enabled
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(Dns, "find"):
                resource = Dns.find(
                    **kwargs
                )
            else:
                resource = Dns()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify Dns: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes DNS domain configuration of the specified SVM.
### Related ONTAP commands
* `vserver services name-service dns delete`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="dns delete")
        async def dns_delete(
        ) -> None:
            """Delete an instance of a Dns resource

            Args:
                attempts: Number of attempts allowed when querying the DNS name servers. 
                domains: 
                packet_query_match: Indicates whether or not the query section of the reply packet is equal to that of the query packet. 
                scope: Set to \"svm\" for DNS owned by an SVM, otherwise set to \"cluster\". 
                servers: 
                service_ips: List of IP addresses for a DNS service. Addresses can be IPv4, IPv6 or both. 
                skip_config_validation: Indicates whether or not the validation for the specified DNS configuration is disabled. 
                source_address_match: Indicates whether or not the DNS responses are from a different IP address to the IP address the request was sent to. 
                timeout: Timeout values for queries to the name servers, in seconds. 
                tld_query_enabled: Enable or disable top-level domain (TLD) queries. 
                uuid: UUID of the DNS object. 
            """

            kwargs = {}
            if attempts is not None:
                kwargs["attempts"] = attempts
            if domains is not None:
                kwargs["domains"] = domains
            if packet_query_match is not None:
                kwargs["packet_query_match"] = packet_query_match
            if scope is not None:
                kwargs["scope"] = scope
            if servers is not None:
                kwargs["servers"] = servers
            if service_ips is not None:
                kwargs["service_ips"] = service_ips
            if skip_config_validation is not None:
                kwargs["skip_config_validation"] = skip_config_validation
            if source_address_match is not None:
                kwargs["source_address_match"] = source_address_match
            if timeout is not None:
                kwargs["timeout"] = timeout
            if tld_query_enabled is not None:
                kwargs["tld_query_enabled"] = tld_query_enabled
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(Dns, "find"):
                resource = Dns.find(
                    **kwargs
                )
            else:
                resource = Dns()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete Dns: %s" % err)


