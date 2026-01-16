# DataFusion PR Review Prompt

Use this prompt with Claude Code to review a DataFusion pull request.

## Usage

```
Review DataFusion PR #XXXX: https://github.com/apache/datafusion/pull/XXXX

Focus areas:
- Correctness of the implementation
- Performance implications
- API design and backwards compatibility
- Test coverage
```

## Before You Start

### PR Eligibility Checks

Before reviewing any PR, verify it meets ALL of these criteria:

```bash
# Check PR state, author, and labels
gh pr view XXXX --repo apache/datafusion --json isDraft,author,labels
```

**Only review PRs that:**
1. **Are NOT drafts** - Draft PRs are work-in-progress and not ready for review
2. **Have the `spark` label** - Focus only on Spark-related PRs
3. **Are NOT created by `andygrove`** - These are your own PRs (self-review not allowed)

If the PR does not meet all criteria, **do not review it**.

### Review Existing Comments First

**CRITICAL: Before adding ANY comments to a PR, you MUST thoroughly review the existing discussion.**

1. **Read ALL existing review comments** on the PR - every single one
2. **Read the full conversation tab** for any discussion threads
3. **Understand the context** of what has already been discussed and resolved
4. **Check if your concern has already been raised** by another reviewer

```bash
# View existing comments on a PR
gh pr view XXXX --repo apache/datafusion --comments

# View the full PR discussion including review comments
gh api repos/apache/datafusion/pulls/XXXX/comments
gh api repos/apache/datafusion/pulls/XXXX/reviews
```

### Only Comment if Adding Value

**Do NOT add a comment unless it provides NEW information or perspective.** Ask yourself:

- Has this issue already been raised by another reviewer? → **Don't comment**
- Is this a "me too" agreement with existing feedback? → **Don't comment**
- Is this summarizing what others have said? → **Don't comment**
- Does this add a genuinely new concern or suggestion? → **Comment**
- Does this provide additional technical context others missed? → **Comment**

**If you have nothing new to add beyond what's already discussed, do not leave a review comment.** Redundant comments waste the PR author's time and clutter the discussion.

---

## Review Workflow

### 1. Gather Context

Before reviewing, use the RAG system to understand related code:

```bash
# Query the codebase for relevant context
python scripts/query.py --backend local -r datafusion -q "<description of the PR's area>"

# Example: For a PR about hash joins
python scripts/query.py --backend local -r datafusion -q "How does DataFusion implement hash joins?"
```

### 2. Review Checklist

#### Code Quality
- [ ] Code follows Rust idioms and DataFusion patterns
- [ ] Error handling is appropriate (using `Result`, `DataFusionError`)
- [ ] No unnecessary allocations or clones
- [ ] Comments explain "why" not "what"

#### Correctness
- [ ] Logic correctly implements the intended behavior
- [ ] Edge cases are handled (nulls, empty inputs, overflow)
- [ ] Type coercion follows expected rules
- [ ] SQL semantics match standard SQL or documented deviations

#### Performance
- [ ] No O(n^2) algorithms where O(n) is possible
- [ ] Appropriate use of iterators vs collecting
- [ ] Memory usage is bounded where possible
- [ ] Vectorized operations preferred over row-by-row

#### Testing
- [ ] Unit tests cover main functionality
- [ ] Edge cases have dedicated tests
- [ ] SQL logic tests for user-facing changes
- [ ] Benchmarks for performance-critical changes

#### API Design
- [ ] Public APIs are well-documented
- [ ] Breaking changes are noted and justified
- [ ] Feature flags used for experimental features

### 3. Key Areas to Examine

#### Physical Plan Changes
Location: `datafusion/physical-plan/src/`

Look for:
- Correct partition handling
- Proper stream implementation
- Memory management with `MemoryConsumer`

#### Logical Plan / Optimizer
Location: `datafusion/optimizer/src/`

Look for:
- Rule correctness (doesn't change semantics)
- Proper handling of nullable columns
- No infinite optimization loops

#### SQL Parsing / Planning
Location: `datafusion/sql/src/`

Look for:
- Correct SQL-to-logical plan translation
- Proper type inference
- Error messages are helpful

#### Expression Evaluation
Location: `datafusion/physical-expr/src/`

Look for:
- Null handling matches SQL semantics
- Type coercion is consistent
- Vectorized array operations used correctly

### 4. Using ChromaDB for Deep Dives

When you need to understand existing patterns:

```bash
# Find similar implementations
python scripts/query.py -r datafusion -q "aggregate function implementation pattern"

# Understand error handling patterns
python scripts/query.py -r datafusion -q "how are errors handled in physical operators"

# Check for consistency with existing code
python scripts/query.py -r datafusion -q "memory tracking in joins"
```

### 5. Check CI Test Failures

**Always check the CI status and summarize any test failures in your review.**

```bash
# View CI check status
gh pr checks XXXX --repo apache/datafusion

# View failed check details
gh pr checks XXXX --repo apache/datafusion --failed
```

If there are test failures:
1. Identify which tests are failing
2. Determine if failures are related to the PR changes or are flaky/pre-existing
3. Include a summary of failures in your review comment

Example failure summary:
```markdown
## CI Status

The following tests are failing:
- `test_xyz` - appears related to this PR's changes
- `test_abc` - likely flaky (unrelated to changes)

Please investigate the `test_xyz` failure.
```

## Review Comment Templates

### Request Changes

```markdown
This implementation may have issues with [specific concern].

Looking at how this is handled elsewhere in the codebase:
[paste relevant code from RAG query]

Consider [suggested approach] instead.
```

### Suggest Improvement

```markdown
This works, but could be improved by [suggestion].

For example, `datafusion/[path]` does something similar:
[paste relevant code]
```

### Approve with Notes

```markdown
LGTM! A few minor suggestions:
- [optional improvement 1]
- [optional improvement 2]

Tested locally and confirmed [what you verified].

---
*This review was generated with AI assistance.*
```

### AI Disclosure

**Always include the following note at the end of every review comment:**

```markdown
---
*This review was generated with AI assistance.*
```

## Common DataFusion Review Issues

1. **Missing null handling**: Ensure functions properly handle null inputs
2. **Type coercion**: Check that implicit casts follow DataFusion's type system
3. **Memory tracking**: Large allocations should use `MemoryConsumer`
4. **Partition preservation**: Operators should preserve partitioning when possible
5. **Statistics propagation**: Operators should propagate statistics for optimizer
