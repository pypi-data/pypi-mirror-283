from enum import Enum

from logger_local.LoggerComponentEnum import LoggerComponentEnum

# connector / cursor
ENTITY_TYPE_PYTHON_PACKAGE_COMPONENT_ID = 116
ENTITY_TYPE_PYTHON_PACKAGE_COMPONENT_NAME = 'entity-type-local'
ENTITY_TYPE_DEVELOPER_EMAIL = 'yaniv.a@circ.zone'
LOGGER_ENTITY_TYPE_CODE_OBJECT = {
    'component_id': ENTITY_TYPE_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': ENTITY_TYPE_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': ENTITY_TYPE_DEVELOPER_EMAIL
}
LOGGER_ENTITY_TYPE_TEST_OBJECT = LOGGER_ENTITY_TYPE_CODE_OBJECT.copy()
LOGGER_ENTITY_TYPE_TEST_OBJECT['component_category'] = LoggerComponentEnum.ComponentCategory.Unit_Test.value
