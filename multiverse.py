from itertools import combinations

def calculate_combinations(items):
    all_combinations = []
    total_items = len(items)
    for i in range(1, total_items + 1):
        all_combinations.extend(list(combinations(items, i)))
    return all_combinations

groups_rac1p = ['White alone', 'Asian alone', 'Two or More Races', 'Some Other Race alone', 'Black or African American alone', 'American Indian alone', 'Native Hawaiian and Other Pacific Islander alone', 'American Indian and Alaska Native tribes specified; or American Indian or Alaska Native, not specified and no other races', 'Alaska Native alone']
combinations_rac1p = calculate_combinations(groups_rac1p)
combinations_rac1p_joined = list(map(lambda x: 'keep-names_race_'+'-'.join(x), combinations_rac1p))

config = {
    "dimensions": {
        # Skipped decisions
        "preprocess_age": [
            "none", # Keep as is by default
            # "bins_10",
            # "quantiles_3",
            # "quantiles_4"
        ],
        "scale": [
            # "scale",
            "do-not-scale" # Keep as is by default
        ],
        "encode_categorical": [
            # "ordinal",
            "one-hot"
        ],
        "stratify_split": [
            "none", # Do not stratify by default
            # "target",
            # "protected-attribute",
            # "both"
        ],
        "cutoff": [[
            # Sub-universe decision, but let's still exclude it
            "raw_0.5",
            # "quantile_0.1",
            # "quantile_0.25"
        ]],

        # Unchanged decisions
        "exclude_features": [
            "none",
            "race",
            "sex",
            "race-sex",
        ],
        "preprocess_income": ["none", "bins_10000", "quantiles_3", "quantiles_4"],
        "eval_exclude_subgroups": [["exclude-in-eval", "keep-in-eval"]],
        "eval_fairness_grouping": [["majority-minority", "race-all"]],

        # Renamed decisions / options
        "model": [
            "logreg", # renamed to simple
            "rf", # renamed to complex
            # "gbm", # Excluded
            # "elasticnet" # Excluded
        ],

        # Changed decisions
        "exclude_subgroups": combinations_rac1p_joined, # all unique combinations between the different race groups
        "eval_on_subset": [[
            "full",
            # Largest PUMA region
            "locality-largest-only",
            # NEW: PUMA region w/ highest share of ppl with health insurance
            "locality-most-privileged",
            # REMOVED: PUMA region w/ highest share of white people (excluded!)
            # "locality-whitest-only",
            # CHANGED: PUMA regions belonging to a large city (switched to only one and renamed)
            # "locality-city-la",
            "locality-city-sf",
            # Exclude military personnel from test dataset
            "exclude-military",
            # Exclude non US citizens from test dataset
            "exclude-non-citizens",
        ]],

        # New decisions (This doesn't need to be a decision, but could rather just be done post-hoc?)
        "fairness_definition": [["sensitivity", "precision"]],
    },
}
