"""This module provides the main functionality of HTTPie.
Invocation flow:
  1. Read, validate and process the input (args, `stdin`).
  2. Create and send a request.
  3. Stream, and possibly process and format, the parts
     of the request-response exchange selected by output options.
  4. Simultaneously write to `stdout`
  5. Exit.
"""
import argparse
import logging
from boto_connections import BotoConnections
import logging
from wall_e import WalleConfiguration


def main():
    """
    The main function.
    Pre-process args, handle some special types of invocations,
    and run the main program with error handling.
    Return exit status code.
    """
    logger = logging.getLogger('Wall-e')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resource', help='AWS Resource', required=True)
    parser.add_argument('-a', '--aws_account', help='AWS account name', required=True)
    parser.add_argument('-d', '--dust', help='Dust file location', required=False)
    args = parser.parse_args()
    resource = args.resource
    account_name = args.aws_account
    dust = args.dust
    logger.info('Building a Wall-e bot...')
    logger.info('Wall-e are going to clean: {0} in account {1}'.format(resource, account_name))
    connection = BotoConnections()
    walle = WalleConfiguration(connection)
    logger.info("Cleaning your ecosystem and saving plants")
    if resource == 'cloudformation':
        walle.clean_cloudformation(resource, account_name, dust)
    if resource == 'autoscaling':
        walle.clean_launchconfiguration(resource, account_name)
    logger.info("Finished, your {0} are clean".format(resource))


if __name__ == '__main__':
    main()
