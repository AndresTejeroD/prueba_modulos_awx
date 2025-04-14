#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2025 Ditra Estrategias Digitales S.A. de C.V.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dcmdb_utils import search
from ansible.module_utils.exceptions import (
    APIRequestError,
    MissingPaginationDataError,
)

DOCUMENTATION = r"""
---
module: search

short_description: Search data from a given URL.

version_added: "1.0.0"

description:
    - This module searches data from a specified URL using a token for authentication.
    - It supports paginated data retrieval and processes data with configurable limits.
    - Provides detailed error messages for API request failures, pagination issues, and unexpected exceptions.
    - Accumulates results across multiple pages into a single array.
    - Utilizes a nested function to handle repeated API calls for pagination.
    - Validates pagination data before processing to ensure robustness.

options:
    url:
        description:
            - The URL to fetch data from.
        required: true
        type: str
    token:
        description:
            - The authentication token to include in the request headers.
        required: true
        type: str
        no_log: true
    search_params:
        description:
            - The parameters to send with the request. These are directly used as the payload for the search operation.
        required: false
        type: dict
    page_limit:
        description:
            - The maximum number of pages to retrieve. If not specified, all pages will be fetched.
        required: false
        type: int

author: "Ditra Estrategias Digitales S.A. de C.V."
"""

EXAMPLES = r"""
- name: Search data from a URL
  ditra.cisco.search:
    url: "https://api.example.com/search"
    token: "your_token_here"
    search_params:
        selects:
            - field: "id"
            - field: "name"
            - field: "code"
        includes:
            - relation: "publisher"
            type: "max"
            field: "id"
        limit: 10
- name: Search data with only URL and token
  ditra.cisco.search:
    url: "https://api.example.com/search"
    token: "your_token_here"
"""

RETURN = r"""
response:
    description: The response data fetched from the URL.
    returned: always
    type: dict
    "data": [
        - item
        - item
        - item
    ]
    
error:
    description: Error details if the module fails.
    returned: on failure
    type: dict
    sample: {
        "error": "Error in search",
        "status": 500,
        "message": "Detailed error message"
    }
"""


def main():

    module_args = dict(
        url=dict(type="str", required=True),
        page_limit=dict(type="int", required=False),
        search_params=dict(type="dict", required=False),
        token=dict(type="str", required=True, no_log=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    url = module.params["url"]
    token = module.params.get("token")
    search_params = module.params.get("search_params")
    page_limit = module.params.get("page_limit")

    try:
        result = search(url, token, search_params, page_limit)
        module.exit_json(changed=True, data=result)
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
