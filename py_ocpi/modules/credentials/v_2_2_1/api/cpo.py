import httpx

from fastapi import APIRouter, Depends, HTTPException, Request, status as fastapistatus
from pydantic import ValidationError

from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core import status
from py_ocpi.core.enums import ModuleID
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.credentials.v_2_2_1.schemas import Credentials

router = APIRouter(
    prefix='/credentials',
)


@router.get("/", response_model=OCPIResponse)
async def get_credentials(request: Request, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.credentials_and_registration,
                              auth_token, version=VersionNumber.v_2_2_1)
        return OCPIResponse(
            data=[adapter.credentials_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.post("/", response_model=OCPIResponse)
async def post_credentials(request: Request, credentials: Credentials,
                           crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        # Check if the client is already registered
        credentials_client_token = credentials.token
        server_cred = await crud.get(ModuleID.credentials_and_registration, credentials_client_token,
                                     version=VersionNumber.v_2_2_1)
        if server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is already registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            authorization_token = f'Token {credentials_client_token}'
            response_versions = await client.get(credentials.url,
                                                 headers={'authorization': authorization_token})

        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()['data']

            for version in versions:
                if version['version'] == VersionNumber.v_2_2_1:
                    version_url = version['url']

            if not version_url:
                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            async with httpx.AsyncClient() as client:
                authorization_token = f'Token {credentials_client_token}'
                response_versions = await client.get(credentials.url,
                                                     headers={'authorization': authorization_token})

                response_endpoints = await client.get(version_url,
                                                      headers={'authorization': authorization_token})

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Store client credentials
                endpoints = response_endpoints.json()['data'][0]
                await crud.create(
                    ModuleID.credentials_and_registration,
                    {
                        "token_b": credentials.token,
                        "version": VersionNumber.v_2_2_1,
                        "endpoints": endpoints
                    },
                    operation='credentials',
                    auth_token=auth_token,
                    version=VersionNumber.v_2_2_1
                )

                # Generate new credentials for sender
                new_credentials = await crud.create(ModuleID.credentials_and_registration,
                                                    {'url': version_url}, operation='registration',
                                                    auth_token=auth_token, version=VersionNumber.v_2_2_1)

                return OCPIResponse(
                    data=[adapter.credentials_adapter(new_credentials).dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE
                )

    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/", response_model=OCPIResponse)
async def update_credentials(request: Request, credentials: Credentials,
                             crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        # Check if the client is already registered
        credentials_client_token = credentials.token
        server_cred = await crud.get(ModuleID.credentials_and_registration, credentials_client_token,
                                     auth_token=auth_token, version=VersionNumber.v_2_2_1)
        if not server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is not registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            authorization_token = f'Token {credentials_client_token}'
            response_versions = await client.get(credentials.url, headers={'authorization': authorization_token})
        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()['data']

            for version in versions:
                if version['version'] == VersionNumber.v_2_2_1:
                    version_url = version['url']

            if not version_url:
                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            async with httpx.AsyncClient() as client:
                authorization_token = f'Token {credentials_client_token}'
                response_versions = await client.get(credentials.url,
                                                     headers={'authorization': authorization_token})

                response_endpoints = await client.get(version_url,
                                                      headers={'authorization': authorization_token})

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Update server credentials to access client's system
                endpoints = response_endpoints.json()['data'][0]
                await crud.update(ModuleID.credentials_and_registration,
                                  {
                                      "token_b": credentials.token,
                                      "version": VersionNumber.v_2_2_1,
                                      "endpoints": endpoints
                                  },
                                  operation='credentials',
                                  auth_token=auth_token,
                                  version=VersionNumber.v_2_2_1)

                # Generate new credentials token
                new_credentials = await crud.update(ModuleID.credentials_and_registration,
                                                    {'url': version_url}, auth_token=auth_token,
                                                    operation='registration',
                                                    version=VersionNumber.v_2_2_1)
                return OCPIResponse(
                    data=[adapter.credentials_adapter(new_credentials).dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE
                )

    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
