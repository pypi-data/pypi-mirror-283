import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class PdfDevice(aspose.tex.presentation.Device):
    '''Implements the interface for outputting text and graphic content to PDF document.'''
    
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
        
        :param origin: Top-left corner of the shown image.
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

class PdfEncryptionDetails:
    '''Contains details for a pdf encryption.'''
    
    def __init__(self, user_password: str, owner_password: str, permissions: int, encryption_algorithm: aspose.tex.presentation.pdf.PdfEncryptionAlgorithm):
        '''Initializes a new instance of the  class.
        
        :param user_password: The user password.
        :param owner_password: The owner password.
        :param permissions: The permissions.
        :param encryption_algorithm: The encryption algorithm.'''
        ...
    
    @property
    def user_password(self) -> str:
        '''Gets or sets the User password.
        
        Opening the document with the correct user password (or opening a document
        that does not have a user password) allows additional operations to be
        performed according to the user access permissions specified in the document’s
        encryption dictionary.'''
        ...
    
    @user_password.setter
    def user_password(self, value: str):
        ...
    
    @property
    def owner_password(self) -> str:
        '''Gets or sets the Owner password.
        
        Opening the document with the correct owner password (assuming it is not the
        same as the user password) allows full (owner) access to the document. This
        unlimited access includes the ability to change the document’s passwords and
        access permissions.'''
        ...
    
    @owner_password.setter
    def owner_password(self, value: str):
        ...
    
    @property
    def permissions(self) -> int:
        '''Gets or sets the permissions.'''
        ...
    
    @permissions.setter
    def permissions(self, value: int):
        ...
    
    @property
    def encryption_algorithm(self) -> aspose.tex.presentation.pdf.PdfEncryptionAlgorithm:
        '''Gets or sets the encryption mode.'''
        ...
    
    @encryption_algorithm.setter
    def encryption_algorithm(self, value: aspose.tex.presentation.pdf.PdfEncryptionAlgorithm):
        ...
    
    ...

class PdfSaveOptions(aspose.tex.presentation.SaveOptions):
    '''Class representing options of saving to PDF.'''
    
    def __init__(self):
        '''Creates new instance of options.'''
        ...
    
    @property
    def jpeg_quality_level(self) -> int:
        '''The Quality category specifies the level of compression for an image.
        Available values are 0 to 100.
        The lower the number specified, the higher the compression and therefore the lower the quality of the image.
        0 value results in lowest quality image, while 100 results in highest.'''
        ...
    
    @jpeg_quality_level.setter
    def jpeg_quality_level(self, value: int):
        ...
    
    @property
    def outline_tree_height(self) -> int:
        '''Specifies the height of the document outline tree to save.
        0 - the outline tree will not be converted,
        1 - only the first level outline items will be converted,
        ans so on.'''
        ...
    
    @outline_tree_height.setter
    def outline_tree_height(self, value: int):
        ...
    
    @property
    def outline_tree_expansion_level(self) -> int:
        '''Specifies up to what level the document outline should be expanded when the PDF file is viewed.
        1 - only the first level outline items are shown,
        2 - only the first and second level outline items are shown,
        and so on.
        Default is 1.'''
        ...
    
    @outline_tree_expansion_level.setter
    def outline_tree_expansion_level(self, value: int):
        ...
    
    @property
    def text_compression(self) -> aspose.tex.presentation.pdf.PdfTextCompression:
        '''Specifies compression type to be used for all content streams except images.
        Default is :attr:`PdfTextCompression.FLATE`.'''
        ...
    
    @text_compression.setter
    def text_compression(self, value: aspose.tex.presentation.pdf.PdfTextCompression):
        ...
    
    @property
    def image_compression(self) -> aspose.tex.presentation.pdf.PdfImageCompression:
        '''Specifies compression type to be used for all images in the document.
        Default is :attr:`PdfImageCompression.AUTO`.'''
        ...
    
    @image_compression.setter
    def image_compression(self, value: aspose.tex.presentation.pdf.PdfImageCompression):
        ...
    
    @property
    def encryption_details(self) -> aspose.tex.presentation.pdf.PdfEncryptionDetails:
        '''Gets or sets a encryption details. If not set, then no encryption will be performed.'''
        ...
    
    @encryption_details.setter
    def encryption_details(self, value: aspose.tex.presentation.pdf.PdfEncryptionDetails):
        ...
    
    ...

class PdfEncryptionAlgorithm:
    '''Encryption mode enum. Describe using algorithm and key length.
    This enum is extended in order to be able to further increase functionality.
    This enum implements "Base-to-Core" pattern.'''
    
    RC4_40: int
    RC4_128: int

class PdfImageCompression:
    '''Specifies the type of compression applied to images in the PDF file.'''
    
    AUTO: int
    NONE: int
    RLE: int
    FLATE: int
    LZW_BASELINE_PREDICTOR: int
    LZW_OPTIMIZED_PREDICTOR: int
    JPEG: int

class PdfTextCompression:
    '''Specifies a type of compression applied to all contents in the PDF file except images.'''
    
    NONE: int
    RLE: int
    LZW: int
    FLATE: int

