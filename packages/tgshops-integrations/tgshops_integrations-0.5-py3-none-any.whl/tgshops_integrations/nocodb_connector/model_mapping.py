import json
import secrets

import markdown

from tgshops_integrations.models.categories import CategoryModel
from tgshops_integrations.models.products import ExtraAttribute, ProductModel
from tgshops_integrations.models.categories import CategoryResponseModel,PaginationResponseModel
from tgshops_integrations.models.products import  ProductModel


def get_pagination_info(page_info: dict) -> PaginationResponseModel:
    page_info = PaginationResponseModel(total_rows=page_info['totalRows'],
                                        page=page_info['page'],
                                        page_size=page_info['pageSize'],
                                        is_first_page=page_info['isFirstPage'],
                                        is_last_page=page_info['isLastPage'])
    return page_info


ID_FIELD = "Id"
NEW_ID_FIELD = "id"
CATEGORY_IMAGE_FIELD = "Изображение"
CATEGORY_NAME_FIELD = "Название"
CATEGORY_PARENT_FIELD = "Назначить родительскую категорию"
CATEGORY_PARENT_ID_FIELD = "ID родительской категории"


def parse_category_data(data: dict) -> CategoryResponseModel:
    preview_url = ""
    if data.get(CATEGORY_IMAGE_FIELD):
        preview_url = data[CATEGORY_IMAGE_FIELD][0].get("url", "")
    return CategoryResponseModel(
        id=str(data[ID_FIELD]),
        name=data.get(CATEGORY_NAME_FIELD, ""),
        parent_category=str(data.get(CATEGORY_PARENT_ID_FIELD, 0)),
        preview_url=preview_url,
    )


def dump_category_data(data: CategoryModel) -> dict:
    return {
        CATEGORY_NAME_FIELD: data.name,
        CATEGORY_PARENT_FIELD: data.parent_category,
        CATEGORY_IMAGE_FIELD: [
            {"url": data.preview_url, 'title': f'{secrets.token_hex(6)}.jpeg', 'mimetype': 'image/jpeg'}]
    }


# PRODUCT_IMAGE_FIELD = "Изображения"
# PRODUCT_NAME_FIELD = "Название"
# PRODUCT_STOCK_FIELD = "Доступное количество"
# PRODUCT_PRICE_FIELD = "Стоимость"
# PRODUCT_CURRENCY_FIELD = "Валюта"
# PRODUCT_DESCRIPTION_FIELD = "Описание"
# PRODUCT_CATEGORY_NAME_FIELD = "Название категорий"
# PRODUCT_DISCOUNT_PRICE_FIELD = "Стоимость со скидкой"

PRODUCT_IMAGE_FIELD="Images"
PRODUCT_NAME_FIELD="Name"
PRODUCT_DESCRIPTION_FIELD = "Description"
PRODUCT_ID_FIELD="ID"
PRODUCT_EXTERNAL_ID="ExternalId"
PRODUCT_PRICE_FIELD="Price"
PRODUCT_CURRENCY_FIELD = "Currency"
PRODUCT_STOCK_FIELD = "Number of pieces"
PRODUCT_CATEGORY_ID_FIELD = "Category"
PRODUCT_DISCOUNT_PRICE_FIELD = "Discounted price"
PRODUCT_CATEGORY_NAME_FIELD = "Name of categories"
# PRODUCT_CATEGORY_ID_LOOKUP_FIELD = "ID Категории"
PRODUCT_CATEGORY_ID_LOOKUP_FIELD = "ID of category"
PRODUCT_REQUIRED_OPTIONS_FIELD = "Выбор обязательных опций"
PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD = "Выбор категории доп опций"
PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD = "Названия категорий доп опций"
PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD = "Обязательный выбор?"


def dump_product_data(data: ProductModel) -> dict:
    if data.external_id=="21":
        print("Hoi")
    preview_url = ([{'url': image_url,
                     'title': f'{secrets.token_hex(6)}.jpeg',
                     'mimetype': 'image/jpeg'}
                    for image_url in data.preview_url]
                   if data.preview_url
                   else [])

    return {
        PRODUCT_NAME_FIELD: data.name,
        PRODUCT_DESCRIPTION_FIELD: data.description,
        PRODUCT_PRICE_FIELD: data.price,
        PRODUCT_CURRENCY_FIELD: data.currency,
        PRODUCT_STOCK_FIELD: data.stock_qty,
        #TODO Add for several categories
        PRODUCT_CATEGORY_NAME_FIELD:[data.category_name] if data.category_name else None,
        # PRODUCT_CATEGORY_ID_FIELD: [{"id": int(data.category[0])}] if data.category else None,
        PRODUCT_CATEGORY_ID_FIELD: [{'Id': data.category}] if data.category else None,
        PRODUCT_IMAGE_FIELD: preview_url,
        PRODUCT_DISCOUNT_PRICE_FIELD: data.final_price
    }

