# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),

and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.1] - 2026-02-09


### Added

- Added a missing service: `add_batch()` to help decouple the service layer from the domain layer.

- New helper function for `test_api.py`: `post_to_add_batch()`. It accounts for the modified version of `add_batch()` in the flask API. 

- Added the unit of work to the service layer, to fully decouple the service layer from the data layer.

- Added the `FakeUnitOfWork` class to `test_services.py`.

### Changed

- On the services layer the signature of `allocate()` changed from `def allocate(line: OrderLine, repo: RepositoryProtocol, session) -> str:` to `def allocate(orderid: str, sku: str, qty: int, repo: RepositoryProtocol, session) -> str:`. The newer signature accepts
as parameters primitives. This allows the service layer to be fully decoupled from the domain layer.

- The test `test_returns_allocation()` was replaced with the new test `test_allocate_returns_allocation()` to accomodate refactoring  of `allocate()` and the addition of the `add_batch()` service. Once the unit of work is introduced the test is updated to account for this
change again.

- The test `test_error_for_invalid_sku()` was replaced with the new test `test_allocate_errors_for_invalid_sku()` to accomodate refactoring  of `allocate()` and the addition of the `add_batch()` service. Once the unit of work is introduced the test is updated to account for this
change again.

- In the flask API `add_batch()` was updated with the missing service `..service_layer.services.add_batch()` to avoid the original coupling with the domain model.

- In `test_api.py` the function `test_happy_path_returns_201_and_allocated_batch()` was upgraded with a new version that uses the new helper function `post_to_add_batch()`. As a side effect the pytest fixture `add_stock` is no longer needed.

### Removed

- The pytest fixture `add_stock` is no longer used in `test_api.py`. 

### Fixed

- Fixed bug 1

### Release Notes

- Text