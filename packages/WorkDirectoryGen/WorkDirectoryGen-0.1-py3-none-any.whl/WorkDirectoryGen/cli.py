import argparse
from WorkDirectoryGen.core import WorkDirectoryGen


def main():
    parser = argparse.ArgumentParser(description="Generate folder structure from various input formats.")
    parser.add_argument('-i', '--input', required=True, help="Input text, file path, or image path")
    parser.add_argument('-o', '--out_directory', required=True, help="Output directory to create the folder structure")

    args = parser.parse_args()

    workdir = WorkDirectoryGen(input_path=args.input, output_directory=args.out_directory)
    workdir.generate()


if __name__ == "__main__":
    main()
