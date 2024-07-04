# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory
.network`` module provides classes to manage the network config.

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


class Network(VapiStruct):
    """
    The Network class contains spec to define standard network in vCenter
    Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 permissions=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Identifier of the network.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network``.
        :type  parent_path: :class:`str`
        :param parent_path: Absolute path of the inventory object's parent.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the network.
            If None, then no permissions defined on this inventory object.
        """
        self.name = name
        self.parent_path = parent_path
        self.permissions = permissions
        VapiStruct.__init__(self)


Network._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network.network', {
        'name': type.IdType(resource_types='com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network'),
        'parent_path': type.StringType(),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
    },
    Network,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

