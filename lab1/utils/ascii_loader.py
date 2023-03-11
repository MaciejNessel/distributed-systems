class AsciiArt:
    @staticmethod
    def load(file_path: str):
        try:
            with open(file_path) as f:
                data = f.read()
        except OSError:
            data = None
        return data
