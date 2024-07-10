# compute_api_client.TransactionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_transaction_transactions_id_get**](TransactionsApi.md#read_transaction_transactions_id_get) | **GET** /transactions/{id} | Retrieve transactions
[**read_transactions_transactions_get**](TransactionsApi.md#read_transactions_transactions_get) | **GET** /transactions/ | List transactions


# **read_transaction_transactions_id_get**
> Transaction read_transaction_transactions_id_get(id)

Retrieve transactions

Get transaction by ID.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.transaction import Transaction
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.TransactionsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve transactions
        api_response = await api_instance.read_transaction_transactions_id_get(id)
        print("The response of TransactionsApi->read_transaction_transactions_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->read_transaction_transactions_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Transaction**](Transaction.md)

### Authorization

[user_bearer](../README.md#user_bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_transactions_transactions_get**
> List[Transaction] read_transactions_transactions_get(latest=latest, sort_by=sort_by, page_number=page_number, items_per_page=items_per_page, id=id, domain__isnull=domain__isnull, domain=domain, job__isnull=job__isnull, job=job, team_id=team_id, member_id__isnull=member_id__isnull, member_id=member_id, change=change, timestamp=timestamp)

List transactions

Read transactions.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.domain import Domain
from compute_api_client.models.transaction import Transaction
from compute_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
async with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.TransactionsApi(api_client)
    latest = True # bool |  (optional)
    sort_by = 'sort_by_example' # str |  (optional)
    page_number = 56 # int |  (optional)
    items_per_page = 56 # int |  (optional)
    id = 56 # int |  (optional)
    domain__isnull = True # bool |  (optional)
    domain = compute_api_client.Domain() # Domain |  (optional)
    job__isnull = True # bool |  (optional)
    job = 56 # int |  (optional)
    team_id = 56 # int |  (optional)
    member_id__isnull = True # bool |  (optional)
    member_id = 56 # int |  (optional)
    change = 56 # int |  (optional)
    timestamp = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # List transactions
        api_response = await api_instance.read_transactions_transactions_get(latest=latest, sort_by=sort_by, page_number=page_number, items_per_page=items_per_page, id=id, domain__isnull=domain__isnull, domain=domain, job__isnull=job__isnull, job=job, team_id=team_id, member_id__isnull=member_id__isnull, member_id=member_id, change=change, timestamp=timestamp)
        print("The response of TransactionsApi->read_transactions_transactions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->read_transactions_transactions_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **sort_by** | **str**|  | [optional] 
 **page_number** | **int**|  | [optional] 
 **items_per_page** | **int**|  | [optional] 
 **id** | **int**|  | [optional] 
 **domain__isnull** | **bool**|  | [optional] 
 **domain** | [**Domain**](.md)|  | [optional] 
 **job__isnull** | **bool**|  | [optional] 
 **job** | **int**|  | [optional] 
 **team_id** | **int**|  | [optional] 
 **member_id__isnull** | **bool**|  | [optional] 
 **member_id** | **int**|  | [optional] 
 **change** | **int**|  | [optional] 
 **timestamp** | **datetime**|  | [optional] 

### Return type

[**List[Transaction]**](Transaction.md)

### Authorization

[user_bearer](../README.md#user_bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

