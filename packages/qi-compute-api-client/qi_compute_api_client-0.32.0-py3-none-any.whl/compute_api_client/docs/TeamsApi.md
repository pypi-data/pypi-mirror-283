# compute_api_client.TeamsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**read_team_teams_id_get**](TeamsApi.md#read_team_teams_id_get) | **GET** /teams/{id} | Retrieve teams
[**read_teams_teams_get**](TeamsApi.md#read_teams_teams_get) | **GET** /teams/ | List teams


# **read_team_teams_id_get**
> Team read_team_teams_id_get(id)

Retrieve teams

Get team by ID.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.team import Team
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
    api_instance = compute_api_client.TeamsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve teams
        api_response = await api_instance.read_team_teams_id_get(id)
        print("The response of TeamsApi->read_team_teams_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TeamsApi->read_team_teams_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Team**](Team.md)

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

# **read_teams_teams_get**
> List[Team] read_teams_teams_get(latest=latest, sort_by=sort_by, page_number=page_number, items_per_page=items_per_page, id=id, name=name, slug=slug, individual_user=individual_user)

List teams

Read teams.

### Example

* OAuth Authentication (user_bearer):
```python
import time
import os
import compute_api_client
from compute_api_client.models.team import Team
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
    api_instance = compute_api_client.TeamsApi(api_client)
    latest = True # bool |  (optional)
    sort_by = 'sort_by_example' # str |  (optional)
    page_number = 56 # int |  (optional)
    items_per_page = 56 # int |  (optional)
    id = 56 # int |  (optional)
    name = 'name_example' # str |  (optional)
    slug = 'slug_example' # str |  (optional)
    individual_user = True # bool |  (optional)

    try:
        # List teams
        api_response = await api_instance.read_teams_teams_get(latest=latest, sort_by=sort_by, page_number=page_number, items_per_page=items_per_page, id=id, name=name, slug=slug, individual_user=individual_user)
        print("The response of TeamsApi->read_teams_teams_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TeamsApi->read_teams_teams_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **latest** | **bool**|  | [optional] 
 **sort_by** | **str**|  | [optional] 
 **page_number** | **int**|  | [optional] 
 **items_per_page** | **int**|  | [optional] 
 **id** | **int**|  | [optional] 
 **name** | **str**|  | [optional] 
 **slug** | **str**|  | [optional] 
 **individual_user** | **bool**|  | [optional] 

### Return type

[**List[Team]**](Team.md)

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

