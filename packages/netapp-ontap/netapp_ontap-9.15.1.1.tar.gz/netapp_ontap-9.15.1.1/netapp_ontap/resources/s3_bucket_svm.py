r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 bucket is a container of objects. Each bucket defines an object namespace. S3 server requests specify objects using a bucket-name and object-name pair. An object consists of data, along with optional metadata and access controls, accessible via a name. An object resides within a bucket. There can be more than one bucket in an S3 server. Buckets which are created for the server are associated with an S3 user that is created on the S3 server.
An access policy is an object that when associated with a resource, defines their permissions. Buckets and objects are defined as resources. By default, only the "root" user can access these resources. Access policies are used to manage access to these resources by enabling ONTAP admin to provide "grants" to allow other users to perform operations on the buckets.
## Examples
### Retrieving all fields for all S3 buckets of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            S3BucketSvm.get_collection(
                "12f3ba4c-7ae0-11e9-8c06-0050568ea123", fields="**"
            )
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    S3BucketSvm(
        {
            "name": "bucket-2",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "size": 209715200,
            "comment": "S3 bucket.",
            "audit_event_selector": {"permission": "all", "access": "all"},
            "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
            "encryption": {"enabled": False},
            "volume": {
                "name": "fg_oss_1558514455",
                "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
            },
            "qos_policy": {
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            },
            "logical_used_size": 157286400,
        }
    ),
    S3BucketSvm(
        {
            "name": "bucket-1",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "size": 1677721600,
            "comment": "bucket1",
            "uuid": "a8234aec-7e06-11e9-97e8-0050568ea123",
            "encryption": {"enabled": False},
            "policy": {
                "statements": [
                    {
                        "resources": ["*"],
                        "principals": ["Alice"],
                        "actions": ["*"],
                        "effect": "allow",
                        "sid": "fullAccessForAliceToBucket",
                    },
                    {
                        "resources": ["bucket-1", "bucket-1/*"],
                        "principals": ["ann", "jack"],
                        "conditions": [
                            {"source_ips": ["1.1.1.1/10"], "operator": "ip_address"},
                            {
                                "delimiters": ["del1", "del2"],
                                "usernames": ["user1", "user2"],
                                "prefixes": ["pref1", "pref2"],
                                "operator": "string_equals",
                            },
                            {"max_keys": [100], "operator": "numeric_equals"},
                        ],
                        "actions": ["ListBucket", "GetObject"],
                        "effect": "allow",
                        "sid": "AccessToListAndGetObjectForAnnAndJack",
                    },
                    {
                        "resources": [
                            "bucket-1/policy-docs/*",
                            "bucket-1/confidential-*",
                        ],
                        "principals": ["mike", "group/group1", "nasgroup/group2"],
                        "actions": ["*Object"],
                        "effect": "deny",
                        "sid": "DenyAccessToGetPutDeleteObjectForMike",
                    },
                    {
                        "resources": ["bucket-1/readme"],
                        "principals": ["*"],
                        "actions": ["GetObject"],
                        "effect": "allow",
                        "sid": "AccessToGetObjectForAnonymousUsers",
                    },
                    {
                        "resources": ["bucket-1/policies/examples/*"],
                        "principals": [],
                        "actions": ["GetObject"],
                        "effect": "allow",
                        "sid": "AccessToGetObjectForAllUsersOfSVM",
                    },
                ]
            },
            "volume": {
                "name": "fg_oss_1558690256",
                "uuid": "a36a1ea7-7e06-11e9-97e8-0050568ea123",
            },
            "qos_policy": {
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            },
            "logical_used_size": 0,
        }
    ),
]

```
</div>
</div>

### Retrieving the specified bucket associated with an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="527812ab-7c6d-11e9-97e8-0050568ea123",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3BucketSvm(
    {
        "name": "bucket-2",
        "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
        "size": 209715200,
        "comment": "S3 bucket.",
        "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
        "encryption": {"enabled": False},
        "volume": {
            "name": "fg_oss_1558514455",
            "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
        },
        "qos_policy": {
            "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
            "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
        },
        "logical_used_size": 157286400,
    }
)

```
</div>
</div>

