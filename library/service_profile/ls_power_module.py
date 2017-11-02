#!/usr/bin/env python

from ansible.module_utils.basic import *

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}



DOCUMENTATION = '''
---
module: cisco_ucs_ls_requirement
short_description: configures ls requirement on a cisco ucs server profile's ls server
version_added: 0.9.0.0
description:
   -  configures ls requirement on a cisco ucs server profile's ls server
options:
    ansi_state:
        description:
         - if C(present), will perform create/add/enable operation
         - if C(absent), will perform delete/remove/disable operation
        required: false
        choices: ['present', 'absent']
        default: "present"
    ls_server_dn:
        description: ls_server_dn
        required: true
    state:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['admin-down', 'admin-up', 'bmc-reset-immediate', 
                  'bmc-reset-wait', 'cmos-reset-immediate',
                  'cycle-immediate', 'cycle-wait', 'diagonostic-interrupt', 
                  'down', 'hard-reset-immediate', 'hard-reset-wait', 
                  'ipmi-reset', 'kvm-reset', 'soft-shut-down', 
                  'soft-shut-down-only', 'up']
requirements: ['ucsmsdk', 'ucsm_apis']
author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name:
  ls_power_module:
    ls_server_dn: "org-root/ls-spt-test"
    state: 'up'
    ansi_state: "present"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''

#Arguments object for the Managed Object in question
def _argument_mo():
    return dict(
                ls_server_dn=dict(required=True, type='str'),
                state=dict(type='str')
    )

#Arguments object unique to the Ansible Module
def _argument_custom():
    return dict(
        ansi_state=dict(default="present",
                        choices=['present', 'absent'],
                        type='str'),
    )

#Arguments object related to the UcsHandle
def _argument_connection():
    return  dict(
        # UcsHandle
        ucs_server=dict(type='dict'),

        # Ucs server credentials
        ucs_ip=dict(type='str'),
        ucs_username=dict(default="admin", type='str'),
        ucs_password=dict(type='str', no_log=True),
        ucs_port=dict(default=None),
        ucs_secure=dict(default=None),
        ucs_proxy=dict(default=None)
    )


#Creates the AnsibleModule object with the all arguments
def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_connection())
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_custom())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


#Retrieves non-None mo properties
def _get_mo_params(params):
    from ansible.module_utils.cisco_ucs import UcsConnection
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
            continue
        args[key] = params.get(key)
    return args


def setup_ls_power(server, module):
    from ucsm_apis.service_profile.ls_power import ls_power_create
    from ucsm_apis.service_profile.ls_power import ls_power_exists
    from ucsm_apis.service_profile.ls_power import ls_power_delete

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = ls_power_exists(handle=server, **args_mo)

    if ansible["ansi_state"] == "present":
        if module.check_mode or exists:
            return not exists
        ls_power_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        ls_power_delete(server, args_mo['ls_server_dn'])

    return True

#Attempts to run the above method and provides error handling if it fails
def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_ls_power(server, module)
    except Exception as e:
        err = True
        result["msg"] = "setup error: %s " % str(e)
        result["changed"] = False

    return result, err

#Creates the module and makes the connections, only real work is done in setup
def main():
    from ansible.module_utils.cisco_ucs import UcsConnection

    module = _ansible_module_create()
    conn = UcsConnection(module)
    server = conn.login()
    result, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**result)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
