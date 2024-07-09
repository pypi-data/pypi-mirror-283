import logging
from typing import Dict, Union, Any, TypeVar
import requests
from .http_client import HTTPClient
from .exceptions import APIClientError
from .config import  APIOption, APIID,ObservationDataSchemaType, ObservationRecordSchemaType

T = TypeVar('T')

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.logger = logging.getLogger(__name__)

    def _get_full_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def authenticate(self, auth_endpoint, auth_data):
        url = self._get_full_url(auth_endpoint)
        response = HTTPClient.post(url, headers=self.headers, json=auth_data)
        token = response.json().get("token")
        if token:
            self.headers['Authorization'] = f"Bearer {token}"

    def get(self, endpoint, params=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.post(url, headers=self.headers, json=json)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None):
        url = self._get_full_url(endpoint)
        response = HTTPClient.put(url, headers=self.headers, json=json)
        return self._handle_response(response)

    def delete(self, endpoint):
        url = self._get_full_url(endpoint)
        response = HTTPClient.delete(url, headers=self.headers)
        return self._handle_response(response)

    def get_record(self, host: str, scope: str, scope_id: Union[int, str], schema: str, record_id: Union[int, str], *options: APIOption):
        url = f"{host}/scopes/{scope}/{scope_id}/records/{schema}/{record_id}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self._handle_response(response)

    # =======================
        # Permission Scopes
    # =======================
    
    def get_scope(self, host: str, scope: str, scope_id: APIID,  *options: APIOption) -> Dict[str, Any]:
        """
        Gets the record representing the scope with the id of scope_id.
        
        Args:
            host (str): The scheme and host of the Platform API. Should be of the format https://host.
            scope (str): The scope to operate under.
            scope_id (APIID): The id of the scope. This can be undefined or SCOPE_ID_SELF for all scopes except STUDY and ORGANIZATION.
            *options (APIOption): Set of API options for configuring the request.
        
        Returns:
            Dict[str, Any]: The response payload from the API.
        
        Raises:
            APIError: If the API request fails.
        """
        
        url = f"{host}/scopes/{scope}/{scope_id}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self.parse_json(response)
    
    def get_scopes(self, host: str, scope: str, *options: APIOption) -> Any:
        """
        Gets a subset of records representing scopes.

        Args:
            host (str): The scheme and host of the Platform API. Should be of the format https://host
            scope {str}: The scope records to find
             *options (APIOption): Set of API options for configuring the request.

        Returns:
            Dict[str, Any]: he response payload from the API.
        Raises:
            APIError: If the API request fails.
        """
        
        url = f"{host}/scopes/{scope}"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self.parse_json(response)
    
    def get_available_plugins(self, host:str, scope:str, scope_id:APIID, *options: APIOption) -> Dict[str, Any]:
        """
        Gets a list of records using a set of query params

        Args:
            host (str): The scheme and host of the Platform API. Should be of the format https://host
            scope (str): The scope to operate under
            scope_id (APIID): The id of the scope. This can be undefined or SCOPE_ID_SELF for all scopes except STUDY and ORGANIZATION
        
        Raises:
            TypeError:  APIError: If the API request fails.
        Returns:
            Dict[str, Any]: he response payload from the API.
        """
        url = f"{host}/scopes/{scope}/{scope_id}/plugins/available"
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)

        response = HTTPClient.get(url, headers=headers, params=params)
        return self.parse_json(response)
    # =======================
        # Observational Data
    # =======================
    def get_observation(self, host:str, scope: str, scopeID: APIID, dataSchema: ObservationDataSchemaType, observationUUID: APIID, *options: APIOption ):
        """
        Gets an individual observation with the given data schema and matching UUID.
        
        Args:
            host (str):         The scheme and host of the Platform API. Should be of the format https://host
            scope (str):        The scope to operate under
            scopeID (APIID)     The id of the scope. This can be undefined or SCOPE_ID_SELF for all scopes except STUDY and ORGANIZATION
            dataSchema:          The schema of the observation
            observationUUID:     The id of the observation
            options:         Set of API options for configuring the request
            
        Returns:
            Dict[str, Any]: The response payload from the API.
        
        Raises:
            APIError: If the API request fails.
        """
        
        if not isinstance(dataSchema, str) or dataSchema not in ObservationDataSchemaType.__args__:
            raise TypeError(f"dataSchema must be one of {len(ObservationDataSchemaType.__args__)} allowed values")
        
        url = f"{host}/scopes/{scope}/{scopeID}/observations/{dataSchema}/{observationUUID}"
    
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)
                
        response = HTTPClient.get(url, headers=headers, params=params)
        
        return self.parse_json(response)
    
    def get_observations(self, host:str, scope: str, scopeID: APIID, dataSchema: ObservationDataSchemaType, *options: APIOption ):
        """
        Gets a list of observation within the scope using a set of query params
        
        Args:
            host (str):         The scheme and host of the Platform API. Should be of the format https://host
            scope (str):            The scope to operate under
            scopeID (APIID)   		The id of the scope. This can be undefined or SCOPE_ID_SELF for all scopes except STUDY and ORGANIZATION
            dataSchema        The schema of the observation
            observationUUID          The id of the observation
            options         Set of API options for configuring the request
            
        Returns:
            Dict[str, Any]: The response payload from the API.
        
        Raises:
            APIError: If the API request fails.
        """
        
        if not isinstance(dataSchema, str) or dataSchema not in ObservationDataSchemaType.__args__:
            raise TypeError(f"dataSchema must be one of {len(ObservationDataSchemaType.__args__)} allowed values")
        
        url = f"{host}/scopes/{scope}/{scopeID}/observations/{dataSchema}"
    
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)
                
        response = HTTPClient.get(url, headers=headers, params=params)
        
        return self.parse_json(response)
    
    def get_record_observations(self, host: str, scope: str, scope_id: APIID, record_schema: ObservationRecordSchemaType, record_id: APIID, data_schema: ObservationDataSchemaType, *options: APIOption):
        """
        Gets a list of observation related to the record using a set of query params
        
        Args:
            host (str):  The scheme and host of the Platform API. Should be of the format https://host
            scope (str): The scope to operate under
            scope_id (APIID): The id of the scope. This can be undefined or SCOPE_ID_SELF for all scopes except STUDY and ORGANIZATION
            record_schema (any): The schema of the record the observations are related to
            record_id (any): The id of the record
            data_schema (any): The schema of the data within the observation
            options: A set options for customizing the API request

        Raises:
            APIError: If the API request fails.
        Returns:
            Dict[str, Any]: The response payload from the API.
        """
        
        if not isinstance(data_schema, str) or data_schema not in ObservationDataSchemaType.__args__:
            raise TypeError(f"dataSchema must be one of {len(ObservationDataSchemaType.__args__)} allowed values")
        
        if not isinstance(record_schema, str) or record_schema not in ObservationRecordSchemaType.__args__:
            raise TypeError(f"recordSchema must be one of {len(ObservationRecordSchemaType.__args__)} allowed values")
        
        url = f"{host}/scopes/{scope}/{scope_id}/records/{record_schema}/{record_id}/observations/{data_schema}"
    
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)
                
        response = HTTPClient.get(url, headers=headers, params=params)
        
        return self.parse_json(response)
        
     # =======================
        # Platform Migration
    # =======================
    def get_migration_status(self, host:str, *options: APIOption)->Dict[str,any]:
        """
        Gets the migration status of the platform
        
        Args:
            host (str): The scheme and host of the Platform API. Should be of the format https://host

        Raises:
            APIError: If the API request fails.
        Returns:
            Dict[str, Any]: The response payload from the API.
        """
        url = f"{host}/migration/status"
    
        headers = self.headers.copy()
        params = {}

        for option in options:
            if option.header:
                headers.update(option.header)
            if option.param:
                params.update(option.param)
                
        response = HTTPClient.get(url, headers=headers, params=params)
        
        return self.parse_json(response)
    # =======================
        #
    # =======================
    def parse_json(self, response: requests.Response) -> Any:
        try:
            if response.status_code in (200, 201, 202):
                if response.headers.get('Content-Length') == '0':
                    return response.text
                return response.json()
            else:
                self.parse_error(response)
        except ValueError as e:
            raise APIClientError(f"JSON decoding failed: {str(e)}", response)

    def parse_error(self, response: requests.Response):
        error_body = {
            "status": response.status_code,
            "statusText": response.reason,
            "userText": "The platform is currently being worked on"
        }
        raise APIClientError(f"Error: {response.status_code} - {response.text}", response, error_body)

    def _handle_response(self, response):
        if response.status_code >= 400:
            self.logger.error(f"Error: {response.status_code} - {response.text}")
            raise APIClientError(f"Error: {response.status_code} - {response.text}")
        return response.json()