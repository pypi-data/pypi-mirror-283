# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.
#---------------------------------------------------------------------------

"""
The
``com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster_client``
module provides classes to manage the vCenter Server Inventory cluster
configurations

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


class ClusterConfigInfo(VapiStruct):
    """
    The ``ClusterConfigInfo`` class contains attributes describing the complete
    configuration of a cluster. It contains cluster-wide configurations of DRS,
    HA VSAN Cluster etc.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 ha=None,
                 ha_vm_overrides=None,
                 drs=None,
                 drs_vm_overrides=None,
                 rules=None,
                 groups=None,
                 proactive_ha=None,
                 hosts=None,
                 permissions=None,
                 resource_pools=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Name of the cluster
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: Absolute path from root folder to cluster's parent.
            If None, then inventory object placed in root folder.
        :type  ha: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client.VsphereHA` or ``None``
        :param ha: List of vsphere HA configurations for clusters.
            If None, then HA configurations are not set.
        :type  ha_vm_overrides: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client.HaVmOverrides` or ``None``
        :param ha_vm_overrides: Settings for HA vm overrides.
        :type  drs: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.DrsConfig` or ``None``
        :param drs: Cluster-wide configuration of the vSphere DRS service.
        :type  drs_vm_overrides: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.DrsVmOverrides` or ``None``
        :param drs_vm_overrides: List of virtual machine configurations for the vSphere DRS service.
            Each entry applies to one virtual machine. If a virtual machine is
            not specified in this list, the service uses the default settings
            for that virtual machine.
            If None or empty, the value is skipped.
        :type  rules: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.Rule` or ``None``
        :param rules: Cluster-wide rules.
            If None or empty, the value is skipped.
        :type  groups: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.Group` or ``None``
        :param groups: Cluster-wide groups.
            If None or empty, the value is skipped.
        :type  proactive_ha: :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.ProactiveHAConfig` or ``None``
        :param proactive_ha: Cluster-wide configuration of the vSphere InfraUpdateHA service.
            If None or empty, the value is skipped.
        :type  hosts: :class:`list` of :class:`str` or ``None``
        :param hosts: Host configuration on the datacenter.
            If None, then no hosts present in the datacenter.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permissions defined on the cluster.
            If None, then no permissions defined on this inventory object.
        :type  resource_pools: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool_client.ResourcePool` or ``None``
        :param resource_pools: List of Resource pools.
        """
        self.name = name
        self.parent_path = parent_path
        self.ha = ha
        self.ha_vm_overrides = ha_vm_overrides
        self.drs = drs
        self.drs_vm_overrides = drs_vm_overrides
        self.rules = rules
        self.groups = groups
        self.proactive_ha = proactive_ha
        self.hosts = hosts
        self.permissions = permissions
        self.resource_pools = resource_pools
        VapiStruct.__init__(self)


ClusterConfigInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.cluster_config_info', {
        'name': type.OptionalType(type.StringType()),
        'parent_path': type.OptionalType(type.StringType()),
        'ha': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client', 'VsphereHA')),
        'ha_vm_overrides': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client', 'HaVmOverrides'))),
        'drs': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client', 'DrsConfig')),
        'drs_vm_overrides': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client', 'DrsVmOverrides'))),
        'rules': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client', 'Rule')),
        'groups': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client', 'Group')),
        'proactive_ha': type.OptionalType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client', 'ProactiveHAConfig')),
        'hosts': type.OptionalType(type.ListType(type.StringType())),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
        'resource_pools': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool_client', 'ResourcePool'))),
    },
    ClusterConfigInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
        'drs': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.drs_client.StubFactory',
        'ha': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.ha_client.StubFactory',
        'vsan': 'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.vsan_client.StubFactory',
    }

