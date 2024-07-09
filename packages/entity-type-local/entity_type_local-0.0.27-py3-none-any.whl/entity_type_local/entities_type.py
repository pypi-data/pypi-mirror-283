from database_mysql_local.connector import Connector
from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from language_remote.lang_code import LangCode

ENTITY_TYPE_COMPONENT_ID = 116
ENTITY_TYPE_COMPONENT_NAME = 'entity-type-local-python-package'

logger_code_init = {
    'component_id': ENTITY_TYPE_COMPONENT_ID,
    'component_name': ENTITY_TYPE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circ.zone'
}

# TODO Create new class and new method EntitiesTypeEntity.valide_entity_type_entity_id() - Please use this function both in importer-local and entity-moderation-local
class EntitiesType(GenericCRUDML, metaclass=MetaLogger, object=logger_code_init):

    def __init__(self):
        GenericCRUDML.__init__(
            self,
            default_schema_name="entity_type",
            default_table_name="entity_type_table",
            default_column_name= "entity_type_id",
            default_view_table_name="entity_type_view",
            default_ml_view_table_name="entity_type_ml_view")


    def get_entity_type_id_by_title(self, entity_type_title: str) -> int:
        entity_type_id = self.select_one_value_by_column_and_value(
            select_clause_value="entity_type_id",
            column_name="title",
            column_value=entity_type_title, 
            view_table_name="entity_type_ml_view"
            )
        return entity_type_id

    # TODO Can we get the user_id from UserContext
    def insert_entity_type_id_by_title(self, entity_type_title: str, user_id: int) -> int:
        data_dict = {
            "name": entity_type_title
        }
        data_ml_dict = {
            "title": entity_type_title
        }
        entity_type_id, entity_type_ml_id = self.add_value(
            ml_table_name='entity_type_ml_table',
            lang_code=LangCode.ENGLISH, 
            data_dict=data_dict, 
            data_ml_dict=data_ml_dict
        )
        return entity_type_id