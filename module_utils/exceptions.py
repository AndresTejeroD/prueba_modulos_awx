#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2025 Ditra Estrategias Digitales S.A. de C.V.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class APIRequestError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"API request failed with status {status_code}: {message}")

class MissingPaginationDataError(Exception):
    def __init__(self, message):
        super().__init__(f"Missing pagination data error: {message}")
