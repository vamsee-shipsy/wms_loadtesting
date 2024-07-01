import random
from locust import TaskSet, task



class ProductCreationTaskSet(TaskSet):
    
    def on_start(self):
        self.access_token_data = self.user.access_token_data
    
    
    @task
    def create_product(self):
        token_data = random.choice(self.access_token_data)
        headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = {
            "warehouse": f"{token_data.get('warehouse')}",
            "skus": [
                {
                    "sku_code": "async_test_10",
                    "sku_type": "FG",
                    "sku_desc": "SKU1 description",
                    "sku_category_name": "Pharma",
                    "sub_category": "Tablet",
                    "sku_brand": "IPCA Lab Lts",
                    "scan_picking":False,
                    "price": 15,
                    "cost_price": 12,
                    "mrp": 20,
                    "sku_class": "Class 2",
                    "style_name": "",
                    "hsn_code": "",
                    "gst_slab": 5,
                    "sku_size": "20 Mg",
                    "size_type": "",
                    "ean_number": "0987654",
                    "threshold_quantity": 50,
                    "product_shelf_life": 40.2,
                    "customer_shelf_life": 10.5,
                    "length": 0.7,
                    "breadth": 0.5,
                    "height": 0.1,
                    "weight": 250,
                    "pick_group": "Pharma",
                    "batch_based": False,
                    "reciept_tolerance" : 10
                },
                {
                    "sku_code": "async_test_20",
                    "sku_type": "FG",
                    "sku_desc": "SKU1 description",
                    "sku_category_name": "Pharma",
                    "sub_category": "Tablet",
                    "sku_brand": "IPCA Lab Lts",
                    "scan_picking":False,
                    "price": 15,
                    "cost_price": 12,
                    "mrp": 20,
                    "sku_class": "Class 2",
                    "style_name": "",
                    "hsn_code": "",
                    "gst_slab": 5,
                    "sku_size": "20 Mg",
                    "size_type": "",
                    "ean_number": "0987654",
                    "threshold_quantity": 50,
                    "product_shelf_life": 40.2,
                    "customer_shelf_life": 10.5,
                    "length": 0.7,
                    "breadth": 0.5,
                    "height": 0.1,
                    "weight": 250,
                    "pick_group": "Pharma",
                    "batch_based": False,
                    "reciept_tolerance" : 10
                }
            ]
                
        }
        self.client.post("/product/create", headers=headers, data=payload)

        