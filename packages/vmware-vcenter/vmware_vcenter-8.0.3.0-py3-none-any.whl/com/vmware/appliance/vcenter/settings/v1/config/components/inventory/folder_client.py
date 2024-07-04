# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory
.folder`` module provides classes to manage the folder config.

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


class Folder(VapiStruct):
    """
    The Folder class contains spec to define folder in vCenter Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 datastore=None,
                 datacenter=None,
                 vm=None,
                 network=None,
                 host=None,
                ):
        """
        :type  datastore: :class:`list` of :class:`FolderDetails` or ``None``
        :param datastore: List of datastore folders.
            If None. then there are no datastore folders.
        :type  datacenter: :class:`list` of :class:`FolderDetails` or ``None``
        :param datacenter: List of datacenter folders.
            If None. then there are no datacenter folders.
        :type  vm: :class:`list` of :class:`FolderDetails` or ``None``
        :param vm: List of vm folders.
            If None. then there are no vm folders.
        :type  network: :class:`list` of :class:`FolderDetails` or ``None``
        :param network: List of network folders.
            If None. then there are no network folders.
        :type  host: :class:`list` of :class:`FolderDetails` or ``None``
        :param host: List of host folders.
            If None. then there are no host folders.
        """
        self.datastore = datastore
        self.datacenter = datacenter
        self.vm = vm
        self.network = network
        self.host = host
        VapiStruct.__init__(self)


Folder._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder.folder', {
        'datastore': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FolderDetails'))),
        'datacenter': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FolderDetails'))),
        'vm': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FolderDetails'))),
        'network': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FolderDetails'))),
        'host': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FolderDetails'))),
    },
    Folder,
    False,
    None))



class FolderDetails(VapiStruct):
    """
    The FolderDetails class contains spec to define folder in vCenter Server.

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
        :param name: Name of the vCenter Server folder.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder``.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: Absolute path of the inventory object's parent.
            If None, then inventory object placed in root folder.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the folder.
            If None, then no permissions defined on this inventory object.
        """
        self.name = name
        self.parent_path = parent_path
        self.permissions = permissions
        VapiStruct.__init__(self)


FolderDetails._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder.folder_details', {
        'name': type.IdType(resource_types='com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder'),
        'parent_path': type.OptionalType(type.StringType()),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
    },
    FolderDetails,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

