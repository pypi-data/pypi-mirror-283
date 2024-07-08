import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List, Optional

def send_slack_message(
    token: str,
    channel: str,
    subject: str,
    message: Optional[str] = None,
    attachments: Optional[List[str]] = None
):
    """
    Posts a message to a specified Slack channel.
    
    Args:
        token: str - The Slack API token.
        channel: str - The Slack channel ID or name.
        subject: str - The subject or main text of the Slack message.
        message: Optional[str] - An optional additional message to post in a thread.
        attachments: Optional[List[str]] - A list of file paths to attach to the Slack message.
    
    Returns:
        None
    """
    client = WebClient(token=token)
    
    try:
        # Post the main message
        response = client.chat_postMessage(channel=channel, text=subject)
        logging.info("Message posted successfully.")
        
        thread_ts = response['ts']
        
        # Post the additional message in a thread, if provided
        if message:
            client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=message)
            logging.info("Thread message posted successfully.")
        
        # Upload attachments, if provided
        if attachments:
            for attachment in attachments:
                try:
                    client.files_upload(
                        channels=channel,
                        file=attachment,
                        title=attachment.split("/")[-1],
                        thread_ts=thread_ts,
                        initial_comment=''
                    )
                    logging.info(f"Attachment {attachment} uploaded successfully.")
                except SlackApiError as e:
                    logging.error(f"Error uploading attachment {attachment}: {e.response['error']}")
    
    except SlackApiError as e:
        logging.error(f"Error posting message: {e.response['error']}")
        raise