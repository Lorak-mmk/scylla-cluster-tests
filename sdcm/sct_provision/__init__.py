# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2021 ScyllaDB

from sdcm.sct_provision.azure.azure_instance_request_definition_builder import azure_instance_request_builder
from sdcm.sct_provision.instances_request_definition_builder import InstancesRequestBuilder

instances_request_builder = InstancesRequestBuilder()
instances_request_builder.register_builder(backend="azure", builder_function=azure_instance_request_builder)
