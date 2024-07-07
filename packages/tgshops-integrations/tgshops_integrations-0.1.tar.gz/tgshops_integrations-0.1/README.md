




```python

import tgshops_integrations
import ExternalProductModel, ExternalCategoryModel from tgshops_integrations.models

# Load external data
external_categories = [ExternalCategoryModel(
    name="Drinks",
    image_url="https://example.com/image.jpg",
    external_id="0"
), CategoryModel(
    name="Coffee",
    image_url="https://example.com/image.jpg",
    external_id="1"
)]
external_products = [ExternalProductModel(
    name="Coffee",
    description="",
    price=10.0,
    currency="USD",
    image_url="https://example.com/image.jpg",
    category=List["0", "1"],
    external_id="0"
)]


# Initialise
product_service = tgshops_integrations.ProductService(token="your_token_here")

await product_service.update_categories(
    external_categories=external_categories
)

await product_service.update_products(
    external_products=external_products
)

# Here is the the custom integration of your service, which has to return products according to the ExternalProductModel
bitrixService=BitrixClient()
bitrix_product_list=await bitrixService.get_crm_product_list()

# One gateway can work with several table / DBs
NocoGateway = Gateway(NOCODB_HOST=NOCODB_HOST,NOCODB_API_KEY=NOCODB_API_KEY)

# await NocoGateway.load_data()
# await NocoGateway.delete_all_products()

# Load data provides the access to the certain table and allows to obtain the data about the products or catergories
await NocoGateway.load_data(SOURCE=SOURCE)
await NocoGateway.category_manager.update_categories(external_products=bitrix_product_list)
await NocoGateway.update_products(external_products=bitrix_product_list)




```