from typing import List,Optional

import httpx
import requests
from loguru import logger

from tgshops_integrations.nocodb_connector.model_mapping import ID_FIELD


def custom_key_builder(func, *args, **kwargs):
    # Exclude 'self' by starting args processing from args[1:]
    args_key_part = "-".join(str(arg) for arg in args[1:])
    kwargs_key_part = "-".join(f"{key}-{value}" for key, value in sorted(kwargs.items()))
    return f"{func.__name__}-{args_key_part}-{kwargs_key_part}"


class NocodbClient:
      
    def __init__(self,NOCODB_HOST=None,NOCODB_API_KEY=None,SOURCE=None):
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.SOURCE=SOURCE
        self.httpx_client = httpx.AsyncClient()
        self.httpx_client.headers = {
            "xc-token": self.NOCODB_API_KEY
        }

    def construct_get_params(self,
                             required_fields: list = None,
                             projection: list = None,
                             extra_where: str = None,
                             offset: int = None,
                             limit: int = None) -> dict:
        extra_params = {}
        if projection:
            extra_params["fields"] = ','.join(projection)
        if required_fields:
            extra_params["where"] = ""
            for field in required_fields:
                extra_params["where"] += f"({field},isnot,null)~and"
            extra_params["where"] = extra_params["where"].rstrip("~and")
        if extra_where:
            if not extra_params.get("where"):
                extra_params["where"] = extra_where
            else:
                extra_params["where"] += f"~and{extra_where}"
        if offset:
            extra_params['offset'] = offset
        if limit:
            extra_params["limit"] = limit
        return extra_params

    async def get_table_records(self,
                                table_name: str,
                                required_fields: list = None,
                                projection: list = None,
                                extra_where: str = None,
                                limit: int = None) -> List[dict]:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        extra_params = self.construct_get_params(required_fields, projection, extra_where, limit=limit)
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()["list"]
        raise Exception(response.text)

    async def get_table_records_v2(self,
                                   table_name: str,
                                   required_fields: list = None,
                                   projection: list = None,
                                   extra_where: str = None,
                                   offset: int = None,
                                   limit: int = 25) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        extra_params = self.construct_get_params(required_fields, projection, extra_where, offset=offset, limit=limit)
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)
    
    # class ProductModel(BaseProductModel):
    #     extra_option_choice_required: bool = False
    #     extra_option_categories: List[ExtraOptionCategoriesResponseModel] = []
    #     related_products: List[BaseProductModel] = None
    #     metadata : ProductModel

    async def get_table_record(self,
                               table_name: str,
                               record_id: str,
                               required_fields: list = None,
                               projection: list = None) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records/{record_id}"
        extra_params = self.construct_get_params(required_fields, projection)
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def create_table_record(self, table_name: str, record: dict) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        response = await self.httpx_client.post(url, json=record)
        if response.status_code == 200:
            record["id"] = response.json().get("id")
            if not record["id"]:
                record["id"] = response.json().get("Id")
            return record
        raise Exception(response.text)

    async def count_table_records(self, table_name: str) -> int:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records/count"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json().get("count", 0)
        raise Exception(response.text)

    async def update_table_record(self, table_name: str, record_id: str, updated_data: dict) -> bool:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        updated_data[ID_FIELD] = record_id
        response = await self.httpx_client.patch(url, json=updated_data)
        if response.status_code == 200:
            return True
        raise Exception(response.text)

    async def delete_table_record(self, table_name: str, record_id: str) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        response = requests.delete(url, json={"Id": record_id}, headers=self.httpx_client.headers)
        if response.status_code == 200:
            logger.info(f"Deleted item {record_id}")
        return response.json()

    # Not transport
    async def get_product_categories(self, table_id: str,table_name : str) -> int:
        url = f"{self.NOCODB_HOST}/tables/{table_id}/records"
        limit=75
        extra_params = self.construct_get_params(limit=limit)
        response = await self.httpx_client.get(url, params=extra_params)

        if response.status_code == 200:
            self.categories={category[table_name] : category["Id"] for category in response.json()["list"]}
        # raise Exception(response.text)
    
    async def create_product_category(self, table_id: str, category_name : str, table_name : str, category_id : int = 0)  -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_id}/records"

        record={table_name: category_name, "Id" : category_id}

        response = await self.httpx_client.post(url, json=record)
        if response.status_code == 200:
            # record["id"] = response.json().get("Id")
            # if not record["id"]:
            #     record["id"] = response.json().get("Id")
            await self.get_product_categories(table_id=table_id, table_name=table_name)
            return record
        raise Exception(response.text)
    
    async def get_table_meta(self, table_name: str):
        return (await self.httpx_client.get(
            f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/tables/{table_name}")).json()


    async def get_all_tables(self, source: Optional[str] = None):
        if not source:
            source=self.SOURCE

        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/projects/{source}/tables?includeM2M=false"
        response=(await self.httpx_client.get(url)).json()
        tables_info=response.get('list', [])
        self.tables_list={table["title"] : table["id"] for table in tables_info}
        return self.tables_list

    async def get_sources(self):
        return (await self.httpx_client.get(
            f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/projects/")).json().get(
            'list', [])

    def link_tables(self, source: str, parent_id: str, child_id: str, parent_table: str, child_table: str):
        """
        Связывает таблицы
        :param source:
        :param parent_id:
        :param child_id:
        :param parent_table:
        :param child_table:
        :return:
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/data/noco/{source}/{parent_table}/{parent_id}/mm/{child_table}/{child_id}"
        return requests.post(url, headers=self.httpx_client.headers).json()
