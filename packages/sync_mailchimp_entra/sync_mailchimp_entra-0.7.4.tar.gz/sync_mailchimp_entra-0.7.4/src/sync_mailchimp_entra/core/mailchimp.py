from mailchimp_marketing.api_client import ApiClientError
from mailchimp_marketing import Client
import hashlib
from sync_mailchimp_entra.utils.errors import deserial_error


class MailchimpClient(Client):
    """Client used to communicate with MailChimp API."""

    _instance = None

    @staticmethod
    def get_instance(api_token_mailchimp=None, server_prefix=None):
        """Singleton to only create one instance of this class."""
        if MailchimpClient._instance is None or (
            api_token_mailchimp is not None and server_prefix is not None
        ):
            if api_token_mailchimp is None or server_prefix is None:
                raise ValueError(
                    "API token and server prefix must be provided for the first initialization of MailchimpClient."
                )
            MailchimpClient._instance = MailchimpClient(
                {"api_key": api_token_mailchimp, "server": server_prefix}
            )
            print("MailchimpClient created.")
        return MailchimpClient._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MailchimpClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, config={}):
        if not hasattr(self, "initialized"):  # Avoid reinitialization
            super(MailchimpClient, self).__init__(config)
            self.initialized = True

    def add_member(
        self,
        list_id,
        email,
        first_name="",
        last_name="",
        state="subscribed",
        language="en",
    ):
        """Add member to MailChimp list."""
        member_info = {
            "email_address": email,
            "status": state,
            "merge_fields": {"FNAME": first_name, "LNAME": last_name},
            "language": language,
        }

        try:
            return self.lists.add_list_member(list_id, member_info)
        except ApiClientError as error:
            error_obj = deserial_error(error.text)
            if error_obj.title == "Member Exists":
                self.update_member(
                    list_id, email, first_name, last_name, state, language
                )
            elif error_obj.title == "Forgotten Email Not Subscribed":
                print(
                    f"Member {email} was permanently deleted from the list of contacts and cannot be re-imported."
                )
            else:
                print("An exception occurred: {}".format(error.text))

    def remove_member(self, list_id, email):
        """Remove member from MailChimp list."""
        member_email_hash = hashlib.md5(email.encode("utf-8").lower()).hexdigest()
        member_update = {"status": "unsubscribed"}

        try:
            return self.lists.update_list_member(
                list_id, member_email_hash, member_update
            )
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))

    def update_member(
        self, list_id, email, first_name, last_name, state="subscribed", language="en"
    ):
        """Update member data."""
        member_email_hash = hashlib.md5(email.encode("utf-8").lower()).hexdigest()
        member_info = {
            "email_address": email,
            "status": state,
            "merge_fields": {"FNAME": first_name, "LNAME": last_name},
            "language": language,
        }

        try:
            return self.lists.update_list_member(
                list_id, member_email_hash, member_info
            )
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))

    def get_list_members(self, list_id, fields, count, offset):
        """Get list of members."""
        try:
            return self.lists.get_list_members_info(
                list_id=list_id, fields=fields, count=count, offset=offset
            )["members"]
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))

    def list_mailchimp_emails(self, list_mailchimp_id):
        """Get list of emails."""
        members_mailchimp_emails = []
        i = 0
        while members_mailchimp := self.get_list_members(
            list_id=list_mailchimp_id,
            fields=["members.email_address", "members.status"],
            count=1000,
            offset=i,
        ):
            for member in members_mailchimp:
                if member["status"] == "subscribed":
                    members_mailchimp_emails.append(member["email_address"])
            i += 1000

        return members_mailchimp_emails
