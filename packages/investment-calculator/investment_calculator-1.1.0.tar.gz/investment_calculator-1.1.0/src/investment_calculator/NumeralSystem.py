def get_indian_numeral(amount):
    is_amount_negative = amount < 0
    amount = abs(amount)
    values = []
    mod = 1000

    while amount > mod:
        if mod == 1000:
            values.append('%03d'%(amount % mod))
        else:
            values.append('%02d'%(amount % mod))
        amount = amount // mod
        mod = 100

    if amount > 0:
        values.append(str(amount))
    
    result = ','.join(values[::-1])
    if is_amount_negative:
        return '-' + result
    return result

def get_international_numeral(amount):
    is_amount_negative = amount < 0
    amount = abs(amount)
    values = []
    mod = 1000
    while amount > mod:
        values.append('%03d'%(amount % mod))
        amount = amount // mod

    if amount > 0:
        values.append(str(amount))

    result = ','.join(values[::-1])
    if is_amount_negative:
        return '-' + result
    return result