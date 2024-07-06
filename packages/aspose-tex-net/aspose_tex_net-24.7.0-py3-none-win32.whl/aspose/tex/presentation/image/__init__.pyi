import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class BmpSaveOptions(aspose.tex.presentation.image.ImageSaveOptions):
    '''Class representing options of saving to BMP image(s).'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    ...

class ImageDevice(aspose.tex.presentation.Device):
    '''Implements the interface for outputting text and graphic content to image(s).'''
    
    @overload
    def __init__(self):
        '''Creates a new instance.
        The output file will be written to the output working
        directory taking the job name as a file name.'''
        ...
    
    @overload
    def __init__(self, white_background: bool):
        '''Creates a new instance.
        The output file will be written to the output working
        directory taking the job name as a file name.
        
        :param white_background: If true then fills white background on every page.'''
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
        i.e. switches composing context to the level higher then this device's graphics state.'''
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
    
    @property
    def result(self) -> list[bytes]:
        '''Returns the resulting images byte arrays.
        The first dimension is for inner documents
        and the second one is for pages within inner documents.'''
        ...
    
    ...

class ImageSaveOptions(aspose.tex.presentation.SaveOptions):
    '''Basic class representing options of saving to raster images.'''
    
    @property
    def resolution(self) -> float:
        '''Gets/sets the image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: float):
        ...
    
    @property
    def smoothing_mode(self) -> aspose.pydrawing.Drawing2D.SmoothingMode:
        '''Gets/sets the smoothing mode.'''
        ...
    
    @smoothing_mode.setter
    def smoothing_mode(self, value: aspose.pydrawing.Drawing2D.SmoothingMode):
        ...
    
    @property
    def interpolation_mode(self) -> aspose.pydrawing.Drawing2D.InterpolationMode:
        '''Gets/sets the interpolation mode.'''
        ...
    
    @interpolation_mode.setter
    def interpolation_mode(self, value: aspose.pydrawing.Drawing2D.InterpolationMode):
        ...
    
    @property
    def device_writes_images(self) -> bool:
        '''Gets/sets the flag that determines whether the image device will write output images.
        Set it to
        false
        
         if you are planning to write images using image device's
        Result property.'''
        ...
    
    @device_writes_images.setter
    def device_writes_images(self, value: bool):
        ...
    
    ...

class JpegSaveOptions(aspose.tex.presentation.image.ImageSaveOptions):
    '''Class representing options of saving to JPEG image(s).'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    ...

class PngSaveOptions(aspose.tex.presentation.image.ImageSaveOptions):
    '''Class representing options of saving to PNG image(s).'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    ...

class TiffSaveOptions(aspose.tex.presentation.image.ImageSaveOptions):
    '''Class representing options of saving to TIFF image(s).'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    @property
    def multipage(self) -> bool:
        '''Gets/sets the flag that defines if multiple images
        should be saved in a single multipage TIFF file.'''
        ...
    
    @multipage.setter
    def multipage(self, value: bool):
        ...
    
    @property
    def compression(self) -> aspose.tex.presentation.image.TiffCompression:
        '''Gets/sets the TIFF compression scheme.'''
        ...
    
    @compression.setter
    def compression(self, value: aspose.tex.presentation.image.TiffCompression):
        ...
    
    ...

class TiffCompression:
    '''Enumerates TIFF compression schemes.'''
    
    COMPRESSION_LZW: int
    COMPRESSION_CCITT3: int
    COMPRESSION_CCITT4: int
    COMPRESSION_RLE: int
    COMPRESSION_NONE: int

