import argparse

from . import __version__
from .main import split_pdf, merge_pdfs

package_name = "pdfman"

example_uses = '''example:
   pdfman merge file1.pdf file2.pdf
   pdfman split file.pdf -r 2,4-6,8'''

def main(argv = None):
    parser = argparse.ArgumentParser(prog=package_name, description="Edit your pdf files", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    split_parser = subparsers.add_parser("split", help="Split pdf into multiple parts")
    split_parser.add_argument('filename', type=str, help='Path to the input PDF file')
    split_parser.add_argument('-r', '--ranges', type=str, help="Give Comma-separated range numbers or single numbers")

    merge_parser = subparsers.add_parser("merge", help="Merge two or more pdf files")
    merge_parser.add_argument("filenames", type=str, nargs='+', help="two or more files to merge")
    
    parser.add_argument('-v',"--version",
                            action="version",
                            version=__version__,
                            help="check version of deb")

    args = parser.parse_args(argv)

    if args.command == "split":
        if args.ranges:
            split_pdf(args.filename, args.ranges)
        else:
            ranges = input('Enter Comma-separated or space-separated range numbers or single numbers : ')
            split_pdf(args.filename, ranges)

    elif args.command == "merge":
        merge_pdfs(args.filenames)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    raise SystemExit(main())