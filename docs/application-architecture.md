# Application Architecture

## Key Components

- **Pipeline Runner**: Main entry point that reads the configuration and orchestrates classification.
- **Matching Engine**: Performs field-wise semantic comparisons (e.g., sport, gender, type).
- **Override System**: Allows hardcoded control of similarity between specific values.
- **Embedding Manager**: Handles caching and reuse of embeddings to save time.
- **Debug Logger**: Records all intermediate results for traceability and analysis.

## Extensibility

- New match types can be added via the config.
- Each match test supports custom field selection and weighting.
- Overrides and model parameters are controlled externally via JSON.