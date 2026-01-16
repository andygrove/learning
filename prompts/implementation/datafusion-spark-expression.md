# DataFusion-Spark Expression Implementation Prompt

Use this prompt with Claude Code to contribute Spark-compatible expressions upstream to the DataFusion `datafusion-spark` crate.

## Quick Start

```
Implement Spark expression: <expression_name>
Repository: ~/git/apache/datafusion
Tracking issue: https://github.com/apache/datafusion/issues/15914

Reference:
- Spark docs: https://spark.apache.org/docs/latest/api/sql/#<function_name>
- sparkreference.io: https://sparkreference.io/expressions/<expression_name>/
```

---

## Repository Structure

| Component | Location |
|-----------|----------|
| Function implementations | `datafusion/spark/src/function/<category>/` |
| Module registration | `datafusion/spark/src/function/<category>/mod.rs` |
| SLT tests | `datafusion/sqllogictest/test_files/spark/<category>/` |
| Crate entry point | `datafusion/spark/src/lib.rs` |

**Function categories:**
- `datetime` - Date/time functions (date_add, trunc, hour, etc.)
- `string` - String functions (ascii, concat, trim, etc.)
- `math` - Math functions (abs, ceil, hex, etc.)
- `hash` - Hash functions (md5, sha2, xxhash64, etc.)
- `array` - Array functions
- `map` - Map functions
- `aggregate` - Aggregate functions
- `conditional` - Conditional functions (if, coalesce, etc.)
- `conversion` - Type conversion functions

---

## Implementation Steps

### Step 1: Create Feature Branch

```bash
cd ~/git/apache/datafusion
git checkout main && git pull
git checkout -b spark-<expression-name>
```

### Step 2: Research Spark Behavior

```bash
# Check sparkreference.io for detailed behavior
# Look up edge cases, null handling, type coercion

# Check if there's an existing commented-out SLT test
cat datafusion/sqllogictest/test_files/spark/<category>/<function_name>.slt
```

Key things to understand:
- **Signature**: Input types and return type
- **Type coercion**: How Spark coerces input types
- **Null handling**: Behavior with NULL inputs
- **Edge cases**: Empty strings, overflow, special values

### Step 3: Implement the Function

Create `datafusion/spark/src/function/<category>/<function_name>.rs`:

```rust
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// ... (Apache 2.0 license header)

use std::any::Any;
use std::sync::Arc;

use arrow::datatypes::DataType;
use datafusion_common::{Result, exec_err};
use datafusion_expr::{
    ColumnarValue, ScalarFunctionArgs, ScalarUDFImpl, Signature, Volatility,
};

/// <https://spark.apache.org/docs/latest/api/sql/index.html#function_name>
#[derive(Debug, PartialEq, Eq, Hash)]
pub struct SparkFunctionName {
    signature: Signature,
}

impl Default for SparkFunctionName {
    fn default() -> Self {
        Self::new()
    }
}

impl SparkFunctionName {
    pub fn new() -> Self {
        Self {
            signature: Signature::exact(
                vec![DataType::Utf8],  // adjust types as needed
                Volatility::Immutable,
            ),
        }
    }
}

impl ScalarUDFImpl for SparkFunctionName {
    fn as_any(&self) -> &dyn Any {
        self
    }

    fn name(&self) -> &str {
        "function_name"
    }

    fn signature(&self) -> &Signature {
        &self.signature
    }

    fn return_type(&self, _arg_types: &[DataType]) -> Result<DataType> {
        Ok(DataType::Utf8)  // adjust as needed
    }

    fn invoke_with_args(&self, args: ScalarFunctionArgs) -> Result<ColumnarValue> {
        // Implementation here
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    // Add unit tests here
}
```

### Step 4: Register the Function

Edit `datafusion/spark/src/function/<category>/mod.rs`:

```rust
// Add module declaration
pub mod function_name;

// Add make_udf_function macro call
make_udf_function!(function_name::SparkFunctionName, function_name);

// Add to expr_fn module
pub mod expr_fn {
    export_functions!((
        function_name,
        "Description of what the function does.",
        arg1 arg2
    ));
}

// Add to functions() vector
pub fn functions() -> Vec<Arc<ScalarUDF>> {
    vec![
        // ... existing functions ...
        function_name(),
    ]
}
```

### Step 5: Write SLT Tests

Create or update `datafusion/sqllogictest/test_files/spark/<category>/<function_name>.slt`:

```sql
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# ... (Apache 2.0 license header)

# Test with scalar input
query T
SELECT function_name('input');
----
expected_output

# Test with array input (REQUIRED)
query T
SELECT function_name(a) FROM VALUES ('input1'), ('input2'), (NULL) AS t(a);
----
output1
output2
NULL

# Test with explicit type casting
query I
SELECT function_name(123::INT);
----
expected_int_output

# Test error cases
statement error Expected error message
SELECT function_name();

# Test NULL handling
query T
SELECT function_name(NULL);
----
NULL
```

