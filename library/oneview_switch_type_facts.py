#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2019) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_switch_type_facts
short_description: Retrieve facts about the OneView Switch Types.
description:
    - Retrieve facts about the Switch Types from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 5.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the Switch Type.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Switch Types
  oneview_switch_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800

- debug: var=switch_types

- name: Gather paginated, filtered and sorted facts about Switch Types
  oneview_switch_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "partNumber='N5K-C56XX'"

- debug: var=switch_types

- name: Gather facts about a Switch Type by name
  oneview_switch_type_facts:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    name: "Name of the Switch Type"

- debug: var=switch_types
'''

RETURN = '''
switch_types:
    description: Has all the OneView facts about the Switch Types.
    returned: Always, but can be null.
    type: dict
'''

from ansible.module_utils.oneview import OneViewModule


class SwitchTypeFactsModule(OneViewModule):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(SwitchTypeFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.switch_types

    def execute_module(self):
        if self.module.params['name']:
            switch_types = self.resource_client.get_by('name', self.module.params['name'])
        else:
            switch_types = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(switch_types=switch_types))


def main():
    SwitchTypeFactsModule().run()


if __name__ == '__main__':
    main()
