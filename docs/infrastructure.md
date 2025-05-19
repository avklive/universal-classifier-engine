# Infrastructure Overview

This project supports both local and remote execution environments. In absolute majority of cases, local is enough - this was one of the main the Architecture principles

## Local

- Python-based CLI tool
- Run on CPU or GPU with pre-downloaded Hugging Face models
- No external API dependencies


## Cloud/RunPod

- GPU-accelerated execution for embedding large datasets
- Easily deployable using containerized Python environments
- Compatible with Hugging Face model cache and volume mounts