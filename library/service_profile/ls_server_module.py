#!/usr/bin/env python

from ansible.module_utils.basic import *

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}



DOCUMENTATION = '''
---
module: cisco_ucs_ls_server
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
    name:
        version_added: "1.0(1e)"
        description: boot policy name
        required: true
    org_dn:
        description: org dn
        required: false
        default: "org-root"
    agent_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    bios_profile_name:
        version_added: "1.0(1e)"
        description:
        required: false
    boot_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    descr:
        version_added: "1.0(1e)"
        description:
        required: false
    dynamic_con_policy:
        version_added: "1.0(1e)"
        description:
        required: false
    ext_ip_pool_name:
        version_added: "1.0(1e)"
        description:
        required: false
    ext_ip_state:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['none', 'pooled', 'static']
    host_fw_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    ident_pool_name:
        version_added: "1.0(1e)"
        description:
        required: false
    local_disk_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    maint_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    mgmt_access_policy:
        version_added: "1.0(1e)"
        description:
        required: false
    mgmt_fw_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    policy_owner:
        version_added: "1.0(1e)"
        description:
        required: false
        choices: ['local', 'pending-policy', 'policy']
        default: "local"
    power_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    resolve_remote:
        version_added: "1.0(1e)"
        description:
        required: false
        choice: ['yes', 'no']
    scrub_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    sol_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
    src_templ_name:
        version_added: "1.0(1e)"
        description:
        required: false
    stats_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
        default: "default"
    type:
        version_added: "1.0(1e)"
        description: should not be changed to make a service profile template
        required: false
        choices: ['initial-template', 'instance', 'updating-template']
        default: "initial-template"
    usr_lbl:
        version_added: "1.0(1e)"
        description:
        required: false
    uuid:
        version_added: "1.0(1e)"
        description:
        required: false
        default: "derived"
    vcon_profile_name:
        version_added: "1.0(1e)"
        description:
        required: false
    vmedia_policy_name:
        version_added: "1.0(1e)"
        description:
        required: false
requirements: ['ucsmsdk', 'ucsm_apis']
author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name:
  ls_server_module:
    name: "spt-test"
    org_dn: "org-root"
    boot_policy_name: "example_boot"
    policy_owner: "local"
    ident_pool_name: "ident_pool"
    state: "present"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''

#Arguments object for the Managed Object in question
def _argument_mo():
    return dict(
                name=dict(required=True, type='str'),
                org_dn=dict(type='str', default="org-root"),
                agent_policy_name=dict(type='str'),
                bios_profile_name=dict(type='str'),
                boot_policy_name=dict(type='str'),
                descr=dict(type='str'),
                dynamic_con_policy_name=dict(type='str'),
                ext_ip_pool_name=dict(type='str'),
                ext_ip_state=dict(type='str', choices=['none','pooled','static'],default="none"),
                host_fw_policy_name=dict(type='str'),
                ident_pool_name=dict(type='str'),
                kvm_mgmt_policy_name=dict(type='str'),
				local_disk_policy_name=dict(type='str'),
                maint_policy_name=dict(type='str'),
                mgmt_access_policy_name=dict(type='str'),
                mgmt_fw_policy_name=dict(type='str'),
                policy_owner=dict(type='str', choices=['local', 'pending-policy', 'policy'], default="local"),
                power_policy_name=dict(type='str'),
                power_sync_policy=dict(type='str'),
                resolve_remote=dict(type='str', choices=['yes','no'], default="no"),
                scrub_policy_name=dict(type='str'),
                sol_policy_name=dict(type='str'),
                src_templ_name=dict(type='str'),
                stats_policy_name=dict(type='str'),
                type=dict(type='str', choices=['initial-template','instance','updating-template'], default="initial-template"),
                usr_lbl=dict(type='str'),
                uuid=dict(type='str', default="derived"),
                vcon_profile_name=dict(type='str'),
                vmedia_policy_name=dict(type='str')
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


def setup_ls_server(server, module):
    from ucsm_apis.service_profile.ls_server import ls_server_create
    from ucsm_apis.service_profile.ls_server import ls_server_exists
    from ucsm_apis.service_profile.ls_server import ls_server_delete

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = ls_server_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        ls_server_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        ls_server_delete(server, mo.name, args_mo['org_dn'])

    return True

#Attempts to run the above method and provides error handling if it fails
def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_ls_server(server, module)
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
