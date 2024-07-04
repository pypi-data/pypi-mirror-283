# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.system.security.
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


class GlobalFips(VapiInterface):
    """
    The ``GlobalFips`` class provides methods to enable/disable appliance FIPS
    mode. This class was added in vSphere API 7.0.1.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.security.global_fips'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _GlobalFipsStub)
        self._VAPI_OPERATION_IDS = {}

    class UpdateSpec(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     enabled=None,
                    ):
            """
            :type  enabled: :class:`bool` or ``None``
            :param enabled: FIPS setting state. This attribute was added in vSphere API
                7.0.1.0.
                If None, the value is unchanged.
            """
            self.enabled = enabled
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.system.security.global_fips.update_spec', {
            'enabled': type.OptionalType(type.BooleanType()),
        },
        UpdateSpec,
        False,
        None))


    class Info(VapiStruct):
        """


        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     enabled=None,
                    ):
            """
            :type  enabled: :class:`bool`
            :param enabled: FIPS setting state. This attribute was added in vSphere API
                7.0.1.0.
            """
            self.enabled = enabled
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.system.security.global_fips.info', {
            'enabled': type.BooleanType(),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Get current appliance FIPS settings. This method was added in vSphere
        API 7.0.1.0.


        :rtype: :class:`GlobalFips.Info`
        :return: Current FIPS settings state.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)

    def update(self,
               spec,
               ):
        """
        Enable/Disable Global FIPS mode for the appliance. 
        
        **Caution:** Changing the value of this setting will reboot the
        Appliance.. This method was added in vSphere API 7.0.1.0.

        :type  spec: :class:`GlobalFips.UpdateSpec`
        :param spec: 
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('update',
                            {
                            'spec': spec,
                            })
class _GlobalFipsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/system/global-fips',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'GlobalFips.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/system/global-fips',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'GlobalFips.Info'),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.security.global_fips',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'GlobalFips': GlobalFips,
    }

