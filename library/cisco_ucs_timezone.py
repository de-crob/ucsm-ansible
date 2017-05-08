#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_ucs_timezone
short_description: configures timezone on a cisco ucs server
version_added: 0.9.0.0
description:
   -  configures timezone on a cisco ucs server
Input Params:
    timezone:
        description: time zone e.g. "Asia/Kolkata"
        required: True
    policy_owner:
        description: policy owner
        required: False
        choices: ['local', 'pending-policy', 'policy']
        default: "local"
    admin_state:
        description: admin state
        required: False
        choices: ['disabled', 'enabled']
        default: "enabled"
    port:
        description: port
        required: False
        default: "0"
    descr:
        description: timezone description
        required: False

requirements: ['ucsmsdk', 'ucsm_apis']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_ucs_timezone:
    timezone:
    policy_owner:
    admin_state:
    port:
    descr:
    state: "present"
    ucs_ip: "192.168.1.1"
    ucs_username: "admin"
    ucs_password: "password"
'''


def _argument_mo():
    return dict(
                timezone=dict(required=True, type='str'),
                policy_owner=dict(type='str', choices=['local', 'pending-policy', 'policy'], default="local"),
                admin_state=dict(type='str', choices=['disabled', 'enabled'], default="enabled"),
                port=dict(type='str', default="0"),
                descr=dict(type='str'),
    )


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


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    from ansible.module_utils.cisco_ucs import UcsConnection
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
            continue
        args[key] = params.get(key)
    return args


def setup_timezone(server, module):
    from ucsm_apis.admin.timezone import timezone_set
    from ucsm_apis.admin.timezone import timezone_exists

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = timezone_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists
    timezone_set(handle=server, **args_mo)

    return True


def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_timezone(server, module)
    except Exception as e:
        err = True
        result["msg"] = "setup error: %s " % str(e)
        result["changed"] = False

    return result, err


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

