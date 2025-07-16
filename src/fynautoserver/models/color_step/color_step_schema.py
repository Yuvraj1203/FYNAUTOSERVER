from pydantic import BaseModel
from typing import Optional

class Elevation(BaseModel):
    level0: Optional[str]=None
    level1: Optional[str]=None
    level2: Optional[str]=None
    level3: Optional[str]=None
    level4: Optional[str]=None
    level5: Optional[str]=None
   

class color_schema(BaseModel):
    primary: Optional[str]=None
    onPrimary: Optional[str]=None
    primaryContainer:Optional[str]=None
    onPrimaryContainer:Optional[str]=None
    secondary: Optional[str]=None
    onSecondary: Optional[str]=None
    secondaryContainer: Optional[str]=None
    onSecondaryContainer: Optional[str]=None
    tertiary: Optional[str]=None
    onTertiary: Optional[str]=None
    tertiaryContainer: Optional[str]=None
    onTertiaryContainer: Optional[str]=None
    error: Optional[str]=None
    onError: Optional[str]=None
    errorContainer:Optional[str]=None
    onErrorContainer: Optional[str]=None
    background: Optional[str]=None
    onBackground: Optional[str]=None
    surface: Optional[str]=None
    onSurface: Optional[str]=None
    surfaceVariant: Optional[str]=None
    onSurfaceVariant: Optional[str]=None
    outline: Optional[str]=None
    outlineVariant: Optional[str]=None
    shadow: Optional[str]=None
    scrim: Optional[str]=None
    inverseSurface: Optional[str]=None
    inverseOnSurface: Optional[str]=None
    inversePrimary:Optional[str]=None
    elevation:Elevation
    surfaceDisabled: Optional[str]=None
    onSurfaceDisabled: Optional[str]=None
    backdrop: Optional[str]=None
    lightPrimaryContainer: Optional[str]=None

class ThemeSchema(BaseModel): 
    light: Optional[color_schema]=None
    dark: Optional[color_schema]=None