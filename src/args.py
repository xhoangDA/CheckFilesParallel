from argparse import ArgumentParser
from sys import argv
import sys

class arguments():
    def argsFunc():
        parser = ArgumentParser()
        parser.add_argument(
            "--old-images",
            "-o",
            type=str,
            help = """Old images kèm tag (Ví dụ: mysql:1.2).
            Có thể nhập nhiều image, phân tách bởi dấu phẩy (Ví dụ: mysql:1.2,redis:1.1)"""
        )
        parser.add_argument(
            "--new-images",
            "-n",
            type=str,
            help = """New images kèm tag (Ví dụ: mysql:1.3).
            Có thể nhập nhiều image, phân tách bởi dấu phẩy (Ví dụ: mysql:1.3,redis:1.2)"""
        )
        parser.add_argument(
            "--product-name",
            "-p",
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
            "--authen-file",
            "-a",
            type=str,
            help = "Đường dẫn tới file credential để kết nối SMB (JSON format). Ví dụ: smb_config.json"
        )
        parser.add_argument(
            "--export-dir",
            "-e",
            type=str,
            default = "\\storage1\DU_LIEU_CHUYEN_RA_NGOAI\Compare_file",
            help = "Đường dẫn SMB lưu trữ file kết quả. Mặc định: \\storage1\DU_LIEU_CHUYEN_RA_NGOAI\Compare_file"
        )
        parser.add_argument(
            "--tag-new",
            "-t",
            type=str,
            default = "old-release",
            help = "Tên tag đặt lại cho new images sau khi checkfiles thành công. Mặc định: old-release"
        )
        parser.add_argument(
            "--robot-account",
            "-r",
            type=str,
            help = "Tên robot account để đẩy image lên registry. Ví dụ: robot@amisplatform"
        )
        parser.add_argument(
            "--robot-secret",
            "-s",
            type=str,
            help = "Mật khẩu robot account."
        )                

        argsList = []
        args = vars(parser.parse_args())
        oldOmage = args["old-images"]
        newImage = args["new-images"]
        productName = args["product-name"]
        version = args["version"]
        authen = args["authen-file"]
        export = args["export-dir"]
        tag = args["tag-new"]
        robotAccount = args["robot-account"]
        robotSecret = args["robot-secret"]
        if args["product"]: productName = ' '.join(args["product"])
        
        argsList.append(oldOmage)
        argsList.append(newImage)
        argsList.append(productName)
        argsList.append(version)
        argsList.append(authen)
        argsList.append(export)
        argsList.append(tag)
        argsList.append(robotAccount)
        argsList.append(robotSecret)

        if len(argv) < 1:
            parser.print_help()
            sys.exit(1)

        errorMessage = ''
        if not oldOmage and not newImage:
            errorMessage += "\nError: Yêu cầu nhập old images và new images. (option -o, -n)"
        if not newImage:
            errorMessage += "\nError: Yêu cầu nhập new images. (option -n)"
        if not version:
            errorMessage += "\nError: Yêu cầu nhập mã phát hành (option -v)"
        if not productName:
            errorMessage += "\nError: Yêu cầu nhập tên sản phẩm (option -p)."
        if not authen:
            errorMessage += "\nError: Yêu cầu nhập đường dẫn file SMB credential (option -a)."
        if not robotAccount:
            errorMessage += "\nError: Yêu cầu nhập robot account (option -r)."
        if not robotSecret:
            errorMessage += "\nError: Yêu cầu nhập mật khẩu robot account (option -s)."                        
        if errorMessage:
            print(errorMessage)
            parser.print_help()
            sys.exit(1)
        
        return argsList