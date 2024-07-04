# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.vsan.
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


class VsanConfigInfo(VapiStruct):
    """
    The :class:`VsanConfigInfo` data object contains configuration data for the
    VSAN service in a cluster. This data object is used both for specifying
    cluster-wide settings when updating the VSAN service, and as an output
    datatype when retrieving current cluster-wide VSAN service settings.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 enabled=None,
                 default_config=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Whether the VSAN service is enabled for the cluster.
        :type  default_config: :class:`HostDefaultInfo` or ``None``
        :param default_config: Default VSAN settings to use for hosts admitted to the cluster when
            the VSAN service is enabled. If omitted, values will default as
            though the fields in the :class:`HostDefaultInfo` have been
            omitted.
        """
        self.enabled = enabled
        self.default_config = default_config
        VapiStruct.__init__(self)


VsanConfigInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.vsan.vsan_config_info', {
        'enabled': type.OptionalType(type.BooleanType()),
        'default_config': type.OptionalType(type.ReferenceType(__name__, 'HostDefaultInfo')),
    },
    VsanConfigInfo,
    False,
    None))



class HostDefaultInfo(VapiStruct):
    """
    Default VSAN service configuration to be used for hosts admitted to the
    cluster.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 checksum_enabled=None,
                ):
        """
        :type  checksum_enabled: :class:`bool` or ``None``
        :param checksum_enabled: Whether the VSAN service is configured to enforce checksum
            protection. If omitted while enabling the VSAN service, this value
            will default to ``false``. Change this value to ``false`` shall not
            affect any existing disk status. Changing this value to ``true``
            shall do disk enforcement check that all VSAN disks are checksum
            enabled.````
        """
        self.checksum_enabled = checksum_enabled
        VapiStruct.__init__(self)


HostDefaultInfo._set_binding_type(type.StructType(
    'com.vmware.appliance.vcenter.settings.v1.config.components.inventory.cluster.vsan.host_default_info', {
        'checksum_enabled': type.OptionalType(type.BooleanType()),
    },
    HostDefaultInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

