# DataFusion Comet PR Review Prompt

Use this prompt with Claude Code to review a DataFusion Comet pull request.

## Usage

```
Review Comet PR #XXXX: https://github.com/apache/datafusion-comet/pull/XXXX

Focus areas:
- Spark compatibility (behavior must match Spark exactly)
- Serde implementation correctness
- Test coverage including edge cases
```

## Before You Start

### Skip Your Own PRs

**Do not review PRs created by `andygrove`.** These are your own PRs and reviewing them would be self-review.

### Skip Draft PRs

**Do not review draft PRs.** Draft PRs are work-in-progress and not ready for review. Check the PR state before reviewing:

```bash
gh pr view XXXX --repo apache/datafusion-comet --json isDraft
```

### Review Existing Comments First

Before adding any comments to a PR:

1. **Read all existing review comments** on the PR
2. **Check the conversation tab** for any discussion
3. **Avoid duplicating feedback** that others have already provided
4. **Build on existing discussions** rather than starting new threads on the same topic

```bash
# View existing comments on a PR
gh pr view XXXX --repo apache/datafusion-comet --comments
```

---

## Review Workflow

### 1. Gather Context

Use both the RAG system and Spark reference docs:

```bash
# Query the codebase for similar implementations
python scripts/query.py --backend local -r datafusion-comet -q "<description of the PR's area>"

# For expression PRs, check Spark reference docs
cat sparkreference/docs/expressions/<expression_name>.md
```

### 2. Spark Compatibility Check

**This is the most critical aspect of Comet reviews.** Comet must produce identical results to Spark.

For expression PRs, verify against `sparkreference/docs/expressions/`:

1. **Check edge cases documented in Spark reference**
   - Null handling
   - Overflow behavior
   - Empty input behavior
   - Type-specific behavior

2. **Verify all data types are handled**
   - Does Spark support this type?
   - Does the PR handle all Spark-supported types?

3. **Check for ANSI mode differences**
   - Spark behavior may differ between legacy and ANSI modes
   - PR should handle both or mark as `Incompatible`

### 3. Check Against Implementation Guidelines

**Always verify PRs follow the implementation guidelines in `prompts/implementation/comet-expression.md`.**

#### Scala Serde (`spark/src/main/scala/org/apache/comet/serde/`)

- [ ] Expression class correctly identified
- [ ] All child expressions converted via `exprToProtoInternal`
- [ ] Return type correctly serialized
- [ ] `getSupportLevel` reflects true compatibility:
  - `Compatible()` - matches Spark exactly
  - `Incompatible(Some("reason"))` - differs in documented ways
  - `Unsupported(Some("reason"))` - cannot be implemented
- [ ] Serde in appropriate file (datetime.scala, strings.scala, arithmetic.scala, etc.)

#### Registration (`QueryPlanSerde.scala`)

- [ ] Added to correct map (temporal, string, arithmetic, etc.)
- [ ] No duplicate registrations
- [ ] Import statement added

#### Rust Implementation (if applicable)

Location: `native/spark-expr/src/`

- [ ] Matches DataFusion/Arrow conventions
- [ ] Null handling is correct
- [ ] No panics (use `Result` types)
- [ ] Efficient array operations (avoid row-by-row)

#### Protobuf (if applicable)

Location: `native/proto/src/proto/expr.proto`

- [ ] Message structure is minimal
- [ ] Field types are appropriate
- [ ] Backwards compatible with existing messages

#### Tests (`spark/src/test/scala/org/apache/comet/`)

**CRITICAL: Verify all test requirements from implementation guidelines:**

- [ ] Basic functionality tested with `checkSparkAnswerAndOperator`
- [ ] Null handling tested (`SELECT expression(NULL)`)
- [ ] Edge cases from Spark reference tested
- [ ] **CRITICAL: Literal tests MUST disable constant folding:**
  ```scala
  withSQLConf(SQLConf.OPTIMIZER_EXCLUDED_RULES.key ->
      "org.apache.spark.sql.catalyst.optimizer.ConstantFolding") {
    checkSparkAnswerAndOperator("SELECT func(literal)")
  }
  ```
- [ ] Tests with column data (not just literals) using table or generated data
- [ ] Consider using `FuzzDataGenerator.generateDataFrame` for comprehensive testing

### 4. Using Resources for Review

#### ChromaDB Queries

```bash
# Find similar serde implementations
python scripts/query.py -r datafusion-comet -q "CometExpressionSerde for datetime"

# Check how similar Spark expressions work
python scripts/query.py -r spark -q "DateTrunc expression implementation"

# Understand DataFusion function patterns
python scripts/query.py -r datafusion -q "date_trunc function"
```

#### Spark Reference

```bash
# View full Spark spec for the expression
cat sparkreference/docs/expressions/<name>.md

# Check related expressions
ls sparkreference/docs/expressions/ | grep -i <pattern>
```

### 5. Common Comet Review Issues

1. **Incomplete type support**: Spark expression supports types not handled in PR
2. **Missing edge cases**: Null, overflow, empty string, negative values
3. **Wrong return type**: Return type must match Spark exactly
4. **Literal value tests**: Must disable constant folding optimizer
5. **Stale native code**: PR might need `./mvnw install -pl common -DskipTests`
6. **Missing `getSupportLevel`**: Edge cases should be marked `Incompatible`

### 6. Build Verification

PRs should have run the full build:

```bash
# Contributors should have run:
make  # This runs format, build, test, and updates docs
```

Check for:
- [ ] No formatting issues
- [ ] configs.md updated (if new configs added)
- [ ] All tests pass

## Review Comment Templates

### Spark Compatibility Issue

```markdown
This may not match Spark behavior for [specific case].

From the Spark reference (`sparkreference/docs/expressions/<name>.md`):
> [quote relevant edge case documentation]

Can you add a test for this case and verify it matches Spark?
```

### Missing Test Coverage

```markdown
Please add tests for these edge cases documented in Spark:
- [edge case 1]
- [edge case 2]

Reference: `sparkreference/docs/expressions/<name>.md`
```

### Suggest Incompatible Marking

```markdown
This case differs from Spark behavior and may be difficult to implement exactly.

Consider marking this as `Incompatible`:
```scala
override def getSupportLevel(expr: X): SupportLevel = {
  if (problematicCondition) Incompatible(Some("Reason"))
  else Compatible()
}
```

This allows users to opt-in with `spark.comet.expr.<name>.allow_incompatible=true`.
```

### Approve

```markdown
LGTM! Verified:
- [x] Matches Spark behavior per `sparkreference/docs/expressions/<name>.md`
- [x] Edge cases covered
- [x] Tests pass locally

---
*This review was generated with AI assistance.*
```

### AI Disclosure

**Always include the following note at the end of every review comment:**

```markdown
---
*This review was generated with AI assistance.*
```
