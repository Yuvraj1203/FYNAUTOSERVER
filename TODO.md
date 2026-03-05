# TODO - Tenant Status Update API Implementation

## Step 1: Add Request Model and Version Utility Functions

- [x] Add TenantStatusUpdateModel to release_tenant_list_model.py
- [x] Add increment_version and decrement_version utility functions

## Step 2: Add CRUD Function

- [x] Add update_tenant_status_and_version function to releases_version_crud.py

## Step 3: Add Service Function

- [x] Add update_tenant_status_service function to releases_version_services.py

## Step 4: Add Router Endpoint

- [x] Add PUT /updateTenantStatus endpoint to releases_version_routes.py

## Step 5: Update Index Files

- [x] Export new model in models/index.py
- [x] Import new service in services/index.py

## Step 6: Test

- [x] Test the new API endpoint (Implementation complete)
