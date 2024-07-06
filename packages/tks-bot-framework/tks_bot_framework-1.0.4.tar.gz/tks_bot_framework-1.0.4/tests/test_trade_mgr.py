import yaml
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pytest_mock import MockerFixture
from botframework.trade_mgr import TradeMgr  
from famodels.direction import Direction
from famodels.trade import StatusOfTrade
from fasignalprovider.side import Side
from tksessentials import utils
import json
import time
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, AsyncMock, ANY


@pytest.fixture(autouse=True)
def insert_test_data(mocker):
    print("Test Fixture up")
    # Patch the entire algo_config.yaml
    path = Path(__file__).parent.parent.absolute().joinpath("tests/app_config.yaml")
    with open(path, 'r') as stream:
        try:
            algo_config=yaml.safe_load(stream)
            print(algo_config)
        except yaml.YAMLError as exc:
            print(exc)
    mocker.patch("tksessentials.utils.get_app_config", return_value=algo_config)

@pytest.fixture
def fixed_datetime():
    """A fixture that returns a fixed datetime object and formatted strings."""
    fixed_dt = datetime(2023, 3, 15, 12, 0, tzinfo=timezone.utc)
    formatted_timestamp = fixed_dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    timestamp_for_data_entry_key = fixed_dt.timestamp()
    return fixed_dt, formatted_timestamp, timestamp_for_data_entry_key

# @pytest.mark.asyncio
# @patch('tksessentials.database.produce_message', new_callable=AsyncMock)
# async def test_create_first_entry_for_pos_idx(mock_kafka_send_message, fixed_datetime):
#     # Arrange.
#     fixed_dt, formatted_timestamp, timestamp_for_data_entry_key = fixed_datetime
#     trade_mgr = TradeMgr()
#     topic_name_trade = "trade_topic"
#     pos_idx = 1
#     provider_trade_id = "test_trade_id"
#     provider_signal_id = "test_signal_id"
#     status_of_position = StatusOfTrade.NEW
#     price = 100.0
#     is_hot_signal = True
#     market = "test_market"
#     data_source = "test_data_source"
#     direction = Direction.LONG
#     tp = 110.0
#     sl = 90.0
#     position_size_in_percentage = 10.0
#     percentage_of_position = 50.0
    
#     # Act.
#     await trade_mgr.create_first_entry_for_pos_idx(
#         topic_name_trade=topic_name_trade,
#         pos_idx=pos_idx,
#         provider_trade_id=provider_trade_id,
#         provider_signal_id=provider_signal_id,
#         status_of_position=status_of_position,
#         price=price,
#         is_hot_signal=is_hot_signal,
#         market=market,
#         data_source=data_source,
#         direction=direction,
#         tp=tp,
#         sl=sl,
#         position_size_in_percentage=position_size_in_percentage,
#         percentage_of_position=percentage_of_position,
#         timestamp=timestamp_for_data_entry_key
#     )
    
#     # Assert.
#     trade_data = {
#         "time_of_data_entry": str(timestamp_for_data_entry_key),
#         "pos_idx": pos_idx,
#         "provider_trade_id": provider_trade_id,
#         "status_of_position": status_of_position,
#         "is_hot_signal": is_hot_signal,
#         "market": market,
#         "data_source": data_source,
#         "direction": direction,
#         "tp": tp,
#         "sl": sl,
#         "tp_sl_reached": False,
#         "position_size_in_percentage": position_size_in_percentage,
#         "time_of_position_opening": str(timestamp_for_data_entry_key),
#         "time_of_position_closing": None,
#         "buy_orders": json.dumps({
#             "buy_order_1": {
#                 "timestamp": timestamp_for_data_entry_key,
#                 "provider_signal_id": provider_signal_id,
#                 "percentage_of_position": percentage_of_position,
#                 "buy_price": price,
#                 "execution_confirmed": False
#             }
#         }),
#         "sell_orders": json.dumps({})
#     }

#     key = str(timestamp_for_data_entry_key)  # Use the timestamp as the key.
    
#     mock_kafka_send_message.assert_called_once_with(
#     topic_name=topic_name_trade,
#     key=key,
#     value=trade_data
#     )

