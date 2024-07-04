# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.tagging.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.tagging_client`` module provides classes for managing
tags.

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


class Associations(VapiInterface):
    """
    The ``Associations`` class provides methods to list tag associations. This
    class was added in vSphere API 7.0.0.0.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.tagging.associations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AssociationsStub)
        self._VAPI_OPERATION_IDS = {}

    class LastIterationStatus(Enum):
        """
        The last status for the iterator. A field of this type is returned as part
        of the result and indicates to the caller of the API whether it can
        continue to make requests for more data. 
        
        The last status only reports on the state of the iteration at the time data
        was last returned. As a result, it not does guarantee if the next call will
        succeed in getting more data or not. 
        
        Failures to retrieve results will be returned as Error responses. These
        last statuses are only returned when the iterator is operating as
        expected.. This enumeration was added in vSphere API 7.0.0.0.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        READY = None
        """
        Iterator has more data pending and is ready to provide it. The caller can
        request the next page of data at any time. 
        
        The number of results returned may be less than the usual size. In other
        words, the iterator may not fill the page. The iterator has returned at
        least 1 result.. This class attribute was added in vSphere API 7.0.0.0.

        """
        END_OF_DATA = None
        """
        Iterator has finished iterating through its inventory. There are currently
        no more entities to return and the caller can terminate iteration. If the
        iterator returned some data, the marker may be set to allow the iterator to
        continue from where it left off when additional data does become available.
        This value is used to indicate that all available data has been returned by
        the iterator. This class attribute was added in vSphere API 7.0.0.0.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`LastIterationStatus` instance.
            """
            Enum.__init__(string)

    LastIterationStatus._set_values({
        'READY': LastIterationStatus('READY'),
        'END_OF_DATA': LastIterationStatus('END_OF_DATA'),
    })
    LastIterationStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.tagging.associations.last_iteration_status',
        LastIterationStatus))


    class IterationSpec(VapiStruct):
        """
        The ``Associations.IterationSpec`` class contains attributes used to break
        results into pages when listing tags associated to objects see
        :func:`Associations.list`). This class was added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque token that allows the caller to request the
                next page of tag associations. This attribute was added in vSphere
                API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``.
                If None or empty, first page of tag associations will be returned.
            """
            self.marker = marker
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.iteration_spec', {
            'marker': type.OptionalType(type.IdType()),
        },
        IterationSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Associations.Summary`` describes a tag association. This class was
        added in vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tag=None,
                     object=None,
                    ):
            """
            :type  tag: :class:`str`
            :param tag: The identifier of a tag. This attribute was added in vSphere API
                7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.tagging.Tag``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.cis.tagging.Tag``.
            :type  object: :class:`com.vmware.vapi.std_client.DynamicID`
            :param object: The identifier of an associated object. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.tag = tag
            self.object = object
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.summary', {
            'tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag'),
            'object': type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'),
        },
        Summary,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Associations.ListResult`` class contains the list of tag associations
        in a page, as well as related metadata fields. This class was added in
        vSphere API 7.0.0.0.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     associations=None,
                     marker=None,
                     status=None,
                    ):
            """
            :type  associations: :class:`list` of :class:`Associations.Summary`
            :param associations: List of tag associations. This attribute was added in vSphere API
                7.0.0.0.
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of tag associations. This attribute was added
                in vSphere API 7.0.0.0.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``.
                If None or empty, there are no more tag associations to request.
            :type  status: :class:`Associations.LastIterationStatus`
            :param status: The last status for the iterator that indicates whether any more
                results can be expected if the caller continues to make requests
                for more data using the iterator. This attribute was added in
                vSphere API 7.0.0.0.
            """
            self.associations = associations
            self.marker = marker
            self.status = status
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.list_result', {
            'associations': type.ListType(type.ReferenceType(__name__, 'Associations.Summary')),
            'marker': type.OptionalType(type.IdType()),
            'status': type.ReferenceType(__name__, 'Associations.LastIterationStatus'),
        },
        ListResult,
        False,
        None))



    def list(self,
             iterate=None,
             ):
        """
        Returns tag associations that match the specified iteration spec. This
        method was added in vSphere API 7.0.0.0.

        :type  iterate: :class:`Associations.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Associations.ListResult`
        :return: A page of the tag associations matching the iteration spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if :attr:`Associations.IterationSpec.marker` is not a marker
            returned from an earlier invocation of this {\\\\@term operation).
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'iterate': iterate,
                            })
class _AssociationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Associations.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/tagging/associations',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Associations.ListResult'),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.tagging.associations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Associations': Associations,
    }

