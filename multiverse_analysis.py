#!/usr/bin/env python

import argparse
from pathlib import Path
from itertools import combinations

from fairness_multiverse.multiverse import MultiverseAnalysis

parser = argparse.ArgumentParser("multiverse_analysis")
parser.add_argument(
    "--mode",
    help=(
        "How to run the multiverse analysis. "
        "(continue: continue from previous run, "
        "full: run all universes, "
        "test: run only a small subset of universes)"
    ),
    choices=["full", "continue", "test"],
    default="full",
)
def verify_dir(string):
    if Path(string).is_dir():
        return string
    else:
        raise NotADirectoryError(string)
parser.add_argument(
    "--output-dir",
    help=(
        "Relative path to output directory for the results."
    ),
    default="./output",
    type=verify_dir,
)
parser.add_argument(
    "--seed",
    help=(
        "The seed to use for the analysis."
    ),
    default="2024",
    type=int,
)
args = parser.parse_args()

def calculate_combinations(items):
    all_combinations = []
    total_items = len(items)
    for i in range(1, total_items + 1):
        all_combinations.extend(list(combinations(items, i)))
    return all_combinations

groups_rac1p = ['White alone', 'Asian alone', 'Two or More Races', 'Some Other Race alone', 'Black or African American alone', 'American Indian alone', 'Native Hawaiian and Other Pacific Islander alone', 'American Indian and Alaska Native tribes specified; or American Indian or Alaska Native, not specified and no other races', 'Alaska Native alone']
combinations_rac1p = calculate_combinations(groups_rac1p)
combinations_rac1p_joined = list(map(lambda x: 'keep-names_race_'+'-'.join(x), combinations_rac1p))

multiverse_analysis = MultiverseAnalysis(
    dimensions={
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
    output_dir=Path(args.output_dir),
    new_run=(args.mode != "continue"),
    seed=args.seed,
)

multiverse_grid = multiverse_analysis.generate_grid(save=True)
print(f"Generated N = {len(multiverse_grid)} universes")


print(f"~ Starting Run No. {multiverse_analysis.run_no} (Seed: {multiverse_analysis.seed})~")

# Run the analysis for the first universe
if args.mode == "test":
    print("Small-Scale-Test Run")
    multiverse_analysis.visit_universe(multiverse_grid[0])
    multiverse_analysis.visit_universe(multiverse_grid[1])
elif args.mode == "continue":
    print("Continuing Previous Run")
    missing_universes = multiverse_analysis.check_missing_universes()[
        "missing_universes"
    ]

    # Run analysis only for missing universes
    multiverse_analysis.examine_multiverse(multiverse_grid=missing_universes)
else:
    print("Full Run")
    # Run analysis for all universes
    multiverse_analysis.examine_multiverse(multiverse_grid=multiverse_grid)

multiverse_analysis.aggregate_data(save=True)

multiverse_analysis.check_missing_universes()
