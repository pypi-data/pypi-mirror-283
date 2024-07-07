# Configuration

## Models

Types:

```python
from marly.types.configuration import (
    ModelCreateResponse,
    ModelRetrieveResponse,
    ModelUpdateResponse,
    ModelListResponse,
)
```

Methods:

- <code title="post /configuration/models/models">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">create</a>(\*\*<a href="src/marly/types/configuration/model_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/model_create_response.py">ModelCreateResponse</a></code>
- <code title="get /configuration/models/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">retrieve</a>(model_id) -> <a href="./src/marly/types/configuration/model_retrieve_response.py">ModelRetrieveResponse</a></code>
- <code title="put /configuration/models/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">update</a>(model_id, \*\*<a href="src/marly/types/configuration/model_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/model_update_response.py">ModelUpdateResponse</a></code>
- <code title="get /configuration/models/models">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">list</a>() -> <a href="./src/marly/types/configuration/model_list_response.py">ModelListResponse</a></code>
- <code title="delete /configuration/models/models/{model_id}">client.configuration.models.<a href="./src/marly/resources/configuration/models.py">delete</a>(model_id) -> None</code>

## Schemas

Types:

```python
from marly.types.configuration import (
    SchemaCreateResponse,
    SchemaRetrieveResponse,
    SchemaUpdateResponse,
    SchemaListResponse,
)
```

Methods:

- <code title="post /configuration/schemas/schemas">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">create</a>(\*\*<a href="src/marly/types/configuration/schema_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/schema_create_response.py">SchemaCreateResponse</a></code>
- <code title="get /configuration/schemas/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">retrieve</a>(schema_id) -> <a href="./src/marly/types/configuration/schema_retrieve_response.py">SchemaRetrieveResponse</a></code>
- <code title="put /configuration/schemas/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">update</a>(schema_id, \*\*<a href="src/marly/types/configuration/schema_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/schema_update_response.py">SchemaUpdateResponse</a></code>
- <code title="get /configuration/schemas/schemas">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">list</a>() -> <a href="./src/marly/types/configuration/schema_list_response.py">SchemaListResponse</a></code>
- <code title="delete /configuration/schemas/schemas/{schema_id}">client.configuration.schemas.<a href="./src/marly/resources/configuration/schemas.py">delete</a>(schema_id) -> None</code>

## Pipelines

Types:

```python
from marly.types.configuration import (
    PipelineCreateResponse,
    PipelineRetrieveResponse,
    PipelineUpdateResponse,
    PipelineListResponse,
)
```

Methods:

- <code title="post /configuration/pipelines/pipelines">client.configuration.pipelines.<a href="./src/marly/resources/configuration/pipelines.py">create</a>(\*\*<a href="src/marly/types/configuration/pipeline_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/pipeline_create_response.py">PipelineCreateResponse</a></code>
- <code title="get /configuration/pipelines/pipelines/{pipeline_id}">client.configuration.pipelines.<a href="./src/marly/resources/configuration/pipelines.py">retrieve</a>(pipeline_id) -> <a href="./src/marly/types/configuration/pipeline_retrieve_response.py">PipelineRetrieveResponse</a></code>
- <code title="put /configuration/pipelines/pipelines/{pipeline_id}">client.configuration.pipelines.<a href="./src/marly/resources/configuration/pipelines.py">update</a>(pipeline_id, \*\*<a href="src/marly/types/configuration/pipeline_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/pipeline_update_response.py">PipelineUpdateResponse</a></code>
- <code title="get /configuration/pipelines/pipelines">client.configuration.pipelines.<a href="./src/marly/resources/configuration/pipelines.py">list</a>() -> <a href="./src/marly/types/configuration/pipeline_list_response.py">PipelineListResponse</a></code>
- <code title="delete /configuration/pipelines/pipelines/{pipeline_id}">client.configuration.pipelines.<a href="./src/marly/resources/configuration/pipelines.py">delete</a>(pipeline_id) -> None</code>

## OutputMappings

Types:

```python
from marly.types.configuration import (
    OutputMappingCreateResponse,
    OutputMappingRetrieveResponse,
    OutputMappingUpdateResponse,
    OutputMappingListResponse,
)
```

Methods:

- <code title="post /configuration/output-mappings/output-mappings">client.configuration.output_mappings.<a href="./src/marly/resources/configuration/output_mappings.py">create</a>(\*\*<a href="src/marly/types/configuration/output_mapping_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/output_mapping_create_response.py">OutputMappingCreateResponse</a></code>
- <code title="get /configuration/output-mappings/output-mappings/{output_mapping_id}">client.configuration.output_mappings.<a href="./src/marly/resources/configuration/output_mappings.py">retrieve</a>(output_mapping_id) -> <a href="./src/marly/types/configuration/output_mapping_retrieve_response.py">OutputMappingRetrieveResponse</a></code>
- <code title="put /configuration/output-mappings/output-mappings/{output_mapping_id}">client.configuration.output_mappings.<a href="./src/marly/resources/configuration/output_mappings.py">update</a>(output_mapping_id, \*\*<a href="src/marly/types/configuration/output_mapping_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/output_mapping_update_response.py">OutputMappingUpdateResponse</a></code>
- <code title="get /configuration/output-mappings/output-mappings">client.configuration.output_mappings.<a href="./src/marly/resources/configuration/output_mappings.py">list</a>() -> <a href="./src/marly/types/configuration/output_mapping_list_response.py">OutputMappingListResponse</a></code>
- <code title="delete /configuration/output-mappings/output-mappings/{output_mapping_id}">client.configuration.output_mappings.<a href="./src/marly/resources/configuration/output_mappings.py">delete</a>(output_mapping_id) -> None</code>

## Normalizations

Types:

```python
from marly.types.configuration import (
    NormalizationCreateResponse,
    NormalizationRetrieveResponse,
    NormalizationUpdateResponse,
    NormalizationListResponse,
)
```

Methods:

- <code title="post /configuration/normalizations/normalizations">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">create</a>(\*\*<a href="src/marly/types/configuration/normalization_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/normalization_create_response.py">NormalizationCreateResponse</a></code>
- <code title="get /configuration/normalizations/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">retrieve</a>(normalization_id) -> <a href="./src/marly/types/configuration/normalization_retrieve_response.py">NormalizationRetrieveResponse</a></code>
- <code title="put /configuration/normalizations/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">update</a>(normalization_id, \*\*<a href="src/marly/types/configuration/normalization_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/normalization_update_response.py">NormalizationUpdateResponse</a></code>
- <code title="get /configuration/normalizations/normalizations">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">list</a>() -> <a href="./src/marly/types/configuration/normalization_list_response.py">NormalizationListResponse</a></code>
- <code title="delete /configuration/normalizations/normalizations/{normalization_id}">client.configuration.normalizations.<a href="./src/marly/resources/configuration/normalizations.py">delete</a>(normalization_id) -> None</code>

## Prompts

Types:

```python
from marly.types.configuration import (
    PromptCreateResponse,
    PromptRetrieveResponse,
    PromptUpdateResponse,
    PromptListResponse,
)
```

Methods:

- <code title="post /configuration/prompts/prompts">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">create</a>(\*\*<a href="src/marly/types/configuration/prompt_create_params.py">params</a>) -> <a href="./src/marly/types/configuration/prompt_create_response.py">PromptCreateResponse</a></code>
- <code title="get /configuration/prompts/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">retrieve</a>(prompt_id) -> <a href="./src/marly/types/configuration/prompt_retrieve_response.py">PromptRetrieveResponse</a></code>
- <code title="put /configuration/prompts/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">update</a>(\*, path_prompt_id, \*\*<a href="src/marly/types/configuration/prompt_update_params.py">params</a>) -> <a href="./src/marly/types/configuration/prompt_update_response.py">PromptUpdateResponse</a></code>
- <code title="get /configuration/prompts/prompts">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">list</a>() -> <a href="./src/marly/types/configuration/prompt_list_response.py">PromptListResponse</a></code>
- <code title="delete /configuration/prompts/prompts/{prompt_id}">client.configuration.prompts.<a href="./src/marly/resources/configuration/prompts.py">delete</a>(prompt_id) -> None</code>

# Orchestration

## Pipelines

Types:

```python
from marly.types.orchestration import PipelineRunPipelineResponse
```

Methods:

- <code title="post /orchestration/pipelines/run-pipeline">client.orchestration.pipelines.<a href="./src/marly/resources/orchestration/pipelines.py">run_pipeline</a>(\*\*<a href="src/marly/types/orchestration/pipeline_run_pipeline_params.py">params</a>) -> <a href="./src/marly/types/orchestration/pipeline_run_pipeline_response.py">object</a></code>

# Integrations

## Sources

Types:

```python
from marly.types.integrations import SourceRegisterS3Response
```

Methods:

- <code title="post /integrations/sources/register-s3">client.integrations.sources.<a href="./src/marly/resources/integrations/sources.py">register_s3</a>(\*\*<a href="src/marly/types/integrations/source_register_s3_params.py">params</a>) -> <a href="./src/marly/types/integrations/source_register_s3_response.py">SourceRegisterS3Response</a></code>

## Destinations

Types:

```python
from marly.types.integrations import DestinationRegisterExcelResponse, DestinationRegisterS3Response
```

Methods:

- <code title="post /integrations/destinations/register_excel">client.integrations.destinations.<a href="./src/marly/resources/integrations/destinations.py">register_excel</a>(\*\*<a href="src/marly/types/integrations/destination_register_excel_params.py">params</a>) -> <a href="./src/marly/types/integrations/destination_register_excel_response.py">DestinationRegisterExcelResponse</a></code>
- <code title="post /integrations/destinations/register_s3">client.integrations.destinations.<a href="./src/marly/resources/integrations/destinations.py">register_s3</a>(\*\*<a href="src/marly/types/integrations/destination_register_s3_params.py">params</a>) -> <a href="./src/marly/types/integrations/destination_register_s3_response.py">DestinationRegisterS3Response</a></code>
