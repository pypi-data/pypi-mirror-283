import aspose.tex
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class IFileCollector:
    '''Defines methods for selecting collections of files.'''
    
    def get_file_names_by_extension(self, extension: str, path: str) -> list[str]:
        '''Returns the array of file names by an extension.
        
        :param extension: The file extension.
        :param path: The path inside the directory.
        :returns: The array of file names.'''
        ...
    
    ...

class IFileTerminal:
    '''Interface of terminals which actually are files.'''
    
    def write_file(self) -> None:
        '''Finalizes the log, e.g., writes it to file.'''
        ...
    
    @property
    def file_name(self) -> str:
        '''Gets/sets the file name.'''
        ...
    
    @file_name.setter
    def file_name(self, value: str):
        ...
    
    ...

class IInputTerminal:
    '''Interface for abstract input terminal.'''
    
    @property
    def reader(self) -> aspose.tex.io.TerminalReader:
        '''Gets the reader for the input terminal.'''
        ...
    
    ...

class IInputWorkingDirectory:
    '''Interface of generalized input working directory.'''
    
    def get_file(self, file_name: str, search_subdirectories: bool) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from. MUST NOT return a null object.
        In case a stream cannot be returned, it MUST return a NamedStream object with a null Stream property value instead.
        
        :param file_name: The file name.
        :param search_subdirectories: Indicates whether to look for a file in subdirectories.
        :returns: The named stream.'''
        ...
    
    ...

class IOutputTerminal:
    '''Interface for abstract output terminal.'''
    
    @property
    def writer(self) -> aspose.tex.io.TerminalWriter:
        '''Gets the writer for the output terminal.'''
        ...
    
    ...

class IOutputWorkingDirectory:
    '''Interface of generalized output working directory.'''
    
    def get_output_file(self, file_name: str) -> aspose.tex.io.NamedStream:
        '''Returns the stream to write to. MUST NOT return a null object.
        In case a stream cannot be returned, it MUST return a NamedStream object with a null Stream property value instead.
        
        :param file_name: The file name.
        :returns: The named stream.'''
        ...
    
    ...

class InputConsoleTerminal:
    '''Provides the console as a terminal input source. Wrapper for .'''
    
    def __init__(self):
        ...
    
    @property
    def reader(self) -> aspose.tex.io.TerminalReader:
        '''Gets the console as a terminal input source.'''
        ...
    
    ...

class InputFileSystemDirectory(aspose.tex.io.InputWorkingDirectory):
    '''Implements the regular file system's method for getting a file stream to read from.'''
    
    def __init__(self, base_path: str):
        '''Creates new instance.
        
        :param base_path: The base path of the directory.'''
        ...
    
    @overload
    def get_file(self, file_name: str, search_subdirectories: bool) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from.
        
        :param file_name: The file name.
        :param search_subdirectories: Indicates whether to look for a file in subdirectories.
        :returns: The named stream.'''
        ...
    
    def get_file_names_by_extension(self, extension: str, path: str) -> list[str]:
        '''Returns the array of file names by an extension.
        
        :param extension: The file extension.
        :param path: The path inside the directory.
        :returns: The array of file names.'''
        ...
    
    ...

class InputWorkingDirectory:
    '''The basic class for input working directories.'''
    
    @overload
    def get_file(self, file_name: str) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from.
        
        :param file_name: The file name.
        :returns: The named stream.'''
        ...
    
    @overload
    def get_file(self, file_name: str, search_subdirectories: bool) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from.
        
        :param file_name: The file name.
        :param search_subdirectories: Indicates whether to look for a file in subdirectories.
        :returns: The named stream.'''
        ...
    
    ...

class InputZipDirectory(aspose.tex.io.InputWorkingDirectory):
    '''Implements the method for getting a file stream to write to when working directory is a ZIP archive.'''
    
    def __init__(self, zip_stream: io.BytesIO, base_path: str):
        '''Creates new instance.
        
        :param zip_stream: The stream to read the archive from.
        :param base_path: The base path inside the ZIP archive.'''
        ...
    
    @overload
    def get_file(self, file_name: str, search_subdirectories: bool) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from.
        
        :param file_name: The file name.
        :param search_subdirectories: Indicates whether to look for a file in subdirectories.
        :returns: The named stream.'''
        ...
    
    def get_file_names_by_extension(self, extension: str, path: str) -> list[str]:
        '''Returns the array of file names by an extension.
        
        :param extension: The file extension.
        :param path: The path inside the directory.
        :returns: The array of file names.'''
        ...
    
    ...

class NamedStream:
    '''Associates a stream of a random nature with a name.'''
    
    def __init__(self, stream: io.BytesIO, full_name: str):
        '''Creates a new instance.
        
        :param stream: The stream.
        :param full_name: The full name of the stream.'''
        ...
    
    @property
    def full_name(self) -> str:
        '''Gets the full name of the stream.'''
        ...
    
    @property
    def stream(self) -> io.BytesIO:
        '''Gets the stream itself.'''
        ...
    
    ...

