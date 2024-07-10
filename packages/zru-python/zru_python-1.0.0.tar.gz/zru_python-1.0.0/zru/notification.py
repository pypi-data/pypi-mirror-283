import hashlib

class NotificationData(object):
    """
    Notification data - class to manage notifications from ZRU
    """
    NOTIFICATION_SIGNATURE_PARAM = 'signature'
    NOTIFICATION_SIGNATURE_IGNORE_FIELDS = ['fail', 'signature']

    TYPE_TRANSACTION = 'P'
    TYPE_SUBSCRIPTION = 'S'
    TYPE_AUTHORIZATION = 'A'

    STATUS_DONE = 'D'
    STATUS_CANCELLED = 'C'
    STATUS_EXPIRED = 'E'
    STATUS_PENDING = 'N'

    SUBSCRIPTION_STATUS_WAIT = 'W'
    SUBSCRIPTION_STATUS_ACTIVE = 'A'
    SUBSCRIPTION_STATUS_PAUSED = 'P'
    SUBSCRIPTION_STATUS_STOPPED = 'S'

    AUTHORIZATION_STATUS_ACTIVE = 'A'
    AUTHORIZATION_STATUS_REMOVED = 'R'

    SALE_GET = 'G'
    SALE_HOLD = 'H'
    SALE_VOID = 'V'
    SALE_CAPTURE = 'C'
    SALE_REFUND = 'R'
    SALE_SETTLE = 'S'
    SALE_ESCROW_REJECTED = 'E'
    SALE_ERROR = 'I'

    def __init__(self, json_body, zru):
        """
        Initializes a notification data
        :param json_body: content of request from ZRU
        :param zru: ZRUClient
        """
        self.json_body = json_body
        self.zru = zru

    @property
    def is_transaction(self):
        """
        Check if the notification type is a transaction.
        
        :return: True if the notification is a transaction, False otherwise
        """
        return self.type == self.TYPE_TRANSACTION

    @property
    def is_subscription(self):
        """
        Check if the notification type is a subscription.
        
        :return: True if the notification is a subscription, False otherwise
        """
        return self.type == self.TYPE_SUBSCRIPTION

    @property
    def is_authorization(self):
        """
        Check if the notification type is an authorization.
        
        :return: True if the notification is an authorization, False otherwise
        """
        return self.type == self.TYPE_AUTHORIZATION

    @property
    def transaction(self):
        """
        :return: transaction generated when payment was created
        """
        if not self.is_transaction:
            return None

        return self.zru.Transaction.get(self.json_body['id'])

    @property
    def subscription(self):
        """
        :return: subscription generated when payment was created
        """
        if not self.is_subscription:
            return None

        return self.zru.Subscription.get(self.json_body['id'])

    @property
    def authorization(self):
        """
        :return: authorization generated when payment was created
        """
        if not self.is_authorization:
            return None

        return self.zru.Authorization.get(self.json_body['id'])

    @property
    def sale(self):
        """
        :return: sale generated when payment was paid
        """
        if not self.json_body.get('sale_id', False):
            return None

        return self.zru.Sale.get(self.json_body['sale_id'])

    @property
    def is_status_done(self):
        """
        Check if the notification indicates a done status.
        
        :return: True if the status is done, False otherwise
        """
        return self.status == self.STATUS_DONE

    @property
    def is_status_cancelled(self):
        """
        Check if the notification indicates a cancelled status.
        
        :return: True if the status is cancelled, False otherwise
        """
        return self.status == self.STATUS_CANCELLED

    @property
    def is_status_expired(self):
        """
        Check if the notification indicates an expired status.
        
        :return: True if the status is expired, False otherwise
        """
        return self.status == self.STATUS_EXPIRED

    @property
    def is_status_pending(self):
        """
        Check if the notification indicates a pending status.
        
        :return: True if the status is pending, False otherwise
        """
        return self.status == self.STATUS_PENDING

    @property
    def is_subscription_waiting(self):
        """
        Check if the notification indicates a waiting subscription.
        
        :return: True if the subscription is waiting, False otherwise
        """
        return self.subscription_status == self.SUBSCRIPTION_STATUS_WAIT

    @property
    def is_subscription_active(self):
        """
        Check if the notification indicates an active subscription.
        
        :return: True if the subscription is active, False otherwise
        """
        return self.subscription_status == self.SUBSCRIPTION_STATUS_ACTIVE

    @property
    def is_subscription_paused(self):
        """
        Check if the notification indicates a paused subscription.
        
        :return: True if the subscription is paused, False otherwise
        """
        return self.subscription_status == self.SUBSCRIPTION_STATUS_PAUSED

    @property
    def is_subscription_stopped(self):
        """
        Check if the notification indicates a stopped subscription.
        
        :return: True if the subscription is stopped, False otherwise
        """
        return self.subscription_status == self.SUBSCRIPTION_STATUS_STOPPED

    @property
    def is_authorization_active(self):
        """
        Check if the notification indicates an active authorization.
        
        :return: True if the authorization is active, False otherwise
        """
        return self.authorization_status == self.AUTHORIZATION_STATUS_ACTIVE

    @property
    def is_authorization_removed(self):
        """
        Check if the notification indicates a removed authorization.
        
        :return: True if the authorization is removed, False otherwise
        """
        return self.authorization_status == self.AUTHORIZATION_STATUS_REMOVED

    @property
    def is_sale_get(self):
        """
        Check if the sale action is 'Get'.
        
        :return: True if the sale action is 'Get', False otherwise
        """
        return self.sale_action == self.SALE_GET

    @property
    def is_sale_hold(self):
        """
        Check if the sale action is 'Hold'.
        
        :return: True if the sale action is 'Hold', False otherwise
        """
        return self.sale_action == self.SALE_HOLD

    @property
    def is_sale_void(self):
        """
        Check if the sale action is 'Void'.
        
        :return: True if the sale action is 'Void', False otherwise
        """
        return self.sale_action == self.SALE_VOID

    @property
    def is_sale_capture(self):
        """
        Check if the sale action is 'Capture'.
        
        :return: True if the sale action is 'Capture', False otherwise
        """
        return self.sale_action == self.SALE_CAPTURE

    @property
    def is_sale_refund(self):
        """
        Check if the sale action is 'Refund'.
        
        :return: True if the sale action is 'Refund', False otherwise
        """
        return self.sale_action == self.SALE_REFUND

    @property
    def is_sale_settle(self):
        """
        Check if the sale action is 'Settle'.
        
        :return: True if the sale action is 'Settle', False otherwise
        """
        return self.sale_action == self.SALE_SETTLE

    @property
    def is_sale_escrow_rejected(self):
        """
        Check if the sale action is 'Escrow Rejected'.
        
        :return: True if the sale action is 'Escrow Rejected', False otherwise
        """
        return self.sale_action == self.SALE_ESCROW_REJECTED

    @property
    def is_sale_error(self):
        """
        Check if the sale action is 'Error'.
        
        :return: True if the sale action is 'Error', False otherwise
        """
        return self.sale_action == self.SALE_ERROR

    def check_signature(self) -> str:
        dict_obj = dict(self.json_body)

        # Sort keys
        sorted_keys = self._get_sorted_keys(dict_obj)

        # Join all the values
        text_to_sign = ''

        for key in sorted_keys:
            if dict_obj[key] is None or key in self.NOTIFICATION_SIGNATURE_IGNORE_FIELDS or key.startswith('_'):
                continue
            # Clean values
            text_to_sign += self._clean_value(dict_obj[key])

        # Join Secret Code
        text_to_sign += self.zru.api_request.secret_key

        # Calculate SHA256
        signature = self._sha256(text_to_sign)

        return signature == dict_obj[self.NOTIFICATION_SIGNATURE_PARAM]

    def _get_sorted_keys(self, dict_obj):
        """
        Get sorted keys of a dictionary.

        :param dict_obj: Dictionary to get keys from
        :return: Sorted list of keys
        """
        keys = list(dict_obj.keys())
        keys.sort()
        return keys

    def _clean_value(self, value):
        """
        Clean the input value by replacing specific characters with spaces and stripping leading/trailing spaces.

        Parameters:
        value: The input value to be cleaned.

        Returns:
        str: The cleaned value.
        """
        value = str(value)
        # Define characters to replace
        chars_to_replace = '<>\"\'()\\'
        # Create a translation table
        translation_table = str.maketrans(chars_to_replace, ' ' * len(chars_to_replace))
        # Translate and strip the value
        cleaned_value = value.translate(translation_table).strip()
        return cleaned_value

    def _sha256(self, text):
        """
        Calculate the SHA256 hash of the given text.

        :param text: The input text to hash
        :return: The SHA256 hash of the input text
        """
        text_encoded = text.encode('utf-8')
        return hashlib.sha256(text_encoded).hexdigest()

    def __getattr__(self, name):
        """
        Handle attribute access for missing attributes.
        
        This method is called when an attribute is not found in the instance's __dict__.
        It first checks the instance's __dict__, then the class attributes, and finally
        looks for the attribute in the json_body dictionary.

        @param name: The name of the attribute to access.
        @return: The value of the attribute if found in the instance's __dict__, 
                 class attributes, or json_body dictionary.
        @raises AttributeError: If the attribute is not found in any of the above locations.
        """
        # First, try to get the attribute from the instance dictionary
        if name in self.__dict__:
            return self.__dict__[name]

        # Then, try to get the attribute from the class attributes
        if hasattr(self.__class__, name):
            return getattr(self.__class__, name)

        # Finally, try to get the attribute from the json_body dictionary
        if name in self.json_body:
            return self.json_body[name]

        # If the attribute is not found, raise an AttributeError
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")