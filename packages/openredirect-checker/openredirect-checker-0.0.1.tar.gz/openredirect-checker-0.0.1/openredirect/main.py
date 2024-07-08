import argparse
from openredirect.utils import banner
from openredirect.includes import scan
from openredirect.includes import readfile
from openredirect.utils import check_inter
from openredirect.includes import readfile
import webbrowser


def banner_h():
    banner.display_help()

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-u", '--url', type=str, help="URL to scan")
    parser.add_argument("-l", '--input', type=str, help="lost of input file")
    parser.add_argument("-o", '--output', type=str, help="output in text file")
    parser.add_argument("-b", '--browser',action='store_true',help=" to know more about the vulnerability")

    parser.add_argument("-h", "--help", action="store_true", help="Help menu")

    args = parser.parse_args()

    if args.help:
        banner.display_help()
    if args.browser:
        webbrowser.open("https://portswigger.net/kb/issues/00500100_open-redirection-reflected")
    if args.url and not args.output:
        banner.banner()
        if readfile.is_valid_url(args.url):
            scan.openrescan(args.url)
        else:
            print(f"invalid url {args.url}")

    if args.input or args.output:
        banner.banner()
        readfile.reader(args.input,args.output)
    



if __name__ == "__main__":
    if check_inter.check_internet():
         main()
    else:
        print("Check Internet Connection")

