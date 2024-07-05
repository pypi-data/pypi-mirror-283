<div align="center">
        <img src="https://github.com/speakeasy-sdks/clerk-ts/assets/68016351/62e27b17-7a99-46cf-a09e-13d2f06f733e" width="250">
   <p>The most comprehensive User Management Platform</p>
   <a href="https://clerk.com/docs/reference/backend-api"><img src="https://img.shields.io/static/v1?label=Docs&message=API Ref&color=000000&style=for-the-badge" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" /></a>
</div>
<br></br>

The Clerk Python library provides convenient access to the Clerk REST API from any Python application 3.0+. The library includes type definitions for all request params and response fields, and offers synchronous and asynchronous support powered by [httpx](https://www.python-httpx.org/)

> ⚠️ **Warning**
>
> This is a pre production SDK that has not yet been published to PYPI.

<!-- Start SDK Installation [installation] -->
## SDK Installation

PIP
```bash
pip install clerk-dev
```

Poetry
```bash
poetry add clerk-dev
```
<!-- End SDK Installation [installation] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from clerk_dev import Clerk

s = Clerk(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.email_addresses.get(email_address_id="email_address_id_example")

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from clerk_dev import Clerk

async def main():
    s = Clerk(
        bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
    )
    res = await s.email_addresses.get_async(email_address_id="email_address_id_example")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [actor_tokens](docs/sdks/actortokens/README.md)

* [create](docs/sdks/actortokens/README.md#create) - Create actor token
* [revoke](docs/sdks/actortokens/README.md#revoke) - Revoke actor token

### [allowlist_identifiers](docs/sdks/allowlistidentifiers/README.md)

* [list](docs/sdks/allowlistidentifiers/README.md#list) - List all identifiers on the allow-list
* [create](docs/sdks/allowlistidentifiers/README.md#create) - Add identifier to the allow-list
* [delete](docs/sdks/allowlistidentifiers/README.md#delete) - Delete identifier from allow-list

### [beta_features](docs/sdks/betafeatures/README.md)

* [~~update_production_instance_domain~~](docs/sdks/betafeatures/README.md#update_production_instance_domain) - Update production instance domain :warning: **Deprecated**
* [update_instance_auth_config](docs/sdks/betafeatures/README.md#update_instance_auth_config) - Update instance settings
* [change_production_instance_domain](docs/sdks/betafeatures/README.md#change_production_instance_domain) - Update production instance domain

### [blocklist_identifiers](docs/sdks/blocklistidentifierssdk/README.md)

* [list](docs/sdks/blocklistidentifierssdk/README.md#list) - List all identifiers on the block-list
* [create](docs/sdks/blocklistidentifierssdk/README.md#create) - Add identifier to the block-list
* [delete](docs/sdks/blocklistidentifierssdk/README.md#delete) - Delete identifier from block-list

### [clients](docs/sdks/clients/README.md)

* [~~list~~](docs/sdks/clients/README.md#list) - List all clients :warning: **Deprecated**
* [get](docs/sdks/clients/README.md#get) - Get a client
* [verify](docs/sdks/clients/README.md#verify) - Verify a client

### [domains](docs/sdks/domainssdk/README.md)

* [list](docs/sdks/domainssdk/README.md#list) - List all instance domains
* [add](docs/sdks/domainssdk/README.md#add) - Add a domain
* [delete](docs/sdks/domainssdk/README.md#delete) - Delete a satellite domain
* [update](docs/sdks/domainssdk/README.md#update) - Update a domain

### [email_addresses](docs/sdks/emailaddresses/README.md)

* [create](docs/sdks/emailaddresses/README.md#create) - Create an email address
* [delete](docs/sdks/emailaddresses/README.md#delete) - Delete an email address
* [get](docs/sdks/emailaddresses/README.md#get) - Retrieve an email address
* [update](docs/sdks/emailaddresses/README.md#update) - Update an email address

### [instance_settings](docs/sdks/instancesettingssdk/README.md)

* [update](docs/sdks/instancesettingssdk/README.md#update) - Update instance settings
* [update_organization_settings](docs/sdks/instancesettingssdk/README.md#update_organization_settings) - Update instance organization settings
* [update_restrictions](docs/sdks/instancesettingssdk/README.md#update_restrictions) - Update instance restrictions

### [invitations](docs/sdks/invitations/README.md)

* [list](docs/sdks/invitations/README.md#list) - List all invitations
* [create](docs/sdks/invitations/README.md#create) - Create an invitation
* [revoke](docs/sdks/invitations/README.md#revoke) - Revokes an invitation

### [jwks](docs/sdks/jwks/README.md)

* [get](docs/sdks/jwks/README.md#get) - Retrieve the JSON Web Key Set of the instance

### [jwt_templates](docs/sdks/jwttemplates/README.md)

* [list](docs/sdks/jwttemplates/README.md#list) - List all templates
* [create](docs/sdks/jwttemplates/README.md#create) - Create a JWT template
* [delete](docs/sdks/jwttemplates/README.md#delete) - Delete a Template
* [get](docs/sdks/jwttemplates/README.md#get) - Retrieve a template
* [update](docs/sdks/jwttemplates/README.md#update) - Update a JWT template

### [o_auth_applications](docs/sdks/oauthapplicationssdk/README.md)

* [list](docs/sdks/oauthapplicationssdk/README.md#list) - Get a list of OAuth applications for an instance
* [create](docs/sdks/oauthapplicationssdk/README.md#create) - Create an OAuth application
* [delete](docs/sdks/oauthapplicationssdk/README.md#delete) - Delete an OAuth application
* [get](docs/sdks/oauthapplicationssdk/README.md#get) - Retrieve an OAuth application by ID
* [update](docs/sdks/oauthapplicationssdk/README.md#update) - Update an OAuth application
* [rotate_secret](docs/sdks/oauthapplicationssdk/README.md#rotate_secret) - Rotate the client secret of the given OAuth application

### [organizations](docs/sdks/organizationssdk/README.md)

* [list](docs/sdks/organizationssdk/README.md#list) - Get a list of organizations for an instance
* [create](docs/sdks/organizationssdk/README.md#create) - Create an organization
* [delete](docs/sdks/organizationssdk/README.md#delete) - Delete an organization
* [get](docs/sdks/organizationssdk/README.md#get) - Retrieve an organization by ID or slug
* [update](docs/sdks/organizationssdk/README.md#update) - Update an organization
* [delete_logo](docs/sdks/organizationssdk/README.md#delete_logo) - Delete the organization's logo.
* [upload_logo](docs/sdks/organizationssdk/README.md#upload_logo) - Upload a logo for the organization
* [merge_metadata](docs/sdks/organizationssdk/README.md#merge_metadata) - Merge and update metadata for an organization

### [organization_invitations](docs/sdks/organizationinvitationssdk/README.md)

* [list](docs/sdks/organizationinvitationssdk/README.md#list) - Get a list of organization invitations
* [create](docs/sdks/organizationinvitationssdk/README.md#create) - Create and send an organization invitation
* [get](docs/sdks/organizationinvitationssdk/README.md#get) - Retrieve an organization invitation by ID
* [revoke](docs/sdks/organizationinvitationssdk/README.md#revoke) - Revoke a pending organization invitation
* [create_bulk](docs/sdks/organizationinvitationssdk/README.md#create_bulk) - Bulk create and send organization invitations
* [~~list_pending~~](docs/sdks/organizationinvitationssdk/README.md#list_pending) - Get a list of pending organization invitations :warning: **Deprecated**

### [organization_memberships](docs/sdks/organizationmembershipssdk/README.md)

* [list](docs/sdks/organizationmembershipssdk/README.md#list) - Get a list of all members of an organization
* [create](docs/sdks/organizationmembershipssdk/README.md#create) - Create a new organization membership
* [delete](docs/sdks/organizationmembershipssdk/README.md#delete) - Remove a member from an organization
* [update](docs/sdks/organizationmembershipssdk/README.md#update) - Update an organization membership
* [update_metadata](docs/sdks/organizationmembershipssdk/README.md#update_metadata) - Merge and update organization membership metadata

### [phone_numbers](docs/sdks/phonenumbers/README.md)

* [create](docs/sdks/phonenumbers/README.md#create) - Create a phone number
* [delete](docs/sdks/phonenumbers/README.md#delete) - Delete a phone number
* [get](docs/sdks/phonenumbers/README.md#get) - Retrieve a phone number
* [update](docs/sdks/phonenumbers/README.md#update) - Update a phone number

### [proxy_checks](docs/sdks/proxychecks/README.md)

* [verify](docs/sdks/proxychecks/README.md#verify) - Verify the proxy configuration for your domain

### [misc](docs/sdks/misc/README.md)

* [get_public_interstitial](docs/sdks/misc/README.md#get_public_interstitial) - Returns the markup for the interstitial page

### [redirect_urls](docs/sdks/redirecturls/README.md)

* [list](docs/sdks/redirecturls/README.md#list) - List all redirect URLs
* [create](docs/sdks/redirecturls/README.md#create) - Create a redirect URL
* [delete](docs/sdks/redirecturls/README.md#delete) - Delete a redirect URL
* [get](docs/sdks/redirecturls/README.md#get) - Retrieve a redirect URL

### [saml_connections](docs/sdks/samlconnectionssdk/README.md)

* [list](docs/sdks/samlconnectionssdk/README.md#list) - Get a list of SAML Connections for an instance
* [create](docs/sdks/samlconnectionssdk/README.md#create) - Create a SAML Connection
* [delete](docs/sdks/samlconnectionssdk/README.md#delete) - Delete a SAML Connection
* [get](docs/sdks/samlconnectionssdk/README.md#get) - Retrieve a SAML Connection by ID
* [update](docs/sdks/samlconnectionssdk/README.md#update) - Update a SAML Connection

### [sessions](docs/sdks/sessions/README.md)

* [list](docs/sdks/sessions/README.md#list) - List all sessions
* [get](docs/sdks/sessions/README.md#get) - Retrieve a session
* [revoke](docs/sdks/sessions/README.md#revoke) - Revoke a session
* [create_token_from_template](docs/sdks/sessions/README.md#create_token_from_template) - Create a session token from a jwt template
* [~~verify~~](docs/sdks/sessions/README.md#verify) - Verify a session :warning: **Deprecated**

### [sign_in_tokens](docs/sdks/signintokens/README.md)

* [create](docs/sdks/signintokens/README.md#create) - Create sign-in token
* [revoke](docs/sdks/signintokens/README.md#revoke) - Revoke the given sign-in token

### [sign_ups](docs/sdks/signups/README.md)

* [update](docs/sdks/signups/README.md#update) - Update a sign-up

### [templates](docs/sdks/templates/README.md)

* [list](docs/sdks/templates/README.md#list) - List all templates
* [get](docs/sdks/templates/README.md#get) - Retrieve a template
* [upsert](docs/sdks/templates/README.md#upsert) - Update a template for a given type and slug
* [preview](docs/sdks/templates/README.md#preview) - Preview changes to a template
* [revert](docs/sdks/templates/README.md#revert) - Revert a template
* [toggle_delivery](docs/sdks/templates/README.md#toggle_delivery) - Toggle the delivery by Clerk for a template of a given type and slug

### [testing_tokens](docs/sdks/testingtokens/README.md)

* [create](docs/sdks/testingtokens/README.md#create) - Retrieve a new testing token

### [users](docs/sdks/users/README.md)

* [list](docs/sdks/users/README.md#list) - List all users
* [create](docs/sdks/users/README.md#create) - Create a new user
* [delete](docs/sdks/users/README.md#delete) - Delete a user
* [get](docs/sdks/users/README.md#get) - Retrieve a user
* [update](docs/sdks/users/README.md#update) - Update a user
* [ban](docs/sdks/users/README.md#ban) - Ban a user
* [lock](docs/sdks/users/README.md#lock) - Lock a user
* [update_metadata](docs/sdks/users/README.md#update_metadata) - Merge and update a user's metadata
* [disable_mfa](docs/sdks/users/README.md#disable_mfa) - Disable a user's MFA methods
* [get_o_auth_access_token](docs/sdks/users/README.md#get_o_auth_access_token) - Retrieve the OAuth access token of a user
* [get_organization_memberships](docs/sdks/users/README.md#get_organization_memberships) - Retrieve all memberships for a user
* [delete_profile_image](docs/sdks/users/README.md#delete_profile_image) - Delete user profile image
* [set_profile_image](docs/sdks/users/README.md#set_profile_image) - Set user profile image
* [unban](docs/sdks/users/README.md#unban) - Unban a user
* [unlock](docs/sdks/users/README.md#unlock) - Unlock a user
* [verify_password](docs/sdks/users/README.md#verify_password) - Verify the password of a user
* [verify_totp](docs/sdks/users/README.md#verify_totp) - Verify a TOTP or backup code for a user
* [count](docs/sdks/users/README.md#count) - Count users

### [webhooks](docs/sdks/webhooks/README.md)

* [delete_svix_app](docs/sdks/webhooks/README.md#delete_svix_app) - Delete a Svix app
* [create_svix_app](docs/sdks/webhooks/README.md#create_svix_app) - Create a Svix app
* [generate_svix_auth_url](docs/sdks/webhooks/README.md#generate_svix_auth_url) - Create a Svix Dashboard URL
<!-- End Available Resources and Operations [operations] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object       | Status Code        | Content Type       |
| ------------------ | ------------------ | ------------------ |
| models.ClerkErrors | 400,402,422        | application/json   |
| models.SDKError    | 4xx-5xx            | */*                |

### Example

```python
from clerk_dev import Clerk, models

s = Clerk(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = None
try:
    res = s.actor_tokens.create(actor={
    "sub": "user_2OEpKhcCN1Lat9NQ0G6puh7q5Rb",
}, user_id="user_1a2b3c", expires_in_seconds=3600, session_max_duration_in_seconds=1800)

except models.ClerkErrors as e:
    # handle exception
    raise(e)
except models.SDKError as e:
    # handle exception
    raise(e)

if res is not None:
    # handle response
    pass

```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://api.clerk.com/v1` | None |

#### Example

```python
from clerk_dev import Clerk

s = Clerk(
    server_idx=0,
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.actor_tokens.create(actor={
    "sub": "user_2OEpKhcCN1Lat9NQ0G6puh7q5Rb",
}, user_id="user_1a2b3c", expires_in_seconds=3600, session_max_duration_in_seconds=1800)

if res is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from clerk_dev import Clerk

s = Clerk(
    server_url="https://api.clerk.com/v1",
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.actor_tokens.create(actor={
    "sub": "user_2OEpKhcCN1Lat9NQ0G6puh7q5Rb",
}, user_id="user_1a2b3c", expires_in_seconds=3600, session_max_duration_in_seconds=1800)

if res is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from clerk_dev import Clerk
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Clerk(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from clerk_dev import Clerk
from clerk_dev.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Clerk(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name          | Type          | Scheme        |
| ------------- | ------------- | ------------- |
| `bearer_auth` | http          | HTTP Bearer   |

To authenticate with the API the `bearer_auth` parameter must be set when initializing the SDK client instance. For example:
```python
from clerk_dev import Clerk

s = Clerk(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.actor_tokens.create(actor={
    "sub": "user_2OEpKhcCN1Lat9NQ0G6puh7q5Rb",
}, user_id="user_1a2b3c", expires_in_seconds=3600, session_max_duration_in_seconds=1800)

if res is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
from clerk_dev import Clerk

s = Clerk(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.organizations.upload_logo(organization_id="org_12345", file={
    "file_name": "your_file_here",
    "content": open("<file_path>", "rb"),
    "content_type": "<value>",
}, uploader_user_id="user_67890")

if res is not None:
    # handle response
    pass

```
<!-- End File uploads [file-upload] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
```python
from clerk_dev import Clerk

s = Clerk(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)


res = s.clients.list(limit=20, offset=10)

if res is not None:
    while True:
        # handle items

        res = res.Next()
        if res is None:
            break


```
<!-- End Pagination [pagination] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release!

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