class NondisposableMemoryStream:
    '''The class that encapsulates a stream that cannot be disposed by calling
    the  method, whether explicitly or implicitly.'''
    
    @overload
    def __init__(self):
        '''Creates a new instance.'''
        ...
    
    @overload
    def __init__(self, stream: io.BytesIO):
        '''Creates a new instance using some data stream.
        
        :param stream: The data stream.'''
        ...
    
    ...

class OutputConsoleTerminal:
    '''Provides the console as a terminal output destination. Wrapper for .'''
    
    def __init__(self):
        ...
    
    @property
    def writer(self) -> aspose.tex.io.TerminalWriter:
        '''Gets the console as a terminal output destination.'''
        ...
    
    ...

class OutputFileSystemDirectory(aspose.tex.io.InputFileSystemDirectory):
    '''Implements the regular file system's method for getting a file stream to write to.'''
    
    def __init__(self, base_path: str):
        '''Creates new instance.
        
        :param base_path: The base path of the directory.'''
        ...
    
    def get_output_file(self, file_name: str) -> aspose.tex.io.NamedStream:
        '''Returns the stream to write to.
        
        :param file_name: The file name.
        :returns: The named stream.'''
        ...
    
    ...

class OutputFileTerminal:
    '''Implements a terminal whose output is to be written to a file in some working directory.'''
    
    def __init__(self, working_directory: aspose.tex.io.IOutputWorkingDirectory):
        '''Creates new instance.
        
        :param working_directory: The working directory.'''
        ...
    
    def write_file(self) -> None:
        '''Finalizes the log, e.g., writes it to file.'''
        ...
    
    @property
    def file_name(self) -> str:
        '''Gets/sets the file name.'''
        ...
    
    @file_name.setter
    def file_name(self, value: str):
        ...
    
    @property
    def writer(self) -> aspose.tex.io.TerminalWriter:
        '''Gets the writer for the output terminal.'''
        ...
    
    ...

class OutputMemoryTerminal:
    '''Provides a memory stream as a terminal output destination.'''
    
    def __init__(self):
        ...
    
    @property
    def writer(self) -> aspose.tex.io.TerminalWriter:
        '''Gets the writer for the output terminal.'''
        ...
    
    @property
    def stream(self) -> io.BytesIO:
        '''Gets the memory stream.'''
        ...
    
    ...

class OutputZipDirectory(aspose.tex.io.InputWorkingDirectory):
    '''Implements the method for getting a file stream to write to when working directory is a ZIP archive.'''
    
    def __init__(self, zip_stream: io.BytesIO):
        '''Creates new instance.
        
        :param zip_stream: The stream to write the archive to.'''
        ...
    
    @overload
    def get_file(self, file_name: str, search_subdirectories: bool) -> aspose.tex.io.NamedStream:
        '''Returns the stream to read from.
        
        :param file_name: The file name.
        :param search_subdirectories: Indicates whether to look for a file in subdirectories.
        :returns: The named stream.'''
        ...
    
    def get_output_file(self, file_name: str) -> aspose.tex.io.NamedStream:
        '''Returns the stream to write to.
        
        :param file_name: The file name.
        :returns: The named stream.'''
        ...
    
    def finish(self) -> None:
        '''Finalizes ZIP archive.'''
        ...
    
    ...

class TerminalReader:
    '''Provides reading from a text stream.'''
    
    @overload
    def read(self) -> int:
        '''Reads the next character from the text reader and advances the character position by one character.
        
        :returns: The next character from the text reader, or -1 if no more characters are available.'''
        ...
    
    @overload
    def read(self, buffer: list[str], index: int, count: int) -> int:
        '''Reads a specified maximum number of characters from the current reader and writes the data to a buffer,
        beginning at the specified index.
        
        :param buffer: When this method returns, contains the specified character array with the values
                       between index and (index + count - 1) replaced by the characters read from the current source.
        :param index: The position in buffer at which to begin writing.
        :param count: he maximum number of characters to read. If the end of the reader is reached before
                      the specified number of characters is read into the buffer, the method returns.
        :returns: The number of characters that have been read. The number will be less than or equal to count,
                  depending on whether the data is available within the reader. This method returns 0 (zero) if it is called
                  when no more characters are left to read.'''
        ...
    
    def read_to_end(self) -> str:
        '''Reads all characters from the current position to the end of the text reader and returns them as one string.
        
        :returns: A string that contains all characters from the current position to the end of the text reader.'''
        ...
    
    def read_line(self) -> str:
        '''Reads a line of characters from the text reader and returns the data as a string.
        
        :returns: The next line from the reader, or null if all characters have been read.'''
        ...
    
    def close(self) -> None:
        '''Closes the TextReader and releases any system resources associated with the TextReader.'''
        ...
    
    ...

