# ORDER AND CART MANAGEMENT #
#
# Orders are lists of ordered items
# An order item has four components:
# - a name
# - a quantity (the number of such items bought)
# - a unit price (in pence)
# - a unit weight (in pounds)
#
# DO NOT MODIFY CONSTANTS
ORDER_SAMPLE_1 = [
    ("Lamp", 2, 2399, 2),
    ("Chair", 4, 3199, 10),
    ("Table", 1, 5599, 85)
    ]

ORDER_SAMPLE_2 = [
    ("Sofa", 1, 18399, 140),
    ("Bookshelf", 2, 4799, 40)
    ]

CATALOGUE = [
    ('table', 9999, 20),
    ('chair', 2999, 5),
    ('lamp', 1999, 10)
]


def delivery_charges(order):
    """
    Compute the delivery charges for an order. The company charges a flat £50
    fee plus £20 for each 100lbs (additional weight under 100lbs is ignored).

    E.g., delivery_charges([("Desk", 1, 11999, 160)]) is 7000 (pence)
    E.g., delivery_charges([("Desk", 2, 11999, 160)]) is 11000 (pence)
    E.g., delivery_charges([("Lamp", 1, 2399, 2)]) is 5000 (pence)
    E.g., delivery_charges([("Lamp", 50, 2399, 2)]) is 7000 (pence)

    :param order: order to process. See samples for examples.
    :return: delivery fee in pence
    :rtype: float | int
    """

    flat = 50*100
    lbs100 = 20*100
    qty = 0
    l_wt = 0
    totwt = 0
    for i in order:
        qty = i[1]
        l_wt = i[3]
        totwt += l_wt*qty

    l_dc = flat + (round((totwt//100))*lbs100)
    return l_dc


delivery_charges([('X', 1, 0, 1)])
delivery_charges([('X', 1, 0, 100)])
delivery_charges([('X', 1, 0, 101)])
delivery_charges([('X', 1, 11999, 160)])
delivery_charges([('X', 2, 11999, 160)])
delivery_charges([('X', 1, 2399, 2)])
delivery_charges([('X', 50, 2399, 2)])
delivery_charges([('X', 4, 0, 99), ('Y', 1, 0, 300), ('Z', 2, 0, 500)])


def total_charge(order):
    """
    Compute the total charge for an order. It includes:
        - total price of items,
        - VAT (20% of the price of items),
        - delivery fee

    NOTE: in this computation, VAT is not applied to the delivery

    E.g., total_charge([("Desk", 2, 11999, 160)]) is 39797 (pence)
    E.g., total_charge([("Lamp", 50, 2399, 2)]) is 150940 (pence)

    Hint: Look up the built-in Python function round().

    :param order: order to process. See samples.
    :return: total price, in pence, rounded to the nearest penny.
    :rtype: float | int
    """

    flat = 50*100
    lbs100 = 20*100
    qty = 0
    l_wt = 0
    l_up = 0
    totwt = 0
    totup = 0
    for i in order:
        qty = i[1]
        l_up = i[2]
        l_wt = i[3]
        totwt += l_wt * qty
        totup += l_up * qty

    l_dc = flat + (round((totwt//100))*lbs100)
    price = totup + round((totup*.20))+l_dc
    return price


total_charge([('X', 1, 0, 1)])
total_charge([('X', 1, 100, 1)])
total_charge([('X', 5, 100, 50)])
total_charge([('X', 5, 100, 50), ('Y', 10, 50, 0)])
total_charge([('Desk', 1, 11999, 160)])
total_charge([('Desk', 2, 11999, 160)])
total_charge([('Lamp', 1, 2399, 2)])
total_charge([('Lamp', 50, 2399, 2)])


def add_item_to_order(name, quantity, order):
    """
    When a customer adds items to their basket, you need to update their
    order. The customer provides some of the details (the name of the item and
    the quantity they want); the CATALOGUE contains additional details (price
    and weight).

    NOTE: you must return a new order list and leave the argument unmodified.

    NOTE: if the order already contains some of the items, you must update the
    quantity field for that item; otherwise, you must add a new entry in the
    order

    NOTE: if the item cannot be found in the order or the catalogue, the function
    should return the original order.

    E.g., add_item_to_order("table", 1, [("table", 1, 9999, 20)]) is
    [("table", 2, 9999, 20)]
    E.g., add_item_to_order("chair", 1, [("table", 1, 9999, 20)]) is
    [("table", 1, 9999, 20), ("chair", 1, 2999, 5)]

    :param name: name of the item to add
    :param quantity: number of items to add
    :param order: previous order
    :return: a new order with the added items. If the item is unknown, return
    None instead.
    :rtype: list | NoneType
    """
    l_orders = []
    l_items = []
    found = False
    for items in order:
        print(items)
        l_items = list(items)
        if name in items:
            l_items[1] = l_items[1]+quantity
            print(l_items)
            found = True
    if l_items != []:
        l_orders.append(tuple(l_items))
    if not found:
        for cat in CATALOGUE:
            c_cat = list(cat)
            if name in c_cat:
                l_orders.append((name, quantity, 2999, 5))
    return l_orders


add_item_to_order("chair", 11, [])
add_item_to_order("computer", 1, [("table", 1, 9999, 20)])
