# Introduction

# Installation

# Configuration
Add the following to `settings.py`.
```
AUTHENTICATION_BACKENDS = [
    'netbox_rbac.backend.Backend',
]

REST_FRAMEWORK.update({
	'DEFAULT_PERMISSION_CLASSES': (
		'netbox_rbac.api.TokenPermissions',
		'netbox.api.TokenPermissions',
	)
})

INSTALLED_APPS += (
	'netbox_rbac',
)

MIDDLEWARE += (
	'netbox_rbac.middleware.Middleware',
)

TEMPLATES[0]['DIRS'].insert(0, os.path.join(BASE_DIR, 'netbox_rbac', 'templates'))

LOGGING.update({
	'loggers': {
		'netbox_rbac': {
			'handlers': ['console'],
			'level':     'INFO',
		},
	},
})

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

Add the following to `urls.py`.
```
_patterns += [
	path('', include('netbox_rbac.urls') ),
]
```
