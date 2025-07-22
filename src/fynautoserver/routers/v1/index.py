from fastapi import APIRouter
from fynautoserver.routers.v1.tenant_info.tenant_info import router as tenant_info_router
from fynautoserver.routers.v1.file_configs.file_configs import router as file_configs_router
from fynautoserver.routers.v1.fonts_file.fonts_file_upload import fonts_router
from fynautoserver.routers.v1.color_step.color_step_route import color_router
from fynautoserver.routers.v1.icon_generator.icon_generator import icon_gen_router

router_v1 = APIRouter()

router_v1.include_router(tenant_info_router,prefix='/tenantInfo')
router_v1.include_router(file_configs_router,prefix='/fileConfigs')
router_v1.include_router(fonts_router,prefix='/fontsUpload')
router_v1.include_router(color_router,prefix="/colorStep")
router_v1.include_router(icon_gen_router,prefix="/iconGenerator")