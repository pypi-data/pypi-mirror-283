from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .LabelConstants import LABEL_LOCATION_CODE_LOGGER_OBJECT


class LabelsLocationLocal(GenericCRUD, metaclass=MetaLogger, object=LABEL_LOCATION_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="label_location",
                         default_table_name="label_location_table",
                         default_view_table_name='label_location_view',
                         is_test_data=is_test_data)

    def add_label_location(self, *, label_id: int, location_id: int) -> int:
        label_data = {
            "label_id": label_id,
            "location_id": location_id
        }
        label_location_id = self.insert(data_dict=label_data)
        return label_location_id
