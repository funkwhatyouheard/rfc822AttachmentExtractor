#!/usr/bin/python
import re, base64, optparse, sys
from os import path

def extract_attachment(file,outputdir=r"./"):
    with open(file,"r") as file:
        contents = file.read()
    attachment_boundary_regex = r"----.+\n+Content-Type:\s(.+)\n+Content-Transfer-Encoding:\s(.+)\n+Content-Disposition:\sattachment.*?\n+(.*?)\n+----"
    attachment_info = re.findall(attachment_boundary_regex,contents,re.DOTALL)[0]
    content_type, file_name = attachment_info[0].split("; ")
    file_name = file_name.split("name=")[1].replace('"','')
    content_transfer_encoding = attachment_info[1]
    encoded_attachment = attachment_info[2]
    if content_transfer_encoding == 'base64':
        attachment_contents = base64.b64decode(encoded_attachment)
    else:
        return "Don't know how to handle {0} content-type".format(content_transfer_encoding)
    output_file = path.join(outputdir,file_name)
    if "text" in content_type:
        flags = "w"
        attachment_contents = attachment_contents.decode()
    # assumes binary file
    else:
        flags = "wb"
        attachment_contents = bytes(attachment_contents)
    with open(output_file,flags) as file:
        file.write(attachment_contents)
        
def Main():
    oParser = optparse.OptionParser(usage='usage: -f [file] -o [outputdir]\n')
    oParser.add_option('-f', '--file', type="str", help='the path of the rfc822 compliant text file')
    oParser.add_option('-o', '--outputdir', default=r"./", type="str", help='the output directory (default ./)')
    (args, _) = oParser.parse_args()

    if args.file is None:
        oParser.print_help()
    else:
        extract_attachment(args.file,args.outputdir)

if __name__ == '__main__':
    sys.exit(Main())
