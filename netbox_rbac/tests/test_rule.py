from netbox_rbac import rule

from netbox_rbac.tests.types import *


config = {
    # Grants all rack permissions when the rack is in DC1.
    "dcim_rack_admin_dc1": {
        "groups": ["DC1-Rack-Admins"],
        "perms": ["dcim.*_rack"],
        "rule": 'obj.site.name == "DC1"',
    },
    # Grants all rack change permission when the rack is in DC2.
    "dcim_rack_admin_dc2": {
        "groups": ["DC2-Rack-Users"],
        "perms": ["dcim.change_rack"],
        "rule": 'obj.site.name == "DC2"',
    },
    # Grants all permissions to all sites.
    "dcim_site_admin_all": {"groups": ["DCIM-Site-Admins"], "perms": ["dcim.*_site"]},
    "import_test": {
        "groups": ["DCIM-Site-Admins"],
        "imports": ["os", "os.path"],
        "perms": ["test.*_import"],
        "rule": 'os.path.basename("/foo/bar") == "bar"',
    },
}


class TestRule:
    def test_rule(self):
        roles = set(config.keys())
        rules = rule.Rule(config)

        tests = [
            # Blank rack, granted by dcim_rack_admin_dc1.
            ("dcim.add_rack", True, None),
            # Blank region, no roles grant region permissions.
            ("dcim.add_region", False, None),
            # DC1 rack, all permissions granted.
            ("dcim.add_rack", True, Rack(name="R1", site=Site(name="DC1"))),
            ("dcim.change_rack", True, Rack(name="R1", site=Site(name="DC1"))),
            ("dcim.delete_rack", True, Rack(name="R1", site=Site(name="DC1"))),
            # All site permissions granted.
            ("dcim.add_site", True, None),
            ("dcim.add_site", True, Site(name="DC1")),
            ("dcim.change_site", True, Site(name="DC1")),
            ("dcim.delete_site", True, Site(name="DC1")),
            # DC2 rack, only changes are allowed.
            ("dcim.add_rack", False, Rack(name="R1", site=Site(name="DC2"))),
            ("dcim.change_rack", True, Rack(name="R1", site=Site(name="DC2"))),
            ("dcim.delete_rack", False, Rack(name="R1", site=Site(name="DC2"))),
            # Module import test.
            ("test.test_import", True, Site(name="DC1")),
        ]

        for perm, result, obj in tests:
            assert rules.has_perm(roles, perm, obj) == result
