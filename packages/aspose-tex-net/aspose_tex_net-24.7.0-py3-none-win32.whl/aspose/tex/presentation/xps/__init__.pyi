import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class XpsDevice(aspose.tex.presentation.Device):
    '''Implements the interface for outputting text and graphic content to XPS document.'''
    
    @overload
    def __init__(self):
        '''Creates a new instance.
        The output file will be written to the output working
        directory taking the job name as a file name.'''
        ...
    
    @overload
    def __init__(self, stream: io.BytesIO):
        '''Creates a new instance.
        The output file will be written to specified stream.
        
        :param stream: The stream to write the output file to.'''
        ...
    
    def initialize(self) -> None:
        '''Initializes the device.'''
        ...
    
    def create(self) -> aspose.tex.presentation.Device:
        '''Creates a copy of this device.
        
        :returns: Copy of this device.'''
        ...
    
    def dispose(self) -> None:
        '''Disposes this device instance. Finalizes this device instance graphics state,
        i.e. switches APS composing context to the  of the level higher then this
        device's graphics state .'''
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
        '''Set the hyperlink with a URI as its target.
        
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
    
    def draw_path(self, path: aspose.pydrawing.Drawing2D.GraphicsPath) -> None:
        '''Draws a path.
        
        :param path: A path to draw.'''
        ...
    
    def fill_path(self, path: aspose.pydrawing.Drawing2D.GraphicsPath) -> None:
        '''Fill a path.
        
        :param path: A path to fill.'''
        ...
    
    def show_image(self, origin: aspose.pydrawing.PointF, size: aspose.pydrawing.SizeF, image_data: bytes) -> None:
        '''Shows a raster image.
        
        :param origin: The bottom-left corner of the shown image.
        :param size: The size of the shown image.
        :param image_data: The image data.'''
        ...
    
    def add_bookmark(self, name: str, position: aspose.pydrawing.PointF) -> None:
        '''Adds the bookmark identified by the name.
        
        :param name: The name.
        :param position: The position.'''
        ...
    
    def start_fragment(self) -> None:
        '''Starts a fragment to rasterize.'''
        ...
    
    def end_fragment(self) -> None:
        '''Ends a fragment to rasterize.'''
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

class XpsSaveOptions(aspose.tex.presentation.SaveOptions):
    '''Class representing options of saving to XPS.'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    ...

