# -*- coding: utf-8 -*-

from typing import Any
import os,requests
from fosforml.constants import connection_manager_url

class snowflakesession:
    def __init__(self):
        self.connection_params = None
        self.session = None
        self._connection_details()

    def _connection_details(self):
        if not self.connection_params:
            project_id = os.getenv('PROJECT_ID')
            if not project_id:
                raise ValueError("PROJECT_ID not set")
            if not connection_manager_url:
                raise ValueError("CONNECTION_MANAGER_BASE_URL not set")
            
            url = f"{connection_manager_url}/connections/api/ConnectionManager/v1/allConnections?projectId={project_id}"

            self.connection_params = requests.get(url, verify=False).json()
        
    def get_session(self):
        if not self.session:
            try:
                connection_details=self.connection_params[0]["connectionDetails"]
                connection_parameters = {
                    'account':f"{connection_details['accountName']}.{connection_details['region']}.{connection_details['cloudPlatform']}",
                    "user": connection_details["dbUserName"],
                    "password": connection_details["dbPassword"],
                    "database": connection_details["defaultDb"],
                    "schema": connection_details["defaultSchema"],
                    "warehouse": connection_details["wareHouse"],
                    "role": connection_details["role"],
                }
                connection_parameters = self.validate_connection_params(connection_parameters)

                ## snowflake session creation
                from snowflake.snowpark import Session
                self.session = Session.builder.configs(connection_parameters).create()
            except Exception as e:
                raise Exception(f"Failed to create snowflake session. {str(e)}")
            
        return self.session
    
    @staticmethod
    def validate_connection_params(connection_params):
        if not connection_params["account"]:
            raise ValueError("Account name is required")
        if not connection_params["user"]:
            raise ValueError("Username is required")
        if not connection_params["password"]:
            raise ValueError("Password is required")
        if not connection_params["database"]:
            raise ValueError("Database is required")
        if not connection_params["schema"]:
            raise ValueError("Schema is required")
        if not connection_params["warehouse"]: 
            raise ValueError("Warehouse is required")
        if not connection_params["role"]:
            raise ValueError("Role is required")
        
        return connection_params
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.session:
            return self.get_session()
        
        return self.session

    def __enter__(self):
        if not self.session:
            return self.get_session()
        return self.session
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise Exception(exc_type, exc_value, traceback)
        
        if self.session:
            self.session.close()

    def execute(self, query):
        pass

    def close(self):
        pass


def get_session():
    session_obj = snowflakesession()
    return session_obj.get_session()