# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.
#---------------------------------------------------------------------------

"""
The
``com.vmware.appliance.vcenter.settings.v1.config.components.inventory_client``
module provides classes to manage the vCenter Server Inventory configurations.

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


class InventoryManagement(VapiStruct):
    """
    The ``InventoryManagement`` class contains attributes describing the
    inventory of a vCenter Server.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 folders=None,
                 datacenters=None,
                 clusters=None,
                 storage_pods=None,
                 datastores=None,
                 networks=None,
                 hosts=None,
                ):
        """
        :type  folders: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder_client.Folder` or ``None``
        :param folders: List of Folders.
        :type  datacenters: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter_client.Datacenter` or ``None``
        :param datacenters: List of Datacenters.
        :type  clusters: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster_client.ClusterConfigInfo` or ``None``
        :param clusters: List of ClusterConfigurations.
        :type  storage_pods: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore_client.StoragePod` or ``None``
        :param storage_pods: List of Datastore Clusters.
        :type  datastores: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore_client.Datastore` or ``None``
        :param datastores: List of Datastores.
        :type  networks: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network_client.Network` or ``None``
        :param networks: List of standard networks.
        :type  hosts: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.host_client.HostConfig` or ``None``
        :param hosts: List of Hosts.
        """
        self.folders = folders
        self.datacenters = datacenters
        self.clusters = clusters
        self.storage_pods = storage_pods
        self.datastores = datastores
        self.networks = networks
        self.hosts = hosts
        VapiStruct.__init__(self)


InventoryManagement._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.inventory_management', {
        'folders': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder_client', 'Folder')),
        'datacenters': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter_client', 'Datacenter'))),
        'clusters': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster_client', 'ClusterConfigInfo'))),
        'storage_pods': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore_client', 'StoragePod'))),
        'datastores': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore_client', 'Datastore'))),
        'networks': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network_client', 'Network'))),
        'hosts': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.host_client', 'HostConfig'))),
    },
    InventoryManagement,
    False,
    None))



class Settings(VapiStruct):
    """
    The ``Settings`` class defines vCenter Server settings as key-value pairs.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 settings=None,
                ):
        """
        :type  settings: :class:`dict` of :class:`str` and :class:`str`
        :param settings: 
        """
        self.settings = settings
        VapiStruct.__init__(self)


Settings._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.settings', {
        'settings': type.MapType(type.StringType(), type.StringType()),
    },
    Settings,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
        'cluster': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster_client.StubFactory',
        'common': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.StubFactory',
        'datacenter': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datacenter_client.StubFactory',
        'datastore': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.datastore_client.StubFactory',
        'folder': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.folder_client.StubFactory',
        'host': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.host_client.StubFactory',
        'network': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.network_client.StubFactory',
        'resourcepool': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool_client.StubFactory',
        'vm': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.vm_client.StubFactory',
    }

