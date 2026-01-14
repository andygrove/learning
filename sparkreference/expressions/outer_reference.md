# Named Expressions Reference

## Overview
Named expressions in Apache Spark Catalyst are expressions that have an associated name and globally unique identifier. They serve as the foundation for column references, aliases, and attributes in SQL query plans, enabling proper column resolution and reference tracking across different operators in the query execution tree.

## Core Components

### NamedExpression Trait
Base trait for all expressions that have a name and can be referenced by other parts of the query plan.

### ExprId
```scala
case class ExprId(id: Long, jvmId: UUID)
```
A globally unique identifier consisting of a JVM-local ID and UUID for cross-JVM uniqueness.

## Expression Types

---

# Alias

## Overview
Assigns a new name to a computation result. The Alias expression wraps another expression and provides it with a name that can be referenced in subsequent operations. It preserves the child expression's data type and evaluation behavior while adding naming metadata.

## Syntax
```sql
-- SQL syntax
expression AS alias_name

-- With qualifier
table.column AS alias_name
```

```scala
// DataFrame API
df.select(col("expression").alias("alias_name"))

// Catalyst expression construction
Alias(child = someExpression, name = "alias_name")()
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The computation being performed |
| name | String | The name to be associated with the result |
| exprId | ExprId | Globally unique ID (auto-assigned if not provided) |
| qualifier | Seq[String] | Optional qualifier sequence for fully qualified names |
| explicitMetadata | Option[Metadata] | Explicit metadata that overwrites child's metadata |
| nonInheritableMetadataKeys | Seq[String] | Metadata keys to remove when inheriting from child |

## Return Type
Same data type as the child expression. The alias acts as a transparent wrapper that doesn't modify the underlying data type or nullability.

## Supported Data Types
All data types are supported since Alias is a pass-through wrapper around any expression.

## Algorithm
- Evaluation directly delegates to the child expression via `child.eval(input)`
- Code generation passes through to child's generated code
- Metadata inheritance follows these rules:
  - Uses explicitMetadata if provided
  - Otherwise inherits from child (NamedExpression or GetStructField)
  - Removes keys specified in nonInheritableMetadataKeys
  - Returns empty metadata for other expression types

## Partitioning Behavior
- Preserves the partitioning behavior of the child expression
- Does not introduce shuffle operations
- Partitioning keys are updated to reference the new alias name

## Edge Cases
- **Null handling**: Inherits null behavior from child expression
- **Generator children**: Alias wrapping a Generator marks the expression as unresolved, requiring transformation to Generate operator
- **Metadata inheritance**: Performance-optimized to avoid MetadataBuilder manipulation when possible
- **Foldable override**: Always returns false to prevent constant folding that would remove the alias

## Code Generation
Supports full code generation by delegating to the child expression's `genCode` method. The generated code is identical to the child's code since Alias is purely a naming construct.

## Examples
```sql
-- Basic alias
SELECT salary * 1.1 AS increased_salary FROM employees;

-- Qualified alias  
SELECT emp.salary AS emp_salary FROM employees emp;

-- Complex expression alias
SELECT CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END AS category FROM employees;
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._

df.select(
  col("salary").multiply(1.1).alias("increased_salary"),
  when(col("age") > 30, "Senior").otherwise("Junior").alias("category")
)

