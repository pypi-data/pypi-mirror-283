# SPDX-FileCopyrightText: 2024 OpenBit
#
# SPDX-License-Identifier: MIT

"""Boxer exceptions

Custom exceptions used within Boxer
"""


class ProcessError(Exception):
    """When a subprocess (local or remote) fails"""


class RequiredBinaryError(Exception):
    """A builder requires a local binary that is not available"""
