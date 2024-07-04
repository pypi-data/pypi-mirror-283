# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory
.datastore`` module provides classes to manage the datastore and storagepod
config.

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

class MaintenanceModeState(Enum):
    """
    The ``MaintenanceModeState`` class defines the maintenance mode states of
    the datastore.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    NORMAL = None
    """
    Default state.

    """
    ENTERING_MAINTENANCE = None
    """
    Started entering maintenance mode, but not finished. This could happen when
    waiting for user input or for long-running vmotions to complete.

    """
    IN_MAINTENANCE = None
    """
    Successfully entered maintenance mode.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`MaintenanceModeState` instance.
        """
        Enum.__init__(string)

MaintenanceModeState._set_values({
    'NORMAL': MaintenanceModeState('NORMAL'),
    'ENTERING_MAINTENANCE': MaintenanceModeState('ENTERING_MAINTENANCE'),
    'IN_MAINTENANCE': MaintenanceModeState('IN_MAINTENANCE'),
})
MaintenanceModeState._set_binding_type(type.EnumType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.maintenance_mode_state',
    MaintenanceModeState))




class Datastore(VapiStruct):
    """
    ``Datastore`` class defines the spec for datastore configurations in
    vCenter Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 summary=None,
                 permissions=None,
                ):
        """
        :type  name: :class:`str`
        :param name: The identifier of the datastore.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore``.
        :type  parent_path: :class:`str`
        :param parent_path: Absolute path of the inventory object's parent.
        :type  summary: :class:`Summary` or ``None``
        :param summary: Summary of the datastore.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the datastore.
            If None, then no permissions defined on this inventory object.
        """
        self.name = name
        self.parent_path = parent_path
        self.summary = summary
        self.permissions = permissions
        VapiStruct.__init__(self)


Datastore._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.datastore', {
        'name': type.IdType(resource_types='com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore'),
        'parent_path': type.StringType(),
        'summary': type.OptionalType(type.ReferenceType(__name__, 'Summary')),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
    },
    Datastore,
    False,
    None))



class Summary(VapiStruct):
    """
    ``Summary`` class defines the datastore summary properties.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 capacity=None,
                 multiple_host_access=None,
                 type=None,
                 maintenance_mode=None,
                ):
        """
        :type  capacity: :class:`long` or ``None``
        :param capacity: Maximum capacity of this datastore, in bytes. This value is updated
            periodically by the server. It can be explicitly refreshed with the
            Refresh operation.
        :type  multiple_host_access: :class:`bool` or ``None``
        :param multiple_host_access: More than one host in the datacenter has been configured with
            access to the datastore. This is only provided by VirtualCenter.
            If None, then the datastore not configured with access from more
            than one host.
        :type  type: :class:`str` or ``None``
        :param type: Type of file system volume, such as VMFS or NFS.
        :type  maintenance_mode: :class:`MaintenanceModeState` or ``None``
        :param maintenance_mode: The current maintenance mode state of the datastore.
            If None, then the current maintenance mode state of the datastore
            is set to normal.
        """
        self.capacity = capacity
        self.multiple_host_access = multiple_host_access
        self.type = type
        self.maintenance_mode = maintenance_mode
        VapiStruct.__init__(self)


Summary._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.summary', {
        'capacity': type.OptionalType(type.IntegerType()),
        'multiple_host_access': type.OptionalType(type.BooleanType()),
        'type': type.OptionalType(type.StringType()),
        'maintenance_mode': type.OptionalType(type.ReferenceType(__name__, 'MaintenanceModeState')),
    },
    Summary,
    False,
    None))



class StoragePod(VapiStruct):
    """
    The StoragePod class contains spec to define storage pod in vCenter Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 pod_storage_drs_entry=None,
                 permissions=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Identifier of the Storage Pod.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.storagepod``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.storagepod``.
        :type  parent_path: :class:`str`
        :param parent_path: Absolute path of the inventory object's parent.
        :type  pod_storage_drs_entry: :class:`PodStorageDrsEntry`
        :param pod_storage_drs_entry: Storage DRS related attributes of the Storage Pod.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the Storage Pod.
            If None, then no permissions defined on this inventory object.
        """
        self.name = name
        self.parent_path = parent_path
        self.pod_storage_drs_entry = pod_storage_drs_entry
        self.permissions = permissions
        VapiStruct.__init__(self)


StoragePod._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.storage_pod', {
        'name': type.IdType(resource_types='com.vmware.appliance.vcenter.settings.v1.config.components.inventory.storagepod'),
        'parent_path': type.StringType(),
        'pod_storage_drs_entry': type.ReferenceType(__name__, 'PodStorageDrsEntry'),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
    },
    StoragePod,
    False,
    None))



class PodStorageDrsEntry(VapiStruct):
    """
    The PodStorageDrsEntry class contains spec to define storage DRS related
    attributes of the Storage Pod.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 storage_drs_config=None,
                ):
        """
        :type  storage_drs_config: :class:`StorageDrsConfigInfo`
        :param storage_drs_config: Storage DRS configuration.
        """
        self.storage_drs_config = storage_drs_config
        VapiStruct.__init__(self)


PodStorageDrsEntry._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.pod_storage_drs_entry', {
        'storage_drs_config': type.ReferenceType(__name__, 'StorageDrsConfigInfo'),
    },
    PodStorageDrsEntry,
    False,
    None))



class StorageDrsConfigInfo(VapiStruct):
    """
    The StorageDrsConfigInfo class contains spec to define storage DRS
    configurations.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 pod_config=None,
                ):
        """
        :type  pod_config: :class:`StorageDrsPodConfigInfo`
        :param pod_config: Pod-wide configuration information for the storage DRS service.
        """
        self.pod_config = pod_config
        VapiStruct.__init__(self)


StorageDrsConfigInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.storage_drs_config_info', {
        'pod_config': type.ReferenceType(__name__, 'StorageDrsPodConfigInfo'),
    },
    StorageDrsConfigInfo,
    False,
    None))



class StorageDrsPodConfigInfo(VapiStruct):
    """
    The StorageDrsConfigInfo class contains spec to define pod-wide
    configuration information for the storage DRS service.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool`
        :param enabled: Flag indicating whether or not storage DRS is enabled.
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


StorageDrsPodConfigInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore.storage_drs_pod_config_info', {
        'enabled': type.BooleanType(),
    },
    StorageDrsPodConfigInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

