# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.content.type.ovf.policy.
#---------------------------------------------------------------------------

"""


"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from vmware.vapi.bindings import type
from vmware.vapi.bindings.converter import TypeConverter
from vmware.vapi.bindings.enum import Enum
from vmware.vapi.bindings.error import VapiError
from vmware.vapi.bindings.struct import VapiStruct
from vmware.vapi.bindings.stub import (
    ApiInterfaceStub, StubFactoryBase, VapiInterface)
from vmware.vapi.bindings.common import raise_core_exception
from vmware.vapi.data.validator import (UnionValidator, HasFieldsOfValidator)
from vmware.vapi.exception import CoreException
from vmware.vapi.lib.constants import TaskType
from vmware.vapi.lib.rest import OperationRestMetadata


class StoragePolicy(VapiStruct):
    """
    Provide information of the membership of a particular storage policy group.
    
    It is valid for disk, virtual machine or virtual machine collection.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 group_id=None,
                ):
        """
        :type  group_id: :class:`str`
        :param group_id: Id reference of the particular storage policy group.
        """
        self.group_id = group_id
        VapiStruct.__init__(self)


StoragePolicy._set_binding_type(type.StructType(
    'com.vmware.content.type.ovf.policy.storage_policy', {
        'group_id': type.StringType(),
    },
    StoragePolicy,
    False,
    None))



class StoragePolicyGroup(VapiStruct):
    """
    Provide information of storage policy for a group of disks, virtual
    machines and/or virtual machine collections.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 name=None,
                 description=None,
                ):
        """
        :type  id: :class:`str`
        :param id: Id of the policy
        :type  name: :class:`str`
        :param name: Name of the policy
        :type  description: :class:`str` or ``None``
        :param description: Description of the policy
            Description is not required.
        """
        self.id = id
        self.name = name
        self.description = description
        VapiStruct.__init__(self)


StoragePolicyGroup._set_binding_type(type.StructType(
    'com.vmware.content.type.ovf.policy.storage_policy_group', {
        'id': type.StringType(),
        'name': type.StringType(),
        'description': type.OptionalType(type.StringType()),
    },
    StoragePolicyGroup,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

