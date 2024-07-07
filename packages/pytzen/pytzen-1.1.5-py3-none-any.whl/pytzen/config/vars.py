'''The `Config` class in Python is designed to manage configuration 
files across different formats including JSON, TOML, and YAML. It 
dynamically reads configuration data from a specified path and returns 
an object containing configuration properties, tailored to the file 
format. Through its methods, it can handle different file extensions by 
identifying the type and loading the content accordingly. This approach 
simplifies the process of accessing varied configuration data in a 
uniform manner, allowing for easy integration and manipulation of 
settings within Python applications.'''


import json
import tomllib
import yaml

class Config:
    """
    A class to handle configuration files in JSON, TOML, or YAML 
    formats.

    Attributes:
        path (str): The file path to the configuration file.
    """
    
    def __init__(self, path: str = None) -> None:
        """
        Initializes the Config object with the path to the configuration 
        file.
        
        Args:
            path (str, optional): The file path to the configuration 
            file. Defaults to None.
        """
        self.path = path
    
    def get(self):
        """
        Retrieves the configuration based on the file extension and 
        returns a CONFIG object.
        
        Returns:
            object: An instance of a dynamically created CONFIG class 
            containing configuration properties.
        """
        if '.json' in self.path:
            return self.json_config()
        if '.toml' in self.path:
            return self.toml_config()
        if '.yml' in self.path or '.yaml' in self.path:
            return self.yaml_config()

    def json_config(self) -> object:
        """
        Reads a JSON configuration file and returns a CONFIG object.

        Returns:
            object: An instance of a dynamically created CONFIG class 
            containing JSON configuration properties.
        """
        with open(self.path, "r") as file:
            config = json.load(file)
            return type("JSON", (object,), config)
    
    def toml_config(self) -> object:
        """
        Reads a TOML configuration file and returns a CONFIG object.

        Returns:
            object: An instance of a dynamically created CONFIG class 
            containing TOML configuration properties.
        """
        with open(self.path, "r") as file:
            config = tomllib.load(file)
            return type("TOML", (object,), config)
    
    def yaml_config(self) -> object:
        """
        Reads a YAML configuration file and returns a CONFIG object.

        Returns:
            object: An instance of a dynamically created CONFIG class 
            containing YAML configuration properties.
        """
        with open(self.path, "r") as file:
            config = yaml.safe_load(file)
            return type("YAML", (object,), config)
