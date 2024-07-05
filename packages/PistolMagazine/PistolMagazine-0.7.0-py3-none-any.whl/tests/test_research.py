from pprint import pprint
from random import choice

from pistol_magazine import *


@provider
class Param(DataMocker):
    a: ProviderField = ProviderField(
        CyclicParameterProvider(parameter_list=[1000, 1031, 1001, 1002, 1009]).get_next_param
    )
    b: ProviderField = ProviderField(
        FixedValueProvider(fixed_value="STATIC").get_fixed_value
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

# 禔 礽 祉 禛 禩 禟 䄉 祥 禵
    def param_info(self):
        return self.mock(num_entries=3, as_list=True, to_json=True)


class PostmanJson(DataMocker):
    name: ProviderField = ProviderField(
        FixedValueProvider(fixed_value="getinfo").get_fixed_value
    )
    method: ProviderField = ProviderField(
        CyclicParameterProvider(parameter_list=["GET", "POST"]).get_next_param
    )
    url: ProviderField = ProviderField(
        FixedValueProvider(fixed_value="https://api.example.com/user").get_fixed_value
    )
    header: Dict = Dict(
        {
            "Authorization": ProviderField(
                FixedValueProvider(fixed_value="Bearer token").get_fixed_value
            )
        }
    )
    body: ProviderField = ProviderField(Param().param_info)

    def gen_data(self):
        return self.mock(as_list=True, to_json=False)


def test_gen_data():
    data = Param().param_info()
    pprint(data)


def test_gen_postman_data():
    data = PostmanJson().gen_data()
    pprint(data)
