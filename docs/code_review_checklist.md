# Code Review Checklist for AI-Generated Code

## Functional Correctness
- [ ] Does the code do what was specified in the prompt?
- [ ] Are edge cases handled (empty input, null values, boundary conditions)?
- [ ] Does error handling produce user-friendly messages (no raw tracebacks)?
- [ ] Are all code paths tested?

## Code Quality
- [ ] Does the code follow PEP 8 style guidelines?
- [ ] Are all functions documented with docstrings?
- [ ] Are variable and function names descriptive and consistent?
- [ ] Is the code DRY (Don't Repeat Yourself)?
- [ ] Are there no unused imports or variables?

## Type Safety
- [ ] Do all functions have type hints for parameters and return values?
- [ ] Are type hints accurate and specific (not just `Any`)?
- [ ] Does mypy pass without errors?

## Design Patterns
- [ ] Is the Strategy Pattern correctly implemented with an abstract base class?
- [ ] Does the Factory Pattern properly decouple creation from usage?
- [ ] Are classes focused on a single responsibility?

## Testing
- [ ] Do tests cover happy paths and error paths?
- [ ] Are test names descriptive of what they test?
- [ ] Is code coverage above 80%?
- [ ] Are tests independent and not dependent on execution order?

## Security
- [ ] Is user input validated before processing?
- [ ] Are file paths validated before access?
- [ ] Are there no hardcoded secrets or sensitive data?
