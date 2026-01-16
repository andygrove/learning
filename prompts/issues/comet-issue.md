# Comet Issue Creation Prompt

Use this prompt with Claude Code to create GitHub issues for unsupported Spark expressions in DataFusion Comet.

## Quick Start

```
Create a GitHub issue for the Spark expression: <expression_name>

Use the Spark reference documentation and issue generation script.
Repository: apache/datafusion-comet
```

## Workflow

### 1. Find Unimplemented Expressions

```bash
# List all expressions with documentation and their implementation status
python scripts/generate_comet_issues.py --list-available

# Or query the codebase for what's implemented
python scripts/query.py -r datafusion-comet -q "implemented expressions in QueryPlanSerde"
```

### 2. Review Spark Reference Documentation

Before creating an issue, understand the expression:

```bash
# Read the Spark reference doc
cat sparkreference/docs/expressions/<expression_name>.md
```

Key sections to review:
- **Syntax**: Function signature
- **Arguments**: Parameter descriptions
- **Return Type**: Output type rules
- **Edge Cases**: Special handling for nulls, overflow, etc.
- **Examples**: Usage examples

### 3. Preview the Generated Issue

```bash
# Dry-run (default) - preview without creating
python scripts/generate_comet_issues.py --expression <name>
```

Review the output for:
- Accurate description of the expression
- Correct difficulty classification (small/medium/large)
- Relevant edge cases included
- No excluded sections (Code Generation, Partitioning)

### 4. Create the Issue

```bash
# Create the issue on GitHub
python scripts/generate_comet_issues.py --expression <name> --create-issues
```

Requires: GitHub CLI (`gh`) authenticated with write access to `apache/datafusion-comet`

### 5. Batch Issue Creation

For multiple expressions:

```bash
# Create issues in parallel
python scripts/generate_comet_issues.py --expression expr1 --create-issues &
python scripts/generate_comet_issues.py --expression expr2 --create-issues &
python scripts/generate_comet_issues.py --expression expr3 --create-issues &
wait
```

---

## Issue Format

Generated issues follow the Comet feature request template:

### Title
```
[Feature] Support Spark expression: <expression_name>
```

### Body Structure

1. **AI Disclaimer** - Required transparency note
2. **Problem Statement** - Why this expression matters
3. **Spark Specification** - Syntax, arguments, return type, edge cases
4. **Implementation Approach** - Links to contributor guide
5. **Difficulty Classification** - Small/Medium/Large
6. **Additional Context** - Related expressions, Spark class name

---

## Difficulty Classifications

The script classifies expressions by implementation complexity:

### Small
Simple expressions that map directly to DataFusion built-ins:
- `acosh`, `asinh`, `atanh`, `cbrt`, `degrees`, `radians`
- `base64`, `unbase64`, `left`, `right`
- `nanvl`, `typeof`, `uuid`

### Medium
Expressions requiring custom logic or multiple steps:
- `bin`, `conv`, `format_number`, `levenshtein`
- `regexp_extract`, `regexp_count`
- `date_diff`, `months_between`, `to_date`
- `collect_list`, `collect_set`

### Large
Complex expressions involving:
- Window functions: `row_number`, `rank`, `lag`, `lead`
- Higher-order functions: `transform`, `filter`, `aggregate`
- JSON/XML parsing: `from_json`, `xpath`, `get_json_object`
- Timezone handling: `convert_timezone`, `from_utc_timestamp`

---

## Customizing Issues

### Update Implemented Expressions

When expressions are added to Comet, update `scripts/generate_comet_issues.py`:

```python
IMPLEMENTED_EXPRESSIONS = {
    # Add new expression here
    "new_expression",
    ...
}
```

### Update Difficulty Classification

```python
DIFFICULTY = {
    "small": [...],
    "medium": [...],  # Add expression here
    "large": [...],
}
```

### Exclude Documentation Sections

```python
EXCLUDED_SECTIONS = [
    "Code Generation",      # Not relevant to Comet
    "Partitioning Behavior", # Usually not relevant
    # Add more sections to exclude
]
```

---

## Pre-requisites

1. **GitHub CLI**: Install and authenticate
   ```bash
   gh auth login
   ```

2. **Spark Reference Docs**: Ensure docs exist
   ```bash
   ls sparkreference/docs/expressions/
   ```

3. **Virtual Environment**: Activate if needed
   ```bash
   source .venv/bin/activate
   ```

---

## Verifying Issue Quality

Before creating, verify:

- [ ] Expression is not already implemented (`--list-available`)
- [ ] Spark reference doc exists and is accurate
- [ ] Difficulty classification is appropriate
- [ ] Edge cases are relevant and complete
- [ ] No duplicate issues exist on GitHub

Check for duplicates:
```bash
gh issue list --repo apache/datafusion-comet --search "expression_name"
```

---

## Resources

- **Spark Reference**: `sparkreference/docs/expressions/`
- **Issue Script**: `scripts/generate_comet_issues.py`
- **Expression Pipeline**: `docs/comet_expressions_pipeline.md`
- **Comet Contributor Guide**: https://datafusion.apache.org/comet/contributor-guide/adding_a_new_expression.html