### Creating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("12f3ba4c-7ae0-11e9-8c06-0050568ea123")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3BucketSvm({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with QoS policies and event selector for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
    resource.comment = "S3 bucket."
    resource.name = "bucket-3"
    resource.qos_policy = {
        "min_throughput_iops": 0,
        "min_throughput_mbps": 0,
        "max_throughput_iops": 1000000,
        "max_throughput_mbps": 900000,
        "uuid": "02d07a93-6177-11ea-b241-000c293feac8",
        "name": "vs0_auto_gen_policy_02cfa02a_6177_11ea_b241_000c293feac8",
    }
    resource.audit_event_selector = {"access": "all", "permission": "all"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3BucketSvm({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with policies for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.policy = {
        "statements": [
            {
                "actions": ["GetObject"],
                "conditions": [
                    {
                        "operator": "ip_address",
                        "source_ips": ["1.1.1.1/23", "1.2.2.2/20"],
                    },
                    {"max_keys": [1000], "operator": "numeric_equals"},
                    {
                        "delimiters": ["/"],
                        "operator": "string_equals",
                        "prefixes": ["pref"],
                        "usernames": ["user1"],
                    },
                ],
                "effect": "allow",
                "resources": ["bucket-3/policies/examples/*"],
                "sid": "AccessToGetObjectForAllUsersofSVM",
            },
            {
                "actions": ["*Object"],
                "effect": "deny",
                "principals": ["mike", "group/grp1"],
                "resources": ["bucket-3/policy-docs/*", "bucket-3/confidential-*"],
                "sid": "DenyAccessToObjectForMike",
            },
            {
                "actions": ["GetObject"],
                "effect": "allow",
                "principals": ["*"],
                "resources": ["bucket-3/readme"],
                "sid": "AnonnymousAccessToGetObjectForUsers",
            },
        ]
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
S3BucketSvm({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with lifecycle management rules
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-4"
    resource.lifecycle_management = {
        "rules": [
            {
                "name": "rule1",
                "expiration": {"object_age_days": "1000"},
                "abort_incomplete_multipart_upload": {"after_initiaion_days": 200},
                "object_filter": {"prefix": "obj1*/", "size_greater_than": "1000"},
            },
            {
                "name": "rule2",
                "object_filter": {"size_greater_than": "50"},
                "expiration": {"object_age_days": "5000"},
            },
        ]
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
S3BucketSvm({"name": "bucket-4", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket with object locking enabled for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("12f3ba4c-7ae0-11e9-8c06-0050568ea143")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea143"}
    ]
    resource.comment = "S3 Compliance mode bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-5"
    resource.retention = {"mode": "compliance", "default_period": "P1Y"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
S3BucketSvm({"name": "bucket-5", "comment": "S3 Compliance mode bucket."})

```
</div>
</div>

### Updating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.comment = "Bucket modified."
    resource.size = 111111111111
    resource.qos_policy = {
        "min_throughput_iops": 0,
        "min_throughput_mbps": 0,
        "max_throughput_iops": 1000000,
        "max_throughput_mbps": 900000,
        "uuid": "02d07a93-6177-11ea-b241-000c293feac8",
        "name": "vs0_auto_gen_policy_02cfa02a_6177_11ea_b241_000c293feac8",
    }
    resource.patch()

```

### Updating an S3 bucket policy and event selector for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.policy = {
        "statements": [
            {
                "actions": ["*"],
                "conditions": [
                    {
                        "operator": "ip_address",
                        "source_ips": ["1.1.1.1/23", "1.2.2.2/20"],
                    },
                    {"max_keys": [1000], "operator": "numeric_equals"},
                    {
                        "delimiters": ["/"],
                        "operator": "string_equals",
                        "prefixes": ["pref"],
                        "usernames": ["user1"],
                    },
                ],
                "effect": "allow",
                "resources": ["*"],
                "sid": "fullAccessForAllPrincipalsToBucket",
            }
        ]
    }
    resource.audit_event_selector = {"access": "read", "permission": "deny"}
    resource.patch()

```

### Updating the default-retention period on an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.retention = {"default_period": "P10Y"}
    resource.patch()

```

### Deleting an S3 bucket policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.policy = {"statements": []}
    resource.patch()

```

### Deleting an S3 bucket for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea123",
    )
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


__all__ = ["S3BucketSvm", "S3BucketSvmSchema"]
__pdoc__ = {
    "S3BucketSvmSchema.resource": False,
    "S3BucketSvmSchema.opts": False,
    "S3BucketSvm.s3_bucket_svm_show": False,
    "S3BucketSvm.s3_bucket_svm_create": False,
    "S3BucketSvm.s3_bucket_svm_modify": False,
    "S3BucketSvm.s3_bucket_svm_delete": False,
}


class S3BucketSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvm object"""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_aggregates.S3BucketAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" A list of aggregates for FlexGroup volume constituents where the bucket is hosted. If this option is not specified, the bucket is auto-provisioned as a FlexGroup volume. The "uuid" field cannot be used with the field "storage_service_level"."""

    audit_event_selector = marshmallow_fields.Nested("netapp_ontap.models.s3_audit_event_selector.S3AuditEventSelectorSchema", data_key="audit_event_selector", unknown=EXCLUDE, allow_none=True)
    r""" The audit_event_selector field of the s3_bucket_svm."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the bucket being created or modified.

Example: S3 bucket."""

    constituents_per_aggregate = Size(
        data_key="constituents_per_aggregate",
        validate=integer_validation(minimum=1, maximum=1000),
        allow_none=True,
    )
    r""" Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.

Example: 4"""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_encryption.S3BucketSvmEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the s3_bucket_svm."""

    lifecycle_management = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_lifecycle_management.S3BucketSvmLifecycleManagementSchema", data_key="lifecycle_management", unknown=EXCLUDE, allow_none=True)
    r""" The lifecycle_management field of the s3_bucket_svm."""

    logical_used_size = Size(
        data_key="logical_used_size",
        allow_none=True,
    )
    r""" Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=3, maximum=63),
        allow_none=True,
    )
    r""" Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, ".", and "-".

Example: bucket1"""

    nas_path = marshmallow_fields.Str(
        data_key="nas_path",
        allow_none=True,
    )
    r""" Specifies the NAS path to which the nas bucket corresponds to.

Example: /"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_policy.S3BucketPolicySchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the s3_bucket_svm."""

    protection_status = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_protection_status.S3BucketSvmProtectionStatusSchema", data_key="protection_status", unknown=EXCLUDE, allow_none=True)
    r""" The protection_status field of the s3_bucket_svm."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The qos_policy field of the s3_bucket_svm."""

    retention = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_retention.S3BucketRetentionSchema", data_key="retention", unknown=EXCLUDE, allow_none=True)
    r""" The retention field of the s3_bucket_svm."""

    role = marshmallow_fields.Str(
        data_key="role",
        validate=enum_validation(['standalone', 'active', 'passive']),
        allow_none=True,
    )
    r""" Specifies the role of the bucket. This field cannot be set in a POST method.

Valid choices:

* standalone
* active
* passive"""

    size = Size(
        data_key="size",
        validate=integer_validation(minimum=199229440, maximum=62672162783232000),
        allow_none=True,
    )
    r""" Specifies the bucket size in bytes; ranges from 190MB to 62PB.

Example: 819200000"""

    storage_service_level = marshmallow_fields.Str(
        data_key="storage_service_level",
        validate=enum_validation(['value', 'performance', 'extreme']),
        allow_none=True,
    )
    r""" Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are "value", "performance" or "extreme". This field cannot be used with the field "aggregates.uuid" or with the "constituents_per_aggregate" in a POST method. This field cannot be set using the PATCH method.

Valid choices:

* value
* performance
* extreme"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_bucket_svm."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['s3', 'nas']),
        allow_none=True,
    )
    r""" Specifies the bucket type. Valid values are "s3"and "nas". This field cannot be set using the PATCH method.

Valid choices:

* s3
* nas"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method."""

    versioning_state = marshmallow_fields.Str(
        data_key="versioning_state",
        validate=enum_validation(['disabled', 'enabled', 'suspended']),
        allow_none=True,
    )
    r""" Specifies the versioning state of the bucket. Valid values are "disabled", "enabled" or "suspended". Note that the versioning state cannot be modified to 'disabled' from any other state.

Valid choices:

* disabled
* enabled
* suspended"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the s3_bucket_svm."""

    @property
    def resource(self):
        return S3BucketSvm

    gettable_fields = [
        "audit_event_selector",
        "comment",
        "encryption",
        "lifecycle_management",
        "logical_used_size",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.links",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "role",
        "size",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
        "versioning_state",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """audit_event_selector,comment,encryption,lifecycle_management,logical_used_size,name,nas_path,policy,protection_status,qos_policy.links,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,role,size,svm.links,svm.name,svm.uuid,type,uuid,versioning_state,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "audit_event_selector",
        "comment",
        "lifecycle_management",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "size",
        "type",
        "versioning_state",
    ]
    """audit_event_selector,comment,lifecycle_management,nas_path,policy,protection_status,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,type,versioning_state,"""

    postable_fields = [
        "aggregates.name",
        "aggregates.uuid",
        "audit_event_selector",
        "comment",
        "constituents_per_aggregate",
        "lifecycle_management",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "size",
        "storage_service_level",
        "type",
        "versioning_state",
    ]
    """aggregates.name,aggregates.uuid,audit_event_selector,comment,constituents_per_aggregate,lifecycle_management,name,nas_path,policy,protection_status,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,storage_service_level,type,versioning_state,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in S3BucketSvm.get_collection(fields=field)]
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
            raise NetAppRestError("S3BucketSvm modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class S3BucketSvm(Resource):
    r""" A bucket is a container of objects. Each bucket defines an object namespace. S3 requests specify objects using a bucket-name and object-name pair. An object resides within a bucket. """

    _schema = S3BucketSvmSchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/buckets"
    _keys = ["svm.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 bucket's configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 bucket svm show")
        def s3_bucket_svm_show(
            svm_uuid,
            comment: Choices.define(_get_field_list("comment"), cache_choices=True, inexact=True)=None,
            constituents_per_aggregate: Choices.define(_get_field_list("constituents_per_aggregate"), cache_choices=True, inexact=True)=None,
            logical_used_size: Choices.define(_get_field_list("logical_used_size"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            nas_path: Choices.define(_get_field_list("nas_path"), cache_choices=True, inexact=True)=None,
            role: Choices.define(_get_field_list("role"), cache_choices=True, inexact=True)=None,
            size: Choices.define(_get_field_list("size"), cache_choices=True, inexact=True)=None,
            storage_service_level: Choices.define(_get_field_list("storage_service_level"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            versioning_state: Choices.define(_get_field_list("versioning_state"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["comment", "constituents_per_aggregate", "logical_used_size", "name", "nas_path", "role", "size", "storage_service_level", "type", "uuid", "versioning_state", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of S3BucketSvm resources

            Args:
                comment: Can contain any additional information about the bucket being created or modified.
                constituents_per_aggregate: Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.
                logical_used_size: Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method.
                name: Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, \".\", and \"-\".
                nas_path: Specifies the NAS path to which the nas bucket corresponds to.
                role: Specifies the role of the bucket. This field cannot be set in a POST method.
                size: Specifies the bucket size in bytes; ranges from 190MB to 62PB.
                storage_service_level: Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are \"value\", \"performance\" or \"extreme\". This field cannot be used with the field \"aggregates.uuid\" or with the \"constituents_per_aggregate\" in a POST method. This field cannot be set using the PATCH method.
                type: Specifies the bucket type. Valid values are \"s3\"and \"nas\". This field cannot be set using the PATCH method.
                uuid: Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method.
                versioning_state: Specifies the versioning state of the bucket. Valid values are \"disabled\", \"enabled\" or \"suspended\". Note that the versioning state cannot be modified to 'disabled' from any other state.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if constituents_per_aggregate is not None:
                kwargs["constituents_per_aggregate"] = constituents_per_aggregate
            if logical_used_size is not None:
                kwargs["logical_used_size"] = logical_used_size
            if name is not None:
                kwargs["name"] = name
            if nas_path is not None:
                kwargs["nas_path"] = nas_path
            if role is not None:
                kwargs["role"] = role
            if size is not None:
                kwargs["size"] = size
            if storage_service_level is not None:
                kwargs["storage_service_level"] = storage_service_level
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if versioning_state is not None:
                kwargs["versioning_state"] = versioning_state
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return S3BucketSvm.get_collection(
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
        """Returns a count of all S3BucketSvm resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3BucketSvm resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3BucketSvm"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 bucket configuration of an SVM.
### Important notes
- The following fields can be modified for a bucket:
  * `comment` - Any information related to the bucket.
  * `size` - Bucket size.
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Policy conditions can also be modified using this API.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets.  None can be specified for both access and permission to remove audit event selector.
  * `versioning_state` - Versioning state for buckets.
  * `nas_path` - NAS path to which the NAS bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3BucketSvm"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3BucketSvm"], NetAppResponse]:
        r"""Creates the S3 bucket configuration of an SVM.
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup.
- Constituents per aggregate specifies the number of components (or FlexVols) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
### Required properties
* `svm.uuid` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets. Hence specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3.
* `retention.mode` - no_lock
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket lifecycle-management-rule create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
        records: Iterable["S3BucketSvm"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 bucket's configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 bucket configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
        r"""Creates the S3 bucket configuration of an SVM.
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup.
- Constituents per aggregate specifies the number of components (or FlexVols) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
### Required properties
* `svm.uuid` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets. Hence specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3.
* `retention.mode` - no_lock
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket lifecycle-management-rule create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 bucket svm create")
        async def s3_bucket_svm_create(
            svm_uuid,
            aggregates: dict = None,
            audit_event_selector: dict = None,
            comment: str = None,
            constituents_per_aggregate: Size = None,
            encryption: dict = None,
            lifecycle_management: dict = None,
            logical_used_size: Size = None,
            name: str = None,
            nas_path: str = None,
            policy: dict = None,
            protection_status: dict = None,
            qos_policy: dict = None,
            retention: dict = None,
            role: str = None,
            size: Size = None,
            storage_service_level: str = None,
            svm: dict = None,
            type: str = None,
            uuid: str = None,
            versioning_state: str = None,
            volume: dict = None,
        ) -> ResourceTable:
            """Create an instance of a S3BucketSvm resource

            Args:
                aggregates: A list of aggregates for FlexGroup volume constituents where the bucket is hosted. If this option is not specified, the bucket is auto-provisioned as a FlexGroup volume. The \"uuid\" field cannot be used with the field \"storage_service_level\".
                audit_event_selector: 
                comment: Can contain any additional information about the bucket being created or modified.
                constituents_per_aggregate: Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.
                encryption: 
                lifecycle_management: 
                logical_used_size: Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method.
                name: Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, \".\", and \"-\".
                nas_path: Specifies the NAS path to which the nas bucket corresponds to.
                policy: 
                protection_status: 
                qos_policy: 
                retention: 
                role: Specifies the role of the bucket. This field cannot be set in a POST method.
                size: Specifies the bucket size in bytes; ranges from 190MB to 62PB.
                storage_service_level: Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are \"value\", \"performance\" or \"extreme\". This field cannot be used with the field \"aggregates.uuid\" or with the \"constituents_per_aggregate\" in a POST method. This field cannot be set using the PATCH method.
                svm: 
                type: Specifies the bucket type. Valid values are \"s3\"and \"nas\". This field cannot be set using the PATCH method.
                uuid: Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method.
                versioning_state: Specifies the versioning state of the bucket. Valid values are \"disabled\", \"enabled\" or \"suspended\". Note that the versioning state cannot be modified to 'disabled' from any other state.
                volume: 
            """

            kwargs = {}
            if aggregates is not None:
                kwargs["aggregates"] = aggregates
            if audit_event_selector is not None:
                kwargs["audit_event_selector"] = audit_event_selector
            if comment is not None:
                kwargs["comment"] = comment
            if constituents_per_aggregate is not None:
                kwargs["constituents_per_aggregate"] = constituents_per_aggregate
            if encryption is not None:
                kwargs["encryption"] = encryption
            if lifecycle_management is not None:
                kwargs["lifecycle_management"] = lifecycle_management
            if logical_used_size is not None:
                kwargs["logical_used_size"] = logical_used_size
            if name is not None:
                kwargs["name"] = name
            if nas_path is not None:
                kwargs["nas_path"] = nas_path
            if policy is not None:
                kwargs["policy"] = policy
            if protection_status is not None:
                kwargs["protection_status"] = protection_status
            if qos_policy is not None:
                kwargs["qos_policy"] = qos_policy
            if retention is not None:
                kwargs["retention"] = retention
            if role is not None:
                kwargs["role"] = role
            if size is not None:
                kwargs["size"] = size
            if storage_service_level is not None:
                kwargs["storage_service_level"] = storage_service_level
            if svm is not None:
                kwargs["svm"] = svm
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if versioning_state is not None:
                kwargs["versioning_state"] = versioning_state
            if volume is not None:
                kwargs["volume"] = volume

            resource = S3BucketSvm(
                svm_uuid,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to create S3BucketSvm: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 bucket configuration of an SVM.
### Important notes
- The following fields can be modified for a bucket:
  * `comment` - Any information related to the bucket.
  * `size` - Bucket size.
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Policy conditions can also be modified using this API.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets.  None can be specified for both access and permission to remove audit event selector.
  * `versioning_state` - Versioning state for buckets.
  * `nas_path` - NAS path to which the NAS bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 bucket svm modify")
        async def s3_bucket_svm_modify(
            svm_uuid,
            comment: str = None,
            query_comment: str = None,
            constituents_per_aggregate: Size = None,
            query_constituents_per_aggregate: Size = None,
            logical_used_size: Size = None,
            query_logical_used_size: Size = None,
            name: str = None,
            query_name: str = None,
            nas_path: str = None,
            query_nas_path: str = None,
            role: str = None,
            query_role: str = None,
            size: Size = None,
            query_size: Size = None,
            storage_service_level: str = None,
            query_storage_service_level: str = None,
            type: str = None,
            query_type: str = None,
            uuid: str = None,
            query_uuid: str = None,
            versioning_state: str = None,
            query_versioning_state: str = None,
        ) -> ResourceTable:
            """Modify an instance of a S3BucketSvm resource

            Args:
                comment: Can contain any additional information about the bucket being created or modified.
                query_comment: Can contain any additional information about the bucket being created or modified.
                constituents_per_aggregate: Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.
                query_constituents_per_aggregate: Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.
                logical_used_size: Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method.
                query_logical_used_size: Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method.
                name: Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, \".\", and \"-\".
                query_name: Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, \".\", and \"-\".
                nas_path: Specifies the NAS path to which the nas bucket corresponds to.
                query_nas_path: Specifies the NAS path to which the nas bucket corresponds to.
                role: Specifies the role of the bucket. This field cannot be set in a POST method.
                query_role: Specifies the role of the bucket. This field cannot be set in a POST method.
                size: Specifies the bucket size in bytes; ranges from 190MB to 62PB.
                query_size: Specifies the bucket size in bytes; ranges from 190MB to 62PB.
                storage_service_level: Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are \"value\", \"performance\" or \"extreme\". This field cannot be used with the field \"aggregates.uuid\" or with the \"constituents_per_aggregate\" in a POST method. This field cannot be set using the PATCH method.
                query_storage_service_level: Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are \"value\", \"performance\" or \"extreme\". This field cannot be used with the field \"aggregates.uuid\" or with the \"constituents_per_aggregate\" in a POST method. This field cannot be set using the PATCH method.
                type: Specifies the bucket type. Valid values are \"s3\"and \"nas\". This field cannot be set using the PATCH method.
                query_type: Specifies the bucket type. Valid values are \"s3\"and \"nas\". This field cannot be set using the PATCH method.
                uuid: Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method.
                query_uuid: Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method.
                versioning_state: Specifies the versioning state of the bucket. Valid values are \"disabled\", \"enabled\" or \"suspended\". Note that the versioning state cannot be modified to 'disabled' from any other state.
                query_versioning_state: Specifies the versioning state of the bucket. Valid values are \"disabled\", \"enabled\" or \"suspended\". Note that the versioning state cannot be modified to 'disabled' from any other state.
            """

            kwargs = {}
            changes = {}
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_constituents_per_aggregate is not None:
                kwargs["constituents_per_aggregate"] = query_constituents_per_aggregate
            if query_logical_used_size is not None:
                kwargs["logical_used_size"] = query_logical_used_size
            if query_name is not None:
                kwargs["name"] = query_name
            if query_nas_path is not None:
                kwargs["nas_path"] = query_nas_path
            if query_role is not None:
                kwargs["role"] = query_role
            if query_size is not None:
                kwargs["size"] = query_size
            if query_storage_service_level is not None:
                kwargs["storage_service_level"] = query_storage_service_level
            if query_type is not None:
                kwargs["type"] = query_type
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid
            if query_versioning_state is not None:
                kwargs["versioning_state"] = query_versioning_state

            if comment is not None:
                changes["comment"] = comment
            if constituents_per_aggregate is not None:
                changes["constituents_per_aggregate"] = constituents_per_aggregate
            if logical_used_size is not None:
                changes["logical_used_size"] = logical_used_size
            if name is not None:
                changes["name"] = name
            if nas_path is not None:
                changes["nas_path"] = nas_path
            if role is not None:
                changes["role"] = role
            if size is not None:
                changes["size"] = size
            if storage_service_level is not None:
                changes["storage_service_level"] = storage_service_level
            if type is not None:
                changes["type"] = type
            if uuid is not None:
                changes["uuid"] = uuid
            if versioning_state is not None:
                changes["versioning_state"] = versioning_state

            if hasattr(S3BucketSvm, "find"):
                resource = S3BucketSvm.find(
                    svm_uuid,
                    **kwargs
                )
            else:
                resource = S3BucketSvm(svm_uuid,)
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to modify S3BucketSvm: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if RECLINE_INSTALLED:
        @recline.command(name="s3 bucket svm delete")
        async def s3_bucket_svm_delete(
            svm_uuid,
            comment: str = None,
            constituents_per_aggregate: Size = None,
            logical_used_size: Size = None,
            name: str = None,
            nas_path: str = None,
            role: str = None,
            size: Size = None,
            storage_service_level: str = None,
            type: str = None,
            uuid: str = None,
            versioning_state: str = None,
        ) -> None:
            """Delete an instance of a S3BucketSvm resource

            Args:
                comment: Can contain any additional information about the bucket being created or modified.
                constituents_per_aggregate: Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.
                logical_used_size: Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method.
                name: Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, \".\", and \"-\".
                nas_path: Specifies the NAS path to which the nas bucket corresponds to.
                role: Specifies the role of the bucket. This field cannot be set in a POST method.
                size: Specifies the bucket size in bytes; ranges from 190MB to 62PB.
                storage_service_level: Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are \"value\", \"performance\" or \"extreme\". This field cannot be used with the field \"aggregates.uuid\" or with the \"constituents_per_aggregate\" in a POST method. This field cannot be set using the PATCH method.
                type: Specifies the bucket type. Valid values are \"s3\"and \"nas\". This field cannot be set using the PATCH method.
                uuid: Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method.
                versioning_state: Specifies the versioning state of the bucket. Valid values are \"disabled\", \"enabled\" or \"suspended\". Note that the versioning state cannot be modified to 'disabled' from any other state.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if constituents_per_aggregate is not None:
                kwargs["constituents_per_aggregate"] = constituents_per_aggregate
            if logical_used_size is not None:
                kwargs["logical_used_size"] = logical_used_size
            if name is not None:
                kwargs["name"] = name
            if nas_path is not None:
                kwargs["nas_path"] = nas_path
            if role is not None:
                kwargs["role"] = role
            if size is not None:
                kwargs["size"] = size
            if storage_service_level is not None:
                kwargs["storage_service_level"] = storage_service_level
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if versioning_state is not None:
                kwargs["versioning_state"] = versioning_state

            if hasattr(S3BucketSvm, "find"):
                resource = S3BucketSvm.find(
                    svm_uuid,
                    **kwargs
                )
            else:
                resource = S3BucketSvm(svm_uuid,)
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ReclineCommandError("Unable to delete S3BucketSvm: %s" % err)


