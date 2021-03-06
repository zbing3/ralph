# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph.util.demo import DemoData, register
from ralph.cmdb.models_ci import CIType

from ralph.cmdb.tests.utils import (
    CIRelationFactory,
    DeviceEnvironmentFactory,
    ServiceCatalogFactory,
)
from ralph.cmdb.models import CI_RELATION_TYPES


@register
class DemoDeviceEnvironment(DemoData):
    name = 'envs'
    title = 'Environments'

    def generate_data(self, data):
        # CITypes loaded from fixtures
        ci_type = CIType.objects.get(id=11)
        envs = [('prod', 'Prod'), ('test', 'Test'), ('dev', 'Dev')]
        return {
            slug: DeviceEnvironmentFactory(name=name, type=ci_type)
            for slug, name in envs
        }


@register
class DemoServices(DemoData):
    name = 'services'
    title = 'Services'

    def generate_data(self, data):
        # CITypes loaded from fixtures
        ci_type = CIType.objects.get(id=7)
        return {
            'infrastructure': ServiceCatalogFactory.create(
                type=ci_type,
                name='Infrastructure',
            ),
            'python_developers': ServiceCatalogFactory.create(
                type=ci_type,
                name='Python developers',
            ),
            'java_developers': ServiceCatalogFactory.create(
                type=ci_type,
                name='Java developers',
            ),
        }


@register
class DemoRelations(DemoData):
    name = 'relations'
    title = 'Relations'
    required = ['services', 'envs']

    def generate_data(self, data):
        for service in data['services'].values():
            for env in data['envs'].values():
                CIRelationFactory.create(
                    parent=service,
                    child=env,
                    type=CI_RELATION_TYPES.HASROLE,
                )
