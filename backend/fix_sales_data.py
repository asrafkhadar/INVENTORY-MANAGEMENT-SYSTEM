#!/usr/bin/env python
"""
Fix sales analytics data with current dates
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_system.settings')
django.setup()

from inventory_app.models import Product, SalesAnalytics
from django.utils import timezone
from datetime import timedelta

# Delete old analytics
SalesAnalytics.objects.all().delete()

# Get all products
products = Product.objects.all()

# Create analytics for last 30 days
today = timezone.now().date()
for product in products:
    for j in range(30):
        date = today - timedelta(days=j)
        SalesAnalytics.objects.create(
            product=product,
            date=date,
            units_sold=10 + (j % 15),
            revenue=(10 + (j % 15)) * product.unit_price
        )

print(f"✓ Created {SalesAnalytics.objects.count()} SalesAnalytics records with current dates")
print(f"Date range: {today - timedelta(days=29)} to {today}")
