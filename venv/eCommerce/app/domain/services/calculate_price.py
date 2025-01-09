def final_price(cost, margin):
    dec_margi=margin / 100
    fprice= cost / ( 1 - dec_margi)
    return fprice