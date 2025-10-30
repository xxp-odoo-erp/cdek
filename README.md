# CDEK Python SDK v2

Python library for working with CDEK API version 2.0

## Installation

```bash
pip install cdek
```

## Quick Start

### Creating a Client

```python
from cdek import CdekClient

# Create a test client
client = CdekClient('TEST')

# Create a production client
client = CdekClient('PROD', account='your_account', secure='your_password')
```

### Getting List of Cities

```python
# Get list of cities with filtering
cities = client.get_cities({'size': 10, 'city': 'Moscow'})

for city in cities:
    print(f"{city.get('city')} - {city.get('code')}")
```

### Calculating Tariff

```python
from cdek.requests.tariff import Tariff

# Create tariff calculation object
tariff = Tariff()
tariff.set_type(1)  # Delivery type (1 - courier delivery)
tariff.set_tariff_code(136)  # Tariff code
tariff.set_city_codes(44, 137)  # Sender and recipient city codes
tariff.set_package_weight(1000)  # Weight in grams

# Calculate tariff
result = client.calculate_tariff(tariff)
print(f"Cost: {result.get_total_sum()}")
print(f"Delivery time: {result.get_delivery_period()}")
```

### Creating an Order

```python
from cdek.requests.order import Order
from cdek.requests.location import Location
from cdek.requests.contact import Contact
from cdek.requests.package import Package
from cdek.requests.item import Item
from cdek.requests.money import Money
from cdek.requests.phone import Phone

# Create order
order = Order()

# Order number in shop system
order.set_im_number('ORDER-12345')

# Sender
sender_location = Location()
sender_location.set_code(44)  # Moscow city code
order.set_sender_location(sender_location)

sender_contact = Contact()
sender_contact.set_name('Ivan Ivanov')
sender_phone = Phone()
sender_phone.set_number('+79000000000')
sender_contact.set_phone(sender_phone)
order.set_sender(sender_contact)

# Recipient
recipient_location = Location()
recipient_location.set_code(137)  # Saint Petersburg city code
order.set_recipient_location(recipient_location)

recipient_contact = Contact()
recipient_contact.set_name('Petr Petrov')
recipient_phone = Phone()
recipient_phone.set_number('+79111111111')
recipient_contact.set_phone(recipient_phone)
order.set_recipient(recipient_contact)

# Package
package = Package()
package.set_number('1')
package.set_weight(1000)  # Weight in grams
package.set_length(10)  # Length in cm
package.set_width(10)  # Width in cm
package.set_height(10)  # Height in cm

# Item
item = Item()
item.set_name('Test Item')
item.set_ware_key('12345')
item.set_amount(1)
item.set_cost(1000)  # Cost in rubles

money = Money()
money.set_sum(1000)
money.set_sum_nds(200)
item.set_payment(money)

package.set_items([item])
order.set_packages([package])

# Order parameters
order.set_type(1)  # Delivery type
order.set_tariff_code(136)  # Tariff code

# Create order
result = client.create_order(order)
print(f"Order created: {result.get_entity().get_uuid()}")
```

### Getting Order Information

```python
# By tracking number
order_info = client.get_order_info_by_cdek_number('GRZ123456')

# By shop order number
order_info = client.get_order_info_by_im_number('ORDER-12345')

# By order UUID
order_info = client.get_order_info_by_uuid('order-uuid')
```

### Getting PDF Documents

```python
# Get barcode
barcode_pdf = client.get_barcode_pdf('barcode-uuid')
with open('barcode.pdf', 'wb') as f:
    f.write(barcode_pdf)

# Get invoice
invoice_pdf = client.get_invoice_pdf('invoice-uuid')
with open('invoice.pdf', 'wb') as f:
    f.write(invoice_pdf)
```

## Main Features

- ✅ Automatic authorization with token caching
- ✅ Get directories (regions, cities, pickup points)
- ✅ Calculate delivery costs
- ✅ Create and manage orders
- ✅ Get order information
- ✅ Work with invoices and barcodes
- ✅ Create courier agreements
- ✅ Courier pickup requests
- ✅ Webhook management
- ✅ Get registries and payments
- ✅ Get receipts
- ✅ Full support for CDEK API v2

## Error Handling

```python
from cdek.exceptions import CdekException, CdekAuthException, CdekRequestException

try:
    result = client.get_cities({'size': 10})
except CdekAuthException as e:
    print(f"Authorization error: {e}")
except CdekRequestException as e:
    print(f"Request error: {e}")
    print(f"Status code: {e.status_code}")
except CdekException as e:
    print(f"General error: {e}")
```

## Saving Authorization Token

To reduce the number of authorization requests, you can save the token:

```python
def save_token(data):
    # Save token (to database, file, etc.)
    with open('token.json', 'w') as f:
        import json
        json.dump(data, f)

def load_token():
    # Load token
    try:
        with open('token.json', 'r') as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return None

# Load saved token
token_data = load_token()
if token_data:
    client.set_memory(token_data['cdekAuth'], save_token)

# Create client
client = CdekClient('PROD', account='your_account', secure='your_password')
```

## Documentation

Full CDEK API documentation is available at [https://apidoc.cdek.ru](https://apidoc.cdek.ru)

## License

MIT License

## Support

If you have questions or issues, create an issue in the [GitHub repository](https://github.com/cdek/sdk-python)
