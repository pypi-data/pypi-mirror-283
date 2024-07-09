import json
from jsonschema import validate, ValidationError, SchemaError


class InvalidConfigurationError(Exception):
    pass


class Configuration:
    def __init__(self, config_file_path=None):
        self._config_file_path = config_file_path
        self._environ = None
        self._log_enabled = None
        self._log_level = None

    def set_common_config(self, data):
        self._environ = data.get('environ')
        self._log_enabled = data.get('log_enabled')
        self._log_level = data.get('log_level')


class ConfigurationBuilder:
    def __init__(self):
        self._configuration = Configuration()
        self._sql_builder = None
        self._clickhouse_builder = None
        self._aws_builder = None
        self._elastic_builder = None
        self._kafka_builder = None
        self.required_components = []

    def load_from_file(self, file_path, required_components=[]):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.required_components = required_components
                self.validate_json(data)
                self.set_configuration(data)
        except FileNotFoundError:
            raise InvalidConfigurationError(f"Configuration file '{file_path}' not found.")
        except json.JSONDecodeError:
            raise InvalidConfigurationError("Invalid JSON format.")
        except ValidationError as ve:
            raise InvalidConfigurationError(f"JSON validation error: {ve.message}")
        except SchemaError as se:
            raise InvalidConfigurationError(f"JSON schema error: {se.message}")

    def load_from_dict(self, data, required_components=[]):
        try:
            self.required_components = required_components
            self.validate_json(data)
            self.set_configuration(data)
        except ValidationError as ve:
            raise InvalidConfigurationError(f"JSON validation error: {ve.message}")
        except SchemaError as se:
            raise InvalidConfigurationError(f"JSON schema error: {se.message}")

    def validate_json(self, data):
        schema = {
            "type": "object",
            "properties": {
                "environ": {"type": "string"},
                "sql_user_name": {"type": "string"},
                "sql_server_ip": {"type": "string"},
                "sql_pass_word": {"type": "string"},
                "clickhouse_host": {"type": "string"},
                "clickhouse_port": {"type": "string"},
                "clickhouse_username": {"type": "string"},
                "clickhouse_password": {"type": "string"},
                "elastic_host": {"type": "string"},
                "elastic_username": {"type": "string"},
                "elastic_password": {"type": "string"},
                "elastic_mention_index_name": {"type": "string"},
                "elastic_author_index_name": {"type": "string"},
                "opensearch_python_service_endpoint": {"type": "string"},
                "aws_access_key": {"type": "string"},
                "aws_secret_key": {"type": "string"},
                "s3_bucket_name": {"type": "string"},
                "aws_s3_base_url": {"type": "string"},
                "service_ng_api": {"type": "string"},
                "broker": {"type": "string"},
                "read_topic": {"type": "string"},
                "dead_letter_topic_name": {"type": "string"},
                "g_chat_hook": {"type": "string"},
                "g_chat_error_hook": {"type": "string"},
                "log_enabled": {"type": "string"}
            },
            "required": ["environ"]
        }
        validate(instance=data, schema=schema)
        self.validate_required_components(data)

    def validate_required_components(self, data):
        if "sql" in self.required_components:
            if not data.get('sql_user_name') or not data.get('sql_server_ip') or not data.get('sql_pass_word'):
                raise InvalidConfigurationError("Missing SQL configuration properties")

        if "clickhouse" in self.required_components:
            if not data.get('clickhouse_host') or not data.get('clickhouse_port'):
                raise InvalidConfigurationError("Missing ClickHouse configuration properties")

        if "aws" in self.required_components:
            if not data.get('aws_access_key') or not data.get('aws_secret_key'):
                raise InvalidConfigurationError("Missing AWS configuration properties")

        if "elastic" in self.required_components:
            if not data.get('elastic_host') or not data.get('elastic_username') or not data.get('elastic_password'):
                raise InvalidConfigurationError("Missing ElasticSearch configuration properties")

    def set_configuration(self, data):
        self._configuration.set_common_config(data)

        if self._sql_builder:
            self._sql_builder.build(data)
        if self._clickhouse_builder:
            self._clickhouse_builder.build(data)
        if self._aws_builder:
            self._aws_builder.build(data)
        if self._elastic_builder:
            self._elastic_builder.build(data)
        if self._kafka_builder:
            self._kafka_builder.build(data)

    def set_sql_builder(self, builder):
        self._sql_builder = builder

    def set_clickhouse_builder(self, builder):
        self._clickhouse_builder = builder

    def set_aws_builder(self, builder):
        self._aws_builder = builder

    def set_elastic_builder(self, builder):
        self._elastic_builder = builder

    def set_kafka_builder(self, builder):
        self._kafka_builder = builder

    def get_configuration(self):
        return self._configuration
