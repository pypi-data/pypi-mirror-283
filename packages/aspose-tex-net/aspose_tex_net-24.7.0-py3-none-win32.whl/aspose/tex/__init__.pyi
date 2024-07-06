from aspose.tex import features
from aspose.tex import io
from aspose.tex import plugins
from aspose.tex import presentation
from aspose.tex import resourceproviders
import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable
from typing import Any

def get_pyinstaller_hook_dirs() -> Any:
  """Function required by PyInstaller. Returns paths to module 
  PyInstaller hooks. Not intended to be called explicitly."""

class BuildVersionInfo:
    '''This class provides information about current product build.'''
    
    def __init__(self):
        ...
    
    ASSEMBLY_VERSION: str
    
    PRODUCT: str
    
    FILE_VERSION: str
    
    ...

class License:
    '''Provides methods to license the component.'''
    
    def __init__(self):
        '''Initializes a new instance of this class.'''
        ...
    
    @overload
    def set_license(self, license_name: str) -> None:
        '''Licenses the component.
        
        Tries to find the license in the following locations:
        
        1. Explicit path.'''
        ...
    
    @overload
    def set_license(self, stream: io.BytesIO) -> None:
        '''Licenses the component.
        
        :param stream: A stream that contains the license.
        
        Use this method to load a license from a stream.'''
        ...
    
    @property
    def embedded(self) -> bool:
        '''License number was added as embedded resource.'''
        ...
    
    @embedded.setter
    def embedded(self, value: bool):
        ...
    
    ...

class Metered:
    '''Provides methods to set metered key.'''
    
    def __init__(self):
        '''Initializes a new instance of this class.'''
        ...
    
    def set_metered_key(self, public_key: str, private_key: str) -> None:
        '''Sets metered public and private key.
        If you purchase metered license, when start application, this API should be called, normally, this is enough.
        However, if always fail to upload consumption data and exceed 24 hours, the license will be set to evaluation status,
        to avoid such case, you should regularly check the license status, if it is evaluation status, call this API again.
        
        :param public_key: public key
        :param private_key: private key'''
        ...
    
    @staticmethod
    def get_consumption_quantity(self) -> decimal.Decimal:
        '''Gets consumption file size
        
        :returns: consumption quantity'''
        ...
    
    @staticmethod
    def get_consumption_credit(self) -> decimal.Decimal:
        '''Gets consumption credit
        
        :returns: consumption quantity'''
        ...
    
    ...

class TeXConfig:
    '''Class providing available TeX configurations.'''
    
    @overload
    @staticmethod
    def object_tex(self) -> aspose.tex.TeXConfig:
        '''Gets the configuration of "standard" ObjectTeX engine extension.
        
        :returns: The "standard" ObjectTeX engine extension configuration.'''
        ...
    
    @overload
    @staticmethod
    def object_tex(self, format_provider: aspose.tex.resourceproviders.FormatProvider) -> aspose.tex.TeXConfig:
        '''Gets the configuration of ObjectTeX engine extension with provided format preloaded.
        
        :param format_provider: The format provider.
                                If left equal to null then default ObjectTeX format (which is essentially Plain TeX) will be loaded.
        :returns: "ObjectTeX engine extension with provided format preloaded" configuration.'''
        ...
    
    object_ini_tex: aspose.tex.TeXConfig
    
    object_latex: aspose.tex.TeXConfig
    
    ...

class TeXExtension:
    '''Class defining constants to choose a TeX engine extension from.'''
    
    OBJECT_TEX: aspose.tex.TeXExtension
    
    ...

class TeXJob:
    '''Implements features of a TeX job.'''
    
    @overload
    def __init__(self, stream: io.BytesIO, device: aspose.tex.presentation.Device, options: aspose.tex.TeXOptions):
        '''Creates a TeX job for running the engine in production mode to typeset a TeX file.
        
        :param stream: The stream containing the TeX file.
        :param device: The device defining output representation.
        :param options: TeX engine run options.'''
        ...
    
    @overload
    def __init__(self, path: str, device: aspose.tex.presentation.Device, options: aspose.tex.TeXOptions):
        '''Creates a TeX job for running the engine in production mode to typeset a TeX file.
        
        :param path: The path to the TeX file.
        :param device: The device defining output representation.
        :param options: TeX engine run options.'''
        ...
    
    @overload
    def __init__(self, device: aspose.tex.presentation.Device, options: aspose.tex.TeXOptions):
        '''Creates a TeX job for running the engine in production mode to typeset a TeX document.
        The engine will prompt the file name as soon as it starts.
        Thus this run is supposed to be interactive.
        
        :param device: The device defining output representation.
        :param options: TeX engine run options.'''
        ...
    
    def run(self) -> aspose.tex.TeXJobResult:
        '''Runs TeX job.
        
        :returns: The result of the job execution.'''
        ...
    
    @staticmethod
    def create_format(self, path: str, options: aspose.tex.TeXOptions) -> None:
        '''Runs TeX engine in INITEX mode to create a format file (.fmt).
        
        :param path: The path to the main format source file.
        :param options: TeX engine run options.'''
        ...
    
    ...

