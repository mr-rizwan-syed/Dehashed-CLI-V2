import os

class Config:
    def __init__(self, domain: str, api_key: str):
        self.domain = domain
        self.api_key = api_key
        self.base_url = "https://api.dehashed.com/v2/search"
        self.output_dir = domain
        self._setup_directory()

    def _setup_directory(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        os.chdir(self.output_dir)
