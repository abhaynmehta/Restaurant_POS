from database import SessionLocal, engine, Base
from models import Menu, Category, MenuItem, Order, OrderItem, Payment, APIKey
from datetime import date

# Clear existing data and create fresh tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("Loading data...")

try:
    # API Key
    db.add(APIKey(api_key="sk_test_restaurant_pos_2025_secure_key_12345", key_name="Test", is_active=True))
    
    # Menus
    db.add_all([
        Menu(menu_id=1, menu_name="Food", is_active=True),
        Menu(menu_id=2, menu_name="Drinks", is_active=True)
    ])
    
    # Categories
    db.add_all([
        Category(category_id=1, category_name="Starters", menu_id=1, display_order=1),
        Category(category_id=2, category_name="Soft Drinks", menu_id=2, display_order=1),
        Category(category_id=3, category_name="Mains", menu_id=1, display_order=2),
        Category(category_id=4, category_name="Desserts", menu_id=2, display_order=2),
        Category(category_id=5, category_name="Hot Drinks", menu_id=2, display_order=3)
    ])
    
    # Menu Items (all 10 items)
    db.add_all([
        MenuItem(item_id=1, item_name="Item1", category_id=1, menu_id=1, has_sizes=True, size_options="Small,Large", is_active=True),
        MenuItem(item_id=2, item_name="Item2", category_id=1, menu_id=1, base_price=3.00, has_sizes=False, is_active=True),
        MenuItem(item_id=3, item_name="Item3", category_id=2, menu_id=2, base_price=2.50, has_sizes=False, is_active=True),
        MenuItem(item_id=4, item_name="Item4", category_id=2, menu_id=2, base_price=1.50, has_sizes=False, is_active=True),
        MenuItem(item_id=5, item_name="Item5", category_id=2, menu_id=1, base_price=1.00, has_sizes=False, is_active=True),
        MenuItem(item_id=6, item_name="Item6", category_id=3, menu_id=1, has_sizes=True, size_options="Small,Large", is_active=True),
        MenuItem(item_id=7, item_name="Item7", category_id=3, menu_id=1, base_price=2.50, has_sizes=False, is_active=True),
        MenuItem(item_id=8, item_name="Item8", category_id=4, menu_id=2, has_sizes=True, size_options="Small,Large", is_active=True),
        MenuItem(item_id=9, item_name="Item9", category_id=4, menu_id=2, base_price=1.50, has_sizes=False, is_active=True),
        MenuItem(item_id=10, item_name="Item10", category_id=5, menu_id=2, base_price=2.00, has_sizes=False, is_active=True)
    ])
    
    # Orders (10-20)
    orders_data = [
        (10, date(2025, 10, 1), "Completed", 9.25),
        (11, date(2025, 10, 1), "Completed", 21.25),
        (12, date(2025, 10, 1), "Completed", 17.0),
        (13, date(2025, 10, 1), "Completed", 15.5),
        (14, date(2025, 10, 1), "Completed", 42.8193),
        (15, date(2025, 10, 2), "Completed", 5.136),
        (16, date(2025, 10, 3), "Completed", 19.758),
        (17, date(2025, 10, 1), "Completed", 10.8918),
        (18, date(2025, 10, 5), "Completed", 26.33588),
        (19, date(2025, 10, 1), "Completed", 72.13188),
        (20, date(2025, 10, 1), "Completed", 52.2573),
    ]
    
    for order_id, order_date, status, total in orders_data:
        db.add(Order(order_id=order_id, order_date=order_date, order_status=status, total_amount=total))
    
    # Order Items (all 52 rows from your table)
    order_items_data = [
        (10, 2, None, 2.5, 1, 2.5),
        (10, 3, None, 1.5, 2, 3.0),
        (10, 1, "Small", 3.75, 1, 3.75),
        (11, 5, None, 2.75, 1, 2.75),
        (11, 6, None, 1.75, 2, 3.5),
        (11, 2, None, 2.5, 1, 2.5),
        (11, 3, None, 3.5, 1, 3.5),
        (11, 4, None, 3.75, 2, 7.5),
        (11, 5, None, 1.5, 1, 1.5),
        (12, 6, "Large", 5.5, 2, 11.0),
        (12, 7, None, 2.5, 1, 2.5),
        (12, 1, "Large", 3.5, 1, 3.5),
        (13, 1, "Small", 2.75, 2, 5.5),
        (13, 6, "Small", 1.5, 1, 1.5),
        (13, 8, "Small", 3.5, 1, 3.5),
        (13, 1, "Small", 2.5, 2, 5.0),
        (14, 6, "Large", 2.75, 1, 2.75),
        (14, 1, "Large", 2.75655, 2, 5.5131),
        (14, 8, "Large", 2.75, 2, 5.5),
        (14, 1, "Large", 2.7556, 2, 5.5112),
        (14, 4, None, 5.5, 1, 5.5),
        (14, 3, None, 2.75, 2, 5.5),
        (14, 2, None, 3.5, 1, 3.5),
        (14, 6, "Large", 3.015, 3, 9.045),
        (15, 2, None, 2.568, 2, 5.136),
        (16, 6, "Large", 6.586, 3, 19.758),
        (17, 10, None, 2.5, 1, 2.5),
        (17, 9, None, 2.75636, 1, 2.75636),
        (17, 7, None, 5.63982, 1, 5.63982),
        (18, 1, "Small", 2.5698, 2, 5.1396),
        (18, 6, "Small", 5.36245, 2, 10.7249),
        (18, 8, "Small", 5.23569, 2, 10.47138),
        (19, 2, None, 2.75698, 1, 2.75698),
        (19, 4, None, 2.356, 1, 2.356),
        (19, 5, None, 2.457, 2, 4.914),
        (19, 7, None, 2.6359, 1, 2.6359),
        (19, 9, None, 6.523, 1, 6.523),
        (19, 10, None, 8.54123, 3, 25.6236),
        (19, 6, "Large", 5.6832, 2, 11.3664),
        (19, 2, None, 6.3564, 1, 6.3564),
        (19, 5, None, 7.235, 1, 7.235),
        (19, 7, None, 2.365, 1, 2.365),
        (20, 1, "Large", 2.3658, 1, 2.3658),
        (20, 3, None, 2.356, 1, 2.356),
        (20, 6, "Large", 1.256, 1, 1.256),
        (20, 4, None, 2.635, 1, 2.635),
        (20, 5, None, 5.21, 1, 5.21),
        (20, 7, None, 6.325, 2, 12.65),
        (20, 8, "Small", 7.2514, 1, 7.2514),
        (20, 9, None, 2.3999, 1, 2.3999),
        (20, 4, None, 2.356, 3, 7.068),
        (20, 6, "Small", 4.5326, 2, 9.0652),
    ]
    
    for order_id, item_id, size, price, qty, total in order_items_data:
        db.add(OrderItem(order_id=order_id, item_id=item_id, size=size, unit_price=price, quantity=qty, line_total=total))
    
    # Payments (all 17 rows from your table)
    payments_data = [
        (100, 10, date(2025, 10, 1), 9.25, 9.25, 0, 0, "Card", "Completed"),
        (101, 11, date(2025, 10, 1), 21.25, 10.0, 0, 0, "Cash", "Completed"),
        (102, 11, date(2025, 10, 1), 21.25, 11.25, 0, 0, "Card", "Completed"),
        (103, 12, date(2025, 10, 2), 17.0, 16.0, 3, 4, "Card", "Completed"),
        (104, 13, date(2025, 10, 3), 15.5, 13.5, 0, 2, "Card", "Completed"),
        (105, 14, date(2025, 10, 1), 42.8193, 20.0, 0, 0, "Cash", "Completed"),
        (106, 14, date(2025, 10, 1), 42.8193, 22.82, 0, 0, "Card", "Completed"),
        (107, 15, date(2025, 10, 2), 5.136, 5.14, 0, 0, "Card", "Refunded"),
        (108, 16, date(2025, 10, 3), 19.758, 10.0, 0, 0, "Cash", "Completed"),
        (109, 16, date(2025, 10, 3), 19.758, 9.76, 0, 0, "Card", "Completed"),
        (110, 17, date(2025, 10, 1), 10.8918, 10.9, 0, 0, "Card", "Completed"),
        (111, 18, date(2025, 10, 5), 26.33588, 25.0, 2, 0, "Cash", "Completed"),
        (115, 18, date(2025, 10, 5), 26.33588, 3.34, 0, 0, "Card", "Completed"),
        (116, 19, date(2025, 10, 1), 72.13188, 50.0, 0, 0, "Cash", "Completed"),
        (119, 19, date(2025, 10, 1), 72.13188, 22.13, 0, 0, "Card", "Completed"),
        (120, 20, date(2025, 10, 1), 52.2573, 25.0, 0, 0, "Cash", "Completed"),
        (121, 20, date(2025, 10, 1), 52.2573, 27.28, 0, 0, "Card", "Completed"),
    ]
    
    for payment_id, order_id, payment_date, amount_due, amount_paid, tips, discount, payment_type, status in payments_data:
        db.add(Payment(
            payment_id=payment_id,
            order_id=order_id,
            payment_date=payment_date,
            amount_due=amount_due,
            amount_paid=amount_paid,
            tips=tips,
            discount=discount,
            payment_type=payment_type,
            payment_status=status
        ))
    
    db.commit()
    print("✅ All data loaded successfully!")
    print("   - 2 Menus")
    print("   - 5 Categories")
    print("   - 10 Menu Items")
    print("   - 11 Orders (10-20)")
    print("   - 52 Order Items")
    print("   - 17 Payments")
    print("   - 1 API Key")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error loading data: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
