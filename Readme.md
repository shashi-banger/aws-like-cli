# An example command line framework

The repository has an example python command line application framework based on [click](https://click.palletsprojects.com/en/8.0.x/).
The commandline is largely based on [mkdocs](https://github.com/mkdocs/mkdocs) commandline framework.

## Enabling Completion

Clic's documentation on shell completion is [here](https://click.palletsprojects.com/en/8.0.x/shell-completion/).

For ```bash```
Add this to ~/.bashrc:
```eval "$(_SBAWS_COMPLETE=bash_source sbaws)"```

For ```zshrc```
Add this to ~/.zshrc
```eval "$(_SBAWS_COMPLETE=zsh_source sbaws)"```

## Installation

Clone the repo and run the following

```
pip install --use-feature=2020-resolver  .
```

## Example invocations and output

```console
(base) foo@boo aws-like-cli % sbaws
Usage: sbaws [OPTIONS] COMMAND [ARGS]...

  sbaws cli implementation

Options:
  -V, --version  Show the version and exit.
  -q, --quiet    Silence warnings
  -v, --verbose  Enable verbose output
  -h, --help     Show this message and exit.

Commands:
  ec2  ec2 group
  s3   s3 group

(base) foo@boo aws-like-cli % sbaws ec2 -h
Usage: sbaws ec2 [OPTIONS] COMMAND [ARGS]...

  ec2 group

Options:
  -h, --help  Show this message and exit.

Commands:
  run-instances
  terminate-instances

(base) foo@boo aws-like-cli % sbaws ec2 run-instances -h
Usage: sbaws ec2 run-instances [OPTIONS]

Options:
  --image-id TEXT       The ID of the AMI. An AMI ID is required to launch an
                        instance and must be specified here  or in a launch
                        template.
  --instance-type TEXT  The instance type. More details https://docs.aws.amazo
                        n.com/AWSEC2/latest/UserGuide/instance-types.html
  --user-data TEXT      The user data to make available to the instance. For
                        more information, see  Running commands on your Linux
                        instance at launch (Linux) and Adding User Data
                        (Windows).  If you are using a command line tool,
                        base64-encoding is performed for you, and you can load
                        the text from a file. Otherwise, you must provide
                        base64-encoded text. User data is limited  to 16 KB.
  --count TEXT          Number of instances to launch. If a single number is
                        provided, it is assumed to be the  minimum to launch
                        (defaults to 1). If a range is provided in the form
                        min:max then the  first number is interpreted as the
                        minimum number of instances to launch and the second
                        is  interpreted as the maximum number of instances to
                        launch.
  -h, --help            Show this message and exit.

(base) foo@boo aws-like-cli % sbaws ec2 run-instances --image-id ami-123444 --instance-type c4x.large --user-data 'echo "hello world"' --count 1:5 
image_id=ami-123444 instance_type=c4x.large   user_data=echo "hello world", count=1:5

base) foo@boo aws-like-cli % sbaws s3 -h
Usage: sbaws s3 [OPTIONS] COMMAND [ARGS]...

  s3 group

Options:
  -h, --help  Show this message and exit.

Commands:
  ls    s3 ls command
  sync  s3 sync command

(base) foo@boo aws-like-cli % sbaws s3 sync -h 
Usage: sbaws s3 sync [OPTIONS] SOURCE_URI DEST_URI

  s3 sync command

  SOURCE_URI: Can be local path or s3 uri

  DEST_URI: Can be local path or s3 uri

Options:
  --acl TEXT  Sets the ACL for the object when the command is performed.  If
              you use this parameter you must have the "s3:PutObjectAcl"
              permission  included in the list of actions for your IAM policy.
              Only accepts values  of private, public-read, public-read-write,
              authenticated-read, aws-exec-read,  bucket-owner-read, bucket-
              owner-full-control and log-delivery-write.
  -h, --help  Show this message and exit.

(base) foo@boo aws-like-cli % sbaws s3 sync --acl public-read s3://foo/boo ./boo
s3://foo/boo ./boo   acl=public-read
```

