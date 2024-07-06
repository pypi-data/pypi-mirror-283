from xhydro_temp.extreme_value_analysis.julia_import import Extremes, jl
from typing import Union
import pandas as pd
import xarray as xr
from xhydro_temp.extreme_value_analysis.structures.abstract_extreme_value_model import BlockMaxima, ThresholdExceedance
from xhydro_temp.extreme_value_analysis.structures.abstract_fitted_extreme_value_model import PwmAbstractExtremeValueModel
from xhydro_temp.extreme_value_analysis.structures.dataitem import Variable
from xhydro_temp.extreme_value_analysis.structures.conversions import py_list_to_jl_vector, jl_pwm_aev_to_py_aev, \
    py_dataframe_to_jl_dataframe, py_str_to_jl_symbol, py_blockmaxima_to_jl_blockmaxima, py_str_to_jl_symbol, \
    py_threshold_exceedance_to_jl_threshold_exceedance, jl_vector_tuple_to_py_list


# GEV
def gevfitpwm_1(y: list[float]) -> list:
    jl_y = py_list_to_jl_vector(y)
    # return jl_pwm_aev_to_py_aev(Extremes.gevfitpwm(jl_y))
    return jl_vector_tuple_to_py_list(Extremes.params(Extremes.gevfitpwm(jl_y)))
def gevfitpwm_2(py_dataframe: Union[pd.DataFrame, xr.DataArray], datacol: str) -> PwmAbstractExtremeValueModel:
    jl_df = py_dataframe_to_jl_dataframe(py_dataframe)
    jl_datacol = py_str_to_jl_symbol(datacol)
    return jl_pwm_aev_to_py_aev(Extremes.gevfitpwm(jl_df, jl_datacol))

def gevfitpwm_3(model: BlockMaxima) -> PwmAbstractExtremeValueModel:
    jl_model = py_blockmaxima_to_jl_blockmaxima(model)
    return jl_pwm_aev_to_py_aev(Extremes.gevfitpwm(jl_model))


# Gumbel
def gumbelfitpwm_1(y: list[float]) -> list:
    jl_y = py_list_to_jl_vector(y)
    # return jl_pwm_aev_to_py_aev(Extremes.gumbelfitpwm(jl_y))
    return jl_vector_tuple_to_py_list(Extremes.params(Extremes.gumbelfitpwm(jl_y)))


def gumbelfitpwm_2(py_dataframe: Union[pd.DataFrame, xr.DataArray], datacol: str) -> PwmAbstractExtremeValueModel:
    jl_df = py_dataframe_to_jl_dataframe(py_dataframe)
    jl_datacol = py_str_to_jl_symbol(datacol)
    return jl_pwm_aev_to_py_aev(Extremes.gumbelfitpwm(jl_df, jl_datacol))

def gumbelfitpwm_3(model: BlockMaxima) -> PwmAbstractExtremeValueModel:
    jl_model = py_blockmaxima_to_jl_blockmaxima(model)
    return jl_pwm_aev_to_py_aev(Extremes.gumbelfitpwm(jl_model))


# Gp
def gpfitpwm_1(y: list[float]) -> list:
    jl_y = py_list_to_jl_vector(y)
    # return jl_pwm_aev_to_py_aev(Extremes.gpfitpwm(jl_y))
    return jl_vector_tuple_to_py_list(Extremes.params(Extremes.gpfitpwm(jl_y)))

def gpfitpwm_2(py_dataframe: Union[pd.DataFrame, xr.DataArray], datacol: str) -> PwmAbstractExtremeValueModel:
    jl_df = py_dataframe_to_jl_dataframe(py_dataframe)
    jl_datacol = py_str_to_jl_symbol(datacol)
    return jl_pwm_aev_to_py_aev(Extremes.gpfitpwm(jl_df, jl_datacol))

def gpfitpwm_3(model: ThresholdExceedance) -> PwmAbstractExtremeValueModel:
    jl_model = py_threshold_exceedance_to_jl_threshold_exceedance(model)
    return jl_pwm_aev_to_py_aev(Extremes.gpfitpwm(jl_model))
