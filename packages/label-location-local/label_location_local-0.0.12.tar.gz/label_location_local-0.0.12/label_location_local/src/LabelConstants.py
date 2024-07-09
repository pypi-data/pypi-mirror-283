from logger_local.LoggerComponentEnum import LoggerComponentEnum

DEVELOPER_EMAIL = 'akiva.s@circ.zone'
LABEL_LOCATION_PACKAGE_COMPONENT_NAME = 'label_location_package'
LABEL_LOCATION_PACKAGE_COMPONENT_ID = 254
LABEL_LOCATION_COMPONENT_NAME = 'Label local Python package'
LABEL_LOCATION_CODE_LOGGER_OBJECT = {
    'component_id': LABEL_LOCATION_PACKAGE_COMPONENT_ID,
    'component_name': LABEL_LOCATION_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
LABEL_LOCATION_TEST_LOGGER_OBJECT = {
    'component_id': LABEL_LOCATION_PACKAGE_COMPONENT_ID,
    'component_name': LABEL_LOCATION_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'developer_email': DEVELOPER_EMAIL
}
LOCATION_OUTBOX_LABEL_ID = 18
