import os
import pytesseract
from PIL import Image
import json
import PyPDF2


class WorkDirectoryGen:
    def __init__(self, input_path, output_directory):
        self.input_path = input_path
        self.output_directory = output_directory
        self.input_structure_text = self._read_input()

    @staticmethod
    def _parse_structure(input_string):
        """
        Parses an ASCII tree diagram from a string and converts it to a nested dictionary structure.

        Args:
        input_string (str): The input string containing the ASCII tree diagram.

        Returns:
        dict: A nested dictionary representing the folder structure.
        """
        structure = {}
        current_level = [structure]

        for line in input_string.splitlines():
            if not line.strip():
                continue

            indent_level = len(line) - len(line.lstrip('│').lstrip('├').lstrip('└').lstrip(' '))
            name = line.strip('│').strip('├').strip('└').strip(' ')

            while len(current_level) > indent_level + 1:
                current_level.pop()

            if '.' in name:
                current_level[-1][name] = ""
            else:
                current_level[-1][name] = {}
                current_level.append(current_level[-1][name])

        return structure

    def _create_folder_structure(self, base_path, structure):
        """
        Creates the folder and file structure based on a nested dictionary.

        Args:
        base_path (str): The base directory where the structure will be created.
        structure (dict): A nested dictionary representing the folder structure.
        """
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self._create_folder_structure(path, content)
            else:
                with open(path, 'w') as file:
                    file.write(content)

    @staticmethod
    def _extract_text_from_image(image_path):
        """
        Extracts text from an image using OCR.

        Args:
        image_path (str): The path to the image file.

        Returns:
        str: The extracted text.
        """
        return pytesseract.image_to_string(Image.open(image_path))

    @staticmethod
    def _extract_text_from_pdf(pdf_path):
        """
        Extracts text from a PDF file.

        Args:
        pdf_path (str): The path to the PDF file.

        Returns:
        str: The extracted text.
        """
        text = ""
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extract_text()
        return text

    def _read_input(self):
        """
        Reads input from a file and determines its format.

        Args:
        file_path (str): The path to the input file.

        Returns:
        str: The content of the input file as a string.
        """
        _, file_extension = os.path.splitext(self.input_path)
        if file_extension.lower() == '.txt':
            with open(self.input_path, 'r') as file:
                return file.read()
        elif file_extension.lower() == '.pdf':
            return self._extract_text_from_pdf(self.input_path)
        elif file_extension.lower() == '.json':
            with open(self.input_path, 'r') as file:
                return json.dumps(json.load(file), indent=4)
        elif file_extension.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
            return self._extract_text_from_image(self.input_path)
        else:
            raise ValueError("Unsupported file format")

    def generate(self):
        """
        Generates the folder structure from the input.
        """
        folder_structure = self._parse_structure(self.input_structure_text)
        self._create_folder_structure(self.output_directory, folder_structure)
        print(f"Folder structure created at {self.output_directory}")
