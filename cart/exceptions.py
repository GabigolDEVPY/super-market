class CartError(Exception):
    pass

class OutOfStockError(Exception):
    pass

class MaxCartQuantity(Exception):
    pass

class CartItemNotExists(Exception):
    pass