# Introduction
This package is an opinionated implementation of role based access control for NetBox.

It completely replaces the default authentication backend, using Active Directory for authentication and determining group membership. A user's roles are updated only on login, and are stored in the database.

Once installed, a user may [view their roles](https://netbox/roles/).

# Installation
```
$ pip3 install netbox-rbac
```

# Configuration
Add the following to `urls.py`.

```
_patterns += [
	path('', include('netbox_rbac.urls') ),
]
```

Add the following to `settings.py`. Either the LDAP or MOCK driver can be used, but not both.

```
AUTHENTICATION_BACKENDS = [
    'netbox_rbac.backend.Backend',
]

INSTALLED_APPS += (
	'netbox_rbac',
)

MIDDLEWARE += (
	'netbox_rbac.middleware.Middleware',
)

REST_FRAMEWORK.update({
	'DEFAULT_PERMISSION_CLASSES': (
		'netbox_rbac.api.TokenPermissions',
		'netbox.api.TokenPermissions',
	)
})

LOGGING.update({
	'loggers': {
		'netbox_rbac': {
			'handlers': ['console'],
			'level':     'INFO',
		},
	},
})
```
## LDAP
```
RBAC = {
	'AUTH': {
		'LDAP': {
			'domain': 'COMPANY.COM',
			'server': 'ldap://ldap.company.com:3268',
			'search': {
				'group': {
					'base':   'OU=Groups,DC=company,DC=com',
					'filter': '(&(sAMAccountName=%s)(objectClass=group))',
				},
				'member': {
					'base':   'OU=Accounts,DC=company,DC=com',
					'filter': '(&(sAMAccountName=%s)(memberOf:1.2.840.113556.1.4.1941:=%s))',
				},
				'user': {
					'base':   'OU=Accounts,DC=company,DC=com',
					'filter': '(&(sAMAccountName=%s)(objectClass=user))',
				},
			},
		},
	},
	'RULE': [
		'/opt/netbox-rules/rules.yaml',
		'https://rules.company.com/rules.yaml',
	],
}
```

## Mock
```
RBAC = {
	'AUTH': {
		'MOCK': {
			'users': [{
				'username': 'ebusto',
				'password': 'pw12345',
				'email':    'ebusto@nvidia.com',
				'first_name': 'Eric',
				'last_name':  'Busto',
				'groups': ['Access-NetBox-Read', 'Access-NetBox-Admin-DCIM'],
			}],
		},
	},
	'RULE': [
		'/opt/netbox-rules/rules.yaml',
		'https://rules.company.com/rules.yaml',
	],
}
```

# Database
Generate and apply RBAC model migrations.

```
$ ./manage.py makemigrations netbox_rbac
$ ./manage.py showmigrations
$ ./manage.py migrate
```

# Rules
See the [example](rules.yaml) rules, and [documentation](RULES.md). The rule paths can be local files or URLs, and the backend will try each path in turn until it succeeds.
