import logging
import time
from decimal import Decimal
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, QueryOrderStatus, TimeInForce
from alpaca.trading.models import TradeAccount
from alpaca.trading.models import Position as APosition
from alpaca.trading.models import Order as AOrder

from alpaca.trading.requests import GetOrdersRequest, LimitOrderRequest, ReplaceOrderRequest
from roboquant.account import Account, Position
from roboquant.config import Config
from roboquant.event import Event
from roboquant.brokers.broker import LiveBroker
from roboquant.order import Order

logger = logging.getLogger(__name__)


class AlpacaBroker(LiveBroker):

    def __init__(self, api_key=None, secret_key=None) -> None:
        super().__init__()
        self.__account = Account()
        config = Config()
        api_key = api_key or config.get("alpaca.public.key")
        secret_key = secret_key or config.get("alpaca.secret.key")
        self.__client = TradingClient(api_key, secret_key)
        self.price_type = "DEFAULT"
        self.sleep_after_cancel = 0.0

    def _sync_orders(self):
        orders = []
        request = GetOrdersRequest(status=QueryOrderStatus.OPEN)
        alpaca_orders: list[AOrder] = self.__client.get_orders(request)  # type: ignore
        for alpaca_order in alpaca_orders:
            order = Order(
                alpaca_order.symbol,
                Decimal(alpaca_order.qty),  # type: ignore
                float(alpaca_order.limit_price),  # type: ignore
            )
            order.fill = Decimal(alpaca_order.filled_qty)  # type: ignore
            order.id = str(alpaca_order.id)
            orders.append(order)

        self.__account.orders = orders

    def _sync_positions(self):
        open_pos: list[APosition] = self.__client.get_all_positions()  # type: ignore
        self.__account.positions.clear()
        for p in open_pos:
            size = Decimal(p.qty)
            if p.side == "short":
                size = -size
            new_pos = Position(size, float(p.avg_entry_price), float(p.current_price or "nan"))
            self.__account.positions[p.symbol] = new_pos

    def sync(self, event: Event | None = None) -> Account:
        now = self.guard(event)

        client = self.__client
        acc: TradeAccount = client.get_account()  # type: ignore
        self.__account.buying_power = float(acc.buying_power)  # type: ignore
        self.__account.cash = float(acc.cash)  # type: ignore
        self.__account.last_update = now

        self._sync_positions()
        self._sync_orders()
        return self.__account

    def place_orders(self, orders):

        for order in orders:

            if order.size.is_zero():
                assert order.id is not None, "can only cancel orders with an id"
                self.__client.cancel_order_by_id(order.id)
                if self.sleep_after_cancel:
                    time.sleep(self.sleep_after_cancel)
            else:
                if order.id is None:
                    req = self._get_order_request(order)
                    alpaca_order = self.__client.submit_order(req)
                    order.id = str(alpaca_order.id)  # type: ignore
                    self.__account.orders.append(order)
                else:
                    req = self._get_replace_request(order)
                    self.__client.replace_order_by_id(order.id, req)

    def _get_order_request(self, order: Order):
        side = OrderSide.BUY if order.is_buy else OrderSide.SELL
        return LimitOrderRequest(
            symbol=order.symbol,
            qty=abs(float(order.size)),
            side=side,
            limit_price=order.limit,
            time_in_force=TimeInForce.GTC,
        )

    def _get_replace_request(self, order: Order):
        result = ReplaceOrderRequest(qty=int(abs(float(order.size))), limit_price=order.limit)
        return result
