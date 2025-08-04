from fastapi import APIRouter, Depends
from fynautoserver.routers.v1.tenant_info.tenant_info import router as tenant_info_router
from fynautoserver.routers.v1.file_configs.file_configs import router as file_configs_router
from fynautoserver.routers.v1.fonts_file.fonts_file_upload import fonts_router
from fynautoserver.routers.v1.color_step.color_step_route import color_router
from fynautoserver.routers.v1.icon_generator.icon_generator import icon_gen_router
from fynautoserver.routers.v1.user.user import user_router
from fynautoserver.utils.auth.dependencies import get_current_user


# ============================================= Authenticated routes ==================================

protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

protected_router.include_router(tenant_info_router, prefix='/tenantInfo')
protected_router.include_router(file_configs_router, prefix='/fileConfigs')
protected_router.include_router(fonts_router, prefix='/fontsUpload')
protected_router.include_router(color_router, prefix="/colorStep")
protected_router.include_router(icon_gen_router, prefix="/iconGenerator")

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