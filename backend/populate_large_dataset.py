#!/usr/bin/env python
"""
Populate database with 500 products, warehouses, and inventory data
Run with: python populate_large_dataset.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from inventory_app.models import (
    Supplier, Product, Warehouse, InventoryLocation, SalesAnalytics
)
from django.utils import timezone
from datetime import timedelta
import random

print("🔄 Starting large dataset population...")

# Create suppliers (will be used for 500 products)
print("\n📦 Creating suppliers...")
suppliers_data = [
    {"name": "Tech World International", "email": "contact@techworld.com", "phone": "+1-555-0100"},
    {"name": "Global Electronics Hub", "email": "sales@globaltech.com", "phone": "+1-555-0101"},
    {"name": "Premium Supplies Co", "email": "info@premiumsupply.com", "phone": "+1-555-0102"},
    {"name": "Asia Export Trading", "email": "export@asiatrading.com", "phone": "+1-555-0103"},
    {"name": "European Goods Ltd", "email": "eu@europeangoods.com", "phone": "+1-555-0104"},
    {"name": "Americas Distribution", "email": "dist@americas.com", "phone": "+1-555-0105"},
    {"name": "Direct Manufacturer Co", "email": "mfg@directmfg.com", "phone": "+1-555-0106"},
    {"name": "Wholesale Central", "email": "wholesale@central.com", "phone": "+1-555-0107"},
    {"name": "Premium Import Services", "email": "import@premium.com", "phone": "+1-555-0108"},
    {"name": "Quick Supply Solutions", "email": "quick@supply.com", "phone": "+1-555-0109"},
]

suppliers = []
for supplier_data in suppliers_data:
    supplier, created = Supplier.objects.get_or_create(
        name=supplier_data['name'],
        defaults={
            'email': supplier_data['email'],
            'phone': supplier_data['phone'],
            'address': f"123 Supply Street, District {suppliers_data.index(supplier_data)}",
            'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'][suppliers_data.index(supplier_data) % 5],
            'country': 'USA'
        }
    )
    suppliers.append(supplier)

print(f"✓ Created/found {len(suppliers)} suppliers")

# Create warehouses
print("\n🏭 Creating warehouses...")
warehouse_data = [
    {"name": "Central Hub - NY", "city": "New York", "capacity": 50000},
    {"name": "West Coast - LA", "city": "Los Angeles", "capacity": 45000},
    {"name": "Midwest - Chicago", "city": "Chicago", "capacity": 40000},
    {"name": "South - Houston", "city": "Houston", "capacity": 35000},
    {"name": "Florida - Miami", "city": "Miami", "capacity": 30000},
    {"name": "Denver Distribution", "city": "Denver", "capacity": 25000},
    {"name": "Seattle Storage", "city": "Seattle", "capacity": 20000},
    {"name": "Dallas Center", "city": "Dallas", "capacity": 35000},
]

warehouses = []
for wh_data in warehouse_data:
    warehouse, created = Warehouse.objects.get_or_create(
        name=wh_data['name'],
        defaults={
            'address': f"1000 {wh_data['name']} Road",
            'city': wh_data['city'],
            'country': 'USA',
            'manager_name': f"Manager {wh_data['city']}",
            'capacity': wh_data['capacity']
        }
    )
    warehouses.append(warehouse)

print(f"✓ Created/found {len(warehouses)} warehouses")

# Create 500 products
print("\n📦 Creating 500 products...")
product_categories = ['Electronics', 'Accessories', 'Peripherals', 'Software', 'Storage', 
                      'Networking', 'Printing', 'Security', 'Power', 'Cooling']
product_names = [
    'Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 
    'USB Cable', 'HDMI Cable', 'Power Supply', 'RAM', 'SSD',
    'Hard Drive', 'Graphics Card', 'Motherboard', 'Processor', 'Cooling Fan',
    'Case', 'Printer', 'Scanner', 'Router', 'Switch',
    'Modem', 'Adapter', 'Hub', 'Dock', 'Stand',
    'Screen Protector', 'Camera', 'Microphone', 'Speaker', 'Headphones',
    'Charger', 'Battery', 'Webcam', 'Monitor Arm', 'Desk Pad',
    'Surge Protector', 'UPS', 'Cable Organizer', 'Laptop Bag', 'Cleaning Kit'
]

product_models = [
    'Pro', 'Plus', 'Max', 'Ultra', 'Standard',
    'Elite', 'Compact', 'Professional', 'Home', 'Business',
    'Gaming', 'Workstation', 'Mobile', 'Desktop', 'Server',
    'Budget', 'Premium', 'Economy', 'Enterprise', 'Personal'
]

products_created = 0
products = []

for i in range(500):
    product_name = f"{random.choice(product_names)} {random.choice(product_models)} {i+1}"
    unit_cost = random.randint(10, 800)
    unit_price = int(unit_cost * random.uniform(1.2, 2.5))
    
    product, created = Product.objects.get_or_create(
        barcode=f"PROD-{i+1:05d}",
        defaults={
            'name': product_name,
            'category': random.choice(product_categories),
            'unit_cost': unit_cost,
            'unit_price': unit_price,
            'reorder_level': random.randint(5, 50),
            'status': 'active' if random.random() > 0.1 else 'inactive',
            'supplier': random.choice(suppliers)
        }
    )
    if created:
        products_created += 1
    products.append(product)

print(f"✓ Created {products_created} new products (total: {len(products)})")

# Create inventory locations for products in warehouses
print("\n📍 Creating inventory locations for products in warehouses...")
locations_created = 0

aisles = [chr(65 + i) for i in range(10)]  # A-J
racks = list(range(1, 21))  # 1-20
shelves = list(range(1, 6))  # 1-5
bins = list(range(1, 11))  # 1-10

for product in products:
    # Add each product to 2-4 random warehouses
    selected_warehouses = random.sample(warehouses, k=random.randint(2, 4))
    
    for warehouse in selected_warehouses:
        aisle = random.choice(aisles)
        rack = random.choice(racks)
        shelf = random.choice(shelves)
        bin_num = random.choice(bins)
        
        location, created = InventoryLocation.objects.get_or_create(
            product=product,
            warehouse=warehouse,
            defaults={
                'aisle': aisle,
                'rack': f"R{rack}",
                'shelf': str(shelf),
                'bin': f"B{bin_num}",
                'quantity': random.randint(10, 500),
                'batch_number': f"BATCH-{product.id}-{warehouse.id}",
                'expiry_date': timezone.now().date() + timedelta(days=random.randint(30, 730))
            }
        )
        if created:
            locations_created += 1

print(f"✓ Created {locations_created} inventory locations")

# Create sales analytics for all products
print("\n📊 Creating sales analytics for 500 products...")
today = timezone.now().date()
analytics_created = 0

for product in products:
    for j in range(30):  # Last 30 days
        date = today - timedelta(days=j)
        units_sold = random.randint(1, 30)
        
        analytics, created = SalesAnalytics.objects.get_or_create(
            product=product,
            date=date,
            defaults={
                'units_sold': units_sold,
                'revenue': units_sold * product.unit_price
            }
        )
        if created:
            analytics_created += 1

print(f"✓ Created {analytics_created} sales analytics records")

# Summary
print("\n" + "="*60)
print("✅ DATASET POPULATION COMPLETE!")
print("="*60)
print(f"✓ Suppliers: {len(suppliers)}")
print(f"✓ Warehouses: {len(warehouses)}")
print(f"✓ Products: {products_created} new + {Product.objects.count()} total")
print(f"✓ Inventory Locations: {locations_created}")
print(f"✓ Sales Analytics: {SalesAnalytics.objects.count()} total records")
print("="*60)
print("\n🚀 Your website is now loaded with realistic data!")
print("📌 Access at: http://localhost:8000/login.html")
print("   Username: admin")
print("   Password: admin")
