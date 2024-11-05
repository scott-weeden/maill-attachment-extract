import mailbox
import email
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Directory containing the MBOX files
mbox_directory = os.getenv('MBOX_DIR')
if mbox_directory:
    print(f'Attachments will be extracted from MBOX files here: {mbox_directory}')
else:
    print('The MBOX_DIR environment variable is not set. Please use...MBOX_DIR=%HOME%\\Documents\\MailBoxes for WINDOWS   or...  export ATTACHMENTS_DIR=/Users/owner/Documents/MailBoxes  ...for Mac OSX')

# Directory where attachments will be saved
save_dir = os.getenv('ATTACHMENTS_DIR')
# Check if the environment variable exists
if save_dir:
    print(f'Attachments will be saved to: {save_dir}')
else:
    print('The ATTACHMENTS_DIR environment variable is not set. Please set ATTACHMENTS_DIR=%HOME%\\Documents\\Attachments for WINDOWS  or  export ATTACHMENTS_DIR=/Users/owner/documents/attachments  for Mac OSX')

# Create the directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Function to set the file's last modified time
def set_last_modified(filepath, timestamp):
    os.utime(filepath, (timestamp, timestamp))

# Function to create a unique file path
def get_unique_filepath(base_path):
    if not os.path.exists(base_path):
        return base_path
    base, ext = os.path.splitext(base_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base}_{timestamp}{ext}"

# Loop through each MBOX file in the directory
for mbox_file in os.listdir(mbox_directory):
    if mbox_file.endswith('.mbox'):
        print(f'Processing {mbox_file}')
        mbox_path = os.path.join(mbox_directory, mbox_file)
        mbox = mailbox.mbox(mbox_path)
        
        # Loop through each message in the MBOX file
        for message in mbox:
            # Skip if the message is a non-deliverable report or multipart/report
            if message.get_content_type() == 'multipart/report':
                continue
            
            # Get the message date and ensure it's valid
            email_date = email.utils.parsedate_tz(message['date'])
            if email_date:
                timestamp = email.utils.mktime_tz(email_date)

                # If the message is multipart
                if message.is_multipart():
                    for part in message.get_payload():
                        # If the part has an attachment
                        if part.get_content_disposition() and 'attachment' in part.get_content_disposition():
                            payload = part.get_payload(decode=True)
                            if payload:
                                filename = part.get_filename()
                                if filename:
                                    base_path = os.path.join(save_dir, filename)
                                    filepath = get_unique_filepath(base_path)
                                    with open(filepath, 'wb') as f:
                                        f.write(payload)
                                    set_last_modified(filepath, timestamp)
                else:
                    # If the message is not multipart but still has an attachment
                    if message.get_content_disposition() and 'attachment' in message.get_content_disposition():
                        payload = message.get_payload(decode=True)
                        if payload:
                            filename = message.get_filename()
                            if filename:
                                base_path = os.path.join(save_dir, filename)
                                filepath = get_unique_filepath(base_path)
                                with open(filepath, 'wb') as f:
                                    f.write(payload)
                                set_last_modified(filepath, timestamp)

print(f'Attachments have been saved to {save_dir} with modified dates set to the email dates.')
