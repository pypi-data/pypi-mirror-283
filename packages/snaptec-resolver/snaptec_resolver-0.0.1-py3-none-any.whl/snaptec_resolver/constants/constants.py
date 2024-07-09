import sys
import os
import pathlib

root_lib_path = str(pathlib.Path(__file__).resolve().parent.parent)
# print("aaa", root_lib_path)


# schema
schema_files = [
    "../../appsync/type_schema/notification/order_notification.graphql",
    "../../appsync/type_schema/catalog/product/configurable_product_attribute.graphql",
    "../../appsync/type_schema/catalog/product/configurable_product_list.graphql",
    "../../appsync/type_schema/catalog/product/product_customizable_option.graphql",
    "../../appsync/type_schema/catalog/product/product_salable_quantity.graphql",
    "../../appsync/type_schema/catalog/product/product_calculator.graphql",
    "../../appsync/type_schema/catalog/product/product_information.graphql",
    "../../appsync/type_schema/catalog/product/export_product.graphql",
    "../../appsync/type_schema/system_configuration/general/store_front.graphql",
    "../../appsync/type_schema/system_configuration/general/trans_email.graphql"
]

type_schema_v1_file = "type_schema_v1_file"
query_file = "../../appsync/query_schema/query.graphql"
merge_schema = "../../appsync/schema.graphql"

country_id_path = f"{root_lib_path}/data/country_ids.json"

# print(country_id_path)