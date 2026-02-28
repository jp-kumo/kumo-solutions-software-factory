# Interview Story Pack (COBOL modernization)

## 1) Why COBOL still matters
COBOL remains embedded in mission-critical transaction systems. Replacing it outright is expensive and risky, so practical modernization focuses on safe integration patterns.

## 2) How to modernize safely
Use a bridge pattern: export legacy records, parse/normalize in a controlled pipeline, expose via API/warehouse, and progressively shift consumers to modern interfaces.

## 3) Risk reduction approach
- Keep legacy producer stable
- Add explicit schema/layout checks
- Build traceable transformations
- Keep rollback path simple
