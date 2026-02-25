from fastapi import APIRouter, Depends
from fynautoserver.routers.v1.tenant_info.tenant_info import router as tenant_info_router
from fynautoserver.routers.v1.file_configs.file_configs import router as file_configs_router
from fynautoserver.routers.v1.fonts_file.fonts_file_upload import fonts_router
from fynautoserver.routers.v1.color_step.color_step_route import color_router
from fynautoserver.routers.v1.icon_generator.icon_generator import icon_gen_router
from fynautoserver.routers.v1.user.user import user_router
from fynautoserver.utils.auth.dependencies import get_current_user
from fynautoserver.routers.v1.releases_version_routes.releases_version_routes import releases_version_router
from fynautoserver.routers.v1.global_settings.global_settings import router as global_settings_router


# ============================================= Authenticated routes ==================================

protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

protected_router.include_router(tenant_info_router, prefix='/tenantInfo',tags=["brandings"])
protected_router.include_router(file_configs_router, prefix='/fileConfigs',tags=["brandings"])
protected_router.include_router(fonts_router, prefix='/fontsUpload',tags=["brandings"])
protected_router.include_router(color_router, prefix="/colorStep",tags=["brandings"])
protected_router.include_router(icon_gen_router, prefix="/iconGenerator",tags=["brandings"])

#tenants releases
protected_router.include_router(releases_version_router,prefix="/releasesVersion",tags=["releases"])

#global settings
protected_router.include_router(global_settings_router, prefix="/globalSettings", tags=["global"])

# =====================================================================================================

# ============================================ Public routes (no auth) ================================

public_router = APIRouter()

public_router.include_router(user_router, prefix="/user")

# =====================================================================================================

# ================================== Combine both into one router_v1 ==================================

router_v1 = APIRouter()
router_v1.include_router(protected_router)
router_v1.include_router(public_router)

# =====================================================================================================
# router_v1 = APIRouter(
#     dependencies=[Depends(get_current_user)]
# )

# router_v1.include_router(tenant_info_router,prefix='/tenantInfo')
# router_v1.include_router(file_configs_router,prefix='/fileConfigs')
# router_v1.include_router(fonts_router,prefix='/fontsUpload')
# router_v1.include_router(color_router,prefix="/colorStep")
# router_v1.include_router(icon_gen_router,prefix="/iconGenerator")
# router_v1.include_router(user_router,prefix="/user")