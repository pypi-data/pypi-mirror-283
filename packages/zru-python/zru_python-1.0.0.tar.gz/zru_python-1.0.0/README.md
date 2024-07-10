# ZRU Python


# Overview

ZRU Python provides integration access to the ZRU API.

[![Coverage Status](https://coveralls.io/repos/github/zru/zru-python/badge.svg?branch=master)](https://coveralls.io/github/zru/zru-python?branch=master)

# Installation

You can install using `pip`:

    pip install --upgrade zru-python
    
or `easy_install`

    easy_install --upgrade zru-python

or to install from source, run:

    python setup.py install

# Migration Guide for Versions Prior to 1.x.x

If you are migrating from a version prior to 1.x.x, you will need to update your import statements to reflect the change from mc2p to zru. Here is a guide to help you make these changes.

### Updating Import Statements

For any imports that used the mc2p module, replace mc2p with zru.

#### Example

Before:

    from mc2p.errors import InvalidRequestError

After:

    from zru.errors import InvalidRequestError

### Updating Client class

Replace MC2PClient with ZRUClient.

#### Example

Before:

    client = MC2PClient(...)

After:

    client = ZRUClient(...)

### Steps to Update Your Code

1.  Search and Replace: Use your IDE or a text editor to search for mc2p and replace it with zru.
2.  Verify Imports: Ensure all import statements now reference zru.
3.  Run Tests: Run your test suite to verify that your code is functioning correctly with the updated imports.

## Summary

By following these steps, you can successfully migrate your project from versions prior to 1.x.x, ensuring compatibility with the new zru module naming convention.

# Quick Start Example

    from zru import ZRU
    
    zru = ZRUClient('KEY', 'SECRET_KEY')
    
    # Create transaction
    transaction = zru.Transaction({
        "currency": "EUR",
        "products": [{
            "amount": 1,
            "product_id": "PRODUCT-ID"
        }]
    })
    # or with product details
    transaction = zru.Transaction({
        "currency": "EUR",
        "products": [{
            "amount": 1,
            "product": {
                "name": "Product",
                "price": 5
            }
        }]
    })
    transaction.save()
    transaction.pay_url # Send user to this url to pay
    transaction.iframe_url # Use this url to show an iframe in your site

    # Get plans
    plans_paginator = zru.plan.list()
    plans_paginator.count
    plans_paginator.results # Application's plans
    plans_paginator.get_next_list()
    
    # Get product, change and save
    product = zru.Product.get("PRODUCT-ID")
    product.price = 10
    product.save()
    
    # Create and delete tax
    tax = zru.Tax({
        "name": "Tax",
        "percent": 5
    })
    tax.save()
    tax.delete()
    
    # Check if transaction was paid
    transaction = zru.Transaction.get("TRANSACTION-ID")
    transaction.status == 'D' # Paid
    
    # Create subscription
    subscription = zru.Subscription({
        "currency": "EUR",
        "plan_id": "PLAN-ID",
        "note": "Note example"
    })
    # or with plan details
    subscription = zru.Subscription({
        "currency": "EUR",
        "plan": {
            "name": "Plan",
            "price": 5,
            "duration": 1,
            "unit": "M",
            "recurring": True
        },
        "note": "Note example"
    })
    subscription.save()
    subscription.pay_url # Send user to this url to pay
    subscription.iframe_url # Use this url to show an iframe in your site

    # Receive a notification
    notification_data = zru.NotificationData(JSON_DICT_RECEIVED_FROM_ZRU)
    notification_data.is_status_done # Paid
    notification_data.transaction # Transaction Paid
    notification_data.sale # Sale generated

# Exceptions
    
    from zru.errors import InvalidRequestError
    
    # Incorrect data
    shipping = zru.Shipping({
        "name": "Normal shipping",
        "price": "text" # Price must be number
    })
    try:
        shipping.save()
    except InvalidRequestError as e:
        e._message # Status code of error
        e.json_body # Info from server
        e.resource # Resource used to make the server request
        e.resource_id # Resource id requested