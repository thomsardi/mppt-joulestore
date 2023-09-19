
class MpptEpeverAddress() :
    #Function code 04
    PV_INFO = (0x3100, 4)
    PV_VOLTAGE = (0x3100, 1)
    PV_CURRENT = (0x3101, 1)
    PV_POWER = (0x3102, 2)

    #Function code 04
    LOAD_INFO = (0x310c, 4)
    LOAD_VOLTAGE = (0x310c, 1)
    LOAD_CURRENT = (0x310d,1)
    LOAD_POWER = (0x310e, 2)

    #Function code 04
    TEMPERATURE_INFO = (0x3110, 2)
    BATTERY_TEMPERATURE = (0x3110, 1)
    DEVICE_TEMPERATURE = (0x3111, 1)

    #Function code 04
    BATTERY_SOC = (0x311a, 1)
    BATTERY_RATED_VOLTAGE = (0x311d, 1)

    #Function code 04
    STATUS_INFO = (0x3200, 3)
    BATTERY_STATUS = (0x3200, 1)
    CHARGING_STATUS = (0x3201, 1)
    DISCHARGING_STATUS = (0x3202, 1)

    #Function code 04
    OTHER_INFO = (0x3302, 18)
    MAX_BATTERY_VOLTAGE_TODAY = (0x3302, 1)
    MIN_BATTERY_VOLTAGE_TODAY = (0x3303, 1)
    CONSUMED_ENERGY_INFO = (0x3304, 8)
    CONSUMED_ENERGY_TODAY = (0x3304, 2)
    CONSUMED_ENERGY_THIS_MONTH = (0x3306, 2)
    CONSUMED_ENERGY_THIS_YEAR = (0x3308, 2)
    TOTAL_CONSUMED_ENERGY = (0x330a, 2)
    GENERATED_ENERGY_INFO = (0x330c, 8)
    GENERATED_ENERGY_TODAY = (0x330c, 2)
    GENERATED_ENERGY_THIS_MONTH = (0x330e, 2)
    GENERATED_ENERGY_THIS_YEAR = (0x3310, 2)
    TOTAL_GENERATED_ENERGY = (0x3312, 2)

    #Function code 04
    BATTERY_INFO = (0x331a, 3)
    BATTERY_VOLTAGE = (0x331a, 1)
    BATTERY_CURRENT = (0x331b, 2)

    BATT_VOLTAGE = (12548, 1)

    HARVEST_ENERGY = (13068, 1)
    # DEVICE_STATUS = (12801, 1)

    ARRAY_RATED_VOLTAGE = (0x3000, 1)

    #Function code 04
    RATED_CHARGING_CURRENT = (0x3005, 1)
    RATED_LOAD_CURRENT = (0x300e, 1)

    #Function code 04
    BATTERY_RATED_VOLTAGE = (0x311d, 1)

    #Function code 03 to read, 16 to write
    SETTING_PARAMETER = (0x9000, 15)
    BATTERY_TYPE_PARAMETER = (0x9000, 1)
    BATTERY_CAPACITY_PARAMETER = (0x9001, 1)
    TEMPERATURE_COEFFICIENT = (0x9002, 1)
    OVERVOLTAGE_DISCONNECT = (0x9003, 1)
    CHARGING_LIMIT_VOLTAGE = (0x9004, 1)
    OVERVOLTAGE_RECONNECT_VOLTAGE = (0x9005, 1)
    EQUALIZE_CHARGING_VOLTAGE = (0x9006, 1)
    BOOST_CHARGING_VOLTAGE = (0x9007, 1)
    FLOAT_CHARGING_VOLTAGE = (0x9008, 1)
    BOOST_RECONNECT_CHARGING_VOLTAGE = (0x9009, 1)
    LOW_VOLTAGE_RECONNECT_VOLTAGE = (0x900a, 1)
    UNDER_VOLTAGE_WARNING_RECOVER = (0x900b, 1)
    UNDER_VOLTAGE_WARNING = (0x900c, 1)
    LOW_VOLTAGE_DISCONNECT = (0x900d, 1)
    DISCHARGING_LIMIT_VOLTAGE = (0x900e, 1)

    NIGHT_TIME_THRESHOLD = (0x901e, 1)
    DAY_TIME_THRESHOLD = (0x9020, 1)

    #Function code 03 to read, 16 to write
    BATTERY_RATED_VOLTAGE_PARAMETER = (0x9067, 1)

    #Function code 03 to read, 16 to write
    OTHER_PARAMETER = (0x906a, 3)
    DEFAULT_LOAD_STATE = (0x906a, 1)
    EQUALIZE_DURATION = (0x906b, 1)
    BOOST_DURATION = (0x906c, 1)
    BATTERY_DISCHARGE_PERCENTAGE = (0x906d, 1)
    BATTERY_CHARGE_PERCENTAGE = (0x906e, 1)
    CHARGING_MODE = (0x9070, 1)

    CHARGING_SET = (0x0, 1)
    OUTPUT_CONTROL_MODE = (0x1, 1)
    LOAD_MANUAL_CONTROL = (0x2, 1)
    LOAD_DEFAULT_CONTROL = (0x3, 1)
    LOAD_CONTROL_MODE = (0x903d, 1)
    RESTORE_SYSTEM_DEFAULTS = (0x13, 1)
    CLEAR_LOG = (0x14, 1)

    MODE = (36967, 1)
    DATETIME_ADDR = (0x9013, 3)