# The content of this file is largely based on:
# https://github.com/Azure/azure-iot-sdk-python/blob/d3619f8d5ec0beca87b0d3b98833ae8053c39419/device/samples/iothub_client_sample_module_sender.py

import iothub_client
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_to_output.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 1000

# Default to use MQTT to communicate to IoT Edge
PROTOCOL = IoTHubTransportProvider.MQTT

def send_confirmation_callback(message, result, send_context):
    print('Confirmation for message [%d] received with result %s' % (send_context, result))

class Sender(object):

    def __init__(self, protocol=PROTOCOL):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)
        # set the time until a message times out
        self.client.set_option('messageTimeout', MESSAGE_TIMEOUT)

    def send_event_to_output(self, outputQueueName, event, properties, send_context):
        if not isinstance(event, IoTHubMessage):
            event = IoTHubMessage(bytearray(event, 'utf8'))

        if len(properties) > 0:
            prop_map = event.properties()
            for key in properties:
                prop_map.add_or_update(key, properties[key])

        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)
