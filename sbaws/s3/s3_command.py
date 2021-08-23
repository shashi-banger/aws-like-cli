
def ls(s3uri, recursive, page_size):
    print(f"{s3uri} {recursive}   page_size={page_size}")


def sync(source_uri, dest_uri, acl):
    print(f"{source_uri} {dest_uri}   acl={acl}")