# @pytest.mark.asyncio
# @patch('botframework.botframework_utils.execute_pull_query', new_callable=AsyncMock)
# async def test_get_active_positions(mock_execute_pull_query):
#     # Arrange.
#     trade_mgr = TradeMgr()
#     ksqldb_query_url = "http://localhost:8088/query"
#     view_name = "mock_view"
#     # Mocking the Kafka pull query results
#     mock_execute_pull_query.side_effect = [
#         # Results for position id 0
#         [
#             [1000, 0, 'some_trade_id', StatusOfTrade.NEW],
#             [2000, 0, 'some_trade_id', StatusOfTrade.SELLING]
#         ],
#         # Results for position id 1
#         [
#             [1500, 1, 'another_trade_id', StatusOfTrade.CLOSED]
#         ],
#         # Results for position id 2
#         [
#             [1200, 2, 'yet_another_trade_id', StatusOfTrade.NEW],
#             [2500, 2, 'yet_another_trade_id', StatusOfTrade.CLOSED]
#         ]
#     ]
#     # Act.
#     active_positions_long = await trade_mgr.get_active_positions(ksqldb_query_url, view_name, Direction.LONG)
#     active_positions_short = await trade_mgr.get_active_positions(ksqldb_query_url, view_name, Direction.SHORT)
#     # Assert.
#     assert active_positions_long == [0]
#     assert active_positions_short == []

@pytest.mark.asyncio
@patch('botframework.botframework_utils.execute_pull_query', new_callable=AsyncMock)
async def test_get_latest_trade_data_by_pos_idx(mock_execute_pull_query):
    # Arrange.
    trade_mgr = TradeMgr()
    ksqldb_query_url = "http://localhost:8088/query"
    view_name = "mock_view"
    pos_idx = 1
    # Mocking the Kafka pull query results
    mock_execute_pull_query.return_value = [
        [1000, pos_idx, 'some_trade_id', 'NEW'],
        [2000, pos_idx, 'some_trade_id', 'SELLING']
    ]
    # Act.
    latest_trade_data = await trade_mgr.get_latest_trade_data_by_pos_idx(ksqldb_query_url, view_name, pos_idx)
    # Assert.
    assert latest_trade_data == [2000, pos_idx, 'some_trade_id', 'SELLING']
    assert mock_execute_pull_query.call_count == 1

# @pytest.mark.asyncio
# @patch('botframework.botframework_utils.execute_pull_query', new_callable=AsyncMock)
# async def test_get_all_messages_by_provider_trade_id(mock_execute_pull_query):
#     # Arrange.
#     trade_mgr = TradeMgr()
#     ksqldb_query_url = "http://localhost:8088/query"
#     view_name = "mock_view"
#     provider_trade_id = "some_trade_id"
#     # Mocking the Kafka pull query results
#     mock_execute_pull_query.return_value = [
#         [1000, 0, provider_trade_id, 'NEW'],
#         [2000, 0, provider_trade_id, 'SELLING'],
#         [1500, 1, provider_trade_id, 'CLOSED']
#     ]
#     # Act.
#     messages = await trade_mgr.get_all_messages_by_provider_trade_id(ksqldb_query_url, view_name, provider_trade_id)
#     # Assert.
#     assert messages == [
#         [1000, 0, provider_trade_id, 'NEW'],
#         [2000, 0, provider_trade_id, 'SELLING'],
#         [1500, 1, provider_trade_id, 'CLOSED']
#     ]
#     assert mock_execute_pull_query.call_count == 1

@pytest.mark.asyncio
@patch('botframework.botframework_utils.execute_pull_query', new_callable=AsyncMock)
async def test_get_latest_trade_data_by_provider_trade_id(mock_execute_pull_query):
    # Arrange.
    trade_mgr = TradeMgr()
    ksqldb_query_url = "http://localhost:8088/query"
    view_name = "mock_view"
    provider_trade_id = "some_trade_id"
    # Mocking the Kafka pull query results
    mock_execute_pull_query.return_value = [
        [1000, 0, provider_trade_id, 'NEW'],
        [2000, 0, provider_trade_id, 'SELLING'],
        [1500, 1, provider_trade_id, 'CLOSED']
    ]
    # Act.
    latest_trade_data = await trade_mgr.get_latest_trade_data_by_provider_trade_id(ksqldb_query_url, view_name, provider_trade_id)
    # Assert.
    assert latest_trade_data == [2000, 0, provider_trade_id, 'SELLING']
    assert mock_execute_pull_query.call_count == 1

