###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from unittest import TestCase

from everysk.api.api_resources import Workspace

###############################################################################
#   Workspace TestCase Implementation
###############################################################################
class APIWorkspaceTestCase(TestCase):

    def test_workspace_class_name(self):
        self.assertEqual(Workspace.class_name(), 'workspace')
