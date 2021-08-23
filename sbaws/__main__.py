#!/usr/bin/env python

import os
import sys
import logging
import click
import ast
from sbaws import __version__
from sbaws.s3 import s3_command
from sbaws.ec2 import ec2_command

log = logging.getLogger(__name__)

class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

class State:
    ''' Maintain logging level.'''

    def __init__(self, log_name='s3aws', level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        # Don't restrict level on logger; use handler
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.stream = logging.StreamHandler()
        self.stream.setLevel(level)
        self.stream.name = 'S3awsStreamHandler'
        self.logger.addHandler(self.stream)


def add_options(opts):
    def inner(f):
        for i in reversed(opts):
            f = i(f)
        return f

    return inner


def verbose_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value:
            state.stream.setLevel(logging.DEBUG)
    return click.option('-v', '--verbose',
                        is_flag=True,
                        expose_value=False,
                        help='Enable verbose output',
                        callback=callback)(f)


def quiet_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value:
            state.stream.setLevel(logging.ERROR)
    return click.option('-q', '--quiet',
                        is_flag=True,
                        expose_value=False,
                        help='Silence warnings',
                        callback=callback)(f)


common_options = add_options([quiet_option, verbose_option])




@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    __version__,
    '-V', '--version',
)
@common_options
def cli():
    """
    sbaws cli implementation
    """


@cli.group(name="s3")
def s3():
    """
    s3 group
    """
    
@s3.command(name="ls")
@click.argument('S3URI', required=False)
@click.option('--recursive', 'recursive', is_flag=True, help="Command is performed on all files or objects under the specified directory or prefix.")
@click.option('--page-size', type=click.INT,  default=1000,  help="The number of results to return")
def s3_ls(s3uri, recursive, page_size):
    """
    s3 ls command

    S3URI: S3 uri e.g. s3://foo/boo/. If not presents lists all buckets
    """
    s3_command.ls(s3uri, recursive, page_size)



_help_s3_acl="""Sets the ACL for the object when the command is performed. 
If you use this parameter you must have the "s3:PutObjectAcl" permission 
included in the list of actions for your IAM policy. Only accepts values 
of private, public-read, public-read-write, authenticated-read, aws-exec-read, 
bucket-owner-read, bucket-owner-full-control and log-delivery-write."""

@s3.command(name="sync")
@click.argument('source_uri')
@click.argument('dest_uri')
@click.option('--acl', type=click.STRING, help=_help_s3_acl)
def s3_sync(source_uri, dest_uri, acl):
    """
    s3 sync command

    SOURCE_URI: Can be local path or s3 uri

    DEST_URI: Can be local path or s3 uri
    """
    s3_command.sync(source_uri, dest_uri, acl)

    
################################# EC2 instance commands #############################

# https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html#cli-aws-ec2

@cli.group(name="ec2")
def ec2():
    """
    ec2 group
    """

_help_ec2_imgid = """
The ID of the AMI. An AMI ID is required to launch an instance and must be specified here 
or in a launch template.
"""

_help_ec2_instance_type = """
The instance type. More details https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html
"""

_help_ec2_user_data="""
The user data to make available to the instance. For more information, see 
Running commands on your Linux instance at launch (Linux) and Adding User Data (Windows). 
If you are using a command line tool, base64-encoding is performed for you, and you can load 
the text from a file. Otherwise, you must provide base64-encoded text. User data is limited 
to 16 KB.
"""

_help_ec2_count = """
Number of instances to launch. If a single number is provided, it is assumed to be the 
minimum to launch (defaults to 1). If a range is provided in the form min:max then the 
first number is interpreted as the minimum number of instances to launch and the second is 
interpreted as the maximum number of instances to launch.
"""
@ec2.command(name="run-instances")
@click.option('--image-id', type=click.STRING, help=_help_ec2_imgid)
@click.option('--instance-type', type=click.STRING, help=_help_ec2_instance_type)
@click.option('--user-data', type=click.STRING, help=_help_ec2_user_data)
@click.option('--count', default="1", type=click.STRING, help=_help_ec2_count)
def ec2_run_instances(image_id, instance_type, user_data, count):
    ec2_command.run_instances(image_id, instance_type, user_data, count)


_help_ec2_ti_instance_ids = """
The list of IDs of the instances. 
Constraints: Up to 1000 instance IDs. We recommend breaking up this request into smaller batches.
Syntax: '["string1","string2"]'
"""

_help_ec2_ti_cli_input_json = """
Performs service operation based on the JSON string provided.
"""

@ec2.command(name="terminate-instances")
# Example of passing python list as option
@click.option('--instance-ids', default=[], cls=PythonLiteralOption, help=_help_ec2_ti_instance_ids)
@click.option('--cli-input-json', type=click.STRING, help=_help_ec2_ti_cli_input_json)
def ec2_terminate_instances(instance_ids, cli_input_json):
    ec2_command.terminate_instances(instance_ids, cli_input_json)