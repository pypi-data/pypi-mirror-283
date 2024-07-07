# CLI for lmnr.ai

## Basic usage
```
lmnr pull <pipeline_name> <pipeline_version_name> --project-api-key <PROJECT_API_KEY>
```

Read more [here](https://docs.lmnr.ai/api-reference/introduction#authentication) on how to get `PROJECT_API_KEY`.

To import your pipeline
```python
# submodule with the name of your pipeline will be generated in lmnr_engine.pipelines
from lmnr_engine.pipelines.my_custom_pipeline import MyCustomPipeline


pipeline = MyCustomPipeline()
res = pipeline.run(
    inputs={
        "instruction": "Write me a short linked post about dev tool for LLM developers which they'll love"
    },
    env={
        "OPENAI_API_KEY": <OPENAI_API_KEY>,
    }
)
print(f"RESULT:\n{res}")
```

## Current functionality
- Supports graph generation for graphs with Input, Output, and LLM nodes only
- For LLM nodes, it only supports OpenAI and Anthropic models and doesn't support structured output
