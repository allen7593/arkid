from common.event import Event
import typing
from .celery import app
from app.models import App
from django.db.models import QuerySet
from provisioning.models import Config
from provisioning.constants import ProvisioningStatus
from provisioning.utils import create_user, user_exists
from inventory.models import User, Group
from app.models import App
from webhook.models import WebHook, WebHookTriggerHistory
from common.utils import send_email as send_email_func
import requests


@app.task
def provision_user(tenant_uuid: int, user_id: int):
    apps = App.active_objects.filter(
        tenant__uuid=tenant_uuid,
    )

    for app in apps:
        config: Config = Config.active_objects.filter(
            app=app,
        ).first()

        if config is None or config.status != ProvisioningStatus.Enabled.value:
            continue

        provision_app_user(tenant_uuid, app.id, user_id)


@app.task
def provision_app_user(tenant_uuid: int, app_id: int, user_id: int):
    print(f'task: provision_app_user, tenant: {tenant_uuid}, app: {app_id}, user: {user_id}')
    return

    config: ProvisioningConfig = ProvisioningConfig.objects.filter(
        app__uuid=app_id,
    ).first()

    if config is None or config.status != ProvisioningStatus.Enabled.value:
        return

    # TODO: check the scope of the selected range

    # Sync users
    users: QuerySet = User.objects.filter()

    user: User
    for user in users:
        if not user_exists(config, user):
            create_user(user)

    # Sync groups
    groups: QuerySet = Group.objects.filter()
    group: Group = None
    for group in groups:
        _ = group


@app.task
def notify_webhook(tenant_uuid: int, event: Event):
    webhooks = WebHook.objects.filter(
        tenant__uuid=tenant_uuid,
    )

    webhook: WebHook
    for webhook in webhooks:
        r = requests.post(webhook.url)

@app.task
def send_email(addrs, subject, content):
    '''
    发送邮件
    '''
    send_email_func(addrs, subject, content)
