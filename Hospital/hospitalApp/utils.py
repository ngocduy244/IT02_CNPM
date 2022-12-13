def cart_stats(cart):
    total_amount, total_quantity = 0, 0


    if cart:
        for p in cart.values():
            total_quantity += p['quantity']
            total_amount += p['quantity'] * p['price']


    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }



