from openapi.utils import extend_schema_tags

tag = 'app_permissions'
path = tag
name = '应用权限'

extend_schema_tags(
    tag,
    name
)