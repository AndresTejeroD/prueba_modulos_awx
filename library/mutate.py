#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2025 Ditra Estrategias Digitales S.A. de C.V.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dcmdb_utils import mutate
from ansible.module_utils.exceptions import APIRequestError

# from module_utils.dcmdb_utils import mutate
# from module_utils.exceptions import (
#     APIRequestError,
# )

DOCUMENTATION = r"""
---
module: mutate

short_description: Mutate data in batches from a given URL.

version_added: "1.0.0"

description:
    - This module mutates data in batches from a specified URL using a token for authentication.
    - It supports paginated data mutation and processes data in configurable batch sizes.
    - The module ensures secure handling of authentication tokens and provides detailed error messages in case of failures.

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
        required: true
        type: int

author: "Ditra S.A. de C.V."
"""

EXAMPLES = r"""
- name: Mutate data in batches from a URL
  ditra.cisco.mutate:
    url: "https://api.example.com/data"
    token: "your_token_here"
    operations:
        - item1
        - item2
        - item3
    batch_size: 10

- name: Mutate data without additional payload
  ditra.cisco.mutate:
    url: "https://api.example.com/data"
    token: "your_token_here"
    batch_size: 5
"""

RETURN = r"""
response:
    description: The response data fetched from the URL.
    returned: always
    type: dict
    "data": {
        "created": [
            1,
            2,
            3
        ],
        "updated": [
            1,
            2,
            3
        ]
    }
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
        batch_size=dict(type="int", required=True),
        operations=dict(type="list", required=True),
        token=dict(type="str", required=True, no_log=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    url = module.params["url"]
    token = module.params.get("token")
    operations = module.params.get("operations")
    batch_size = module.params.get("batch_size")

    try:
        result = mutate(url, token, operations, batch_size)
        module.exit_json(changed=True, data=result)
    except Exception as ex:
        module.fail_json(msg=str(ex))


def main():
    run_module()


if __name__ == "__main__":
    main()
