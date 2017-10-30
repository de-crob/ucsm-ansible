:#!/usr/bin/env python

from ansible.module_utils.basic import *

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}



DOCUMENTATION = '''
---
module: cisco_ucs_vnic_ether
short_description: configures vnic ether on a cisco ucs server profile's ls server
version_added: 0.9.0.0
description:
   -  configures vnic ether on a cisco ucs server profile's ls server
options:
    state:
        description:
         - if C(present), will perform create/add/enable operation
         - if C(absent), will perform delete/remove/disable operation
        required: false
        choices: ['present', 'absent']
        default: "present"
    name:
        version_added: "1.0(1e)"
        description: boot policy name
        required: true
    ls_server_dn:
        description: ls_server_dn
        required: true
    adaptor_profile_name:
        version_added: "1.0(1e)"
        description:
        required: false
    addr:
        version_added: "1.0(1e)"
        description:
        required: false
    admin_host_port:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['1', '2', 'ANY', 'NONE']
    admin_vcon:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['1', '2', '3', '4', 'any]
    cdn_prop_in_sync:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['yes', 'no', 'true', 'false']
    cdn_source:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['user-defined', 'vnic-name']
    ident_pool_name:
        version_added: "1.0(1e)"
        description:
        required: false
    mtu:
        version_added: "1.0(1e)"
        description:
        required: false
    nw_ctrl_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    nw_templ_name:
        version_added: "1.0(1e)"
        description:
        required: false
    order:
        version_added: "1.0(1e)"
        description:
        required: false
    pin_to_group_name:
        version_added: "1.0(1e)"
        description:
        required: false
    qos_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    stats_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    switch_id:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['A', 'B', 'A-B', 'B-A', 'NONE']
requirements: ['ucsmsdk', 'ucsm_apis']
author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name:
  vnic_ether_module:
    name: "vnicE-test"
    ls_server_dn: "org-root/ls-spt-test"
    mtu: "9000"
    switch_id: "B"
    state: "present"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''

#Arguments object for the Managed Object in question
def _argument_mo():
    return dict(
                name=dict(required=True, type='str'),
                ls_server_dn=dict(required=True, type='str'),
                adaptor_profile_name=dict(type='str'),
                addr=dict(type='str', default="derived"),
                admin_cdn_name=dict(type='str'),
                admin_host_port=dict(type='str', choices=['1','2','ANY','NONE'], default="ANY"),
                admin_vcon=dict(type='str', choices=['1', '2', '3', '4', 'any'], default="any"),
                cdn_prop_in_sync=dict(type='str', choices=['yes', 'no', 'true', 'false']),
                cdn_source=dict(type='str', choices=['user-defined','vnic-name']),
                ident_pool_name=dict(type='str'),
                mtu=dict(type='str'),
                nw_ctrl_policy_name=dict(type='str'),
                nw_templ_name=dict(type='str'),
                order=dict(type='str'),
                pin_to_group_name=dict(type='str'),
                qos_policy_name=dict(type='str'),
                stats_policy_name=dict(type='str'),
                switch_id=dict(type='str',choices=['A', 'B', 'A-B', 'B-A', 'NONE'])
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


def setup_vnic_ether(server, module):
    from ucsm_apis.server_profile.vnic_ether import vnic_ether_create
    from ucsm_apis.server_profile.vnic_ether import vnic_ether_exists
    from ucsm_apis.server_profile.vnic_ether import vnic_ether_delete

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = vnic_ether_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        vnic_ether_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        vnic_ether_delete(server, mo.name, args_mo['org_dn'])

    return True

#Attempts to run the above method and provides error handling if it fails
def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_vnic_ether(server, module)
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
