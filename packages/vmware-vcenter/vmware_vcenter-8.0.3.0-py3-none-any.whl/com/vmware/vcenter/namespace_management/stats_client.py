# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.stats.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.stats_client`` module provides
classes for gathering statistics related to various Namespaces related
components.

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


class TimeSeries(VapiInterface):
    """
    The ``TimeSeries`` class provides methods to gather statistical values for
    clusters, namespaces and pods.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.stats.time_series'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TimeSeriesStub)
        self._VAPI_OPERATION_IDS = {}

    class TimeSeries(VapiStruct):
        """
        A set of timestamps and statistical values representing a time series. The
        lengths of :attr:`TimeSeries.TimeSeries.time_stamps` and
        :attr:`TimeSeries.TimeSeries.values` will always match each other.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     counter=None,
                     time_stamps=None,
                     values=None,
                    ):
            """
            :type  counter: :class:`str`
            :param counter: Counter identifier.
            :type  time_stamps: :class:`list` of :class:`long`
            :param time_stamps: Sequence of UNIX timestamp values at which statistical values were
                sampled. https://en.wikipedia.org/wiki/Unix_time
            :type  values: :class:`list` of :class:`long`
            :param values: Sequence of sampled values corresponding to the timestamps in tss.
            """
            self.counter = counter
            self.time_stamps = time_stamps
            self.values = values
            VapiStruct.__init__(self)


    TimeSeries._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.stats.time_series.time_series', {
            'counter': type.StringType(),
            'time_stamps': type.ListType(type.IntegerType()),
            'values': type.ListType(type.IntegerType()),
        },
        TimeSeries,
        False,
        None))


    class PodIdentifier(VapiStruct):
        """
        Pod identifier. These are the fields required to uniquely identify a pod.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     namespace=None,
                     pod_name=None,
                    ):
            """
            :type  namespace: :class:`str`
            :param namespace: The namespace that the pod is running in.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespaces.Instance``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.namespaces.Instance``.
            :type  pod_name: :class:`str`
            :param pod_name: The name of the pod itself.
            """
            self.namespace = namespace
            self.pod_name = pod_name
            VapiStruct.__init__(self)


    PodIdentifier._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.stats.time_series.pod_identifier', {
            'namespace': type.IdType(resource_types='com.vmware.vcenter.namespaces.Instance'),
            'pod_name': type.StringType(),
        },
        PodIdentifier,
        False,
        None))


    class Spec(VapiStruct):
        """
        This structure is sent in a request for TimeSeries data and is used to
        specify what object stats should be returned for.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'obj_type',
                {
                    'POD' : [('pod', True)],
                    'NAMESPACE' : [('namespace', True)],
                    'CLUSTER' : [('cluster', True)],
                }
            ),
        ]



        def __init__(self,
                     obj_type=None,
                     pod=None,
                     namespace=None,
                     cluster=None,
                     start=None,
                     end=None,
                    ):
            """
            :type  obj_type: :class:`TimeSeries.Spec.ObjType`
            :param obj_type: Type of statistics object that the request is operating on.
            :type  pod: :class:`TimeSeries.PodIdentifier`
            :param pod: Pod Identifier for queries on an individual pod.
                This attribute is optional and it is only relevant when the value
                of ``objType`` is :attr:`TimeSeries.Spec.ObjType.POD`.
            :type  namespace: :class:`str`
            :param namespace: Namespace name for queries for a namespace.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespaces.Instance``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.namespaces.Instance``.
                This attribute is optional and it is only relevant when the value
                of ``objType`` is :attr:`TimeSeries.Spec.ObjType.NAMESPACE`.
            :type  cluster: :class:`str`
            :param cluster: Cluster identifier for queries for a cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                This attribute is optional and it is only relevant when the value
                of ``objType`` is :attr:`TimeSeries.Spec.ObjType.CLUSTER`.
            :type  start: :class:`long`
            :param start: UNIX timestamp value indicating when the requested series of
                statistical samples should begin.
                https://en.wikipedia.org/wiki/Unix_time
            :type  end: :class:`long`
            :param end: UNIX timestamp value indicating when the requested series of
                statistical samples should end.
                https://en.wikipedia.org/wiki/Unix_time
            """
            self.obj_type = obj_type
            self.pod = pod
            self.namespace = namespace
            self.cluster = cluster
            self.start = start
            self.end = end
            VapiStruct.__init__(self)


        class ObjType(Enum):
            """
            Type of statistics object that this request is operating on.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            CLUSTER = None
            """
            The CLUSTER object type is used when specifying a vSphere cluster.

            """
            NAMESPACE = None
            """
            The NAMESPACE object type is used to specify a namespace.

            """
            POD = None
            """
            The POD object type is used to specify an individual pod within a
            namespace.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`ObjType` instance.
                """
                Enum.__init__(string)

        ObjType._set_values({
            'CLUSTER': ObjType('CLUSTER'),
            'NAMESPACE': ObjType('NAMESPACE'),
            'POD': ObjType('POD'),
        })
        ObjType._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.stats.time_series.spec.obj_type',
            ObjType))

    Spec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.stats.time_series.spec', {
            'obj_type': type.ReferenceType(__name__, 'TimeSeries.Spec.ObjType'),
            'pod': type.OptionalType(type.ReferenceType(__name__, 'TimeSeries.PodIdentifier')),
            'namespace': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
            'start': type.IntegerType(),
            'end': type.IntegerType(),
        },
        Spec,
        False,
        None))



    def get(self,
            spec,
            ):
        """
        Gather statistical values for a cluster, namespace, or pod.

        :type  spec: :class:`TimeSeries.Spec`
        :param spec: Specification of the statistical values that should be returned.
        :rtype: :class:`list` of :class:`TimeSeries.TimeSeries`
        :return: A list of TimeSeries values for each counter specified in the
            request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the start time in :attr:`TimeSeries.Spec.start` is invalid, or
            the end time in :attr:`TimeSeries.Spec.end` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the specified cluster in :attr:`TimeSeries.Spec.cluster` or the
            namespace in :attr:`TimeSeries.Spec.namespace` or
            :attr:`TimeSeries.Spec.pod` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the specified cluster in :attr:`TimeSeries.Spec.cluster` is not
            enabled for Namespaces.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'spec': spec,
                            })
class _TimeSeriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'TimeSeries.Spec'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/stats/time-series',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'TimeSeries.TimeSeries')),
                'errors': get_error_dict,
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.stats.time_series',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'TimeSeries': TimeSeries,
    }

