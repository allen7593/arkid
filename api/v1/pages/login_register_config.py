from openapi.utils import extend_schema_tags

tag = ['login_register_config', 'tenant_register_privacy_notice', 'login_register_config_info']
path = 'login_register_config'
name = '登录注册配置'

login_register_config_tag = 'login_register_config'
login_register_config_name = '登录注册插件配置'

extend_schema_tags(
    login_register_config_tag,
    login_register_config_name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/',
            'method': 'get',
        },
        'global': {
            'create': {
                'tag': 'login_register_config.create'
            }
        },
        'local': {
            'update': {
                'tag': 'login_register_config.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/{id}/',
                'method': 'delete'
            }
        }
    },
)

login_register_config_create_tag = 'login_register_config.create'
login_register_config_create_name = '创建登录注册插件配置信息'

extend_schema_tags(
    login_register_config_create_tag,
    login_register_config_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/',
            'method': 'post',
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/',
                'method': 'post',
            }
        },
    },
)

login_register_config_update_tag = 'login_register_config.update'
login_register_config_update_name = '编辑登录注册插件配置信息'

extend_schema_tags(
    login_register_config_update_tag,
    login_register_config_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/{id}/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/login_register_config/{id}/',
                'method': 'put'
            }
        }
    }
)

tenant_register_privacy_notice_tag = 'tenant_register_privacy_notice'
tenant_register_privacy_notice_name = '租户注册隐私声明'

extend_schema_tags(
    tenant_register_privacy_notice_tag,
    tenant_register_privacy_notice_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
            'method': 'get',
        },
        'global': {
            'update': {
                'tag': 'tenant_register_privacy_notice.update'
            }
        }
    },
)

tenant_register_privacy_notice_update_tag = 'tenant_register_privacy_notice.update'
tenant_register_privacy_notice_update_name = '编辑租户注册隐私声明'

extend_schema_tags(
    tenant_register_privacy_notice_update_tag,
    tenant_register_privacy_notice_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
            'method': 'get',
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/privacy_notice/',
                'method': 'put',
            }
        },
    },
)


login_register_config_info_tag = 'login_register_config_info'
login_register_config_info_name = '登录注册配置'

extend_schema_tags(
    login_register_config_info_tag,
    login_register_config_info_name,
    {
        'type':'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/config/',
            'method': 'get'
        },
        'global': {
            'update': {
                'tag': 'login_register_config_info.update'
            }
        }
    }
)

login_register_config_info_update_tag = 'login_register_config_info.update'
login_register_config_info_update_name = '编辑登录注册配置信息'

extend_schema_tags(
    login_register_config_info_update_tag,
    login_register_config_info_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/config/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/config/',
                'method': 'patch'
            }
        }
    }
)