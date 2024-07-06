from aspose.tex.presentation import image
from aspose.tex.presentation import pdf
from aspose.tex.presentation import svg
from aspose.tex.presentation import xps
import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class Device:
    '''Implements the interface for outputting text and graphic content
    to abstract device. Rendering is performed page by page.'''
    
    def initialize(self) -> None:
        '''Initializes the device.'''
        ...
    
    def create(self) -> aspose.tex.presentation.Device:
        '''Creates a copy of this device.
        
        :returns: Copy of this device.'''
        ...
    
    def dispose(self) -> None:
        '''Disposes the device.'''
        ...
    
    def start_document(self) -> None:
        '''Starts the whole document.'''
        ...
    
    def end_document(self) -> None:
        '''Finalizes the whole document.'''
        ...
    
    def start_page(self, width: float, height: float) -> None:
        '''Starts a new page.
        
        :param width: The page width.
        :param height: The page height.'''
        ...
    
    def end_page(self) -> None:
        '''Finalizes a page.'''
        ...
    
    def add_hyperlink(self, active_rect: aspose.pydrawing.RectangleF, border: aspose.pydrawing.Pen, target_uri: str) -> None:
        '''Sets the hyperlink with a URI as its target.
        
        :param active_rect: The active rectangle of the link.
        :param border: The link border.
        :param target_uri: The target URI.'''
        ...
    
    def set_transform(self, matrix: aspose.pydrawing.Drawing2D.Matrix) -> None:
        '''Sets the current coordinate space transformation.
        
        :param matrix: A transformation matrix.'''
        ...
    
    def set_clip(self, path: aspose.pydrawing.Drawing2D.GraphicsPath) -> None:
        '''Sets the current clip path.
        
        :param path: A clip path.'''
        ...
    
    def draw_string(self, str: str, origin_x: float, origin_y: float, char_infos: list[aspose.tex.presentation.GlyphData]) -> None:
        ...
    
    def draw_path(self, path: aspose.pydrawing.Drawing2D.GraphicsPath) -> None:
        '''Draws a path.
        
        :param path: A path to draw.'''
        ...
    
    def fill_path(self, path: aspose.pydrawing.Drawing2D.GraphicsPath) -> None:
        '''Fills a path.
        
        :param path: A path to fill.'''
        ...
    
    def show_image(self, origin: aspose.pydrawing.PointF, size: aspose.pydrawing.SizeF, image_data: bytes) -> None:
        '''Shows a raster image.
        
        :param origin: The bottom-left corner of the shown image.
        :param size: The size of the shown image.
        :param image_data: The image data.'''
        ...
    
    @property
    def page_count(self) -> int:
        '''Gets the number of pages.'''
        ...
    
    @property
    def is_ready(self) -> bool:
        '''Shows if device is ready for output.'''
        ...
    
    @property
    def destination_name(self) -> str:
        '''Gets destination name: output file name or device description.'''
        ...
    
    @property
    def stroke(self) -> aspose.pydrawing.Pen:
        '''Gets/sets the current stroke.'''
        ...
    
    @stroke.setter
    def stroke(self, value: aspose.pydrawing.Pen):
        ...
    
    @property
    def fill(self) -> aspose.pydrawing.Brush:
        '''Gets/sets the current fill.'''
        ...
    
    @fill.setter
    def fill(self, value: aspose.pydrawing.Brush):
        ...
    
    @property
    def stroke_opacity(self) -> float:
        '''Gets/sets the current stroke opacity.'''
        ...
    
    @stroke_opacity.setter
    def stroke_opacity(self, value: float):
        ...
    
    @property
    def fill_opacity(self) -> float:
        '''Gets/sets the current fill opacity.'''
        ...
    
    @fill_opacity.setter
    def fill_opacity(self, value: float):
        ...
    
    ...

class GlyphData:
    '''Container class for glyph data required for precise typesetting of a text string.'''
    
    def __init__(self):
        '''Creates new instance.'''
        ...
    
    @property
    def natural_width(self) -> float:
        '''Gets/sets glyph width defined by font.'''
        ...
    
    @natural_width.setter
    def natural_width(self, value: float):
        ...
    
    @property
    def advance_width(self) -> float:
        '''Gets/sets glyph width taking into account kerns.'''
        ...
    
    @advance_width.setter
    def advance_width(self, value: float):
        ...
    
    @property
    def u_offset(self) -> float:
        '''Gets/sets horizontal offset.'''
        ...
    
    @u_offset.setter
    def u_offset(self, value: float):
        ...
    
    @property
    def v_offset(self) -> float:
        '''Gets/sets vertical offset.'''
        ...
    
    @v_offset.setter
    def v_offset(self, value: float):
        ...
    
    ...

class IFragmentRasterizer:
    '''Interface that allows to rasterize TeX fragments.'''
    
    def start_fragment(self) -> None:
        '''Starts a fragment to rasterize.'''
        ...
    
    def end_fragment(self) -> None:
        '''Ends a fragment to rasterize.'''
        ...
    
    ...

class IInteractiveDevice:
    '''The interface defining interactive features processing methods.'''
    
    def add_bookmark(self, name: str, position: aspose.pydrawing.PointF) -> None:
        '''Adds the bookmark identified by the name.
        
        :param name: The name.
        :param position: The position.'''
        ...
    
    ...

class SaveOptions:
    '''Basic class for document saving options.'''
    
    @property
    def subset_fonts(self) -> bool:
        '''Gets/sets the flag indicating whether to subset fonts in output file or not.'''
        ...
    
    @subset_fonts.setter
    def subset_fonts(self, value: bool):
        ...
    
    @property
    def rasterize_formulas(self) -> bool:
        '''Gets/sets the flag that allows to rasterize math formulas.'''
        ...
    
    @rasterize_formulas.setter
    def rasterize_formulas(self, value: bool):
        ...
    
    @property
    def rasterize_included_graphics(self) -> bool:
        '''Gets/sets the flag that allows to rasterize PS/EPS and/or XPS/OXPS included graphics.'''
        ...
    
    @rasterize_included_graphics.setter
    def rasterize_included_graphics(self, value: bool):
        ...
    
    ...

