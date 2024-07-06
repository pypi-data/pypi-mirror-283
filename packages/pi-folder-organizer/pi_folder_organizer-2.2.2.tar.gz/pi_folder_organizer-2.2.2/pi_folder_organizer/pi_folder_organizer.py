import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from ._exceptions import DangerZone
from ._exceptions import DestinationInsideSourceError

class PiFolderOrganizer:
    """
    A class for organizing files based on their types into separate folders.

    Attributes:
    - counter (dict): A dictionary that stores the count of files for each category.
    - extensions (dict): A dictionary that maps file categories to their corresponding extensions.

    Methods:
    - get_counter(): Returns the current counter dictionary.
    - set_counter(new_counter: dict): Updates the counter dictionary with a new one.
    - get_extensions(): Returns the current extensions dictionary.
    - set_extensions(new_extensions: dict): Updates the extensions dictionary with a new one.
    - pi_organizer(source_path, destination_path): Organizes files from source_path into separate folders in destination_path
      based on their types according to the extensions dictionary.

    Usage:
    - Create an instance of PiFolderOrganizer.
    - Customize the counter and extensions dictionaries if needed.
    - Use the pi_organizer method to organize files from source_path into separate folders in destination_path.

    Example:
    ```
    pi_organizer = PiFolderOrganizer()
    new_counter = {"Images": [], "Documents": []}
    pi_organizer .set_counter(new_counter)
    new_extensions = {"Images": (".png", ".jpg"), "Documents": (".txt", ".docs")}
    pi_organizer .set_extensions(new_extensions)
    pi_organizer .pi_organizer(source_path, destination_path)
    ```
    """
    
    __RESTRICTED_PATHS = [
        "/bin", "/usr", "/sbin", "/usr/bin", "/usr/sbin", "/etc", "/var/log", "/usr/lib", "/lib", "/tmp",
        r"C:\Windows", r"C:\Program Files", r"C:\Program Files (x86)", r"C:\Users\Public", r"C:\ProgramData", r"C:\Windows\System32", r"C:\Temp",
        "/Applications", "/System", "/Library", "/Users", "/private"
    ]
    def __init__(self) -> None:
        
       
    
        self.__counter = {
                "Images": [],
                "Audios": [],
                "Videos": [],
                "Documents": [],
                "Compressed": [],
                "WindowsSoftwares": [],
                "LinuxSoftwares": [],
                "MacSoftwares": [],
                "CodeFiles": [],
                "ConfigurationFiles": [],
                "SystemFiles": [],
                "DatabaseFiles": [],
                "LogFiles":[],
                "FontsFiles":[],
                "SerializedFiles": [],
                "WebURLs": [],
                "AndroidAPKs": [],
                "ISOsFiles":[],
                "VirtualMachinesFiles":[],
                "JupyterNotebooks":[],
                "Others": []
            }

        self.__extensions = {
                "Images": (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg",".svgz", ".tiff",".tif",".eps",".psd",
                        ".heic","heif",".ind",".indd",".indt",".raw",".arw",".cr2",".nrw",".k25",".dib",
                        ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2",".ico"),
                "Audios": (".mp3", ".wav", ".ogg", ".aac", ".flac", ".wma",".opus"),
                "Videos": ('.mov', '.mp2v', '.3gp', '.mpg', '.hevc', '.ogg', '.avi', '.wmv', '.ts', '.ogv', 
                            '.swf', '.webp', '.rm', '.m2v', '.h264', '.m2ts', '.xvid', '.flv', '.mpeg', 
                            '.vp9', '.divx', '.mp4', '.webm', '.rmvb', '.avchd', '.dv', '.mpeg2', '.m4v',
                            '.vob', '.mpeg4', '.mkv', '.mpg2', '.h265', '.mxf', '.m1v', '.mts', '.3g2', '.mod'),
                
                "Documents": (".pdf",".aspx",".djvu",
                ".csv",".xlsb",".odp",".doc", ".docx",".docs", ".xls", ".xlsx",".xlsm", ".ppt", ".pptx",".accdb", ".odt", ".ods",
                ".txt",'.md','.rtf',".inp",".tex",".odf",".env"),
                "Compressed": (".zip", ".rar", ".tar", ".gz", ".7z",".bz2",".xz",".zar",".lzma"),
                "WindowsSoftwares": (".exe", ".msi", ".bat", ".sh",".jar"),
                "LinuxSoftwares": (".deb", ".sh", ".tar.gz", ".run", ".tar.xz", ".AppImage", ".linux",".flatpakref",".whl",".tgz"),
                "MacSoftwares": (".app", ".dmg", ".pkg", ".bin", ".out", ".command",),
                "CodeFiles": (".py",".nb",".php",".rb",".pl",".sh", ".js", ".html", ".css", ".m",".mlx", ".mojo", ".ts", ".cpp",".java",".c",".mltbx"),
                "ConfigurationFiles": (".yaml",".yml",".config",".ini",".cfg","LICENSE",".cmd",".xml"),
                "SystemFiles":('Dockerfile', '.gitignore', '.htaccess', 'hosts', 'fstab'),
                "LogFiles": (".log",".syslog",".eventlog"),
                "FontsFiles": (".woff",".woff2",".otf",".ttf",".ps",".pfb",".pfm",".font"),
                "DatabaseFiles": (".sqlite",".db",".sql"),
                "WebURLs": (".html",".htm",".shtml", ".xhtml"),
                
                "AndroidAPKs": (".apk",".xapk"),
                "ISOsFiles": (".iso"),
                "JupyterNotebooks": (".ipynb"),
                "VirtualMachinesFiles": (".vbox-extpack",'.vdi', '.vmdk', '.vhd', '.vhdx', 
                        '.vdi.bz2', '.vmdk.gz', '.vhd.gz',
                        '.vbox', '.vbox-prev', '.vbox-extpack', '.ovf', '.ova',
                        '.vbox-snAPSHOT', '.sav',
                        '.log','.vbox-tmp', '.vdi-tmp', '.cdr'),
                "SerializedFiles": (".json", ".pkl", ".npy", ".joblib",".pth",".h5")
            }

    @staticmethod
    def __list_files(folder_path):
        files = []
        for dirpath, _, filenames in os.walk(folder_path):
            for file in filenames:
                files.append(os.path.join(dirpath, file))
        return files

    @staticmethod
    def __get_empty_folders(folder_path):
        empty_folders = []
        for root, dirs, files in os.walk(folder_path, topdown=False):
            if not os.listdir(root):  # Check if the current folder is empty
                empty_folders.append(root)
            else:
                # Check if all subfolders are empty
                all_subfolders_empty = all(os.listdir(os.path.join(root, d)) == [] for d in dirs)
                if all_subfolders_empty:
                    empty_folders.append(root)
        return empty_folders

    @staticmethod
    def __is_subdirectory(parent_path, child_path):
        # Check if child_path is a subdirectory of parent_path
        return os.path.commonpath([parent_path, child_path]) == parent_path

    def get_counter(self):
        """
        Returns the current file counter dictionary used by PiFolderOrganizer.

        Returns:
        ------
            dict: The current file counter dictionary.

        Example:
        ------
            >>> pi_organizer = PiFolderOrganizer()
            >>> counter = pi_organizer.get_counter()
        """

        return self.__counter

    def set_counter(self, new_counter: dict) -> dict:
        """
        Sets a new file counter dictionary for PiFolderOrganizer.

        Args:
        ______
            new_counter (dict): The new file counter dictionary to set.

        Returns:
        ______
            dict: The updated file counter dictionary.

        Example:
        ------
            >>> pi_organizer = PiFolderOrganizer()
            >>> new_counter = {"Images": [], "Documents": []}
            >>> pi_organizer.set_counter(new_counter)
            >>> counter = pi_organizer.get_counter()
        """
        new_counter["Others"] = []
        self.__counter = new_counter

    def get_extensions(self):
        """
        Returns the current file extensions dictionary used by PiFolderOrganizer.

        Returns:
        ------
            dict: The current file extensions dictionary.

        Example:
        ------
            >>> pi_organizer = PiFolderOrganizer()
            >>> extensions = pi_organizer.get_extensions()
        """
        return self.__extensions

    def set_extensions(self, new_extensions: dict) -> dict:
        """
        Sets a new file extensions dictionary for PiFolderOrganizer.

        Args:
        ------
            new_extensions (dict): The new file extensions dictionary to set.

        Returns:
        ------
            dict: The updated file extensions dictionary.

        Example:
        ------
            >>> pi_organizer = PiFolderOrganizer()
            >>> new_extensions = {"Images": (".png", ".jpg"), "Documents": (".txt", ".docs")}
            >>> pi_organizer.set_extensions(new_extensions)
            >>> extensions = pi_organizer.get_extensions()
        """
        self.__extensions = new_extensions
    def __get_restricted_paths(self):
        restricted_paths = []

        # Add standard restricted paths for Unix-based systems (Linux and macOS)
        restricted_paths.extend([
            "/bin", "/usr", "/sbin", "/usr/bin", "/usr/sbin", "/etc", "/var/log", "/usr/lib", "/lib", "/tmp",
            "/Applications", "/System", "/Library", "/Users", "/var/log", "/private", "/tmp"
        ])

        # Dynamically add environment paths for Unix-based systems
        # if os.name == 'posix':
        #     restricted_paths.extend([
        #         os.path.expanduser('~'),
        #         os.environ.get('TMPDIR', '/tmp'),
        #         os.environ.get('LOGDIR', '/var/log'),
        #         os.environ.get('SYSCONFDIR', '/etc'),
        #     ])

        # Add standard restricted paths for Windows systems
        restricted_paths.extend([
            r"C:\Windows", r"C:\Program Files", r"C:\Program Files (x86)", r"C:\Users\Public", r"C:\ProgramData", r"C:\Windows\System32", r"C:\Temp"
        ])

        # Dynamically add environment paths for Windows
        # if os.name == 'nt':
        #     restricted_paths.extend([
        #         os.environ.get('SYSTEMROOT', r"C:\Windows"),
        #         os.environ.get('PROGRAMFILES', r"C:\Program Files"),
        #         os.environ.get('PROGRAMFILES(X86)', r"C:\Program Files (x86)"),
        #         os.environ.get('PUBLIC', r"C:\Users\Public"),
        #         os.environ.get('PROGRAMDATA', r"C:\ProgramData"),
        #         os.environ.get('WINDIR', r"C:\Windows\System32"),
        #         os.environ.get('TEMP', r"C:\Temp"),
        #     ])
        # return restricted_paths
    
    @staticmethod
    def __is_restricted_path(path):
        """
        Checks if a given path is within any of the restricted paths.

        Args:
        ------
        path (str): The path to check.

        Returns:
        ------
        bool: True if the path is within a restricted path, False otherwise.
        """
        # Normalize the input path
        
        
        path = Path(path).resolve()  # Resolve to absolute path
        for restricted_path in PiFolderOrganizer.__RESTRICTED_PATHS:
            
            try:
                # Check if the path starts with the restricted path
                if path == restricted_path or path.is_relative_to(restricted_path):
                    return True
            except ValueError:
                continue
        return False

    def __move_files(self, category, file_paths, destination_path):
        category_path = os.path.join(destination_path, category)
        os.makedirs(category_path, exist_ok=True)
        for file_path in file_paths:
            dest_file = os.path.join(category_path, os.path.basename(file_path))
            shutil.move(file_path, dest_file)
            print(f"File {os.path.basename(file_path)} moved to {category} folder.")
        print(20 * "+-*-+")

    def pi_folder_organizer(self, source_path: str, destination_path: str) -> None:
        """
        Organizes files from the source_path into separate folders in the destination_path based on their types.

        Parameters:
        ------
        - source_path (str): The path to the folder containing the files to be organized.
        - destination_path (str): The path to the folder where the organized files will be stored.

        Returns:
        ------
        - None

        Raises:
        ------
        - NotADirectoryError: If source_path is not a directory.

        Usage:
        ------
        - Create an instance of PiFolderOrganizer.
        - Set the counter and extensions dictionaries if needed.
        - Call this method with the source_path and destination_path to organize files accordingly.

        Example Default:
        ------
        
        >>> pi_organizer = PiFolderOrganizer() 
        >>> pi_organizer.pi_organizer("/path/to/source_folder", "/path/to/destination_folder")
        
        Example Custom:
        ------
        >>> pi_organizer = PiFolderOrganizer() 
        >>> new_counter = {"Images": [], "Documents": []}
        >>> pi_organizer.set_counter(new_counter)
        >>> new_extensions = {"Images": (".png", ".jpg"), "Documents": (".txt", ".docs")}
        >>> pi_organizer.set_extensions(new_extensions)
        >>> pi_organizer.pi_organizer("/path/to/source_folder", "/path/to/destination_folder")
        
        """
        # Normalize paths
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)

        # Check for restricted paths

        if self.__is_restricted_path(source_path) or self.__is_restricted_path(destination_path):
                DangerZone("Path is within restricted system directories can not be processed!")
            

        # Check other conditions before proceeding
        elif len(self.__counter) - 1 != len(self.__extensions):
            print("Counter Dictionary and Extension Dictionary must be of the same length.")
        elif source_path == destination_path:
            print("Source folder and Destination Folder must be different")
        elif not os.path.exists(source_path):
            print(f"Path {source_path} does not exist. Please make sure you have given the correct path.")
        elif self.__is_subdirectory(source_path, destination_path):
            DestinationInsideSourceError("Destination path should not be inside the Source path.")
            
        elif not (os.path.isdir(source_path) or not os.path.isdir(destination_path)):
            raise NotADirectoryError

        else:
            os.makedirs(destination_path, exist_ok=True)
            
            files = self.__list_files(source_path)
            
            print(20*"+-*-+")
            print(f"Total Files: {len(files)}")
            print(20*"+-*-+")
            for file_path in files:
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1].lower()
                if file_ext == "":
                    self.__counter["Others"].append(file_path)
                else:
                    for key, value in self.__extensions.items():
                        if file_ext in value:
                            self.__counter[key].append(file_path)
                            break
                    else:
                        self.__counter["Others"].append(file_path)
                
        
        
            for key,value in self.__counter.items():
                if len(value)>0:
                    print(f"Total {key} : {len(value)}")
            print(20*"+-*-+")
            if input("Would you like to proceed?[y/n]:\n").lower()=='y':
                
                
                with ThreadPoolExecutor() as executor:
                    for category, file_paths in self.__counter.items():
                        if file_paths:
                            executor.submit(self.__move_files, category, file_paths, destination_path)

                empty_folders=self.__get_empty_folders(source_path)
                
                print(f"We found {len(empty_folders)} Empty Folders after cleanup!")
                
                if input("Would you like to delete all empty folders?[y/n]: ").lower()=='y':
                    shutil.rmtree(source_path, ignore_errors=True)
                    print("All Empty Folders deleted successfully!")
                else:
                    print("Good Luck!")
            else:
                print("Good Luck!")