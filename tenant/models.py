from django.db import models
from common.model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory.models import User


class Tenant(BaseModel):

    name = models.CharField(verbose_name='名字', max_length=128)
    slug = models.SlugField(verbose_name='短链接标识')
    icon = models.URLField(verbose_name='图标', blank=True)

    def __str__(self) -> str:
        return f'Tenant: {self.name}'

    @property
    def admin_perm_code(self):
        return f'tenant_admin_{self.uuid}'

    def has_admin_perm(self, user: 'User'):
        return (
            user.is_superuser
            or user.user_permissions.filter(codename=self.admin_perm_code).count() > 0
        )

    @property
    def password_complexity(self):
        result = {}
        comlexity = TenantPasswordComplexity.active_objects.filter(
            tenant=self, is_apply=True
        ).first()
        if comlexity:
            result['title'] = comlexity.title
            result['regular'] = comlexity.regular
        return result


class TenantConfig(BaseModel):

    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='租户')
    data = models.JSONField(blank=True, default=dict)

    def __str__(self) -> str:
        return f'Tenant: {self.tenant.name}'

    @property
    def tenant_uuid(self):
        return self.tenant.uuid


class TenantPasswordComplexity(BaseModel):

    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='租户')
    regular = models.CharField(verbose_name='正则表达式', max_length=512)
    is_apply = models.BooleanField(default=False, verbose_name='是否启用')
    title = models.CharField(
        verbose_name='标题', max_length=128, default='', null=True, blank=True
    )

    @property
    def tenant_uuid(self):
        return self.tenant.uuid

    def check_pwd(self, pwd):
        import re

        result = re.match(self.regular, pwd)
        if result:
            return True
        else:
            return False


class TenantContactsConfig(BaseModel):

    # 功能开关
    # {
    #     "is_open": true
    # }
    # 分组可见性
    # visible_type 所有人可见 部分人可见
    # visible_scope 组内成员可见 下属分组可见 指定分组与人员
    # {
    #     "visible_type": visible_type,
    #     "visible_scope": [],
    #     "assign_group": [],
    #     "assign_user": []
    # }
    # 每个租户会有2条相关的记录

    TYPE_CHOICES = (
        (0, '功能开关'),
        (1, '分组可见性'),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='租户')
    config_type = models.IntegerField(choices=TYPE_CHOICES, default=0, verbose_name='配置类型')
    data = models.JSONField(blank=True, default=dict)

    @property
    def tenant_uuid(self):
        return self.tenant.uuid


class TenantContactsUserFieldConfig(BaseModel):
    # 分组可见性
    # visible_type 所有人可见 部分人可见
    # visible_scope 本人可见 管理员可见 指定分组与人员
    # {
    #     "visible_type": visible_type,
    #     "visible_scope": [],
    #     "assign_group": [],
    #     "assign_user": []
    # }
    # 每个租户会有1条相关的记录

    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='租户')
    name = models.CharField(verbose_name='字段名称', max_length=128, default='', null=True, blank=True)
    data = models.JSONField(blank=True, default=dict)

    @property
    def tenant_uuid(self):
        return self.tenant.uuid


class TenantPrivacyNotice(BaseModel):

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        verbose_name='租户',
        related_name='privacy_notice',
    )
    title = models.CharField(
        verbose_name='标题', max_length=128, blank=True, null=True, default=''
    )
    content = models.TextField(verbose_name='内容', blank=True, null=True, default='')

    def __str__(self) -> str:
        return f'Privacy Notice: {self.title}'


class TenantDevice(BaseModel):

    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='租户')
    device_type = models.CharField(verbose_name='设备类型', max_length=128, default='', null=True, blank=True)
    system_version = models.CharField(verbose_name='操作系统及版本', max_length=216, default='', null=True, blank=True)
    browser_version = models.CharField(verbose_name='浏览器及版本', max_length=216, default='', null=True, blank=True)
    ip = models.CharField(verbose_name='IP地址', max_length=216, default='', null=True, blank=True)
    mac_address = models.CharField(verbose_name='mac地址', max_length=216, default='', null=True, blank=True)
    device_number = models.CharField(verbose_name='设备号', max_length=216, default='', null=True, blank=True)
    device_id = models.CharField(verbose_name='设备编号', max_length=216, default='', null=True, blank=True)
    account_ids = models.JSONField(verbose_name='用户账号ID', blank=True, default=dict)

    @property
    def tenant_uuid(self):
        return self.tenant.uuid

