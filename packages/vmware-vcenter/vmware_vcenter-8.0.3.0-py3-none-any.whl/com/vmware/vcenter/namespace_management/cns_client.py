# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.cns.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.cns_client`` module provides
classes for configuration of Persistent Services capabilities on VC clusters.

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

class MaintenanceActionType(Enum):
    """
    The ``MaintenanceActionType`` class contains actions to be taken when an
    entity enters maintenance mode.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    PermanentRemoval = None
    """
    The entity is getting permanently removed. Move applications, rebuild
    storage on other entities before allowing to proceed.

    """
    EnsureAccessibility = None
    """
    The entity is going down temporarily for maintenance. Still need to ensure
    application availability and storage accessibility at least in a degraded
    level.

    """
    NoAction = None
    """
    Admin override to not delay or stop the entity from entering maintenance
    mode.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`MaintenanceActionType` instance.
        """
        Enum.__init__(string)

MaintenanceActionType._set_values({
    'PermanentRemoval': MaintenanceActionType('PermanentRemoval'),
    'EnsureAccessibility': MaintenanceActionType('EnsureAccessibility'),
    'NoAction': MaintenanceActionType('NoAction'),
})
MaintenanceActionType._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.cns.maintenance_action_type',
    MaintenanceActionType))





class StubFactory(StubFactoryBase):
    _attrs = {
    }