class TerminalWriter:
    '''Provides writing to a text stream.'''
    
    @overload
    def write_line(self) -> None:
        '''Writes a line terminator to the text stream.'''
        ...
    
    @overload
    def write_line(self, value: bool) -> None:
        '''Writes the text representation of a Boolean value to the text stream, followed by a line terminator.
        
        :param value: A boolean value.'''
        ...
    
    @overload
    def write_line(self, value: str) -> None:
        '''Writes a string to the text stream, followed by a line terminator.
        
        :param value: A character string.'''
        ...
    
    @overload
    def write_line(self, value: str) -> None:
        '''Writes a character to the text stream, followed by a line terminator.
        
        :param value: A char value.'''
        ...
    
    @overload
    def write_line(self, buffer: list[str]) -> None:
        '''Writes an array of characters to the text stream, followed by a line terminator.
        
        :param buffer: An array of characters.'''
        ...
    
    @overload
    def write_line(self, value: decimal.Decimal) -> None:
        '''Writes the text representation of a decimal value to the text stream, followed by a line terminator.
        
        :param value: A decimal value.'''
        ...
    
    @overload
    def write_line(self, value: float) -> None:
        '''Writes the text representation of a 8-byte floating-point value to the text stream, followed by a line terminator.
        
        :param value: A double value.'''
        ...
    
    @overload
    def write_line(self, value: float) -> None:
        '''Writes the text representation of a 4-byte floating-point value to the text stream, followed by a line terminator.
        
        :param value: A float value.'''
        ...
    
    @overload
    def write_line(self, value: int) -> None:
        '''Writes the text representation of a 4-byte signed integer to the text stream, followed by a line terminator.
        
        :param value: An integer value.'''
        ...
    
    @overload
    def write_line(self, value: int) -> None:
        '''Writes the text representation of an 8-byte signed integer to the text stream, followed by a line terminator.
        
        :param value: A long integer value.'''
        ...
    
    @overload
    def write_line(self, value: int) -> None:
        '''Writes the text representation of a 4-byte unsigned integer to the text stream, followed by a line terminator.
        
        :param value: An unsigned integer value.'''
        ...
    
    @overload
    def write_line(self, value: int) -> None:
        '''Writes the text representation of an 8-byte unsigned integer to the text stream, followed by a line terminator.
        
        :param value: An unsigned long integer value.'''
        ...
    
    @overload
    def write(self, value: bool) -> None:
        '''Writes the text representation of a Boolean value to the text stream.
        
        :param value: A Boolean value.'''
        ...
    
    @overload
    def write(self, value: str) -> None:
        '''Writes a character to the text stream.
        
        :param value: A character.'''
        ...
    
    @overload
    def write(self, value: str) -> None:
        '''Writes a string to the text stream.
        
        :param value: A character string.'''
        ...
    
    @overload
    def write(self, value: list[str]) -> None:
        '''Writes a character array to the text stream.
        
        :param value: A character array.'''
        ...
    
    @overload
    def write(self, value: decimal.Decimal) -> None:
        '''Writes the text representation of a decimal value to the text stream.
        
        :param value: A decimal value.'''
        ...
    
    @overload
    def write(self, value: float) -> None:
        '''Writes the text representation of an 8-byte floating-point value to the text stream.
        
        :param value: A double value.'''
        ...
    
    @overload
    def write(self, value: float) -> None:
        '''Writes the text representation of a 4-byte floating-point value to the text stream.
        
        :param value: A float value.'''
        ...
    
    @overload
    def write(self, value: int) -> None:
        '''Writes the text representation of a 4-byte signed integer to the text stream.
        
        :param value: An integer value.'''
        ...
    
    @overload
    def write(self, value: int) -> None:
        '''Writes the text representation of an 8-byte signed integer to the text stream.
        
        :param value: A long integer value.'''
        ...
    
    @overload
    def write(self, value: int) -> None:
        '''Writes the text representation of a 4-byte unsigned integer to the text stream.
        
        :param value: An unsigned integer value.'''
        ...
    
    @overload
    def write(self, value: int) -> None:
        '''Writes the text representation of an 8-byte unsigned integer to the text stream.
        
        :param value: An unsigned long integer value.'''
        ...
    
    def flush(self) -> None:
        '''Clears all buffers for the current writer and causes any buffered data to be written to the underlying device.'''
        ...
    
    def close(self) -> None:
        '''Closes the current writer and releases any system resources associated with the writer.'''
        ...
    
    @property
    def encoding(self) -> str:
        '''Returns the character encoding in which the output is written.'''
        ...
    
    @property
    def new_line(self) -> str:
        '''Gets or sets the line terminator string used by the current TextWriter.'''
        ...
    
    ...

