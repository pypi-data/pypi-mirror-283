from django.conf import settings
from django_vobapay.__init__ import __version__

DJANGO_VOBAPAY_VERSION = __version__


class VOBAPAY_PAYMENT_METHODS:
    """
    vobapay payment methods
    """
    CREDIT_CARD = 'CREDIT_CARD'
    PAYPAL = 'PAYPAL'
    SEPA = 'SEPA'


VOBAPAY_VALID_TRANSACTION_STATUSES = [4000]

# TODO currently we only know the staging URL
VOBAPAY_API_BASE_URL = getattr(settings, 'VOBAPAY_API_BASE_URL', 'https://staging-paymentconverter.vobapay.de/vobapaycheckout/api/')
VOBAPAY_API_URL = VOBAPAY_API_BASE_URL + 'transaction/start'
VOBAPAY_API_STATUS_URL = VOBAPAY_API_BASE_URL + 'transaction/status'

# checkout urls
VOBAPAY_RETURN_URL = getattr(settings, 'VOBAPAY_RETURN_URL', '/vobapay/return/')
VOBAPAY_SUCCESS_URL = getattr(settings, 'VOBAPAY_SUCCESS_URL', '/')
VOBAPAY_ERROR_URL = getattr(settings, 'VOBAPAY_ERROR_URL', '/')
VOBAPAY_CANCELLATION_URL = getattr(settings, 'VOBAPAY_CANCELLATION_URL', '/')
VOBAPAY_NOTIFICATION_URL = getattr(settings, 'VOBAPAY_NOTIFICATION_URL', '/vobapay/notify/')

