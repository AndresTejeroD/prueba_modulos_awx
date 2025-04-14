#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2025 Ditra Estrategias Digitales S.A. de C.V.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dcmdb_utils import delete

DOCUMENTATION = r"""
---
module: delete

short_description: Delete data in batches from a given URL.

version_added: "1.0.0"

description:
    - This module deletes data in batches from a specified URL using a token for authentication.
    - It supports paginated data deletion and processes data in configurable batch sizes.
    - The batch size is optional and defaults to 10 if not specified.
    - The module ensures secure handling of authentication tokens and provides detailed error messages in case of failures.
    - The response includes detailed information about the deleted data, such as package details.

options:
    url:
        description:
            - The URL to send data to.
        required: true
        type: str
    token:
        description:
            - The authentication token to include in the request headers.
        required: true
        type: str
        no_log: true
    operations:
        description:
            - The data payload to send with the request.
        required: true
        type: list
    batch_size:
        description:
            - The batch size to use when processing data.
            - Defaults to 10 if not specified.
        required: false
        type: int

author: "Ditra S.A. de C.V."
"""

EXAMPLES = r"""
- name: Delete data in batches from a URL
    ditra.cisco.delete:
        url: "https://api.example.com/data"
        token: "your_token_here"
        operations:
                - 101
                - 102
                - 103
        batch_size: 10
"""

RETURN = r"""
response:
    description: The response data fetched from the URL.
    returned: always
    type: list
    elements: dict
    "data": [
        - item1,
        - item2,
        - item3,
        ...
    ]
error:
    description: Error details if the module fails.
    returned: on failure
    type: dict
    sample: {
        "error": "Error in mutate",
        "status": 500,
        "message": "Detailed error message"
    }
"""


def run_module():

    module_args = dict(
        url=dict(type="str", required=True),
        operations=dict(type="list", required=True),
        token=dict(type="str", required=True, no_log=True),
        batch_size=dict(type="int", required=False, default=10),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    url = module.params["url"]
    token = module.params.get("token")
    operations = module.params.get("operations")
    batch_size = module.params.get("batch_size")

    try:
        result = delete(url, token, operations, batch_size)
        module.exit_json(changed=True, data=result)
    except Exception as ex:
        module.fail_json(msg=str(ex))


def main():
    run_module()


if __name__ == "__main__":
    main()
