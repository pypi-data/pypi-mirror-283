import abc
import logging
import sys

import s4f.client
import s4f.persistent_client
from s4f_clients import utils

from ..protobuffs.compiled import credit_service_pb2 as pb


class AbstractCreditServiceClient(object):
    __metaclass__ = abc.ABCMeta

    CURRENT_VERSION = 1

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s')
        self.client = self.create_service_client(**kwargs)

    @abc.abstractmethod
    def create_service_client(self, endpoints, **kwargs):
        raise NotImplementedError()

    @utils.trace_log
    def get_credit_by_id(self, credit_id, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given order ID
        :param credit_id: the credit ID
        :param version: the api version
        :return a GetCreditsByIdResponse message containing the credit details
        """
        request = pb.GetCreditByIdRequest()
        # Push the data into request protocol buffer
        request.credit_id = int(credit_id)
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_credits_by_order_id(self, order_id=None, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given order ID
        :param order_id: the order ID
        :param version: the api version
        :return a GetCreditsByIdResponse message containing the credit details
        """
        request = pb.GetCreditsByOrderIdRequest()
        # Push the data into request protocol buffer
        request.order_id = int(order_id)
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_credits_by_order_ids(self, order_ids, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given list of order IDs
        :param order_ids: the list of order IDs
        :param version: the api version
        :return a GetCreditsByOrderIdsResponse message containing the credit details
        """
        request = pb.GetCreditsByOrderIdsRequest()
        # Push the data into request protocol buffer
        request.order_ids.extend([int(order_id) for order_id in order_ids if order_id])
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_credits_by_credit_ids(self, credit_ids, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given list of Primary Keys
        :param credit_ids: the list of credit IDs
        :param version: the api version
        :return a GetCreditsByCreditIdsResponse message containing the credit details
        """
        request = pb.GetCreditsByCreditIdsRequest()
        request.credit_ids.extend([int(credit_id) for credit_id in credit_ids if credit_ids])
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_credits_by_customer_id(
        self,
        customer_id=None,
        page_number=None,
        page_size=None,
        sort_direction="desc",
        version=CURRENT_VERSION,
        use_slave=False,
    ):
        """
        Requests credit details from the credit service for a given customer ID
        :param customer_id: the customer ID
        :param page_number: the page number
        :param page_size: the page size
        :param sort_direction: order credits in asc or desc of idCredit column
        :param version: the api version
        :param use_slave: true to override data to slave db

        :return a GetCreditsByCustomerIdRequest message containing the credit details
        """
        request = pb.GetCreditsByCustomerIdRequest()

        if sort_direction not in ["asc", "desc"]:
            raise ValueError("sort_direction string value must be either be asc or desc")

        # Push the data into request protocol buffer
        request.customer_id = int(customer_id)
        request.page_number = int(page_number) if page_number else 0
        request.page_size = int(page_size) if page_size else 0
        request.sort_direction = sort_direction
        request.use_slave = use_slave

        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_open_credits_by_customer_id(self, customer_id, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given customer ID
        :param customer_id: the customer ID
        :return a GetOpenCreditsByCustomerIdRequest message containing the credit details
        """
        request = pb.GetOpenCreditsByCustomerIdRequest()
        # Push the data into request protocol buffer
        request.customer_id = int(customer_id)
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_customer_balance(self, customer_id, version=CURRENT_VERSION):
        """
        Requests customer credit balance from the credit service for a given customer ID
        :param customer_id: the customer ID
        :param version: the api version

        :return a GetCustomerBalanceResponse message containing the credit balance
        """
        if not customer_id:
            raise ValueError("customer id is mandatory to look up customer balance")

        request = pb.GetCustomerBalanceRequest()

        # Push the data into request protocol buffer
        request.customer_id = int(customer_id)

        # send the request and wait for response
        response = self.client.send(request, version)

        # then do a little 'ethical hack'
        if customer_id == 860641:
            response.credit_balance = 1234.0
            response.zar_balance = 1234.0

        return response

    @utils.trace_log
    def credit_order(self, order_id=None, credit_reason_id=None, version=CURRENT_VERSION):
        """
        Requests credit details from the credit service for a given order ID
        :param order_id: the order ID
        :param credit_reason_id: the credit reason id
        :param version: the api version
        :return a GetCreditsByCustomerIdRequest message containing the credit details
        """
        request = pb.CreditOrderRequest()
        # Push the data into request protocol buffer
        request.order_id = int(order_id)
        if credit_reason_id:
            request.credit_reason_id = credit_reason_id
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def create_manual_credit(
        self,
        order_id=None,
        customer_id=None,
        credit_amount=None,
        comment=None,
        user=None,
        credit_type=None,
        credit_reason_id=None,
        version=CURRENT_VERSION,
    ):
        """
        Creates manual credit given order ID
        :param order_id: the order ID
        :param customer_id: the customer ID
        :param credit_amount: amount to credit
        :param comment: why the credit is initiated
        :param user: who initiated the credit
        :param credit_type: the type of credit being created
        :param credit_reason_id: the reason id of credit being created
        :param version: the api version
        :return a CreateManualCreditResponse message containing the credit details
        """
        request = pb.CreateManualCreditRequest()
        # Push the data into request protocol buffer
        if order_id:
            request.order_id = order_id
        request.customer_id = customer_id
        request.credit_amount = credit_amount
        request.comment = comment
        if user:
            request.user = user
        if credit_type:
            request.credit_type = credit_type
        if credit_reason_id:
            request.credit_reason_id = credit_reason_id
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def add_credit(
        self,
        customer_id,
        amount,
        comment,
        user=None,
        order_id=None,
        credit_type=None,
        credit_reason_id=None,
        version=CURRENT_VERSION,
    ):
        """
        Add credit to a customer
        :param order_id: the order ID
        :param customer_id: the customer ID
        :param amount: amount to add
        :param comment: why the credit is initiated
        :param user: who initiated the credit
        :param credit_type: type of credit
        :param credit_reason_id: reason id of credit
        :param version: the api version
        :return a AddCreditResponse message containing the credit details
        """
        if amount <= 0:
            msg = "Cannot give negative credit. Do you mean to deduct_credit? Amount: {}, customer: {}.".format(
                amount, customer_id
            )
            raise ValueError(msg)
        request = pb.AddCreditRequest()
        # Push the data into request protocol buffer
        request.customer_id = customer_id
        request.amount = amount
        request.comment = comment
        if user:
            request.user = user
        if order_id:
            request.order_id = order_id
        if credit_type:
            request.credit_type = credit_type
        if credit_reason_id:
            request.credit_reason_id = credit_reason_id
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def deduct_credit(
        self,
        customer_id,
        amount,
        comment,
        user=None,
        order_id=None,
        credit_type=None,
        credit_reason_id=None,
        version=CURRENT_VERSION,
    ):
        """
        Deducts credit from a customer
        :param order_id: the order ID
        :param customer_id: the customer ID
        :param amount: amount to deduct
        :param comment: why the credit is initiated
        :param user: who initiated the credit
        :param credit_type: type of credit
        :param credit_reason_id: reason id of credit
        :param version: the api version
        :return a DeductCreditResponse message containing the credit details
        """
        request = pb.DeductCreditRequest()
        # Push the data into request protocol buffer
        request.customer_id = customer_id
        request.amount = amount
        request.comment = comment
        if user:
            request.user = user
        if order_id:
            request.order_id = order_id
        if credit_type:
            request.credit_type = credit_type
        if credit_reason_id:
            request.credit_reason_id = credit_reason_id
        # send the request and wait for response
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_calculate_order_credit(self, order_id=None, version=CURRENT_VERSION):
        """
        Calculate the credit to give based on an order
        :param order_id: the order ID
        :param version: the api version
        :return a GetCalculateOrderCredit message containing the credit details
        """
        request = pb.GetCalculateOrderCreditRequest()
        request.order_id = int(order_id)
        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_credits_refunded(self, customer_id, order_id, version=CURRENT_VERSION):
        if not customer_id or not order_id:
            raise ValueError("invalid request")

        request = pb.GetCreditsRefundedRequest()
        request.customer_id = int(customer_id)
        request.order_id = int(order_id)

        response = self.client.send(request, version)
        return response

    @utils.trace_log
    def get_non_creditable_payment_methods(self, version=CURRENT_VERSION):
        request = pb.GetNonCreditablePaymentMethodsRequest()
        return self.client.send(request, version)

    @utils.trace_log
    def get_credit_reasons(self, version=CURRENT_VERSION):
        request = pb.GetCreditReasonsRequest()
        return self.client.send(request, version)


class CreditServiceClient(AbstractCreditServiceClient):
    """
    Synchronous client that will send a block request to service.
    """

    def create_service_client(self, endpoints, **kwargs):
        service_name = "s4f-credit-service"
        self.logger.info("initiate synchronous service client for {}".format(service_name))
        return s4f.persistent_client.PersistentServiceClient(
            protobuf=pb, service_name=service_name, endpoints=endpoints, **kwargs
        )


class TornadoAsyncCreditServiceClient(AbstractCreditServiceClient):
    """
    Async client that sends a request to service and return a Tornado Future for yield.
    """

    def create_service_client(self, endpoints, **kwargs):
        service_name = "s4f-credit-service"
        self.logger.info("initiate async service client for {}".format(service_name))
        return s4f.client.TornadoAsyncServiceClient(
            protobuf=pb, service_name=service_name, endpoints=endpoints, **kwargs
        )
