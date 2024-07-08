from parser_functions.combinators import FailResult, SuccessResult


def assert_success(result, expected_value, expected_index):
    match result:
        case SuccessResult(value, stream):
            assert value == expected_value
            assert stream.idx == expected_index
        case _:
            assert False, f"Received {result} expected SuccessResult"


def assert_fail(result):
    match result:
        case FailResult():
            pass
        case _:
            raise ValueError(f"Expected FailResult got {result}")
