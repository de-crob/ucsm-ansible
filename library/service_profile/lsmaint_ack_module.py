#!/usr/bin/env python

from ansible.module_utils.basic import *

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}



DOCUMENTATION = '''
---
module: cisco_ucs_ls_server_fsmn
short_description: configures ls server on a cisco ucs server profile
version_added: 0.9.0.0
description:
   -  configures ls server on a cisco ucs server profile
options:
    state:
        description:
         - if C(present), will perform create/add/enable operation
         - if C(absent), will perform delete/remove/disable operation
        required: false
        choices: ['present', 'absent']
        default: "present"
    ls_server_dn:
        description: ls_server_dn
        required: true
    admin_state:
        version_added: "1.0(1e)"
        description: 
        required: false
        choices: ['trigger', 'triggered', 'trigger-immediate', 'user-ack', 'user-discard']
    auto_delete:
        version_added: "1.0(1e)"
        description: 
        required: false
        choices: ['yes','no','true','false']
    descr:  
        version_added: "1.0(1e)"
        description: 
        required: false
    policy_owner:   
        version_added: "1.0(1e)"
        description: 
        required: false
        choices: ['local', 'pending-policy', 'policy']
    scheduler:  
        version_added: "1.0(1e)"
        description: 
        required: false
requirements: ['ucsmsdk', 'ucsm_apis']
author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name:
  lsmaint_ack_module:
    ls_server_dn: "org-root/ls-spt-test"
    admin_state: "trigger"
    auto_delete: "no"
    state: "present"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''

#Arguments object for the Managed Object in question
def _argument_mo():
    return dict(
                ls_server_dn=dict(required=True, type='str'),
                admin_state=dict(type='str', choices=['trigger', 'triggered', 'trigger-immediate',
                                 'untriggered','user-ack', 'user-discard']),
                auto_delete=dict(type='str', choices=['yes', 'no', 'true', 'false']),
                descr=dict(type='str'),
                policy_owner=dict(type='str', choices=['local', 'pending-policy', 'policy']),
                scheduler=dict(type='str')
    )

#Arguments object unique to the Ansible Module
def _argument_custom():
    return dict(
        state=dict(default="present",
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


def setup_lsmaint_ack(server, module):
    from ucsm_apis.service_profile.lsmaint_ack import lsmaint_ack_create
    from ucsm_apis.service_profile.lsmaint_ack import lsmaint_ack_exists
    from ucsm_apis.service_profile.lsmaint_ack import lsmaint_ack_delete

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = lsmaint_ack_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        lsmaint_ack_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        lsmaint_ack_fsm_delete(server, mo.name, args_mo['org_dn'])

    return True

#Attempts to run the above method and provides error handling if it fails
def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_ls_server_fsm(server, module)
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
