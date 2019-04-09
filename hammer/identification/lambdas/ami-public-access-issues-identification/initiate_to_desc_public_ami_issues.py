import os
import logging

from library.logger import set_logging
from library.config import Config
from library.aws.utility import Sns


def lambda_handler(event, context):
    """ Lambda handler to initiate to find public AMIs """
    set_logging(level=logging.INFO)
    logging.debug("Initiating AMIs public access checking")

    try:
        sns_arn = os.environ["SNS_PUBLIC_AMI_ARN"]
        config = Config()

        if not config.publicAMIs.enabled:
            logging.debug("AMIs public access checking disabled")
            return

        logging.debug("Iterating over each account to initiate AMIs public access check")
        for account_id, account_name in config.publicAMIs.accounts.items():
            payload = {"account_id": account_id,
                       "account_name": account_name,
                       "regions": config.aws.regions,
                       "sns_arn": sns_arn
                      }
            logging.debug(f"Initiating AMIs public access checking for '{account_name}'")
            Sns.publish(sns_arn, payload)
    except Exception:
        logging.exception("Error occurred while initiation of AMIs public access check")
        return

    logging.debug("AMIs public access checking initiation done")
