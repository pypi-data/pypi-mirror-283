# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Tests for DirectButler._query with PostgreSQL.
"""

from __future__ import annotations

import os
import unittest

from lsst.daf.butler import Butler, ButlerConfig, StorageClassFactory
from lsst.daf.butler.datastore import NullDatastore
from lsst.daf.butler.direct_butler import DirectButler
from lsst.daf.butler.registry.sql_registry import SqlRegistry
from lsst.daf.butler.tests.butler_queries import ButlerQueryTests
from lsst.daf.butler.tests.postgresql import setup_postgres_test_db

TESTDIR = os.path.abspath(os.path.dirname(__file__))


class DirectButlerPostgreSQLTests(ButlerQueryTests, unittest.TestCase):
    """Tests for DirectButler._query with PostgreSQL."""

    data_dir = os.path.join(TESTDIR, "data/registry")

    @classmethod
    def setUpClass(cls):
        cls.postgres = cls.enterClassContext(setup_postgres_test_db())

    def make_butler(self, *args: str) -> Butler:
        config = ButlerConfig()
        self.postgres.patch_butler_config(config)
        registry = SqlRegistry.createFromConfig(config)
        for arg in args:
            self.load_data(registry, arg)
        return DirectButler(
            config=config,
            registry=registry,
            datastore=NullDatastore(None, None),
            storageClasses=StorageClassFactory(),
        )


if __name__ == "__main__":
    unittest.main()