class TeXOptions:
    '''TeX file processing options class.'''
    
    @staticmethod
    def console_app_options(self, config: aspose.tex.TeXConfig) -> aspose.tex.TeXOptions:
        '''Returns options for use in a console application.
        
        :param config: A TeX config.
        :returns: TeX options.'''
        ...
    
    @property
    def job_name(self) -> str:
        '''Gets/set the name of the job.'''
        ...
    
    @job_name.setter
    def job_name(self, value: str):
        ...
    
    @property
    def terminal_in(self) -> aspose.tex.io.IInputTerminal:
        '''Gets/sets the input terminal reader.'''
        ...
    
    @terminal_in.setter
    def terminal_in(self, value: aspose.tex.io.IInputTerminal):
        ...
    
    @property
    def terminal_out(self) -> aspose.tex.io.IOutputTerminal:
        '''Gets/sets the output terminal writer.'''
        ...
    
    @terminal_out.setter
    def terminal_out(self, value: aspose.tex.io.IOutputTerminal):
        ...
    
    @property
    def input_working_directory(self) -> aspose.tex.io.IInputWorkingDirectory:
        '''Gets/sets input working directory.'''
        ...
    
    @input_working_directory.setter
    def input_working_directory(self, value: aspose.tex.io.IInputWorkingDirectory):
        ...
    
    @property
    def output_working_directory(self) -> aspose.tex.io.IOutputWorkingDirectory:
        '''Gets/sets output working directory.'''
        ...
    
    @output_working_directory.setter
    def output_working_directory(self, value: aspose.tex.io.IOutputWorkingDirectory):
        ...
    
    @property
    def required_input_directory(self) -> aspose.tex.io.IInputWorkingDirectory:
        '''Gets/sets the directory for the required input, e.g.,
        packages that are beyond Aspose.TeX's LaTeX support.'''
        ...
    
    @required_input_directory.setter
    def required_input_directory(self, value: aspose.tex.io.IInputWorkingDirectory):
        ...
    
    @property
    def interaction(self) -> aspose.tex.Interaction:
        '''Gets/sets the interaction mode to run a TeX engine in.'''
        ...
    
    @interaction.setter
    def interaction(self, value: aspose.tex.Interaction):
        ...
    
    @property
    def ignore_missing_packages(self) -> bool:
        '''Gets/sets the flag that instructs the engine whether to halt
        on missing package read attempt or ignore it.'''
        ...
    
    @ignore_missing_packages.setter
    def ignore_missing_packages(self, value: bool):
        ...
    
    @property
    def save_options(self) -> aspose.tex.presentation.SaveOptions:
        '''Gets/sets options used for rendering into destination format (XPS, PDF, image, etc.).
        Default value is the set of default options for rendering to XPS.'''
        ...
    
    @save_options.setter
    def save_options(self, value: aspose.tex.presentation.SaveOptions):
        ...
    
    @property
    def date_time(self) -> datetime.datetime:
        '''Gets/sets a certain value for date/time primitives like \\year, \\month, \\day and \\time.'''
        ...
    
    @date_time.setter
    def date_time(self, value: datetime.datetime):
        ...
    
    @property
    def repeat(self) -> bool:
        '''Gets/sets the flag that indicates whether it is necessary to run the TeX job twice in case,
        for example, there are references in input TeX file(s). In general, this behavior is useful when
        the engine collects some data along the typesetting process and stores it in an auxilliary file,
        all at the first run. And at the second run, the engine somehow uses that data.'''
        ...
    
    @repeat.setter
    def repeat(self, value: bool):
        ...
    
    @property
    def no_ligatures(self) -> bool:
        '''Gets/sets the flag that cancels ligatures in all fonts.'''
        ...
    
    @no_ligatures.setter
    def no_ligatures(self, value: bool):
        ...
    
    @property
    def full_input_file_names(self) -> bool:
        '''Gets/sets the flag indicating whether full or short filenames are output
        to the transcript file and to the terminal when file input begins.'''
        ...
    
    @full_input_file_names.setter
    def full_input_file_names(self, value: bool):
        ...
    
    ...

class Interaction:
    '''Represents increasing amounts of user interaction.'''
    
    BATCH_MODE: int
    NONSTOP_MODE: int
    SCROLL_MODE: int
    ERROR_STOP_MODE: int
    FORMAT_DEFINED: int

class TeXJobResult:
    '''Lists possible results of a TeX job.'''
    
    SPOTLESS: int
    WARNING_ISSUED: int
    ERROR_MESSAGE_ISSUED: int
    FATAL_ERROR_STOP: int

