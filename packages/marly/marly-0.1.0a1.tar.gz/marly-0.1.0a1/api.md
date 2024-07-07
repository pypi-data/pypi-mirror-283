# Configuration

## Models

Types:

```python
from marly.types.configuration import ModelConfigResponse, ModelListResponse
```

Methods:

- <code title="post /configuration/models">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">create</a>(\*\*<a href="src/marly/types/configuration/model_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/model_config_response.py">ModelConfigResponse</a></code>
- <code title="get /configuration/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">retrieve</a>(model_id) -> <a href="./src/marly/types/configuration/model_config_response.py">ModelConfigResponse</a></code>
- <code title="put /configuration/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">update</a>(model_id, \*\*<a href="src/marly/types/configuration/model_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/model_config_response.py">ModelConfigResponse</a></code>
- <code title="get /configuration/models">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">list</a>() -> <a href="./src/marly/types/configuration/model_list_response.py">ModelListResponse</a></code>
- <code title="delete /configuration/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">delete</a>(model_id) -> None</code>

## Schemas

Types:

```python
from marly.types.configuration import SchemaConfigResponse, SchemaListResponse
```

Methods:

- <code title="post /configuration/schemas">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">create</a>(\*\*<a href="src/marly/types/configuration/schema_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/schema_config_response.py">SchemaConfigResponse</a></code>
- <code title="get /configuration/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">retrieve</a>(schema_id) -> <a href="./src/marly/types/configuration/schema_config_response.py">SchemaConfigResponse</a></code>
- <code title="put /configuration/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">update</a>(schema_id, \*\*<a href="src/marly/types/configuration/schema_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/schema_config_response.py">SchemaConfigResponse</a></code>
- <code title="get /configuration/schemas">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">list</a>() -> <a href="./src/marly/types/configuration/schema_list_response.py">SchemaListResponse</a></code>
- <code title="delete /configuration/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">delete</a>(schema_id) -> None</code>

## Normalizations

Types:

```python
from marly.types.configuration import NormalizationConfigResponse, NormalizationListResponse
```

Methods:

- <code title="post /configuration/normalizations">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">create</a>(\*\*<a href="src/marly/types/configuration/normalization_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/normalization_config_response.py">NormalizationConfigResponse</a></code>
- <code title="get /configuration/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">retrieve</a>(normalization_id) -> <a href="./src/marly/types/configuration/normalization_config_response.py">NormalizationConfigResponse</a></code>
- <code title="put /configuration/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">update</a>(normalization_id, \*\*<a href="src/marly/types/configuration/normalization_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/normalization_config_response.py">NormalizationConfigResponse</a></code>
- <code title="get /configuration/normalizations">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">list</a>() -> <a href="./src/marly/types/configuration/normalization_list_response.py">NormalizationListResponse</a></code>
- <code title="delete /configuration/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">delete</a>(normalization_id) -> None</code>

## Prompts

Types:

```python
from marly.types.configuration import PromptConfigResponse, PromptListResponse
```

Methods:

- <code title="post /configuration/prompts">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">create</a>(\*\*<a href="src/marly/types/configuration/prompt_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/prompt_config_response.py">PromptConfigResponse</a></code>
- <code title="get /configuration/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">retrieve</a>(prompt_id) -> <a href="./src/marly/types/configuration/prompt_config_response.py">PromptConfigResponse</a></code>
- <code title="put /configuration/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">update</a>(\*, path_prompt_id, \*\*<a href="src/marly/types/configuration/prompt_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/prompt_config_response.py">PromptConfigResponse</a></code>
- <code title="get /configuration/prompts">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">list</a>() -> <a href="./src/marly/types/configuration/prompt_list_response.py">PromptListResponse</a></code>
- <code title="delete /configuration/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">delete</a>(prompt_id) -> None</code>

# Pipelines

Types:

```python
from marly.types import PipelineConfigResponse, PipelineListResponse
```

Methods:

- <code title="post /configuration/pipelines">client.pipelines.<a href="./src/marly/resources/pipelines.py">create</a>(\*\*<a href="src/marly/types/pipeline_create_params.py">params</a>) -> <a href="./src/marly/types/pipeline_config_response.py">PipelineConfigResponse</a></code>
- <code title="get /configuration/pipelines/{pipeline_id}">client.pipelines.<a href="./src/marly/resources/pipelines.py">retrieve</a>(pipeline_id) -> <a href="./src/marly/types/pipeline_config_response.py">PipelineConfigResponse</a></code>
- <code title="put /configuration/pipelines/{pipeline_id}">client.pipelines.<a href="./src/marly/resources/pipelines.py">update</a>(pipeline_id, \*\*<a href="src/marly/types/pipeline_update_params.py">params</a>) -> <a href="./src/marly/types/pipeline_config_response.py">PipelineConfigResponse</a></code>
- <code title="get /configuration/pipelines">client.pipelines.<a href="./src/marly/resources/pipelines.py">list</a>() -> <a href="./src/marly/types/pipeline_list_response.py">PipelineListResponse</a></code>
- <code title="delete /configuration/pipelines/{pipeline_id}">client.pipelines.<a href="./src/marly/resources/pipelines.py">delete</a>(pipeline_id) -> None</code>

# OutputMappings

Types:

```python
from marly.types import OutputMappingConfigResponse, OutputMappingListResponse
```

Methods:

- <code title="post /configuration/output-mappings">client.output_mappings.<a href="./src/marly/resources/output_mappings.py">create</a>(\*\*<a href="src/marly/types/output_mapping_create_params.py">params</a>) -> <a href="./src/marly/types/output_mapping_config_response.py">OutputMappingConfigResponse</a></code>
- <code title="get /configuration/output-mappings/{output_mapping_id}">client.output_mappings.<a href="./src/marly/resources/output_mappings.py">retrieve</a>(output_mapping_id) -> <a href="./src/marly/types/output_mapping_config_response.py">OutputMappingConfigResponse</a></code>
- <code title="put /configuration/output-mappings/{output_mapping_id}">client.output_mappings.<a href="./src/marly/resources/output_mappings.py">update</a>(output_mapping_id, \*\*<a href="src/marly/types/output_mapping_update_params.py">params</a>) -> <a href="./src/marly/types/output_mapping_config_response.py">OutputMappingConfigResponse</a></code>
- <code title="get /configuration/output-mappings">client.output_mappings.<a href="./src/marly/resources/output_mappings.py">list</a>() -> <a href="./src/marly/types/output_mapping_list_response.py">OutputMappingListResponse</a></code>
- <code title="delete /configuration/output-mappings/{output_mapping_id}">client.output_mappings.<a href="./src/marly/resources/output_mappings.py">delete</a>(output_mapping_id) -> None</code>

# Orchestrations

Types:

```python
from marly.types import OrchestrationRunPipelineResponse
```

Methods:

- <code title="post /orchestration/run-pipeline">client.orchestrations.<a href="./src/marly/resources/orchestrations.py">run_pipeline</a>(\*\*<a href="src/marly/types/orchestration_run_pipeline_params.py">params</a>) -> <a href="./src/marly/types/orchestration_run_pipeline_response.py">object</a></code>

# Integrations

Types:

```python
from marly.types import RegisterIntegrationResponse, RegisterSourceResponse
```

Methods:

- <code title="post /integrations/register_excel">client.integrations.<a href="./src/marly/resources/integrations.py">register_excel</a>(\*\*<a href="src/marly/types/integration_register_excel_params.py">params</a>) -> <a href="./src/marly/types/register_integration_response.py">RegisterIntegrationResponse</a></code>
- <code title="post /integrations/register_s3">client.integrations.<a href="./src/marly/resources/integrations.py">register_s3</a>(\*\*<a href="src/marly/types/integration_register_s3_params.py">params</a>) -> <a href="./src/marly/types/register_integration_response.py">RegisterIntegrationResponse</a></code>
