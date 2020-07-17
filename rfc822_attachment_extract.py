#!/usr/bin/python
import email, re, base64, optparse, sys
from os import path

def extract_attachments(file,outputdir=r"./"):
    base64_regex = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
    with open(file,"r") as file:
        message = email.message_from_file(file)
    attachments = message.get_payload()
    for attachment in attachments:
        if attachment.get_filename() is not None:
            output_file = path.join(outputdir,attachment.get_filename())
            if re.match(base64_regex,attachment._payload.replace("\n","")):
                attachment_contents = base64.b64decode(attachment._payload)
            else:
                attachment_contents = attachment._payload
            if "text" in attachment.get_content_type():
                flags = "w"
                attachment_contents = attachment_contents.decode()
            # assumes binary file if not text
            else:
                flags = "wb"
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
        extract_attachments(args.file,args.outputdir)


if __name__ == '__main__':
    sys.exit(Main())
