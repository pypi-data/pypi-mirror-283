
def get_request_ips(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ips = x_forwarded_for.split(",")
        ips = map(str.strip, ips)
    else:
        ips = [request.META.get("REMOTE_ADDR")]

    return ips
