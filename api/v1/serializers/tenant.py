
from django.db.models.enums import Choices
from runtime import get_app_runtime
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField
from tenant.models import (
    Tenant, TenantAgentRule, TenantAuthFactor, TenantAuthRule, TenantConfig, TenantPasswordComplexity, TenantDesktopConfig,
    TenantPrivacyNotice, TenantContactsConfig, TenantContactsUserFieldConfig,
    TenantUserProfileConfig, TenantLogConfig
)
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from common.serializer import BaseDynamicFieldModelSerializer
from inventory.models import Permission, Group, User
from api.v1.fields.custom import (
    create_enum_field,
    create_foreign_key_field,
    create_upload_url_field,
    create_html_field,
)
from ..pages import group, user


class TenantSerializer(BaseDynamicFieldModelSerializer):

    icon = create_upload_url_field(serializers.URLField)(
        hint=_("请选择图标"), required=False
    )

    class Meta:
        model = Tenant

        fields = (
            'uuid',
            'name',
            'slug',
            'icon',
            'created',
        )

    def create(self, validated_data):
        tenant = Tenant.objects.create(**validated_data)
        user = self.context['request'].user
        if user and user.username != "":
            user.tenants.add(tenant)
        permission = Permission.active_objects.filter(
            codename=tenant.admin_perm_code
        ).first()
        if permission:
            user.user_permissions.add(permission)
        # 创建密码规则
        TenantPasswordComplexity.active_objects.get_or_create(
            is_apply=True,
            tenant=tenant,
            title='6-18位字母、数字、特殊字符组合',
            regular='^(?=.*[A-Za-z])(?=.*\d)(?=.*[~$@$!%*#?&])[A-Za-z\d~$@$!%*#?&]{6,18}$',
        )
        # 通讯录配置功能开关
        TenantContactsConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            config_type=0,
            data={
                "is_open": True
            }
        )
        # 通讯录配置分组可见性
        TenantContactsConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            config_type=1,
            data={
                "visible_type": '所有人可见',
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        # 字段可见性
        TenantContactsUserFieldConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            name="用户名",
            data={
                "visible_type": "所有人可见",
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        TenantContactsUserFieldConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            name="姓名",
            data={
                "visible_type": "所有人可见",
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        TenantContactsUserFieldConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            name="电话",
            data={
                "visible_type": "所有人可见",
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        TenantContactsUserFieldConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            name="邮箱",
            data={
                "visible_type": "所有人可见",
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        TenantContactsUserFieldConfig.objects.get_or_create(
            is_del=False,
            tenant=tenant,
            name="职位",
            data={
                "visible_type": "所有人可见",
                "visible_scope": [],
                "assign_group": [],
                "assign_user": []
            }
        )
        return tenant


class TenantExtendSerializer(BaseDynamicFieldModelSerializer):
    class Meta:
        model = Tenant

        fields = (
            'uuid',
            'name',
            'slug',
            'icon',
            'created',
            'password_complexity',
        )


class MobileLoginRequestSerializer(serializers.Serializer):

    mobile = serializers.CharField(label=_('手机号'))
    code = serializers.CharField(label=_('验证码'))


class MobileLoginResponseSerializer(serializers.Serializer):

    token = serializers.CharField(label=_('token'))
    has_tenant_admin_perm = serializers.ListField(
        child=serializers.CharField(), label=_('权限列表')
    )


class MobileRegisterRequestSerializer(serializers.Serializer):

    mobile = serializers.CharField(label=_('手机号'))
    code = serializers.CharField(label=_('验证码'))
    password = serializers.CharField(label=_('密码'))


class MobileRegisterResponseSerializer(serializers.Serializer):

    token = serializers.CharField(label=_('token'))


class UserNameRegisterRequestSerializer(serializers.Serializer):

    username = serializers.CharField(label=_('用户名'))
    password = serializers.CharField(label=_('密码'))


class UserNameLoginRequestSerializer(serializers.Serializer):

    username = serializers.CharField(label=_('用户名'))
    password = serializers.CharField(label=_('密码'))
    code = serializers.CharField(label=_('图片验证码'), required=False)
    code_filename = serializers.CharField(
        label=_('图片验证码的文件名称'), required=False)


class UserNameRegisterResponseSerializer(serializers.Serializer):

    token = serializers.CharField(label=_('token'))


class UserNameLoginResponseSerializer(serializers.Serializer):

    token = serializers.CharField(label=_('token'))
    has_tenant_admin_perm = serializers.ListField(
        child=serializers.CharField(), label=_('权限列表')
    )


class ConfigSerializer(serializers.Serializer):
    is_open_authcode = serializers.BooleanField(label=_('是否打开验证码'))
    error_number_open_authcode = serializers.IntegerField(
        label=_('错误几次提示输入验证码'))
    is_open_register_limit = serializers.BooleanField(label=_('是否限制注册用户'))
    register_time_limit = serializers.IntegerField(label=_('用户注册时间限制(分钟)'))
    register_count_limit = serializers.IntegerField(label=_('用户注册数量限制'))
    upload_file_format = serializers.ListField(
        child=serializers.CharField(), label=_('允许上传的文件格式')
    )
    close_page_auto_logout = serializers.BooleanField(label=_('是否关闭页面自动退出'))

    native_login_register_field_names = serializers.ListField(
        child=serializers.CharField(), label=_('用于密码登录的基础字段')
    )

    custom_login_register_field_uuids = serializers.ListField(
        child=serializers.CharField(), label=_('用于登录的自定义字段UUID')
    )
    custom_login_register_field_names = serializers.ListField(
        child=serializers.CharField(), label=_('用于登录的自定义字段名称')
    )

    need_complete_profile_after_register = serializers.BooleanField(
        label=_('注册完成后跳转到完善用户资料页面')
    )
    can_skip_complete_profile = serializers.BooleanField(
        label=_('完善用户资料页面允许跳过'))


class TenantConfigSerializer(BaseDynamicFieldModelSerializer):

    data = ConfigSerializer()

    class Meta:
        model = TenantConfig

        fields = ('data',)

    def update(self, instance, validated_data):
        data = validated_data.get('data')
        instance.data = data
        instance.save()
        return instance


class TenantPasswordComplexitySerializer(BaseDynamicFieldModelSerializer):
    regular = serializers.CharField(label=_('正则表达式'))
    is_apply = serializers.BooleanField(label=_('是否应用'))
    title = serializers.CharField(label=_('标题'))

    class Meta:
        model = TenantPasswordComplexity

        fields = (
            'uuid',
            'regular',
            'is_apply',
            'title',
        )

        extra_kwargs = {
            'uuid': {'read_only': True},
        }

    def create(self, validated_data):
        tenant_uuid = (
            self.context['request'].parser_context.get(
                'kwargs').get('tenant_uuid')
        )
        regular = validated_data.get('regular')
        is_apply = validated_data.get('is_apply')
        title = validated_data.get('title')
        tenant = Tenant.objects.filter(uuid=tenant_uuid).first()
        complexity = TenantPasswordComplexity()
        complexity.tenant = tenant
        complexity.regular = regular
        complexity.is_apply = is_apply
        complexity.title = title
        complexity.save()
        if is_apply is True:
            TenantPasswordComplexity.active_objects.filter(tenant=tenant).exclude(
                id=complexity.id
            ).update(is_apply=False)
        return complexity

    def update(self, instance, validated_data):
        tenant_uuid = (
            self.context['request'].parser_context.get(
                'kwargs').get('tenant_uuid')
        )
        tenant = Tenant.objects.filter(uuid=tenant_uuid).first()
        is_apply = validated_data.get('is_apply')
        if is_apply is True:
            TenantPasswordComplexity.active_objects.filter(tenant=tenant).exclude(
                id=instance.id
            ).update(is_apply=False)
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


class FunctionSwitchSerializer(serializers.Serializer):
    is_open = serializers.BooleanField(label=_('是否打开通讯录'))


class TenantContactsConfigFunctionSwitchSerializer(BaseDynamicFieldModelSerializer):
    data = FunctionSwitchSerializer()

    class Meta:
        model = TenantContactsConfig

        fields = (
            'data',
        )


class DesktopConfigSerializer(serializers.Serializer):
    access_with_desktop = serializers.BooleanField(
        label=_("用户是否能看到桌面")
    )

    icon_custom = serializers.BooleanField(
        label=_("用户是否可以自主调整桌面图标的位置")
    )


class TenantDesktopConfigSerializer(BaseDynamicFieldModelSerializer):
    data = DesktopConfigSerializer(
        label=_("设置")
    )

    class Meta:
        model = TenantDesktopConfig

        fields = (
            'data',
        )


class PasswordConfigSerializer(serializers.Serializer):
    regex = serializers.CharField(
        label=_("密码复杂度正则表达式"),
        default="(?=.*\d)(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}"
    )

    expire_time = serializers.IntegerField(
        label=_("密码有效时长(天)"),
        default=30
    )


class TenantPasswordConfigSerializer(BaseDynamicFieldModelSerializer):
    data = PasswordConfigSerializer(
        label=_("密码配置")
    )

    class Meta:
        model = TenantDesktopConfig

        fields = (
            'data',
        )


class UserProfileConfigSerializer(serializers.Serializer):
    logout_by_self = serializers.BooleanField(
        label=_("是否允许用户注销自己的账号")
    )

    access_with_token = serializers.BooleanField(
        label=_("是否允许用户查看自己当前Token")
    )

    expire_token = serializers.BooleanField(
        label=_("是否允许用户手动让Token过期")
    )

    record_with_ipaddress = serializers.BooleanField(
        label=_("是否记录用户的IP地址")
    )

    record_with_device = serializers.BooleanField(
        label=_("是否记录用户的设备信息")
    )


class TenantUserProfileConfigSerializer(BaseDynamicFieldModelSerializer):
    data = UserProfileConfigSerializer(
        label=_("设置")
    )

    class Meta:
        model = TenantUserProfileConfig

        fields = (
            'data',
        )


class TenantAuthRefactorSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        label=_("ID")
    )

    name = serializers.CharField(
        label=_("名称")
    )

    is_open = serializers.BooleanField(
        label=_("是否启用")
    )

    description = serializers.CharField(
        label=_("描述")
    )

    is_support_registe = serializers.BooleanField(
        label=_("是否支持注册")
    )
    is_support_auth = serializers.BooleanField(
        label=_("是否支持认证")
    )


class TenantAngentRuleDataSerializer(serializers.Serializer):

    agents = serializers.ListField(
        label=_("身份源代理"),
        child=serializers.ChoiceField(
            choices=(
                ("微软AD", "LDAP")
            )
        )
    )

    apps = serializers.ListField(
        label=_("应用"),
        child=serializers.ChoiceField(
            choices=(
                ("小红书", "阿里云")
            )
        )
    )


class TenantAgentRuleSerializer(BaseDynamicFieldModelSerializer):

    data = TenantAngentRuleDataSerializer(
        label=_("规则")
    )

    class Meta:
        model = TenantAgentRule
        fields = [
            "id",
            "is_apply",
            "title",
            "data"
        ]


class TenantAgentRuleDetailSerializer(BaseDynamicFieldModelSerializer):

    agents = serializers.SerializerMethodField(label=_("身份源代理"))

    apps = serializers.SerializerMethodField(label=_("应用"))

    def get_agents(self, obj):
        return obj.data.get("agents")

    def get_apps(self, obj):
        return obj.data.get("apps")

    class Meta:
        model = TenantAgentRule
        fields = [
            "title",
            "agents",
            "apps",
            "is_apply",
        ]


class TenantAuthRuleDataConditionSerializer(serializers.Serializer):

    event = serializers.ChoiceField(
        label=_("事件"),
        choices=(
            ("认证失败", "认证成功", "使用新设备", "使用新IP", "使用新地点")
        )
    )

    charge = serializers.ChoiceField(
        label=_("判断"),
        choices=(
            ("大于","等于","小于")
        )
    )

    times = serializers.IntegerField(
        label=_("次数")
    )


class TenantAuthRuleDataSerializer(serializers.Serializer):

    major_auth = serializers.ListField(
        label=_("主要认证因素"),
        child=serializers.ChoiceField(
            choices=(
                ("用户名密码", "短信验证码", "图形验证码", "邮箱验证码", "动态口令", "指纹", "人脸识别")
            )
        )
    )

    condition = TenantAuthRuleDataConditionSerializer(
        label=_("条件")
    )

    second_auth = serializers.ListField(
        label=_("主要认证因素"),
        child=serializers.ChoiceField(
            choices=(
                ("用户名密码", "短信验证码", "图形验证码", "邮箱验证码", "动态口令", "指纹", "人脸识别")
            )
        )
    )

    apps = serializers.ListField(
        label=_("应用"),
        child=serializers.ChoiceField(
            choices=(
                ("小红书", "阿里云", "所有应用")
            )
        )
    )


class TenantAuthRuleSerializer(BaseDynamicFieldModelSerializer):

    data = TenantAuthRuleDataSerializer(
        label=_("规则")
    )

    class Meta:
        model = TenantAuthRule
        fields = [
            "id",
            "is_apply",
            "title",
            "data"
        ]


class TenantAuthRuleDetailSerializer(BaseDynamicFieldModelSerializer):

    apps = serializers.SerializerMethodField(label=_("应用"))

    major_auth = serializers.SerializerMethodField(label=_("主认证因素"))

    condition = serializers.SerializerMethodField(label=_("条件"))
    
    second_auth = serializers.SerializerMethodField(label=_("次认证因素"))

    def get_major_auth(self, obj):
        return obj.data.get("major_auth")

    def get_condition(self, obj):
        return obj.data.get("condition")

    def get_second_auth(self, obj):
        return obj.data.get("second_auth")

    def get_apps(self, obj):
        return obj.data.get("apps")

    class Meta:
        model = TenantAgentRule
        fields = [
            "title",
            "apps",
            "major_auth",
            "condition",
            "second_auth",
            "is_apply",
        ]


def get_authfactor_tyoe_choices():
    from runtime import get_app_runtime
    rs = ((item.name, item.id) for item in get_app_runtime().auth_factors)
    print(rs)
    return tuple(rs)


class TenantAuthRefactorCreateSerializer(BaseDynamicFieldModelSerializer):

    type = ChoiceField(
        label=_("类型"),
        choices=get_authfactor_tyoe_choices()
    )

    class Meta:
        model = TenantAuthFactor
        fields = ["type", "id", "is_open"]
        extra_kwargs = {
            'uuid': {'read_only': True},
        }


class InfoVisibilitySerializer(serializers.Serializer):
    visible_type = serializers.ChoiceField(
        choices=(('所有人可见', '部分人可见')), label=_('可见类型'))
    visible_scope = serializers.MultipleChoiceField(choices=(
        ('本人可见', '管理员可见', '指定分组与人员')), label=_('可见范围'), required=False, default=[])
    assign_group = create_foreign_key_field(serializers.ListField)(
        model_cls=Group,
        field_name='uuid',
        page=group.tag,
        child=serializers.CharField(),
        required=False,
        default=[],
        label=_('指定的分组')
    )

    assign_user = create_foreign_key_field(serializers.ListField)(
        model_cls=User,
        field_name='uuid',
        page=user.tag,
        child=serializers.CharField(),
        required=False,
        default=[],
        label=_('指定的人员')
    )


class TenantContactsConfigInfoVisibilitySerializer(BaseDynamicFieldModelSerializer):

    name = serializers.CharField(read_only=True)
    data = InfoVisibilitySerializer()

    class Meta:
        model = TenantContactsUserFieldConfig

        fields = (
            'uuid',
            'data',
            'name',
        )

    def update(self, instance, validated_data):
        data = validated_data.get('data')
        instance.data = {
            'visible_type': data.get('visible_type'),
            'visible_scope': list(data.get('visible_scope')),
            'assign_group': data.get('assign_group'),
            'assign_user': data.get('assign_user'),
        }
        instance.save()
        return instance


class GroupVisibilitySerializer(serializers.Serializer):
    visible_type = serializers.ChoiceField(
        choices=(('所有人可见', '部分人可见')), label=_('可见类型'))
    visible_scope = serializers.MultipleChoiceField(
        choices=(('组内成员可见', '下属分组可见', '指定分组与人员')), label=_('可见范围'))
    assign_group = create_foreign_key_field(serializers.ListField)(
        model_cls=Group,
        field_name='uuid',
        page=group.tag,
        child=serializers.CharField(),
        required=False,
        default=[],
        label=_('指定的分组')
    )

    assign_user = create_foreign_key_field(serializers.ListField)(
        model_cls=User,
        field_name='uuid',
        page=user.tag,
        child=serializers.CharField(),
        required=False,
        default=[],
        label=_('指定的人员')
    )


class TenantContactsConfigGroupVisibilitySerializer(BaseDynamicFieldModelSerializer):
    data = GroupVisibilitySerializer()

    class Meta:
        model = TenantContactsConfig

        fields = (
            'data',
        )

    def update(self, instance, validated_data):
        data = validated_data.get('data')
        instance.data = {
            'visible_type': data.get('visible_type'),
            'visible_scope': list(data.get('visible_scope')),
            'assign_group': data.get('assign_group'),
            'assign_user': data.get('assign_user'),
        }
        instance.save()
        return instance


class ContactsGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', 'uuid')


class ContactsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'nickname', 'mobile', 'email', 'job_title')


class TenantContactsUserTagsSerializer(serializers.Serializer):

    myself_field = serializers.ListField(
        child=serializers.CharField(), label=_('本人可见字段'), default=[])
    manager_field = serializers.ListField(
        child=serializers.CharField(), label=_('管理员可见字段'), default=[])
    part_field = serializers.ListField(
        child=serializers.CharField(), label=_('部分人可见'), default=[])
    all_user_field = serializers.ListField(
        child=serializers.CharField(), label=_('所有人可见字段'), default=[])


class TenantPrivacyNoticeSerializer(BaseDynamicFieldModelSerializer):
    content = create_html_field(serializers.CharField)(
        hint=_("隐私声明内容"), required=True)

    class Meta:
        model = TenantPrivacyNotice

        fields = ('title', 'content')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.content = validated_data.get('content')
        instance.save()
        return instance


class LogConfigSerializer(serializers.Serializer):
    log_api = serializers.CharField(label=_('日志读取API'), read_only=True)
    log_retention_period = serializers.IntegerField(label=_('日志保留时间(天)'))

    account_ids = serializers.ListField(
        child=serializers.CharField(), label=_('用户账号ID'), default=[])

class TenantLogConfigSerializer(BaseDynamicFieldModelSerializer):

    data = LogConfigSerializer(
        label=_("设置数据")
    )

    class Meta:
        model = TenantLogConfig

        fields = ('data', )

    def update(self, instance, validated_data):
        data = validated_data.get('data')
        instance.data = {
            'log_api': data.get('log_api'),
            'log_retention_period': data.get('log_retention_period'),
        }
        instance.save()
        return instance


class ChildManagerSerializer(serializers.Serializer):

    username = serializers.CharField(read_only=True, label=_('用户名'))
    scope = serializers.ListField(child=serializers.CharField(), read_only=True, label=_('范围'))
    permission = serializers.CharField(read_only=True, label=_('权限'))

    class Meta:

        fields = (
            'username',
            'scope',
            'permission',
        )
