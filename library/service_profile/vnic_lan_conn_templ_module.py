#!/usr/bin/env python

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
    obj_dn:
        description: obj_dn
        required: true
    admin_cdn_name:
        version_added: "1.0(1e)"
        description:
        required: false
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
    peer_redundancy_templ_name:
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
                obj_dn=dict(type='str', default="org-root"),
                admin_cdn_name=dict(type='str'),
                cdn_source=dict(type='str', choices=['user-defined','vnic-name']),
                descr=dict(type="str"),
                ident_pool_name=dict(type='str'),
                mtu=dict(type='str'),
                nw_ctrl_policy_name=dict(type='str'),
                peer_redundancy_templ_name=dict(type='str'),
                policy_owner=dict(type="str", choices=['local', 'pending-policy', 'policy']),
                pin_to_group_name=dict(type='str'),
                qos_policy_name=dict(type='str'),
                redundancy_pair_type=dict(type='str', choices=['none', 'primary', 'secondary']),
                stats_policy_name=dict(type='str'),
                switch_id=dict(type='str',choices=['A', 'B', 'A-B', 'B-A', 'NONE'])
                target=dict(type='str'),
                templ_type=dict(type='str', choices=['initial-template', 'updating-template'])
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


def setup_vnic_lan_conn_templ(server, module):
    from ucsm_apis.service_profile.vnic_lan_conn_templ import vnic_lan_conn_templ_create
    from ucsm_apis.service_profile.vnic_lan_conn_templ import vnic_lan_conn_templ_exists
    from ucsm_apis.service_profile.vnic_lan_conn_templ import vnic_lan_conn_templ_delete

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = vnic_lan_conn_templ_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        vnic_lan_conn_templ_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        vnic_lan_conn_templ_delete(server, mo.name, args_mo['org_dn'])

    return True

#Attempts to run the above method and provides error handling if it fails
def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_vnic_lan_conn_templ(server, module)
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