**SLT Test Guidelines:**
- Test BOTH scalar and array inputs
- Use explicit casts (e.g., `123::INT`, `'text'::STRING`)
- Test NULL handling
- Test error conditions with `statement error`
- Query type codes: `T` (text), `I` (integer), `R` (real), `B` (boolean), `D` (date), `P` (timestamp)

---

## Common Patterns

### Type Coercion with Signature

```rust
use datafusion_common::types::{NativeType, logical_string, logical_int64};
use datafusion_expr::{Coercion, TypeSignature, TypeSignatureClass};

// Accept multiple types that coerce to a target type
let coercion = Coercion::new_implicit(
    TypeSignatureClass::Native(logical_int64()),
    vec![TypeSignatureClass::Numeric],
    NativeType::Int64,
);

Self {
    signature: Signature::one_of(
        vec![TypeSignature::Coercible(vec![coercion])],
        Volatility::Immutable,
    ),
}
```

### Using Simplify for Expression Rewriting

```rust
use datafusion_expr::simplify::{ExprSimplifyResult, SimplifyContext};
use datafusion_expr::Expr;

fn simplify(
    &self,
    args: Vec<Expr>,
    _info: &SimplifyContext,
) -> Result<ExprSimplifyResult> {
    // Rewrite to use existing DataFusion functions
    Ok(ExprSimplifyResult::Simplified(
        Expr::ScalarFunction(ScalarFunction::new_udf(
            datafusion_functions::datetime::date_trunc(),
            args,
        ))
    ))
}

fn invoke_with_args(&self, _args: ScalarFunctionArgs) -> Result<ColumnarValue> {
    internal_err!("function should have been simplified")
}
```

### Handling Dictionary-Encoded Arrays

```rust
use arrow::array::{as_dictionary_array, StringArray};
use arrow::datatypes::Int32Type;

DataType::Dictionary(_, value_type) => {
    let dict = as_dictionary_array::<Int32Type>(&array);
    match **value_type {
        DataType::Utf8 => {
            let arr = dict.downcast_dict::<StringArray>().unwrap();
            // Process arr
        }
        _ => exec_err!("Unsupported dictionary value type"),
    }
}
```

### Return Field with Nullability

```rust
use arrow::datatypes::{Field, FieldRef};
use datafusion_expr::ReturnFieldArgs;

fn return_field_from_args(&self, args: ReturnFieldArgs) -> Result<FieldRef> {
    let nullable = args.arg_fields.iter().any(|f| f.is_nullable());
    Ok(Arc::new(Field::new(self.name(), DataType::Int32, nullable)))
}
```

---

## Build and Test Commands

```bash
# Run specific SLT test file
cargo test --package datafusion-sqllogictest -- spark/<category>/<function_name>

# Run all spark SLT tests
cargo test --package datafusion-sqllogictest -- spark/

# Run unit tests for the spark crate
cargo test --package datafusion-spark

# Check formatting and clippy
cargo fmt --all -- --check
cargo clippy --all-targets --workspace

# Full CI check
cargo test --workspace
```

---

## Create PR

```bash
git add .
git commit -m "$(cat <<'EOF'
feat(spark): add <function_name> function

Adds Spark-compatible `<function_name>` function to the datafusion-spark crate.

Part of https://github.com/apache/datafusion/issues/15914

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

git push -u origin spark-<expression-name>

gh pr create --repo apache/datafusion \
  --title "feat(spark): add <function_name> function" \
  --body "$(cat <<'EOF'
## Which issue does this PR close?

Part of https://github.com/apache/datafusion/issues/15914

## Rationale for this change

Adds Spark-compatible `<function_name>` function to enable Spark SQL compatibility.

## What changes are included in this PR?

- Implements `Spark<FunctionName>` UDF in `datafusion/spark/src/function/<category>/`
- Adds SLT tests in `datafusion/sqllogictest/test_files/spark/<category>/`

## Are these changes tested?

Yes, SLT tests are included covering:
- Scalar inputs
- Array inputs
- NULL handling
- Edge cases

## Are there any user-facing changes?

New function `<function_name>` is available when using the datafusion-spark crate.

> **Note:** This PR was generated with AI assistance.
EOF
)"
```

---

## Enabling Commented-Out Tests

Many SLT test files have commented-out tests waiting for implementation. The format is:

```sql
## Original Query: SELECT function_name('input');
## PySpark 3.5.5 Result: {'function_name(input)': 'output', 'typeof(...)': 'string'}
#query T
#SELECT function_name('input'::string);
```

After implementing the function:
1. Uncomment the test queries (remove `#` prefix)
2. Verify the expected output matches Spark
3. Adjust type casts if needed (DataFusion may require explicit casts)

---

## Resources

- **Tracking Epic**: https://github.com/apache/datafusion/issues/15914
- **Spark SQL Reference**: https://spark.apache.org/docs/latest/api/sql/
- **sparkreference.io**: https://sparkreference.io/expressions/
- **Databricks SQL Reference**: https://docs.databricks.com/aws/en/sql/language-manual/functions/
- **Test README**: `datafusion/sqllogictest/test_files/spark/README.md`