// Catalyst construction
val alias = Alias(
  child = Multiply(col("salary"), Literal(1.1)),
  name = "increased_salary"
)(
  exprId = NamedExpression.newExprId,
  qualifier = Seq("emp")
)
```

## See Also
- AttributeReference: For resolved column references
- UnresolvedAttribute: For unresolved column names during analysis

---

# AttributeReference

## Overview
Represents a reference to an attribute (column) produced by another operator in the query execution tree. AttributeReference is the resolved form of column references, containing complete type information, nullability, and metadata. It serves as the primary mechanism for referencing columns across different operators in optimized query plans.

## Syntax
```sql
-- SQL usage (resolved internally)
column_name
table.column_name
schema.table.column_name
```

```scala
// Catalyst construction
AttributeReference(
  name = "column_name",
  dataType = IntegerType,
  nullable = true,
  metadata = Metadata.empty
)(
  exprId = NamedExpression.newExprId,
  qualifier = Seq("table_name")
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | Column name (for analysis and debugging) |
| dataType | DataType | The data type of this attribute |
| nullable | Boolean | Whether null is valid for this attribute |
| metadata | Metadata | Associated metadata (default: empty) |
| exprId | ExprId | Globally unique identifier for reference equality |
| qualifier | Seq[String] | Optional qualifiers (table, schema names) |

## Return Type
The data type specified in the `dataType` parameter. Can be any supported Spark SQL data type.

## Supported Data Types
All Spark SQL data types are supported:
- Primitive types (Boolean, Byte, Short, Integer, Long, Float, Double)
- Complex types (Array, Map, Struct)
- String and Binary types
- Date, Timestamp, and Interval types
- Decimal types
- User-defined types

## Algorithm
- **Reference equality**: Uses `sameRef()` method comparing `exprId` for reference equality
- **Evaluation**: Marked as `Unevaluable` - cannot be directly evaluated without row context
- **Canonicalization**: Strips name and qualifiers, keeping only `dataType` and `exprId`
- **Hash computation**: Combines all fields (name, dataType, nullable, metadata, exprId, qualifier)
- **Semantic hashing**: Uses only `exprId.hashCode()` for semantic equivalence

## Partitioning Behavior
- **Preserves partitioning**: References to partition columns maintain partitioning properties
- **No shuffle required**: Attribute references themselves don't cause data movement
- **Partition pruning**: Enables predicate pushdown and partition elimination when used in filters

## Edge Cases
- **Null handling**: Nullability determined by the `nullable` parameter
- **Expression ID equality**: Two AttributeReferences with same `exprId` refer to the same logical column
- **Qualifier matching**: Empty qualifiers match any qualifier during resolution
- **Metadata preservation**: EventTime watermark delay information preserved in string representation
- **Tree pattern optimization**: Uses singleton BitSet for efficient pattern matching

## Code Generation
Marked as `Unevaluable` - AttributeReferences are resolved to actual column access code by parent expressions during code generation phase.

## Examples
```sql
-- SQL usage (these become AttributeReference internally)
SELECT employee_id, salary FROM employees WHERE department = 'Engineering';

-- Qualified references
SELECT e.name, d.department_name 
FROM employees e JOIN departments d ON e.dept_id = d.id;
```

```scala
// Catalyst construction
val empIdRef = AttributeReference("employee_id", IntegerType, nullable = false)()
val salaryRef = AttributeReference("salary", DecimalType(10, 2), nullable = true)()

// With qualifiers and metadata  
val timestampRef = AttributeReference(
  name = "event_time",
  dataType = TimestampType,
  nullable = false,
  metadata = new MetadataBuilder()
    .putLong(EventTimeWatermark.delayKey, 5000)
    .build()
)(qualifier = Seq("events"))

// Reference equality check
val sameColumn = empIdRef.sameRef(anotherEmpIdRef) // compares exprId
```

## See Also
- Alias: For creating named expressions
- UnresolvedAttribute: For unresolved column references during analysis
- GetStructField: For accessing nested struct fields

---

# OuterReference

## Overview
A placeholder that holds a reference to a field resolved outside the current query plan, specifically used for correlated subqueries. OuterReference wraps a NamedExpression that refers to a column from an outer query scope, enabling proper correlation handling during subquery execution.

## Syntax
```sql
-- SQL usage (resolved internally in correlated subqueries)
SELECT * FROM table1 t1 
WHERE EXISTS (
  SELECT 1 FROM table2 t2 
  WHERE t2.id = t1.id  -- t1.id becomes OuterReference
);
```

```scala
// Catalyst construction
OuterReference(AttributeReference("outer_column", IntegerType)())
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| e | NamedExpression | The named expression from outer scope being referenced |

## Return Type
Same data type as the wrapped NamedExpression (`e.dataType`).

## Supported Data Types
All data types supported by the underlying NamedExpression are supported, as OuterReference is a transparent wrapper.

## Algorithm
- **Delegation**: All core properties (dataType, nullable, name, qualifier, exprId) delegate to wrapped expression `e`
- **Evaluation**: Marked as `Unevaluable` - cannot be directly evaluated in current context
- **SQL generation**: Uses "outer(...)" format or override string if tagged
- **Instance creation**: Creates new instances by wrapping `e.newInstance()`
- **Tree pattern**: Tagged with `OUTER_REFERENCE` pattern for optimizer recognition

## Partitioning Behavior
- **No direct partitioning impact**: OuterReferences don't affect partitioning of current plan
- **Subquery optimization**: May influence broadcast join decisions in correlated subqueries
- **No shuffle introduction**: References themselves don't cause data movement

## Edge Cases
- **Null handling**: Inherits nullability from wrapped expression
- **Nested correlation**: Used in conjunction with OuterScopeReference for multi-level correlation
- **Name override**: Single-pass resolver can override SQL string representation via tags
- **Resolution timing**: Must be resolved after outer plan is available

## Code Generation
Marked as `Unevaluable` - OuterReferences are typically resolved or substituted before code generation phase.

## Examples
```sql
-- Correlated EXISTS subquery
SELECT employee_name 
FROM employees e1
WHERE EXISTS (
  SELECT 1 FROM salaries s 
  WHERE s.emp_id = e1.emp_id  -- e1.emp_id becomes OuterReference(emp_id)
  AND s.salary > 50000
);

-- Correlated scalar subquery
SELECT employee_name,
       (SELECT AVG(salary) FROM salaries s WHERE s.emp_id = e.emp_id) as avg_salary
FROM employees e;
```

```scala
// Catalyst construction for correlated subquery
val outerEmpId = OuterReference(
  AttributeReference("emp_id", IntegerType, nullable = false)()
)

// With single-pass SQL override
val outerRef = OuterReference(someAttribute)
outerRef.setTagValue(OuterReference.SINGLE_PASS_SQL_STRING_OVERRIDE, "custom_name")
```

## See Also
- OuterScopeReference: For references to outer scopes in nested correlation
- LateralColumnAliasReference: For lateral column alias resolution
- SubqueryExpression: Container for subquery expressions with outer references

---

# MetadataAttribute

## Overview
Represents metadata columns that provide additional information about data source records, such as file names, modification times, or row positions. MetadataAttribute extends AttributeReference with special metadata markers that identify it as a metadata column, enabling data sources to populate these columns with source-specific information.

## Syntax
```sql
-- SQL usage (metadata columns exposed by data source)
SELECT *, _metadata.file_name, _metadata.file_size FROM parquet_table;
```

```scala
// Catalyst construction
MetadataAttribute("file_name", StringType, nullable = false)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | Name of the metadata column |
| dataType | DataType | Data type of the metadata values |
| nullable | Boolean | Whether the metadata can be null (default: true) |

## Return Type
The specified `dataType` parameter. Common types include StringType for file paths, LongType for sizes/positions, TimestampType for modification times.

## Supported Data Types
All standard Spark SQL data types, though typical metadata columns use:
- StringType: File names, paths, formats
- LongType: File sizes, row positions, block numbers  
- TimestampType: Creation/modification times
- BinaryType: Checksums, hashes

## Algorithm
- **Metadata marking**: Sets `__metadata_col` key in attribute metadata
- **Source integration**: Data sources check `isValid()` to identify metadata columns
- **Preservation flags**: Supports preservation on DELETE, UPDATE, REINSERT operations
- **Logical naming**: Can have different logical vs physical names to avoid conflicts
- **JSON metadata**: Supports additional metadata from connector specifications

## Partitioning Behavior
- **No partitioning impact**: Metadata columns don't affect data partitioning
- **Predicate pushdown**: File-based metadata (names, sizes) may enable file pruning
- **Broadcast optimization**: Constant metadata enables broadcast join optimizations

## Edge Cases
- **Name conflicts**: Automatic renaming when metadata column names conflict with data columns
- **Preservation semantics**: Configurable behavior during DELETE/UPDATE/REINSERT operations
- **Source compatibility**: Not all data sources support all metadata column types
- **Performance**: Metadata column access may require additional I/O operations

## Code Generation
Metadata columns participate in normal code generation. Values are typically populated during scan operations and accessed like regular columns.

## Examples
```sql
-- Accessing file metadata
SELECT customer_id, order_date, _metadata.file_name, _metadata.file_size
FROM orders_parquet
WHERE _metadata.file_name LIKE '%2023%';

-- Row-level metadata
SELECT *, _metadata.row_index 
FROM large_table 
WHERE _metadata.row_index BETWEEN 1000 AND 2000;
```

```scala
// Creating metadata attributes
val fileNameAttr = MetadataAttribute("file_name", StringType, nullable = false)
val fileSizeAttr = MetadataAttribute("file_size", LongType, nullable = false)
val rowIndexAttr = MetadataAttribute("row_index", LongType, nullable = false)

// Checking if attribute is metadata
someAttribute match {
  case MetadataAttribute(attr) => println(s"Found metadata column: ${attr.name}")
  case _ => println("Regular column")
}

// With preservation settings
val preservedAttr = MetadataAttribute("audit_timestamp", TimestampType)
// Check preservation behavior
MetadataAttribute.isPreservedOnDelete(preservedAttr)
MetadataAttribute.isPreservedOnUpdate(preservedAttr)
```

## See Also
- FileSourceMetadataAttribute: For file-based data source metadata
- AttributeReference: Base class for column references
- MetadataColumn: Connector interface for metadata column definitions