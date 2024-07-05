# llm-dataset-converter-all
Meta-library that combines all [llm-dataset-converter](https://github.com/waikato-llm/llm-dataset-converter) libraries.


## Installation

Via PyPI:

```bash
pip install llm-dataset-converter-all \
            git+https://github.com/waikato-llm/ldc-tint.git
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-llm/llm-dataset-converter-all.git \
            git+https://github.com/waikato-llm/ldc-tint.git
```

**NB:** The [reo-toolkit](https://github.com/TeHikuMedia/reo-toolkit) library is not published on pypi, 
so we have to install that separately from the github repo.

## Docker

[Docker](docker) images are available from:

* Docker hub: [waikatodatamining/llm-dataset-converter](https://hub.docker.com/r/waikatodatamining/llm-dataset-converter)
* In-house registry: `public.aml-repo.cms.waikato.ac.nz:443/tools/llm-dataset-converter`
