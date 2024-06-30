from models import Object
import os
import chardet
import zlib
from hashlib import sha1
from base64 import b64encode


class Stager:
    """
    A class to index files & directories.

    - Takes items list
    - Stages items & creates objects
    - Returns objects info
    """

    objects: list[Object]
    
    def __init__(self, items: list[str]) -> None:
        """
        Create objects from items.
        """

        self.objects = []
        
        # Create & Append Objects
        for item in items:
            self.objects.append(
                self.create_object(os.path.abspath(item))
            )
    
    def create_object(self, item_path: str) -> Object:
        """
        Takes item path as parameter, and creates it's object.
        """


        # Object Type: Blob
        if os.path.isfile(item_path):

            # Read File
            with open(item_path, "rb") as file:
                raw_content: bytes = file.read()

                # Detect Content Encoding
                encoding: str = chardet.detect(raw_content)["encoding"]
                if encoding is None: encoding = "0"

                # Add Headers & Compress
                content: bytes = zlib.compress(
                    b"b" + f"/{encoding}/".encode() + raw_content,
                    level=6
                )
                content_hash: str = sha1(raw_content).hexdigest()

                # Create Object
                self.write_object_file(content, content_hash)

                # Return Object
                return Object(
                    file_path=item_path,
                    content_hash=content_hash,
                    object_type="b"
                )
        
        # Object Type: Tree
        elif os.path.isdir(item_path):
            dir_items: list[str] = os.listdir(item_path)
            raw_content: str = "t"  # Tree

            # Create Object For Each Item
            for dir_item_path in dir_items:
                dir_item_path: str = os.path.join(item_path, dir_item_path)
                object: Object = self.create_object(dir_item_path)
                
                # Append to Raw Content
                raw_content += f"/{object.object_type}/{object.content_hash}/{b64encode(dir_item_path.encode('utf-8')).decode('utf-8')}"

            raw_content: bytes = str(raw_content).encode("utf-8")

            # Add Headers & Compress
            content: bytes = zlib.compress(raw_content, level=6)
            content_hash: str = sha1(raw_content).hexdigest()

            # Create Object
            self.write_object_file(content, content_hash)

            # Return Object
            return Object(
                file_path=item_path,
                content_hash=content_hash,
                object_type="t"
            )
    
    def write_object_file(self, content: bytes, content_hash: str) -> None:
        """
        Creates the hash object file inside "objects/" directory.
        """

        # Split Hash
        head_hash: str = content_hash[:2]
        tail_hash: str = content_hash[2:]

        # Prepare Object Sub-Directory Path
        objects_dir: str = os.path.join(os.getcwd(), ".bit", "objects")
        objects_sub_dir: str = os.path.join(objects_dir, head_hash)

        # Make Directory: /objects
        try: os.mkdir(objects_dir)
        except FileExistsError: ...

        # Make Directory: /objects/..
        try: os.mkdir(objects_sub_dir)
        except FileExistsError: ...

        # Write Content
        with open(os.path.join(objects_sub_dir, tail_hash), "wb") as file:
            file.write(content)

    def index(self) -> str:
        content: str = ""

        # Append Objects Info
        for object in self.objects:
            content += f"{object.object_type}/{object.content_hash}/{b64encode(object.file_path.encode('utf-8')).decode('utf-8')}\n"
        
        return content.strip()
