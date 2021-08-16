from openapi.utils import extend_schema_tags

tag = 'user'
path = tag
name = '用户列表'

extend_schema_tags(
    tag,
    name,
    {
        'type':'table_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/user/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'user.create'
            },
            'export': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/user/user_export/',
                'method': 'get'
            },
            'import': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/user/user_import/',
                'method': 'post'
            }
        },
        'local': {
            'password': {
                'read': {
                    'path': '/api/v1/tenant/{parent_lookup_tenant}/user/{id}/',
                    'method': 'get'
                },
                'write': {
                    'path': '/api/v1/user/reset_password/',
                    'method': 'post'
                }
            },
            'update': {
                'tag': 'user.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/user/{id}/',
                'method': 'delete'
            }
        }
    }
)

user_create_tag = 'user.create'
user_create_name = '创建用户'

extend_schema_tags(
    user_create_tag,
    user_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/user/',
            'method': 'post'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/user/',
                'method': 'post'
            }
        }
    }
)

user_update_tag = 'user.update'
user_update_name = '编辑用户'

extend_schema_tags(
    user_update_tag,
    user_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/user/{id}/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/user/{id}/',
                'method': 'put'
            }
        }
    }
)

user_custom_fields_tag = 'user_custom_fields'
user_custom_fields_name = '用户自定义字段'

extend_schema_tags(
    user_custom_fields_tag,
    user_custom_fields_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/config/custom_field/',
            'method': 'get'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/config/custom_field/',
                'method': 'post'
            }
        },
        'local': {
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/config/custom_field/{id}/',
                'method': 'delete'
            },
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/config/custom_field/{id}/',
                'method': 'put'
            }
        }
    }
)