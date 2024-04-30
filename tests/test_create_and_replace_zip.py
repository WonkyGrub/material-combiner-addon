import os
import shutil
import unittest
import zipfile

class TestAddon(unittest.TestCase):
    def setUp(self):
        self.repo_path = "D:/Code_stuff/material-combiner-addon"  # Replace with your repo path
        self.addon_zip_path = "D:/Code_stuff/Wonky-material-combiner-addon.zip"  # Replace with your addon zip path
        self.inner_dir = "material-combiner-addon"  # The name of the inner directory in the zip file

    def test_create_and_replace_zip(self):
        # Create a new zip file
        new_zip_path = os.path.join(self.repo_path, "Wonky-material-combiner-addon.zip")
        with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    # Get the relative path of the file
                    relative_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                    # Prepend the inner directory to the relative path
                    inner_path = os.path.join(self.inner_dir, relative_path)
                    # Add the file to the zip file with the inner path
                    zipf.write(os.path.join(root, file), arcname=inner_path)

        # Replace the old zip file with the new one
        shutil.move(new_zip_path, self.addon_zip_path)

if __name__ == '__main__':
    unittest.main()