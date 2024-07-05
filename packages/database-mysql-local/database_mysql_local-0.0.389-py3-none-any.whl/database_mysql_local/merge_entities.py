import datetime
from .generic_crud import GenericCRUD
from .generic_crud_ml import GenericCRUDML

class MergeEntities (GenericCRUD, GenericCRUDML):
    def merge_entities(self, entity_id1: int, entity_id2: int, main_entity_ml_id: int = None):


        # establish which id is being merged/ended and which one it is being merged into
        end_id = entity_id1
        main_id = entity_id2

        # Set the main id
        if main_entity_ml_id is not None:
            super().update_value_by_id(
                table_name="city_table",
                ml_table_name="city_ml_table",
                ml_table_id=main_entity_ml_id,
                is_main=True,
            )

        # look for the former in id of city_ml_table and replace it with the latter

        # Data to update
        old_id = end_id
        new_id = main_id

        super().update_value_by_id(
            table_name="city_table",
            ml_table_name="city_ml_table",
            ml_table_id= old_id,
            data_ml_dict={"city_id": new_id},
        )

        super().update_by_column_and_value(
            table_name="city_table",
            column_name="city_id",
            column_value=old_id,
            data_dict={"end_timestamp": datetime.datetime.now()},
        )













