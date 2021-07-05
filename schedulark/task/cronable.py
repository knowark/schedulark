from datetime import datetime, timezone


def cronable(pattern: str, moment: datetime = None) -> bool:
    """Check if a datetime moment matches the given cron pattern.
    .--------------- minute (0-59)
    |  .------------ hour (0-23)
    |  |  .--------- month_day (1-31)
    |  |  |  .------ month (1-12)
    |  |  |  |  .--- week_day (1-7; sunday=7)
    |  |  |  |  |
    *  *  *  *  *  cron command pattern
    """
    if not pattern:
        return False

    valid_characters = '0123456789 */!'
    if any(char not in valid_characters for char in pattern):
        raise ValueError(
            f'Invalid cron pattern. Use "{valid_characters}" only.')

    moment = moment or datetime.now(timezone.utc)

    second = '*'
    minute, hour, month_day, month, week_day = pattern.split()
    if '!' in minute:
        symbol, value = minute.split("!")
        second, minute = (f'*/{value}' if symbol else value, '*')

    return (_check_field(second, moment.second)
            and _check_field(minute, moment.minute)
            and _check_field(hour, moment.hour)
            and _check_field(month_day, moment.day)
            and _check_field(month, moment.month)
            and _check_field(week_day, moment.isoweekday()))


def _check_field(field: str, value: int) -> bool:
    if field == '*':
        return True

    if '/' in field:
        _, interval = field.split('/')
        return value % int(interval) == 0

    return int(field) == value
