from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .LabelConstants import GROUP_LABEL_CODE_LOGGER_OBJECT


class GroupLabelsLocal(GenericCRUD, metaclass=MetaLogger, object=GROUP_LABEL_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="group_label",
                         default_table_name="group_label_table",
                         default_view_table_name='group_label_view',
                         is_test_data=is_test_data)

    def add_group_label(self, *, label_id: int, group_id: int) -> int:
        label_data = {
            "label_id": label_id,
            "group_id": group_id
        }
        group_label_id = self.insert(data_dict=label_data)
        return group_label_id
