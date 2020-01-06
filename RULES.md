# Configuration
Rules are described in a YAML configuration file. A user's roles are determined solely by LDAP group membership. A role grants one or more permissions. If a rule is defined, then the requested permission is granted only if the rule evaluates to true.

```
<role>:
  base:
    - <role>
  context:
    <variable>: <value>
  groups:
    - <group>
  perms:
    - <perm>
  rule:
    obj.attribute == variable
```

# Role
A *role* is a string representing a set of permissions which may be granted. A role will inherit any other role listed as a *base*.

A few special roles are defined.

| Name       | Description                     |
| ---------- | ------------------------------- |
| _is_active | Marks the user as active.       |
| _is_denied | Marks the user as inactive.     |
| _is_staff  | Marks the user as staff.        |
| _is_super  | Marks the user as a superuser.  |

# Rule
A role may define a Python statement to be evaluated against the object, called a *rule*.

The execution environment is minimal, containing only the object being evaluated as `obj`, the variables defined in `context`, and a small number of macros.

# Macros
*Macros* simplify writing rules, which typically follow a small number of patterns.

Macros match values against an attribute using [fnmatch](https://facelessuser.github.io/wcmatch/fnmatch/), which supports pattern matching.

## match
Usage: <code>match(*attribute*, *values*)</code>

Returns `True` if the attribute is not `None`, and matches one of the values.

## match_or_none
Usage: <code>match_or_none(*attribute*, *values*)</code>

Returns `True` if the attribute is either `None`, or matches one of the values.

# Permissions
Permissions can be specified using [fnmatch](https://facelessuser.github.io/wcmatch/fnmatch/) patterns.

All known permissions:

+ circuits.add_circuit
+ circuits.add_circuittermination
+ circuits.add_circuittype
+ circuits.add_provider
+ circuits.change_circuit
+ circuits.change_circuittermination
+ circuits.change_circuittype
+ circuits.change_provider
+ circuits.delete_circuit
+ circuits.delete_circuittermination
+ circuits.delete_circuittype
+ circuits.delete_provider
+ dcim.add_cable
+ dcim.add_consoleport
+ dcim.add_consoleporttemplate
+ dcim.add_consoleserverport
+ dcim.add_consoleserverporttemplate
+ dcim.add_device
+ dcim.add_devicebay
+ dcim.add_devicebaytemplate
+ dcim.add_devicerole
+ dcim.add_devicetype
+ dcim.add_frontport
+ dcim.add_frontporttemplate
+ dcim.add_interface
+ dcim.add_interfacetemplate
+ dcim.add_inventoryitem
+ dcim.add_manufacturer
+ dcim.add_platform
+ dcim.add_poweroutlet
+ dcim.add_poweroutlettemplate
+ dcim.add_powerport
+ dcim.add_powerporttemplate
+ dcim.add_rack
+ dcim.add_rackgroup
+ dcim.add_rackreservation
+ dcim.add_rackrole
+ dcim.add_rearport
+ dcim.add_rearporttemplate
+ dcim.add_region
+ dcim.add_site
+ dcim.add_virtualchassis
+ dcim.change_cable
+ dcim.change_consoleport
+ dcim.change_consoleserverport
+ dcim.change_device
+ dcim.change_devicebay
+ dcim.change_devicerole
+ dcim.change_devicetype
+ dcim.change_frontport
+ dcim.change_interface
+ dcim.change_interfacetemplate
+ dcim.change_inventoryitem
+ dcim.change_manufacturer
+ dcim.change_platform
+ dcim.change_poweroutlet
+ dcim.change_powerport
+ dcim.change_rack
+ dcim.change_rackgroup
+ dcim.change_rackreservation
+ dcim.change_rackrole
+ dcim.change_rearport
+ dcim.change_region
+ dcim.change_site
+ dcim.change_virtualchassis
+ dcim.delete_cable
+ dcim.delete_consoleport
+ dcim.delete_consoleporttemplate
+ dcim.delete_consoleserverport
+ dcim.delete_consoleserverporttemplate
+ dcim.delete_device
+ dcim.delete_devicebay
+ dcim.delete_devicebaytemplate
+ dcim.delete_devicerole
+ dcim.delete_devicetype
+ dcim.delete_frontport
+ dcim.delete_frontporttemplate
+ dcim.delete_interface
+ dcim.delete_interfacetemplate
+ dcim.delete_inventoryitem
+ dcim.delete_manufacturer
+ dcim.delete_platform
+ dcim.delete_poweroutlet
+ dcim.delete_poweroutlettemplate
+ dcim.delete_powerport
+ dcim.delete_powerporttemplate
+ dcim.delete_rack
+ dcim.delete_rackgroup
+ dcim.delete_rackreservation
+ dcim.delete_rackrole
+ dcim.delete_rearport
+ dcim.delete_rearporttemplate
+ dcim.delete_region
+ dcim.delete_site
+ dcim.delete_virtualchassis
+ dcim.napalm_read
+ extras.add_configcontext
+ extras.add_reportresult
+ extras.change_configcontext
+ extras.change_imageattachment
+ extras.delete_configcontext
+ extras.delete_imageattachment
+ ipam.add_aggregate
+ ipam.add_ipaddress
+ ipam.add_prefix
+ ipam.add_rir
+ ipam.add_role
+ ipam.add_service
+ ipam.add_vlan
+ ipam.add_vlangroup
+ ipam.add_vrf
+ ipam.change_aggregate
+ ipam.change_ipaddress
+ ipam.change_prefix
+ ipam.change_rir
+ ipam.change_role
+ ipam.change_service
+ ipam.change_vlan
+ ipam.change_vlangroup
+ ipam.change_vrf
+ ipam.delete_aggregate
+ ipam.delete_ipaddress
+ ipam.delete_prefix
+ ipam.delete_rir
+ ipam.delete_role
+ ipam.delete_service
+ ipam.delete_vlan
+ ipam.delete_vlangroup
+ ipam.delete_vrf
+ secrets.add_secretrole
+ secrets.change_secret
+ secrets.change_secretrole
+ secrets.delete_secret
+ secrets.delete_secretrole
+ taggit.change_tag
+ taggit.delete_tag
+ tenancy.add_tenant
+ tenancy.add_tenantgroup
+ tenancy.change_tenant
+ tenancy.change_tenantgroup
+ tenancy.delete_tenant
+ tenancy.delete_tenantgroup
+ users.add_token
+ users.change_token
+ users.delete_token
+ virtualization.add_cluster
+ virtualization.add_clustergroup
+ virtualization.add_clustertype
+ virtualization.add_virtualmachine
+ virtualization.change_cluster
+ virtualization.change_clustergroup
+ virtualization.change_clustertype
+ virtualization.change_virtualmachine
+ virtualization.delete_cluster
+ virtualization.delete_clustergroup
+ virtualization.delete_clustertype
+ virtualization.delete_virtualmachine
