# Comet Expression Implementation Prompt

Use this prompt with Claude Code to implement a Spark expression in DataFusion Comet.

## Quick Start

```
Implement Comet support for Spark expression: <expression_name>
GitHub issue: https://github.com/apache/datafusion-comet/issues/XXXX

Repository: /home/andy/git/personal/learning/datafusion-comet
Spark reference: sparkreference/docs/expressions/<expression_name>.md

Follow the contributor guide: https://datafusion.apache.org/comet/contributor-guide/adding_a_new_expression.html
```

## Pre-Implementation Research

### 1. Understand Spark Behavior

```bash
# Read the Spark reference documentation
cat sparkreference/docs/expressions/<expression_name>.md
```

Key things to extract:
- **Syntax**: Function signature and arguments
- **Return type**: For each input type combination
- **Edge cases**: Null handling, overflow, empty strings, etc.
- **ANSI mode**: Behavior differences between legacy and ANSI

### 2. Check Existing Implementations

```bash
# Query for similar Comet implementations
python scripts/query.py -r datafusion-comet -q "<expression_name> serde implementation"

# Check if DataFusion has a built-in function
python scripts/query.py -r datafusion -q "<expression_name> function"

# Check datafusion-spark crate for existing function
python scripts/query.py -r datafusion-comet -q "datafusion_spark <expression_name>"
```

### 3. Understand Spark Source

```bash
# Query Spark implementation details
python scripts/query.py -r spark -q "<SparkExpressionClass> implementation"
```

---

## Implementation Steps

### Step 1: Create Feature Branch

```bash
cd /home/andy/git/personal/learning/datafusion-comet
git checkout main && git pull origin main
git checkout -b feature/<expression-name>
```

### Step 2: Implement Scala Serde

Location: `spark/src/main/scala/org/apache/comet/serde/<category>.scala`

Choose the right file:
- `datetime.scala` - Date/time functions
- `strings.scala` - String functions
- `arithmetic.scala` - Math functions
- `hash.scala` - Hash functions
- `bitwise.scala` - Bitwise operations

```scala
import org.apache.spark.sql.catalyst.expressions.<SparkExpressionClass>

object Comet<ExpressionName> extends CometExpressionSerde[<SparkExpressionClass>] {

  // Override if edge cases can't match Spark
  override def getSupportLevel(expr: <SparkExpressionClass>): SupportLevel = {
    // Analyze edge cases from sparkreference doc
    // Return Compatible(), Incompatible(reason), or Unsupported(reason)
    Compatible()
  }

  override def convert(
      expr: <SparkExpressionClass>,
      inputs: Seq[Attribute],
      binding: Boolean): Option[ExprOuterClass.Expr] = {
    // Convert child expressions
    val childExpr = exprToProtoInternal(expr.child, inputs, binding)

    // Use existing scalar function
    scalarFunctionExprToProto("function_name", childExpr)
  }
}
```

### Step 3: Register in QueryPlanSerde

Location: `spark/src/main/scala/org/apache/comet/serde/QueryPlanSerde.scala`

```scala
// Add to appropriate map
private val temporalExpressions = Map(
    // ... existing ...
    classOf[<SparkExpressionClass>] -> Comet<ExpressionName>,
)
```

### Step 4: Register DataFusion-Spark Function (if applicable)

If using a function from the `datafusion-spark` crate:

Location: `native/core/src/execution/jni_api.rs`

```rust
use datafusion_spark::function::datetime::<FunctionStruct>;

fn register_datafusion_spark_function(session_ctx: &SessionContext) {
    // ... existing ...
    session_ctx.register_udf(ScalarUDF::new_from_impl(<FunctionStruct>::default()));
}
```

### Step 5: Add Rust Support (if needed)

Only if DataFusion doesn't have a compatible function.

Location: `native/spark-expr/src/`

```rust
// New cast type in conversion_funcs/cast.rs
(SourceType, TargetType) => {
    // Implementation
}
```

### Step 6: Add Tests

Location: `spark/src/test/scala/org/apache/comet/`

