export const mapDecisionNames = {
  ES: "Exclude Subgroups",
  EF: "Exclude Features",
  M: "Model",
  PI: "Preprocess Income",
  EFD: "Eval Fairness Definition",
  EFG: "Eval Fairness Grouping",
  EOS: "Eval On Subset",
  EES: "Eval Exclude Subgroups",
}

export function parseIndividualDecisionString(nodeString) {
  let key = nodeString.split(":")[0]
  let value = nodeString.split(":")[1]
  if (key === "START") {
    return { key }
  }

  if (key in mapDecisionNames) {
    key = mapDecisionNames[key]
  }

  // Remove first letter(s) from value as they are only used for sorting
  if (value.startsWith("NA")) {
    value = value.slice(2)
  } else {
    value = value.slice(1)
  }
  value = value
    .replaceAll("-", "; ")
    .replaceAll("_", "-")

  return { key, value }
}
