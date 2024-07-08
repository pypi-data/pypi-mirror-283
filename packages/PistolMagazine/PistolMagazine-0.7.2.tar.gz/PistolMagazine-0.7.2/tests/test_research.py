from pprint import pprint
# 禔 礽 祉 禛 禩 禟 䄉 祥 禵
from pistol_magazine import *


class Param(DataMocker):
    a: ProviderField = ProviderField(
        CyclicParameterProvider(parameter_list=[1000, 1031, 1001, 1002, 1009]).get_next_param
    )
    c: ProviderField = ProviderField(
        RandomFloatInRangeProvider(start=0.00, end=4.00, precision=4).get_random_float
    )
    d: ProviderField = ProviderField(
        IncrementalValueProvider(start=0, step=2).get_next_value
    )
    e: ProviderField = ProviderField(
        RegexProvider(pattern=r"\d{3}-[a-z]{2}").get_value
    )
    g = "s"
    f = {"key": "value"}
    create_time: Timestamp = Timestamp(Timestamp.D_TIMEE10, days=2)
    user_name: Str = Str(data_type="name")
    user_email: Str = Str(data_type="email")
    user_age: Int = Int(byte_nums=6, unsigned=True)

    def param_info(self):
        return self.mock(as_list=False)


def test_gen_data():
    data = Param().param_info()
    print(data)

