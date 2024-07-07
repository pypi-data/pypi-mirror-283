from typing import List,Optional

from aiocache import cached
from models.products import ProductModel
from nocodb_connector.client import NocodbClient
from nocodb_connector.model_mapping import dump_product_data,dump_product_data_with_check, get_pagination_info, ID_FIELD, \
    parse_product_data, PRODUCT_CATEGORY_ID_LOOKUP_FIELD, PRODUCT_NAME_FIELD, PRODUCT_PRICE_FIELD, \
    PRODUCT_STOCK_FIELD

from tgshops_integrations.nocodb_connector.categories import CategoryManager
from tgshops_integrations.nocodb_connector.products import ProductManager
from tgshops_integrations.nocodb_connector.tables import *
from loguru import logger
import hashlib


class Gateway(NocodbClient):

    def __init__(self,logging=False,NOCODB_HOST=None,NOCODB_API_KEY=None,SOURCE=None):
        super().__init__(NOCODB_HOST=NOCODB_HOST,NOCODB_API_KEY=NOCODB_API_KEY,SOURCE=SOURCE)
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.logging=logging
        self.required_fields = [PRODUCT_NAME_FIELD, PRODUCT_PRICE_FIELD]
        self.projection = []


    async def load_data(self,SOURCE=None):
        self.SOURCE=SOURCE
        await self.get_all_tables()
        self.category_manager=CategoryManager(table_id=self.tables_list[NOCODB_CATEGORIES],NOCODB_HOST=self.NOCODB_HOST,NOCODB_API_KEY=self.NOCODB_API_KEY)
        self.product_manager=ProductManager(table_id=self.tables_list[NOCODB_PRODUCTS],NOCODB_HOST=self.NOCODB_HOST,NOCODB_API_KEY=self.NOCODB_API_KEY)

    async def create_product(self,product: ProductModel) -> ProductModel:
        products_table = self.tables_list[NOCODB_PRODUCTS]
        data = dump_product_data_with_check(data=product ,data_check=self.category_manager.categories)
        # product_json = dump_product_data_with_check(data=product,data_check=self.categories)
        data.pop("ID")
        record = await self.create_table_record(table_name=products_table, record=data)
        logger.info(f"Created product {record['id']}")
        return parse_product_data(record)

    async def update_products(self, external_products: List[ProductModel]):
        products_table = self.tables_list[NOCODB_PRODUCTS]
        self.product_manager.actual_products=await self.product_manager.get_products_v2(offset=0,limit=200)
        self.ids_mapping={product.external_id : product.id for product in self.product_manager.actual_products}
        products_meta= {product.external_id : product for product in self.product_manager.actual_products}

        for product in external_products:
            if product.external_id in self.ids_mapping.keys():
                product.id=self.ids_mapping[product.external_id]
                if self.product_manager.hash_product(product)!=self.product_manager.hash_product(products_meta[product.external_id]):
                    await self.update_product(product=product)
            else:
                await self.create_product(product=product)
        
    async def update_product(self, product: ProductModel):
        products_table = self.tables_list[NOCODB_PRODUCTS]
        data = dump_product_data_with_check(data=product ,data_check=self.category_manager.categories)

        await self.update_table_record(
            table_name=products_table,
            record_id=product.id,
            updated_data=data)
        logger.info(f"Updated product {product.id}")
        
        
    def find_product_id_by_name(self,name: str):
        for product in self.product_manager.actual_products.products:
            if product.name == name:
                return product.id
        return None  # Return None if no product is found with the given name
    
    async def create_table_column(self, name: str, table_id: Optional[str] = None):

        BEARER_TOKEN = "jpdxJtyfDXdjbvxKAcIij1HA8HGalgalLLXZ46DV"
        
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        if not table_id:
            table_id = self.tables_list[NOCODB_PRODUCTS]

        response = await self.httpx_client.post(
            f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/tables/{table_id}/columns",
            json={
                "column_name": name,
                "dt": "character varying",
                "dtx": "specificType",
                "ct": "varchar(45)",
                "clen": 45,
                "dtxp": "45",
                "dtxs": "",
                "altered": 1,
                "uidt": "SingleLineText",
                "uip": "",
                "uicn": "",
                "title": name
            },
            headers=headers
        )

        logger.info(response.text())

        return response.json()
    
    async def delete_all_products(self):  
        items = await self.product_manager.get_products_v2(offset=0,limit=100)
        products_table = self.tables_list[NOCODB_PRODUCTS]    
        for num,item in enumerate(items):
            await self.delete_table_record(products_table, item.id)