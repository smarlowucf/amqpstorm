""" AMQP-Storm Channel.Queue. """
__author__ = 'eandersson'

import logging

from pamqp.specification import Queue as pamqp_queue


LOGGER = logging.getLogger(__name__)


class Queue(object):
    """ Channel.Queue """

    def __init__(self, channel):
        self._channel = channel

    def declare(self, queue='', passive=False, durable=False,
                exclusive=False, auto_delete=False, arguments=None):
        """ Declare queue.

        :param str queue:
        :param bool passive:
        :param bool durable:
        :param bool exclusive:
        :param bool auto_delete:
        :param dict arguments:
        :return:
        """
        declare_frame = pamqp_queue.Declare(queue=queue,
                                            passive=passive,
                                            durable=durable,
                                            exclusive=exclusive,
                                            auto_delete=auto_delete,
                                            arguments=arguments)
        with self._channel.rpc.lock:
            uuid = self._channel.rpc.register_request(pamqp_queue.Declare)
            self._channel.write_frame(declare_frame)
            return self._channel.rpc.get_request(uuid)

    def delete(self, queue='', if_unused=False, if_empty=False):
        """ Delete queue.

        :param str queue:
        :param bool if_unused: Delete only if unused
        :param bool if_empty: Delete only if empty
        :return:
        """
        delete_frame = pamqp_queue.Delete(queue=queue, if_unused=if_unused,
                                          if_empty=if_empty)
        with self._channel.rpc.lock:
            uuid = self._channel.rpc.register_request(pamqp_queue.Delete)
            self._channel.write_frame(delete_frame)
            return self._channel.rpc.get_request(uuid)

    def purge(self, queue=''):
        """ Purge queue.

        :param str queue:
        :return:
        """
        purge_frame = pamqp_queue.Purge(queue=queue)

        with self._channel.rpc.lock:
            uuid = self._channel.rpc.register_request(pamqp_queue.Purge)
            self._channel.write_frame(purge_frame)
            return self._channel.rpc.get_request(uuid)

    def bind(self, queue='', exchange='', routing_key='', arguments=None):
        """ Bind queue.

        :param str queue:
        :param str exchange:
        :param str routing_key:
        :param dict arguments:
        :return:
        """
        bind_frame = pamqp_queue.Bind(queue=queue,
                                      exchange=exchange,
                                      routing_key=routing_key,
                                      arguments=arguments)
        with self._channel.rpc.lock:
            uuid = self._channel.rpc.register_request(pamqp_queue.Bind)
            self._channel.write_frame(bind_frame)
            return self._channel.rpc.get_request(uuid)

    def unbind(self, queue='', exchange='', routing_key='', arguments=None):
        """ Unbind queue.

        :param str queue:
        :param str exchange:
        :param str routing_key:
        :param dict arguments:
        :return:
        """
        unbind_frame = pamqp_queue.Unbind(queue=queue,
                                          exchange=exchange,
                                          routing_key=routing_key,
                                          arguments=arguments)
        with self._channel.rpc.lock:
            uuid = self._channel.rpc.register_request(pamqp_queue.Unbind)
            self._channel.write_frame(unbind_frame)
            return self._channel.rpc.get_request(uuid)
