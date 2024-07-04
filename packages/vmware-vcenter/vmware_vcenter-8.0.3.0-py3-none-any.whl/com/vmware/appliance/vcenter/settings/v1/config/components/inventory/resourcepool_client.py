# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.vcenter.settings.v1.config.components
inventory.resourcepool`` module provides classes to manage the
ConfigManagement.

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


class ResourcePool(VapiStruct):
    """
    The ``ResourcePool`` class contains information about resource pools
    present in the cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 parent_path=None,
                 child_resource_pools=None,
                 vm=None,
                 config=None,
                 permissions=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the vCenter Server resource pool.
        :type  parent_path: :class:`str` or ``None``
        :param parent_path: Parent name for the resource pool.
            If None, then inventory object placed in root folder.
        :type  child_resource_pools: :class:`list` of :class:`str` or ``None``
        :param child_resource_pools: Identifiers of the child resource pools contained in this resource
            pool.
            If None or empty, the value is skipped.
        :type  vm: :class:`list` of :class:`str` or ``None``
        :param vm: Identifiers of the virtual machines contained in this resource
            pool.
            If None or empty, the value is skipped.
        :type  config: :class:`ResourcePoolSummary`
        :param config: Summary of the Resource pools.
        :type  permissions: :class:`list` of :class:`com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client.Permission` or ``None``
        :param permissions: Permission on the resourcepool.
            If None, then no permissions defined on this inventory object.
        """
        self.name = name
        self.parent_path = parent_path
        self.child_resource_pools = child_resource_pools
        self.vm = vm
        self.config = config
        self.permissions = permissions
        VapiStruct.__init__(self)


ResourcePool._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.resource_pool', {
        'name': type.StringType(),
        'parent_path': type.OptionalType(type.StringType()),
        'child_resource_pools': type.OptionalType(type.ListType(type.StringType())),
        'vm': type.OptionalType(type.ListType(type.StringType())),
        'config': type.ReferenceType(__name__, 'ResourcePoolSummary'),
        'permissions': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.appliance.vcenter.settings.v1.config.components.inventory.common_client', 'Permission'))),
    },
    ResourcePool,
    False,
    None))



class ResourcePoolSummary(VapiStruct):
    """
    The ``ResourcePoolSummary`` class provides summary of ResourcePool.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cpu_allocation=None,
                 memory_allocation=None,
                ):
        """
        :type  cpu_allocation: :class:`ResourceAllocationInfo`
        :param cpu_allocation: Resource allocation information for CPU.
        :type  memory_allocation: :class:`ResourceAllocationInfo`
        :param memory_allocation: Resource allocation information for memory.
        """
        self.cpu_allocation = cpu_allocation
        self.memory_allocation = memory_allocation
        VapiStruct.__init__(self)


ResourcePoolSummary._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.resource_pool_summary', {
        'cpu_allocation': type.ReferenceType(__name__, 'ResourceAllocationInfo'),
        'memory_allocation': type.ReferenceType(__name__, 'ResourceAllocationInfo'),
    },
    ResourcePoolSummary,
    False,
    None))



class Shares(VapiStruct):
    """
    The ``Shares`` class provides specification of shares. 
    
    Shares are used to determine relative allocation between resource
    consumers. In general, a consumer with more shares gets proportionally more
    of the resource, subject to certain other constraints.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 level=None,
                 shares=None,
                ):
        """
        :type  level: :class:`Shares.Level`
        :param level: The allocation level. It maps to a pre-determined set of numeric
            values for shares. If the shares value does not map to a predefined
            size, then the level is set as CUSTOM.
        :type  shares: :class:`long`
        :param shares: When :attr:`Shares.level` is set to CUSTOM, it is the number of
            shares allocated. Otherwise, this value is ignored. 
            
            There is no unit for this value. It is a relative measure based on
            the settings for other resource pools.
        """
        self.level = level
        self.shares = shares
        VapiStruct.__init__(self)


    class Level(Enum):
        """
        The ``Shares.Level`` class defines the possible values for the allocation
        level.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        LOW = None
        """
        For CPU: Shares = 500 \* number of virtual CPUs.
        For Memory: Shares = 5 \* virtual machine memory size in MB.

        """
        NORMAL = None
        """
        For CPU: Shares = 1000 \* number of virtual CPUs.
        For Memory: Shares = 10 \* virtual machine memory size in MB.

        """
        HIGH = None
        """
        For CPU: Shares = 2000 \* nmumber of virtual CPUs.
        For Memory: Shares = 20 \* virtual machine memory size in MB.

        """
        CUSTOM = None
        """
        If :class:`set`, in case there is resource contention the server uses the
        shares value to determine the resource allocation.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Level` instance.
            """
            Enum.__init__(string)

    Level._set_values({
        'LOW': Level('LOW'),
        'NORMAL': Level('NORMAL'),
        'HIGH': Level('HIGH'),
        'CUSTOM': Level('CUSTOM'),
    })
    Level._set_binding_type(type.EnumType(
        'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.shares.level',
        Level))

Shares._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.shares', {
        'level': type.ReferenceType(__name__, 'Shares.Level'),
        'shares': type.IntegerType(),
    },
    Shares,
    False,
    None))



class ResourceAllocationInfo(VapiStruct):
    """
    The ``ResourceAllocationInfo`` class contains resource allocation
    information of a resource pool.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 reservation=None,
                 expandable_reservation=None,
                 limit=None,
                 shares=None,
                ):
        """
        :type  reservation: :class:`long`
        :param reservation: Amount of resource that is guaranteed available to a resource pool.
            Reserved resources are not wasted if they are not used. If the
            utilization is less than the reservation, the resources can be
            utilized by other running virtual machines. Units are MB fo memory,
            and MHz for CPU.
        :type  expandable_reservation: :class:`bool`
        :param expandable_reservation: In a resource pool with an expandable reservation, the reservation
            can grow beyond the specified value, if the parent resource pool
            has unreserved resources. A non-expandable reservation is called a
            fixed reservation.
        :type  limit: :class:`long`
        :param limit: The utilization of a resource pool will not exceed this limit, even
            if there are available resources. This is typically used to ensure
            a consistent performance of resource pools independent of available
            resources. If set to -1, then there is no fixed limit on resource
            usage (only bounded by available resources and shares). Units are
            MB for memory, and MHz for CPU.
        :type  shares: :class:`Shares`
        :param shares: Shares are used in case of resource contention.
        """
        self.reservation = reservation
        self.expandable_reservation = expandable_reservation
        self.limit = limit
        self.shares = shares
        VapiStruct.__init__(self)


ResourceAllocationInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.resourcepool.resource_allocation_info', {
        'reservation': type.IntegerType(),
        'expandable_reservation': type.BooleanType(),
        'limit': type.IntegerType(),
        'shares': type.ReferenceType(__name__, 'Shares'),
    },
    ResourceAllocationInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

