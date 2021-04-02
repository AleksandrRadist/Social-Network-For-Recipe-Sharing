import datetime as dt


def cart_count(request):
    if request.user.is_authenticated:
        count = request.user.carts.all().count()
    else:
        count = None
    return {'count_cart': count}


def year(request):
    return {'year': dt.datetime.today().year}
