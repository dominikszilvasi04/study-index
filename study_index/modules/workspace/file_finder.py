from pathlib import Path
from study_index.modules.models import FileMetadata


class FileFinder:
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)

    def find_files(self) -> list[FileMetadata]:
        if not self.folder_path.is_dir():
            raise NotADirectoryError(f"{self.folder_path} is not a directory")
        files = []
        for file_path in self.folder_path.rglob("*"):
            if not file_path.is_file():
                continue
            file_status = file_path.stat()
            files.append(FileMetadata(str(file_path),
                                      file_path.name,
                                      file_path.suffix.lower(),
                                      file_status.st_size,
                                      file_status.st_mtime))
        return sorted(files, key=lambda file_metadata: file_metadata.full_path.casefold())
