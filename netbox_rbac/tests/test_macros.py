from netbox_rbac import macros

from netbox_rbac.tests.types import *

r1 = Rack(name="R1", site=None)
r2 = Rack(name="R2", site=Site(name="DC1"))


class TestMacros:
    def test_get(self):
        tests = [
            (r1, "name", "R1"),
            (r1, "none", None),
            (r1, "site", None),
            (r1, "site.name", None),
            (r2, "site.name", "DC1"),
        ]

        for obj, path, value in tests:
            assert macros.get(obj, path) == value

    def test_match(self):
        tests = [
            (r1, "name", "R1", True),
            (r1, "name", "R2", False),
            (r1, "site.name", "DC1", False),
            (r2, "site.name", "DC1", True),
            (r1, "site.name", "DC2", False),
            (r2, "site.name", "DC2", False),
            (r2, "site.name", "DC*", True),
            (r2, "site.name", ["DC1", "DC2"], True),
        ]

        for obj, path, value, result in tests:
            assert macros.match(obj, path, value) == result

    def test_match_or_none(self):
        tests = [
            (r1, "name", "R1", True),
            (r1, "name", "R2", False),
            (r1, "site.name", "DC1", True),
            (r2, "site.name", "DC1", True),
            (r1, "site.name", "DC2", True),
            (r2, "site.name", "DC2", False),
            (r2, "site.name", "DC*", True),
            (r2, "site.name", ["DC1", "DC2"], True),
        ]

        for obj, path, value, result in tests:
            assert macros.match_or_none(obj, path, value) == result
