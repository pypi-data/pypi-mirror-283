# Targeting Platform

![Pypi Version](https://img.shields.io/pypi/v/targeting-platform)
![Python Version](https://img.shields.io/pypi/pyversions/targeting-platform)
![License](https://img.shields.io/pypi/l/targeting-platform)

## Prerequsites

To use module following tools need to be configured:

- **Redis** - is used for caching platfrom information (catalog of lineitems/adgroups e.g.). It depends on amount of information in your platfrom but as a starting point 1Gb memory will be enough. For now only single entrypoint is supported. Prefix for key is `PLATFORM_CACHE_` (set in [CACHE_KEYS_PREFIX](https://gitlab.com/dsp6802915/targeting_platform/-/tree/main/src/targeting_platform/utils_cache.py#L17)).

### Credentials for platfroms

Each platfrom has it's own format of credentials. You need to obtaint credetantial before starting to use platfroms thorugh this module.

#### DV360 (dv360)

Requires service account private key (whole JSON for service account). E.g.

```JSON
{
    "type": "service_account",
    "project_id": "",
    "private_key_id": "",
    "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
    "client_email": "",
    "client_id": "",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": ""
}
```

#### Meta (Facebook) (meta)

Example of credentails (`app_scoped_system_user_id` is required for detailed access validation):

```JSON
{
    "access_token": "",
    "app_scoped_system_user_id":
}
```

#### The Trade Desk (ttd)

Example of credentials (login and password is required for automatic token renewal):

```JSON
{
    "PartnerId": "",
    "token": "",
    "Login": "",
    "Password": ""
}
```

## How to use

See examples in [integration tests](https://gitlab.com/dsp6802915/targeting_platform/-/tree/main/tests/integration).

You can adopt these tests by placing appropriate sectet files into folder `secrets`.
