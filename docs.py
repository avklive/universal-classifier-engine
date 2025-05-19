from pathlib import Path

matching_dir = Path("matching")
matching_dir.mkdir(exist_ok=True)

main_script = matching_dir / "match_runner.py"

main_script.write_text("""
import json
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def concat_fields(row, fields):
    return " ".join(str(row[f]) for f in fields if f in row and pd.notnull(row[f]))

def load_overrides(path):
    try:
        df = pd.read_csv(path)
        return {
            (str(row['product_value']), str(row['category_value'])): float(row['score'])
            for _, row in df.iterrows()
        }
    except Exception:
        return {}

def match_products(config_path):
    config = load_config(config_path)
    model = SentenceTransformer(config['model'])

    products = pd.read_csv(config['product_file'])
    categories = pd.read_csv(config['category_file'])

    final_results = []

    for field in config['fields']:
        name = field['name']
        weight = field['weight']
        override_map = load_overrides(field.get('override_file', ''))
        product_fields = field['product_fields']
        category_fields = field['category_fields']

        prod_texts = products.apply(lambda row: concat_fields(row, product_fields), axis=1)
        cat_texts = categories.apply(lambda row: concat_fields(row, category_fields), axis=1)

        prod_embs = model.encode(prod_texts.tolist(), normalize_embeddings=True, show_progress_bar=True)
        cat_embs = model.encode(cat_texts.tolist(), normalize_embeddings=True, show_progress_bar=True)

        scores = util.cos_sim(prod_embs, cat_embs)

        for i, row in products.iterrows():
            top_k = sorted([(j, scores[i][j].item()) for j in range(len(categories))], key=lambda x: -x[1])[:config["top_k"]]
            for j, score in top_k:
                prod_val = concat_fields(row, product_fields)
                cat_val = concat_fields(categories.iloc[j], category_fields)
                override_score = override_map.get((prod_val, cat_val))
                final_score = override_score if override_score is not None else score * weight

                final_results.append({
                    "product_index": i,
                    "category_index": j,
                    "field": name,
                    "product_text": prod_val,
                    "category_text": cat_val,
                    "raw_score": score,
                    "override": override_score,
                    "weight": weight,
                    "final_contribution": final_score
                })

    result_df = pd.DataFrame(final_results)
    output_path = Path("results") / f"debug_results.csv"
    output_path.parent.mkdir(exist_ok=True)
    result_df.to_csv(output_path, index=False)
    print(f"Saved debug results to {output_path}")

if __name__ == "__main__":
    match_products("examples/intersport_config.json")
""".strip())

"Core matching code written to matching/match_runner.py"