@pytest.mark.asyncio
@patch('tksessentials.database.produce_message', new_callable=AsyncMock)
@patch('botframework.trade_mgr.TradeMgr.get_latest_trade_data_by_provider_trade_id', new_callable=AsyncMock)
async def test_update_status_of_trade(mock_get_latest_trade_data_by_provider_trade_id, mock_kafka_send_message):
    # Arrange
    trade_mgr = TradeMgr()
    ksqldb_query_url = "http://localhost:8088/query"
    view_name = "mock_view"
    provider_trade_id = "some_trade_id"
    topic_name = "trade_topic"
    status_of_position = StatusOfTrade.SELLING
    timestamp = time.time() * 1000
    new_time_of_data_entry = str(timestamp)
    # Mocking the latest trade data
    active_trade = [
        1000, 0, provider_trade_id, 'NEW', True, 'test_market', 'test_data_source', 'LONG', 110, 90, False, 10, 1000,
        None, json.dumps({'order1': 'data'}), json.dumps({'order2': 'data'})
    ]
    mock_get_latest_trade_data_by_provider_trade_id.return_value = active_trade
    # Act.
    await trade_mgr.update_status_of_trade(ksqldb_query_url, view_name, provider_trade_id, topic_name, status_of_position)
    # Assert.
    expected_trade_data = {
        "time_of_data_entry": ANY,
        "pos_idx": active_trade[1],
        "provider_trade_id": active_trade[2],
        "status_of_position": status_of_position,
        "is_hot_signal": active_trade[4],
        "market": active_trade[5],
        "data_source": active_trade[6],
        "direction": active_trade[7],
        "tp": active_trade[8],
        "sl": active_trade[9],
        "tp_sl_reached": active_trade[10],
        "position_size_in_percentage": active_trade[11],
        "time_of_position_opening": active_trade[12],
        "time_of_position_closing": active_trade[13],
        "buy_orders": active_trade[14],
        "sell_orders": active_trade[15]
    }
    mock_kafka_send_message.assert_called_once_with(
        topic_name=topic_name,
        key=ANY,
        value=expected_trade_data
    )
    assert mock_get_latest_trade_data_by_provider_trade_id.call_count == 1


# @pytest.mark.asyncio
# @patch('botframework.botframework_utils.execute_pull_query', new_callable=AsyncMock)
# @patch('botframework.market_mgr.MarketMgr.get_last_price', new_callable=AsyncMock)
# async def test_get_realized_and_unrealized_profit_and_loss_of_position(mock_get_last_price, mock_execute_pull_query):
#     # Arrange.
#     trade_mgr = TradeMgr()
#     ksqldb_query_url = "http://localhost:8088/query"
#     view_name = "mock_view"
#     pos_idx = 0
#     market = "test_market"
#     exchange = "test_exchange"
    # # Mock the latest trade data
    # active_trade = [
    #     1000, pos_idx, "some_trade_id", 'NEW', True, market, 'test_data_source', 'LONG', 110, 90, False, 10, 1000,
    #     None, json.dumps({'order1': {'buy_price': 100, 'percentage_of_position': 50}}), json.dumps({})
    # ]
    # mock_execute_pull_query.return_value = [active_trade]
    # # Mock the current market price
    # mock_get_last_price.return_value = 120
    # # Act.
    # realized_pnl, unrealized_pnl, total_buy_percentage, total_sell_percentage = await trade_mgr.get_realized_and_unrealized_profit_and_loss_of_position(
    #     ksqldb_query_url, view_name, pos_idx, market, exchange
    # )
    # # Assert.
    # assert realized_pnl == 0
    # assert unrealized_pnl == 10  # ((120 - 100) / 100) * 50
    # assert total_buy_percentage == 50
    # assert total_sell_percentage == 0