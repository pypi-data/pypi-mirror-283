import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class FigureRendererPlugin:
    '''The Figure Renderer plugin class.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.tex.plugins.IPluginOptions) -> aspose.tex.plugins.ResultContainer:
        '''Runs Figure Renderer processing with the specified parameters.
        
        :param options: An options object containing instructions for the FigureRenderer.
        :returns: An ResultContainer object containing the result of the operation.
        
        :raises System.ArgumentException: When given options instance is null or has inappropriate type,
                                          or one of the input/output sources has unsupported type.'''
        ...
    
    ...

class FigureRendererPluginOptions(aspose.tex.features.FigureRendererOptions):
    '''The options for the :class:`FigureRendererPlugin`.'''
    
    def add_input_data_source(self, data_source: aspose.tex.plugins.IDataSource) -> None:
        '''Adds a new data source to the collection.
        
        :param data_source: The data source.'''
        ...
    
    def add_output_data_target(self, data_target: aspose.tex.plugins.IDataSource) -> None:
        '''Adds a new input data target to the collection.
        
        :param data_target: The data target.'''
        ...
    
    @property
    def input_data_collection(self) -> list[aspose.tex.plugins.IDataSource]:
        '''Gets the collection of data sources.'''
        ...
    
    @property
    def output_data_collection(self) -> list[aspose.tex.plugins.IDataSource]:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    ...

class FigureRendererPluginResult:
    '''The Figure Renderer plugin's common result.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string the file path if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> io.BytesIO:
        '''Tries to convert the result to a stream.
        
        :returns: A stream if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def log(self) -> io.BytesIO:
        '''The stream containing the transcript file.'''
        ...
    
    @property
    def size(self) -> aspose.pydrawing.SizeF:
        '''The size of the rendered formula.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a file path.
        
        :returns: ``True`` if the result is a file path; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a stream.
        
        :returns: ``True`` if the result is a stream; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def is_byte_array(self) -> bool:
        '''Indicates whether the result is a byte array.
        
        :returns: ``True`` if the result is a byte array; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` containing output data.'''
        ...
    
    ...

class IDataSource:
    '''The general data source interface.'''
    
    @property
    def data_type(self) -> aspose.tex.plugins.DataType:
        '''The data source type.'''
        ...
    
    ...

class IOperationResult:
    '''The general operation result interface.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string the file path if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> io.BytesIO:
        '''Tries to convert the result to a stream.
        
        :returns: A stream if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a file path.
        
        :returns: ``True`` if the result is a file path; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a stream.
        
        :returns: ``True`` if the result is a stream; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def is_byte_array(self) -> bool:
        '''Indicates whether the result is a byte array.
        
        :returns: ``True`` if the result is a byte array; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` containing output data.'''
        ...
    
    ...

class IPlugin:
    '''The general plugin interface.'''
    
    def process(self, options: aspose.tex.plugins.IPluginOptions) -> aspose.tex.plugins.ResultContainer:
        '''Runs plugin execution with defined options.
        
        :param options: An options instance.
        :returns: A :class:`ResultContainer` instance containing the execution result.'''
        ...
    
    ...

class IPluginOptions:
    '''The general plugin options interface.'''
    
    ...

class MathRendererPlugin:
    '''MathRenderer plugin class.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.tex.plugins.IPluginOptions) -> aspose.tex.plugins.ResultContainer:
        '''Runs Math Renderer processing with the specified parameters.
        
        :param options: An options object containing instructions for the MathRenderer.
        :returns: An ResultContainer object containing the result of the operation.
        
        :raises System.ArgumentException: When given options instance is null or has inappropriate type,
                                          or one of the input/output sources has unsupported type.'''
        ...
    
    ...

class MathRendererPluginOptions(aspose.tex.features.MathRendererOptions):
    '''The options for the :class:`MathRendererPlugin`.'''
    
    def add_input_data_source(self, data_source: aspose.tex.plugins.IDataSource) -> None:
        '''Adds a new data source to the collection.
        
        :param data_source: The data source.'''
        ...
    
    def add_output_data_target(self, data_target: aspose.tex.plugins.IDataSource) -> None:
        '''Adds a new input data target to the collection.
        
        :param data_target: The data target.'''
        ...
    
    @property
    def input_data_collection(self) -> list[aspose.tex.plugins.IDataSource]:
        '''Gets the collection of data sources.'''
        ...
    
    @property
    def output_data_collection(self) -> list[aspose.tex.plugins.IDataSource]:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    ...

class MathRendererPluginResult:
    '''The Math Renderer plugin's common result.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string the file path if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> io.BytesIO:
        '''Tries to convert the result to a stream.
        
        :returns: A stream if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def log(self) -> io.BytesIO:
        '''The stream containing the transcript file.'''
        ...
    
    @property
    def size(self) -> aspose.pydrawing.SizeF:
        '''The size of the rendered formula.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a file path.
        
        :returns: ``True`` if the result is a file path; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a stream.
        
        :returns: ``True`` if the result is a stream; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def is_byte_array(self) -> bool:
        '''Indicates whether the result is a byte array.
        
        :returns: ``True`` if the result is a byte array; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` containing output data.'''
        ...
    
    ...

class PngFigureRendererPluginOptions(aspose.tex.plugins.FigureRendererPluginOptions):
    '''The Figure Renderer plugin's options to render a LaTeX figure in PNG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    @property
    def resolution(self) -> int:
        '''Gets/sets the image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: int):
        ...
    
    ...

class PngMathRendererPluginOptions(aspose.tex.plugins.MathRendererPluginOptions):
    '''The Math Renderer plugin's options to render a math formula in PNG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    @property
    def resolution(self) -> int:
        '''Gets/sets the image resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value: int):
        ...
    
    ...

class ResultContainer:
    '''The plugin execution result container.'''
    
    @property
    def result_collection(self) -> list[aspose.tex.plugins.IOperationResult]:
        '''Gets the collection of plugin execution results.'''
        ...
    
    ...

class StreamDataSource:
    '''The stream data source for plugin's load and save operations.'''
    
    def __init__(self, data: io.BytesIO):
        '''Creates a new stream data source.
        
        :param data: The stream.'''
        ...
    
    @property
    def data_type(self) -> aspose.tex.plugins.DataType:
        '''The data source type.'''
        ...
    
    @property
    def data(self) -> io.BytesIO:
        '''Gets the underlying stream.'''
        ...
    
    ...

class StringDataSource:
    '''The string data source for plugin's load operations.'''
    
    def __init__(self, data: str):
        '''Creates a new string data source.
        
        :param data: The string data.'''
        ...
    
    @property
    def data_type(self) -> aspose.tex.plugins.DataType:
        '''The data source type.'''
        ...
    
    @property
    def data(self) -> str:
        '''Gets the underlying string.'''
        ...
    
    ...

class SvgFigureRendererPluginOptions(aspose.tex.plugins.FigureRendererPluginOptions):
    '''The Figure Renderer plugin's options to render a LaTeX figure in SVG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    ...

class SvgMathRendererPluginOptions(aspose.tex.plugins.MathRendererPluginOptions):
    '''The Math Renderer plugin's options to render a math formula in SVG.'''
    
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    ...

class DataType:
    '''Enumerates available data types for plugins I/O.'''
    
    STREAM: int
    STRING: int

