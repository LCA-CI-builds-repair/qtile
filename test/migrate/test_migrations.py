# Copyright (c) 2023, elParagmigration_ids = []
for m in MIGRATIONS:
    tests = []
    for i, test in enumerate(m.TESTS):
        tests.append((m.ID, test))
        migration_ids.append(f"{m.ID}-{i}")

    if not tests:l rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
import pytest

from libqtile.scripts.migrations import MIGRATIONS, load_migrations

migration_tests = []

# We store a list of test IDs so that tests can be filtered during development
# e.g. pytest -k MigrationID
migration_ids = []

load_migrations()

for m in MIGRATIONS:
    tests = []
    for i, test in enumerate(m.TESTS):
        tests.append((m.ID, test))
        migration_ids.append(f"{m.ID}-{i}")

    if not tests:
        tests.append((m.ID, None))
        migration_ids.append(f"{m.ID}-no-tests")

    migration_tests.extend(tests)


@pytest.mark.parametrize("migration_tester", migration_tests, indirect=True, ids=migration_ids)
def test_all_migrations(migration_tester):
    # If the migration is expected to result in a change then it should also provide linting
    if migration_tester.test.needs_lint:
        migration_tester.assert_lint(), "No linting provided"

    # Tests whether the expected output is returned by the migration
    migration_tester.assert_migrate()
