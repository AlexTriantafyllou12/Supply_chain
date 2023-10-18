import configparser
import SKUType
import Supplier
import Warehouse
import SolutionsGenerator
import random

# import global varibale from a config file
config = configparser.ConfigParser()
config.read('sim.config')
global_variables = config['global']

nr_SKUs = int(global_variables['nr_SKUs'])
nr_suppliers = int(global_variables['nr_suppliers'])
time_periods = int(global_variables['time_periods'])

skus = []
suppliers = []

for s in range(nr_SKUs):
    sku_name = "SKU{}".format(s)
    starting_inventory = random.randint(100, 500)
    sku = SKUType.SKUType(name=sku_name, 
                          holding_cost=100,
                          actual_inventory=starting_inventory,
                          estimated_inventory=starting_inventory,
                          lead_time_mean=random.randint(1, 5),
                          lead_time_sd=random.randint(1, 3),
                          demand_mean = random.randint(30, 100),
                          demand_sd = random.randint(4, 20)
                          )
    demand = sku.generate_demand()
    sku.set_demand(demand)
    skus.append(sku)
print("SKUs set up")
supplier_1 = Supplier.Supplier(name="Supplier1",
                      items_delivered={"SKU1": {"price_per_item": 100, "discount": {10: 100, 25: 300}}, "SKU2": {"price_per_item": 100, "discount": {10: 150, 20: 300, 30:400}}, "SKU0": {"price_per_item": 40, "discount": {10: 150, 20: 300, 30:400}}},
                      delivery_cost=300,
                      lead_time=4,
                      risk=1)

supplier_2 = Supplier.Supplier(name="Supplier2",
                      items_delivered={"SKU2": {"price_per_item": 80, "discount": {10: 300, 25: 700}}, "SKU3": {"price_per_item": 100, "discount": {10: 150, 20: 300, 30:400}}, "SKU4": {"price_per_item": 40, "discount": {10: 150, 20: 300, 30:400}}, "SKU0": {"price_per_item": 45, "discount": {10: 120, 20: 300, 30:400}}},
                      delivery_cost=400,
                      lead_time=3,
                      risk=2)

suppliers.append(supplier_1)
suppliers.append(supplier_2)

print("Suppliers set up")
warehouse = Warehouse.Warehouse(max_capacity=10000,
                      current_capacity=100,
                      maintenance_cost=1000)


solution_generator = SolutionsGenerator.SolutionGenerator(nr_periods=time_periods,
                                        nr_skus=nr_SKUs)

print("Solution instatiated")
meta_data, solution = solution_generator.generate_random_solution(skus=skus,
                                                       suppliers=suppliers,
                                                       warehouse=warehouse)
print("Solution generated")
print(solution)
print(meta_data)