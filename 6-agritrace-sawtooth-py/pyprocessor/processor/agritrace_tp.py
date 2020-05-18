# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
'''
Transaction family class for agritrace.
'''

import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

LOGGER = logging.getLogger(__name__)

FAMILY_NAME = "agritrace"

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

# Prefix for agritrace is the first six hex digits of SHA-512(TF name).
sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

class AgriTraceTransactionHandler(TransactionHandler):
    '''                                                       
    Transaction Processor class for the agritrace transaction family.       
                                                              
    This with the validator using the accept/get/set functions.
    It implements functions to item_transfer money.
    '''

    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        '''This implements the apply function for this transaction handler.
                                                              
           This function does most of the work for this class by processing
           a single transaction for the agritrace transaction family.   
        '''                                                   
        
        # Get the payload and extract agritrace-specific information.
        header = transaction.header
        payload_list = transaction.payload.decode().split(",")
        operation = payload_list[0]
        transfer_details = payload_list[1]

        # Get the public key sent from the client.
        item_name_code = header.signer_public_key

        # Perform the operation.
        LOGGER.info("Operation = "+ operation)

        if operation == "item_transfer":
            self._make_item_transfer(context, transfer_details, item_name_code)
        else:
            LOGGER.info("Unhandled action. " +
                "Operation should be item_transfer")

    def _make_item_transfer(self, context, transfer_details, item_name_code):
        item_address = self._get_item_address(item_name_code)
        LOGGER.info('Got the key {} and the item address {} '.format(
            item_name_code, item_address))
        current_entry = context.get_state([item_address])
        transfer_history = str(['current_time', 'current_date', 'item_name_code', 'from_client', 'current_client', 'to_client'])
        
        if current_entry == []:
            LOGGER.info('No previous item transfers, creating new item transfer {} '
                .format(item_name_code))
            transfer_history = str(transfer_history) + str(transfer_details)
        else:
            item_history = str(current_entry[0].data)
            item_history = str(item_history) + str(transfer_details)
            transfer_history = str(item_history)

        state_data = str(transfer_history).encode('utf-8')
        addresses = context.set_state({item_address: state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")

    def _get_item_address(self, from_key):
        return _hash(FAMILY_NAME.encode('utf-8'))[0:6] + _hash(from_key.encode('utf-8'))[0:64]

def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

def main():
    '''Entry-point function for the agritrace transaction processor.'''
    setup_loggers()
    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://validator:4004')

        handler = AgriTraceTransactionHandler(sw_namespace)

        processor.add_handler(handler)

        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

