from fynautoserver.services.releases_version_services.releases_version_services import create_releases_version_service, get_releases_version_service,add_custom_tenant_in_version, deploy_tenant_through_azure, check_progress_of_deployment, update_tenant_status_service

from fynautoserver.services.bulk_deployment_services.bulk_deployment_services import create_bulk_deployment_service, delete_bulk_deployment_service,get_available_bulk_deployment_data_service, on_pipeline_success_service

__all__ = [
    "create_releases_version_service",
    "get_releases_version_service",
    "add_custom_tenant_in_version",
    "deploy_tenant_through_azure",
    "check_progress_of_deployment",
    "update_tenant_status_service",
    "create_bulk_deployment_service",
    "delete_bulk_deployment_service",
    "get_available_bulk_deployment_data_service",
    "on_pipeline_success_service"
]
