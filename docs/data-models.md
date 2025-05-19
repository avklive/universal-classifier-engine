# Data Models

This engine is designed to be schema-flexible and driven entirely by configuration.

## Core Concept

Instead of requiring a fixed structure, the classification engine allows users to define which fields from the product and category data should be used for matching — and how they should be compared — via a JSON config.

Each field group (e.g., sport, gender, product type) can be:
- Matched independently
- Assigned a custom weight
- Overridden manually using a mapping file

The examples below illustrate typical product and category structures used in retail matching — but are **not required fields**.

---

## Example: Product Data

| Field             | Description                              |
|-------------------|------------------------------------------|
| `name`            | Full product name                        |
| `description`     | Product description                      |
| `sport`           | Intended sport (e.g., Running, Yoga)     |
| `gender`          | Target gender (e.g., Men, Women, Kids)   |
| `age`             | Age group (e.g., Adult, Kids)            |
| `product_type_code` | Internal product type code            |

## Example: Category Data

| Field            | Description                               |
|------------------|-------------------------------------------|
| `category`       | Full hierarchical category string         |
| `sport`          | Primary sport context of the category     |
| `gender`         | Gender targeted by the category           |
| `product_type`   | Bottom-level product type description     |

---

## Customization

The fields used in matching are defined in the config file (`configs/<tree>.json`) under the `fields[]` section. Each entry in that list specifies:

- Which product fields to use
- Which category fields to compare against
- Optional override mapping
- Weight in final score

This enables flexible adaptation to different taxonomies and input formats without modifying the code.