def dump_product_data_with_check(data: ProductModel, data_check: dict) -> dict:
 
    preview_url = ([{'url': image_url,
                    'title': f'{secrets.token_hex(6)}.jpeg',
                    'mimetype': 'image/jpeg'}
                for image_url in data.preview_url]
                if data.preview_url
                else [])
    product_data = {
        PRODUCT_ID_FIELD: data.id,
        PRODUCT_EXTERNAL_ID: data.external_id,
        PRODUCT_NAME_FIELD: data.name,
        PRODUCT_DESCRIPTION_FIELD: data.description,
        PRODUCT_PRICE_FIELD: data.price,
        PRODUCT_CURRENCY_FIELD: data.currency,
        PRODUCT_STOCK_FIELD: data.stock_qty,
        #TODO Add for several categories
        PRODUCT_CATEGORY_NAME_FIELD:[data.category_name] if data.category_name else None,
        #TODO Add for several categories
        PRODUCT_CATEGORY_ID_FIELD: [{'Id': data_check[data.category_name[0]]}] if data.category else None,
        PRODUCT_IMAGE_FIELD: preview_url,
        PRODUCT_DISCOUNT_PRICE_FIELD: data.final_price
        }
    return product_data


async def parse_product_data(data: dict) -> ProductModel:
    preview_url = [image['url'] for image in data[PRODUCT_IMAGE_FIELD]] if data.get(PRODUCT_IMAGE_FIELD, '') else []
    primary_keys = [ID_FIELD,PRODUCT_NAME_FIELD, PRODUCT_DESCRIPTION_FIELD, PRODUCT_PRICE_FIELD,
                    PRODUCT_CURRENCY_FIELD, PRODUCT_STOCK_FIELD, PRODUCT_CATEGORY_ID_FIELD, PRODUCT_IMAGE_FIELD,
                    PRODUCT_CATEGORY_NAME_FIELD, PRODUCT_DISCOUNT_PRICE_FIELD, PRODUCT_CATEGORY_ID_LOOKUP_FIELD,
                    PRODUCT_REQUIRED_OPTIONS_FIELD, PRODUCT_CATEGORIES_EXTRA_OPTIONS_FIELD,
                    PRODUCT_CATEGORIES_EXTRA_OPTION_NAMES_FIELD, PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD,
                    "UpdatedAt", "CreatedAt"]

    # Dynamically adding extra attributes
    extra_attributes = []
    for key, value in data.items():
        if key not in primary_keys and value is not None and type(value) in [str, int, float]:
            extra_attributes.append(ExtraAttribute(name=key, description=str(value)))

    product = ProductModel(
        id=str(data[ID_FIELD]) if data.get(ID_FIELD) else data.get(NEW_ID_FIELD),
        external_id=data.get(PRODUCT_EXTERNAL_ID, ""),
        name=data.get(PRODUCT_NAME_FIELD, ""),
        description=data.get(PRODUCT_DESCRIPTION_FIELD, "") if data.get(PRODUCT_DESCRIPTION_FIELD) else "",
        price=data.get(PRODUCT_PRICE_FIELD, 0.0),
        currency=data.get(PRODUCT_CURRENCY_FIELD, ["RUB","CZK","GBP"]) if data.get(PRODUCT_CURRENCY_FIELD) else "RUB",
        stock_qty=data.get(PRODUCT_STOCK_FIELD, 0),
        preview_url=preview_url,
        category_name=data.get(PRODUCT_CATEGORY_NAME_FIELD, []) if data.get(PRODUCT_CATEGORY_NAME_FIELD) else [],
        category=data.get(PRODUCT_CATEGORY_ID_LOOKUP_FIELD, []) if data.get(PRODUCT_CATEGORY_ID_LOOKUP_FIELD) else [],
        # category=[],
        extra_attributes=extra_attributes,
        extra_option_choice_required=any(data.get(PRODUCT_EXTRA_CHOICE_REQUIRED_FIELD, [])),
        metadata = data
    )
    if data.get(PRODUCT_DISCOUNT_PRICE_FIELD, data.get(PRODUCT_PRICE_FIELD, 0.0)):
        product.final_price = data.get(PRODUCT_DISCOUNT_PRICE_FIELD, data.get(PRODUCT_PRICE_FIELD, 0.0))
    
    return product




