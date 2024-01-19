from argparse import ArgumentParser
from sys import argv
import sys

class arguments():
    def argsFunc():
        parser = ArgumentParser()
        parser.add_argument(
            "--old",
            "-o",
            type=str,
            help = """Old images kèm tag (Ví dụ: mysql:1.2).
            Có thể nhập nhiều image, phân tách bởi dấu phẩy (Ví dụ: mysql:1.2,redis:1.1)"""
        )
        parser.add_argument(
            "--new",
            "-n",
            type=str,
            help = """New images kèm tag (Ví dụ: mysql:1.3).
            Có thể nhập nhiều image, phân tách bởi dấu phẩy (Ví dụ: mysql:1.3,redis:1.2)"""
        )
        parser.add_argument(
            "-p",
            "--product",
            type=str,
            nargs= "+",
            help = "Tên sản phẩm. Ví dụ: MISA AMIS"
        )
        parser.add_argument(
            "--version",
            "-v",
            type=str,
            help = "Phiên bản phát hành. Ví dụ: R1"
        )
        parser.add_argument(
            "--authen",
            "-a",
            type=str,
            help = "Đường dẫn tới file credential để kết nối SMB (JSON format). Ví dụ: smb_config.json"
        )        
        argsList = []
        args = vars(parser.parse_args())
        oldOmage = args["old"]
        newImage = args["new"]
        productName = args["product"]
        version = args["version"]
        authen = args["authen"]
        if args["product"]: productName = ' '.join(args["product"])
        # output = args["output"]
        
        argsList.append(oldOmage)
        argsList.append(newImage)
        argsList.append(productName)
        argsList.append(version)
        argsList.append(authen)
        # argsList.append(output)

        if len(argv) < 1:
            parser.print_help()
            sys.exit(1)

        if not oldOmage and not newImage:
            print("\nError: Giá trị old images và new images bị thiếu. (option -o)\n")
            parser.print_help()
            sys.exit(1)
        if not newImage:
            print("\nError: Giá trị new images và new images bị thiếu. (option -n)\n")
            parser.print_help()
            sys.exit(1)
        # if not version:
        #     print("\nError: The release version required!\n")
        #     parser.print_help()
        #     sys.exit(1)
        if not productName:
            print("\nError: Yêu cầu nhập tên sản phẩm (option -p).\n")
            parser.print_help()
            sys.exit(1)
        if not authen:
            print("\nError: Yêu cầu nhập đường dẫn file SMB credential (option -a).\n")
            parser.print_help()
            sys.exit(1)            
        return argsList
    