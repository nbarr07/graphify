---
description: Analyze test gaps and create meaningful tests to address the gaps.
---

1. Analyse current code coverage
    * For python projects: by running the script below to an equivalent from Makefile and then reviewing /htmlcov folder, under the relevant folder e.g. backend
    ```shell
    uv run --with-editable . pytest --cov=service --cov-report term --cov-report=html
    ```

    * For vite projects by running in the relevant folder e.g. frontend:
    ```shell
    npx vitest run --coverage
    ```

2. For API tests:
    * When mocking downstream calls, assert the exact arguments (e.g. `assert_called_once_with(...)`) that should be passed so the behavioural contract is enforced.
    * Use mocks (requests_mock in python) to cover API to other downstream calls and verify it was called correctly (e.g. with assert_called_once_with for python) and similar headers, body and url as appropriate.
    * For python fastAPI, use fastAPI TestClient to cover API code base, and verify status code and response for meaning state values instead of not null or len(X) > 0

3. For Repository tests:
    * Make sure CRUD is fully covered with positive and negative use cases
    * If lifecycle stages are supported, ensure it's covered and complete

4. For Service tests:
    * Make sure services have coverage in supporting the API, and verifies integrations with repositories
    * For critical paths, add failure and rollback tests to ensure multi-step transaction are atomic

5. For view model tests
    * Verify positive and negative use cases
    * Verify events to avoid endless change event loops and churn/jitter in views because of that which impact user experience and creates poor client side performance

6. For controller tests
    * Verify positive and negative use cases
    * Verify how downstream view models are being called e.g. with what arguments
    * Verify how downstream output influences code flow of the controllers

7. For model tests
    * Verify downstream integration e.g. with what arguments was called
    * Verify how downstream output influences code flow of the models
    * Verify versioning impacts from API changes and plan for fallback use cases during transit from old APIs to new

8. For view tests
    * Verify that each interactive component is covered e.g. drop down, button etc.
    * Verify downstream integration e.g. with what arguments was called

9. For unit tests
    * Verify positive and negative use cases
    * Focus on the unit and mock the rest, but ensure the test is still meaningful and you are not testing the mocks (useless!)

10. For all tests
    * All tests must have `Arrange` and other Arrange-Act-Assert relevant comments, for each logical section in a test, to and ensure AAA semantics. Use language-specific comment format e.g. for typescript `// Arrange`, for python `# Arrange`, don't use `// Arrange` it's just weird!
    * All tests must have doc strings documenting their intent and what the test is expecting to cover.
    * Make sure the test are purposeful and always choose mocks over stubs
    * After writing the test make sure that the test is testing actual code rather than the mocks it created and only them
    * When patching real code for testing purposes, make sure the patch is undone and doesn't leak to other tests e.g. monkeypatch.setattr, consider using fixture with yield + cleanup after yield

11. Produce output checklist of all the actions you performed
    [ ] Code coverage analysis - X %
    [ ] API tests - N/A, No Identified Improvement, Identified and remediated
    [ ] Repository tests - N/A, No Identified Improvement, Identified and remediated
    [ ] Service tests - N/A, No Identified Improvement, Identified and remediated
    [ ] View Model tests - N/A, No Identified Improvement, Identified and remediated
    [ ] Controller tests - N/A, No Identified Improvement, Identified and remediated
    [ ] Model tests - N/A, No Identified Improvement, Identified and remediated
    [ ] View tests - N/A, No Identified Improvement, Identified and remediated
    [ ] Unit tests - N/A, No Identified Improvement, Identified and remediated
    [ ] All tests - N/A, No Identified Improvement, Identified and remediated
