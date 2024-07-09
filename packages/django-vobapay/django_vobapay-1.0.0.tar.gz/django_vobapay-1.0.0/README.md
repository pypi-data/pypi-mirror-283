Django Vobapay
============================

Implementation of [Vobapay API](https://www.vobapay.de).
The following doc explain how to set up the Vobapay API for django.

## How to install django-vobapay?

There are just two steps needed to install django-vobapay:

1. Install django-vobapay to your virtual env:

	```bash
	pip install django-vobapay
	```

2. Configure your django installation with the following lines:

	```python
    # django-vobapay
    INSTALLED_APPS += ('django_vobapay', )

	```

    There is a list of other settings you could set down below.

3. Include the notification View in your URLs:

	```python
    # urls.py
    from django.conf.urls import include, url

    urlpatterns = [
        url('^vobapay/', include('django_vobapay.urls')),
    ]
	```

## What do you need for django-vobapay?

1. An merchant account for Vobapay
2. Django >= 2.2

## Usage

### Minimal Checkout init example:

```python
from django_vobapay.wrappers import VobapayWrapper
vobapay_wrapper = VobapayWrapper()

vobapay_transaction = vobapay_wrapper.start_transaction(
    merchant_tx_id='first-test',
    amount=1000,  # 10 Euro 
    purpose='first test'
)
```

## Copyright and license

Copyright 2024 Particulate Solutions GmbH, under [MIT license](https://github.com/ParticulateSolutions/django-vobapay/blob/master/LICENSE).