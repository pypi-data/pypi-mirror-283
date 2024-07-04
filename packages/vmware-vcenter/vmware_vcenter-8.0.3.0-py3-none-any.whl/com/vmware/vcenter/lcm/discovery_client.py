# Copyright (c) 2023 VMware, Inc. All rights reserved.
# VMware Confidential
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2024 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.discovery.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.lcm.discovery_client`` module provides classes for
discovering products registered with vCenter Server and interoperability
between those products and vCenter Server.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from com.vmware.cis_client import Tasks
from vmware.vapi.stdlib.client.task import Task
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


class Product(VapiStruct):
    """
    The ``Info`` class contains information about a VMware product which is
    present in the customer Environemnt. The following information about the
    products are present: 
    
    * Name
    * Version
    * Deployments
    * Automatically Discovered or Manually Added

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 installed_product=None,
                 name=None,
                 version=None,
                 target_version=None,
                 deployments=None,
                 auto=None,
                ):
        """
        :type  installed_product: :class:`str`
        :param installed_product: Identifies a product and a version uniquely. 
            
            The identifier consists of product internal name and version.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type: ``PRODUCT``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type: ``PRODUCT``.
        :type  name: :class:`str`
        :param name: A public official product name.
        :type  version: :class:`str`
        :param version: Current product version.
        :type  target_version: :class:`str` or ``None``
        :param target_version: Future version of the product after upgrade.
            ``targetVersion`` may not be applicable.
        :type  deployments: :class:`list` of :class:`str` or ``None``
        :param deployments: The list of hostname/IPs of the instances of the VMware products
            deployed in the environment. This field would be empty for manually
            added products.
        :type  auto: :class:`bool`
        :param auto: Indicates if the product is auto-detected by the system or manually
            added. If it is set to true it means it is auto-detected.
        """
        self.installed_product = installed_product
        self.name = name
        self.version = version
        self.target_version = target_version
        self.deployments = deployments
        self.auto = auto
        VapiStruct.__init__(self)


Product._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.discovery.product', {
        'installed_product': type.IdType(resource_types='PRODUCT'),
        'name': type.StringType(),
        'version': type.StringType(),
        'target_version': type.OptionalType(type.StringType()),
        'deployments': type.OptionalType(type.ListType(type.StringType())),
        'auto': type.BooleanType(),
    },
    Product,
    False,
    None))



class InteropReport(VapiInterface):
    """
    The ``InteropReport`` interface provides methods to report the
    interoperability between a vCenter Server release version and the other
    installed VMware products registered in the vCenter Server instance.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.discovery.interop_report'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _InteropReportStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})

    class ReleaseInfo(VapiStruct):
        """
        The ``InteropReport.ReleaseInfo`` class contains a product release
        information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     note=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: The version of the release.
            :type  note: :class:`str` or ``None``
            :param note: A link to the release notes of the release.
                None if the release notes are not available.
            """
            self.version = version
            self.note = note
            VapiStruct.__init__(self)


    ReleaseInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.release_info', {
            'version': type.StringType(),
            'note': type.OptionalType(type.URIType()),
        },
        ReleaseInfo,
        False,
        None))


    class ReportRow(VapiStruct):
        """
        The ``InteropReport.ReportRow`` class contains the interoperability between
        a given product and the target product.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     product=None,
                     compatible=None,
                     compatible_releases=None,
                    ):
            """
            :type  product: :class:`Product`
            :param product: The product to compare to the target product.
            :type  compatible: :class:`bool`
            :param compatible: Defines whether the product is compatible against the target
                product.
            :type  compatible_releases: :class:`list` of :class:`InteropReport.ReleaseInfo`
            :param compatible_releases: A list of compatible releases of the product with the target
                product.
            """
            self.product = product
            self.compatible = compatible
            self.compatible_releases = compatible_releases
            VapiStruct.__init__(self)


    ReportRow._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.report_row', {
            'product': type.ReferenceType(__name__, 'Product'),
            'compatible': type.BooleanType(),
            'compatible_releases': type.ListType(type.ReferenceType(__name__, 'InteropReport.ReleaseInfo')),
        },
        ReportRow,
        False,
        None))


    class ReportSummary(VapiStruct):
        """
        The ``InteropReport.ReportSummary`` class contains a summary of the
        :attr:`InteropReport.Report.products`. It consists of the count of
        compatible and incompatible products to the target product.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     compatible_count=None,
                     incompatible_count=None,
                    ):
            """
            :type  compatible_count: :class:`long`
            :param compatible_count: Number of compatible products.
            :type  incompatible_count: :class:`long`
            :param incompatible_count: Number of incompatible products.
            """
            self.compatible_count = compatible_count
            self.incompatible_count = incompatible_count
            VapiStruct.__init__(self)


    ReportSummary._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.report_summary', {
            'compatible_count': type.IntegerType(),
            'incompatible_count': type.IntegerType(),
        },
        ReportSummary,
        False,
        None))


    class Report(VapiStruct):
        """
        The ``InteropReport.Report`` class contains the interoperability report
        between the target product and the other registered products in the vCenter
        Server instance.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     date_created=None,
                     target_product=None,
                     products=None,
                     issues=None,
                     summary=None,
                    ):
            """
            :type  date_created: :class:`datetime.datetime`
            :param date_created: Time when the report is created.
            :type  target_product: :class:`Product`
            :param target_product: A product against the other products are compared to. Only vCenter
                Server is supported.
            :type  products: :class:`list` of :class:`InteropReport.ReportRow`
            :param products: Interoperability matrix for the supplied target product and the
                other registered products.
            :type  issues: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param issues: Lists of issues encountered during report creation.
                :class:`set` if any issues encountered.
            :type  summary: :class:`InteropReport.ReportSummary`
            :param summary: A summary of the interoperability matrix.
            """
            self.date_created = date_created
            self.target_product = target_product
            self.products = products
            self.issues = issues
            self.summary = summary
            VapiStruct.__init__(self)


    Report._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.report', {
            'date_created': type.DateTimeType(),
            'target_product': type.ReferenceType(__name__, 'Product'),
            'products': type.ListType(type.ReferenceType(__name__, 'InteropReport.ReportRow')),
            'issues': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
            'summary': type.ReferenceType(__name__, 'InteropReport.ReportSummary'),
        },
        Report,
        False,
        None))


    class Result(VapiStruct):
        """
        The ``InteropReport.Result`` class contains the result of interoperability
        report creation operation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     report=None,
                     csv_report=None,
                    ):
            """
            :type  report: :class:`InteropReport.Report`
            :param report: The interoperability report.
            :type  csv_report: :class:`str` or ``None``
            :param csv_report: The identifier of CSV formatted interopability report. 
                
                com.vmware.vcenter.lcm.report.Report#get provides location where
                the CSV report can be downloaded from based on the ``csvReport``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.lcm.report``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vcenter.lcm.report``.
                None in case of ``errors`` reported in
                :attr:`InteropReport.Report.issues`.
            """
            self.report = report
            self.csv_report = csv_report
            VapiStruct.__init__(self)


    Result._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.result', {
            'report': type.ReferenceType(__name__, 'InteropReport.Report'),
            'csv_report': type.OptionalType(type.IdType()),
        },
        Result,
        False,
        None))


    class Spec(VapiStruct):
        """
        Configuration of report generation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     target_version=None,
                    ):
            """
            :type  target_version: :class:`str`
            :param target_version: The vCenter Server version. 
                
                It is used for checking against the other products registered with
                that instance of vCenter Server.
            """
            self.target_version = target_version
            VapiStruct.__init__(self)


    Spec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.interop_report.spec', {
            'target_version': type.StringType(),
        },
        Spec,
        False,
        None))




    def create_task(self,
               spec=None,
               ):
        """
        Creates interoperability report between a vCenter Server release
        version and all registered products with the vCenter Server instance. 
        
        The result of this operation can be queried by calling the
        com.vmware.cis.Tasks#get method where ``task`` is the response of this
        operation.

        :type  spec: :class:`InteropReport.Spec` or ``None``
        :param spec: 
            Specifies the target version against this interoperability check
            report will be generated. If None the report will be generated for
            the currently installed version of the vCenter server.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        """
        task_id = self._invoke('create$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'InteropReport.Result'))
        return task_instance
class ProductCatalog(VapiInterface):
    """
    The ``ProductCatalog`` class provides information which VMware products can
    be associated with vCenter Server.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.discovery.product_catalog'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProductCatalogStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``ProductCatalog.Summary`` class contains information about each VMware
        product and its corresponding versions that can be associated with vCenter
        Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     versions=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A product name that the customer is aware of.
            :type  versions: :class:`list` of :class:`str`
            :param versions: List of versions the customer can select from.
            """
            self.name = name
            self.versions = versions
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.product_catalog.summary', {
            'name': type.StringType(),
            'versions': type.ListType(type.StringType()),
        },
        Summary,
        False,
        None))



    def list(self):
        """
        Retrieves a list of all VMware products that can be associated with
        vCenter Server.


        :rtype: :class:`list` of :class:`ProductCatalog.Summary`
        :return: List of all the VMware products which can be associated with
            vCenter Server
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('list', None)
class AssociatedProducts(VapiInterface):
    """
    The ``AssociatedProducts`` class provides options to list, add, modify, and
    delete VMware products associated with vCenter Server. Some products can be
    auto-detected by the system while others can be added manually.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.lcm.product"
    """
    The resource type for the products interface.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.discovery.associated_products'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AssociatedProductsStub)
        self._VAPI_OPERATION_IDS = {}

    class CreateSpec(VapiStruct):
        """
        The ``AssociatedProducts.CreateSpec`` class is the specification used for
        the product creation.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     product_name=None,
                     version=None,
                     deployments=None,
                    ):
            """
            :type  product_name: :class:`str`
            :param product_name: The name of the product.
            :type  version: :class:`str`
            :param version: Current product version.
            :type  deployments: :class:`list` of :class:`str` or ``None``
            :param deployments: The list of hostname/IPs of the instances of the VMware products
                deployed in the environment.
            """
            self.product_name = product_name
            self.version = version
            self.deployments = deployments
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.associated_products.create_spec', {
            'product_name': type.StringType(),
            'version': type.StringType(),
            'deployments': type.OptionalType(type.ListType(type.StringType())),
        },
        CreateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``AssociatedProducts.UpdateSpec`` class is the specification for the
        product update.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     deployments=None,
                    ):
            """
            :type  deployments: :class:`list` of :class:`str` or ``None``
            :param deployments: The list of hostname/IPs of the instances of the VMware products
                deployed in the environment.
            """
            self.deployments = deployments
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.discovery.associated_products.update_spec', {
            'deployments': type.OptionalType(type.ListType(type.StringType())),
        },
        UpdateSpec,
        False,
        None))



    def list(self):
        """
        Retrieves a list of all associated VMware product deployments with
        vCenter Server in the environment. The list contains both product
        deployments discovered automatically and deployments registered
        manually through the API.


        :rtype: :class:`list` of :class:`Product`
        :return: List of all the registered products with vCenter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('list', None)

    def create(self,
               spec,
               ):
        """
        Associates a VMware product with vCenter Server manually. The product
        must be taken from the product catalog API.

        :type  spec: :class:`AssociatedProducts.CreateSpec`
        :param spec: Info creation specification.
        :rtype: :class:`str`
        :return: Identifier of the newly-added product.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.product``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if this version is already added
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec argument is not allowed
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def get(self,
            product,
            ):
        """
        Returns the detailed information of a product associated with vCenter
        Server.

        :type  product: :class:`str`
        :param product: An identifier of the product to be modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.product``.
        :rtype: :class:`Product`
        :return: Product details.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no record associated with ``product`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('get',
                            {
                            'product': product,
                            })

    def update(self,
               product,
               spec,
               ):
        """
        Modifies a VMware product associated with vCenter Server which was
        added manually. Automatically discovered VMware products cannot be
        modified.

        :type  product: :class:`str`
        :param product: An id of the product to be modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.product``.
        :type  spec: :class:`AssociatedProducts.UpdateSpec`
        :param spec: 
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the spec argument is not allowed
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no record associated with ``product`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('update',
                            {
                            'product': product,
                            'spec': spec,
                            })

    def delete(self,
               product,
               ):
        """
        Deletes or dissociates a VMware product associated with vCenter Server
        which was added manually. Automatically discovered VMware products
        cannot be deleted or dissociated.

        :type  product: :class:`str`
        :param product: An id of the product to be removed.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.lcm.product``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no record associated with ``product`` in the system
            database.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('delete',
                            {
                            'product': product,
                            })
class _InteropReportStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'InteropReport.Spec')),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/discovery/interop-report',
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
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.discovery.interop_report',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ProductCatalogStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/discovery/product-catalog',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'ProductCatalog.Summary')),
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
            self, iface_name='com.vmware.vcenter.lcm.discovery.product_catalog',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _AssociatedProductsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/discovery/associated-products',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'AssociatedProducts.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/discovery/associated-products',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'product': type.IdType(resource_types='com.vmware.vcenter.lcm.product'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/discovery/associated-products/{product}',
            path_variables={
                'product': 'product',
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
            'product': type.IdType(resource_types='com.vmware.vcenter.lcm.product'),
            'spec': type.ReferenceType(__name__, 'AssociatedProducts.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/lcm/discovery/associated-products/{product}',
            request_body_parameter='spec',
            path_variables={
                'product': 'product',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'product': type.IdType(resource_types='com.vmware.vcenter.lcm.product'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/lcm/discovery/associated-products/{product}',
            path_variables={
                'product': 'product',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Product')),
                'errors': list_error_dict,
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.lcm.product'),
                'errors': create_error_dict,
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Product'),
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
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.discovery.associated_products',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'InteropReport': InteropReport,
        'ProductCatalog': ProductCatalog,
        'AssociatedProducts': AssociatedProducts,
    }

