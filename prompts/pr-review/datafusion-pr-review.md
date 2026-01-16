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

### Skip Your Own PRs

**Do not review PRs created by `andygrove`.** These are your own PRs and reviewing them would be self-review.

### Skip Draft PRs

**Do not review draft PRs.** Draft PRs are work-in-progress and not ready for review. Check the PR state before reviewing:

```bash
gh pr view XXXX --repo apache/datafusion --json isDraft
```

### Review Existing Comments First

Before adding any comments to a PR:

1. **Read all existing review comments** on the PR
2. **Check the conversation tab** for any discussion
3. **Avoid duplicating feedback** that others have already provided
4. **Build on existing discussions** rather than starting new threads on the same topic

```bash
# View existing comments on a PR
gh pr view XXXX --repo apache/datafusion --comments
```

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