```scala
test("<expression_name>") {
  // Generate test data
  val r = new Random(42)
  val schema = StructType(Seq(StructField("c0", DataTypes.StringType, true)))
  val df = FuzzDataGenerator.generateDataFrame(r, spark, schema, 1000, DataGenOptions())
  df.createOrReplaceTempView("tbl")

  // Basic test - verifies Comet matches Spark
  checkSparkAnswerAndOperator("SELECT <expression>(c0) FROM tbl")
}

test("<expression_name> - literals") {
  // IMPORTANT: Disable constant folding for literal tests
  withSQLConf(SQLConf.OPTIMIZER_EXCLUDED_RULES.key ->
      "org.apache.spark.sql.catalyst.optimizer.ConstantFolding") {
    checkSparkAnswerAndOperator("SELECT <expression>('literal_value')")
  }
}

test("<expression_name> - null handling") {
  checkSparkAnswerAndOperator("SELECT <expression>(NULL)")
}

test("<expression_name> - edge cases") {
  // Add tests for edge cases from sparkreference doc
}
```

---

## Build Commands

```bash
# CRITICAL: After ANY Rust changes
cd native && cargo build && cd ..
./mvnw install -pl common -DskipTests

# Run specific test suite (faster iteration)
./mvnw test -pl spark -Dsuites="org.apache.comet.CometExpressionSuite"

# BEFORE PR: Full build (format + test + docs)
make
```

**Troubleshooting stale cache:**
```bash
rm -rf ~/.m2/repository/org/apache/datafusion/comet-*
./mvnw install -pl common -DskipTests
```

---

## Handling Edge Cases

When an edge case can't match Spark:

```scala
override def getSupportLevel(expr: MyExpr): SupportLevel = {
  expr.property match {
    case supported => Compatible()
    case _ => Incompatible(Some("Reason from Spark reference doc"))
  }
}
```

This means:
- Expression falls back to Spark by default
- Users opt-in with `spark.comet.expr.<name>.allow_incompatible=true`

---

## Create PR

```bash
git add .
git commit -m "$(cat <<'EOF'
feat: add support for <expression_name> expression

<Brief description>

Closes #XXXX

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

git push -u origin feature/<expression-name>

gh pr create --repo apache/datafusion-comet \
  --title "feat: add support for <expression_name> expression" \
  --body "$(cat <<'EOF'
## Summary
- Adds native Comet support for Spark `<expression_name>` function

## Test Plan
- Added unit tests for basic functionality
- Added tests for edge cases per Spark documentation
- All existing tests pass

> **Note:** This PR was generated with AI assistance.

Closes #XXXX
EOF
)"
```

---

## Common Patterns

### Simple Scalar Function (uses existing DataFusion function)

```scala
object CometMyFunc extends CometScalarFunction[MyFunc]("datafusion_func_name")
```

### Function with Return Type Override

```scala
scalarFunctionExprToProtoWithReturnType("func", serializeDataType(returnType).get, failOnError, child)
```

### Cast Expression

```scala
val cast = ExprOuterClass.Cast.newBuilder()
  .setChild(child)
  .setDatatype(serializeDataType(targetType).get)
  .setEvalMode(ExprOuterClass.EvalMode.LEGACY)
  .build()
Expr.newBuilder().setCast(cast).build()
```

---

## Key Directories

| Component | Location |
|-----------|----------|
| Scala serde | `spark/src/main/scala/org/apache/comet/serde/` |
| Registration | `spark/src/main/scala/org/apache/comet/serde/QueryPlanSerde.scala` |
| Tests | `spark/src/test/scala/org/apache/comet/` |
| Protobuf | `native/proto/src/proto/expr.proto` |
| Rust expressions | `native/spark-expr/src/` |
| JNI registration | `native/core/src/execution/jni_api.rs` |

---

## Resources

- **Spark reference**: `sparkreference/docs/expressions/<name>.md`
- **Contributor guide**: https://datafusion.apache.org/comet/contributor-guide/adding_a_new_expression.html
- **ChromaDB queries**: `python scripts/query.py -r datafusion-comet -q "..."`
