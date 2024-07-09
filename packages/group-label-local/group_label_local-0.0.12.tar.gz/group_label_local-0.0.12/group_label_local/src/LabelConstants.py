from logger_local.LoggerComponentEnum import LoggerComponentEnum

DEVELOPER_EMAIL = 'akiva.s@circ.zone'
GROUP_LABEL_PACKAGE_COMPONENT_NAME = 'group_label_package'
GROUP_LABEL_PACKAGE_COMPONENT_ID = 254
GROUP_LABEL_COMPONENT_NAME = 'Label local Python package'
GROUP_LABEL_CODE_LOGGER_OBJECT = {
    'component_id': GROUP_LABEL_PACKAGE_COMPONENT_ID,
    'component_name': GROUP_LABEL_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
GROUP_LABEL_TEST_LOGGER_OBJECT = {
    'component_id': GROUP_LABEL_PACKAGE_COMPONENT_ID,
    'component_name': GROUP_LABEL_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'developer_email': DEVELOPER_EMAIL
}
GROUP_OUTBOX_LABEL_ID = 18
