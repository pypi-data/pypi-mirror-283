"""This module contains a simulator for converted Smart Nord data.

The models itself are simple data provider.
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone

import mosaik_api_v3
import numpy as np
import polars as pl
from midas.util.compute_q import compute_p, compute_q

# import pandas as pd
from midas.util.dateformat import GER
from midas.util.dict_util import bool_from_dict, strtobool

# from midas.util.base_data_model import DataModel
# from midas.util.base_data_simulator import BaseDataSimulator
# from midas.util.forecast_data_model import ForecastDataModel
from midas.util.logging import set_and_init_logger
from midas.util.runtime_config import RuntimeConfig

from .meta import META
from .model import DataModel

LOG = logging.getLogger("midas_powerseries.simulator")


class PowerSeriesSimulator(mosaik_api_v3.Simulator):
    """A simulator for electrical power time series."""

    def __init__(self):
        super().__init__(META)

        self.sid = None
        self.step_size = None
        self.now_dt = None
        self.sim_time = 0
        self.seed = None
        self.rng = None
        self.interpolate = False
        self.randomize_data = False
        self.randomize_cos_phi = False
        self.cos_phi = 0.9

        self.data = None
        self.data_step_size = 0
        self.num_models = {}
        self.models = {}

    def init(self, sid, **sim_params):
        """Called exactly ones after the simulator has been started.

        :return: the meta dict (set by mosaik_api.Simulator)
        """
        # super().init(sid, **sim_params)
        self.sid = sid
        self.step_size = int(sim_params.get("step_size", 900))
        self.now_dt = datetime.strptime(
            sim_params["start_date"], GER
        ).astimezone(timezone.utc)

        self.has_datetime_index = bool_from_dict(
            sim_params, "has_datetime_index"
        )

        # Load the data
        data_path = sim_params.get(
            "data_path", RuntimeConfig().paths["data_path"]
        )
        file_path = os.path.join(data_path, sim_params["filename"])
        LOG.debug("Using db file at %s.", file_path)
        self.data_step_size = int(sim_params.get("data_step_size", 900))

        if file_path.endswith(".csv"):
            self.data = pl.scan_csv(file_path)
        else:
            raise NotImplementedError("Only csv is supported, yet. Sorry!")

        self.interpolate = bool_from_dict(sim_params, "interpolate")
        self.randomize_data = bool_from_dict(sim_params, "randomize_data")
        self.randomize_cos_phi = bool_from_dict(
            sim_params, "randomize_cos_phi"
        )

        self.cos_phi = sim_params.get("cos_phi", 0.9)

        # RNG
        self.seed = sim_params.get("seed", None)
        self.seed_max = 2**32 - 1
        if self.seed is not None:
            self.rng = np.random.RandomState(self.seed)
        else:
            LOG.debug("No seed provided. Using random seed.")
            self.rng = np.random.RandomState()
        # self.num_households = len(self.load_p.columns)
        # self.num_lvlands = 8  # TODO store the number of lvlands in db

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

        :return: a list with information on the created entity

        """
        entities = []
        self.num_models.setdefault(model, 0)
        scaling = model_params.get("scaling", 1.0)
        for _ in range(num):
            eid = f"{model}-{self.num_models[model]}"

            # p_series = q_series = None
            p_calculated = q_calculated = False
            name = model_params["name"]

            if model == "CalculatedQTimeSeries":
                data = self.data.select(
                    (pl.col(name) * scaling).alias("p"),
                    compute_q(pl.col(name) * scaling).alias("q"),
                )
                calculate_missing = True
                q_calculated = True
            if model == "CalculatedPTimeSeries":
                data = self.data.select(
                    compute_p(pl.col(name) * scaling).alias("p"),
                    (pl.col(name) * scaling).alias("q"),
                )
                calculate_missing = True
                p_calculated = True
            if model == "CombinedTimeSeries":
                data = self.data.select(
                    (pl.col(name[0]) * scaling).alias("p"),
                    (pl.col(name[1]) * scaling).alias("q"),
                )
                # p_series = self.data.select(name[0])
                # q_series = self.data.select(name[1])
            if model == "ActiveTimeSeries":
                data = self.data.select((pl.col(name) * scaling).alias("p"))
            if model == "ReactiveTimeSeries":
                data = self.data.select((pl.col(name) * scaling).alias("q"))

            self.models[eid] = DataModel(
                data=data.collect(),
                data_step_size=900,
                scaling=model_params.get("scaling", 1.0),
                calculate_missing=calculate_missing,
                p_calculated=p_calculated,
                q_calculated=q_calculated,
                seed=self.rng.randint(self.seed_max),
                interpolate=self.interpolate,
                randomize_data=self.randomize_data,
                randomize_cos_phi=self.randomize_cos_phi,
            )

            self.num_models[model] += 1
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step."""
        self.sim_time = time

        # Default inputs
        for model in self.models.values():
            model.cos_phi = self.cos_phi
            model.now_dt = self.now_dt

        # Inputs from other simulators
        for eid, attrs in inputs.items():
            log_msg = {
                "id": f"{self.sid}.{eid}",
                "name": eid,
                "type": eid.split("-")[1],
                "sim_time": self.sim_time,
                "msg_type": "input",
                "src_eids": [],
            }

            for attr, src_ids in attrs.items():
                setpoint = 0.0
                all_none = True
                for src_id, value in src_ids.items():
                    if value is not None:
                        all_none = False
                        setpoint += float(value)
                        log_msg["src_eids"].append(src_id)
                if not all_none:
                    log_msg[attr] = setpoint
                    setattr(self.models[eid], attr, setpoint)

            log_msg["src_eids"] = list(set(log_msg["src_eids"]))
            LOG.info(json.dumps(log_msg))

        # Step the models
        for model in self.models.values():
            model.step()

        self.now_dt += timedelta(seconds=self.step_size)

        return time + self.step_size

    def get_data(self, outputs):
        """Returns the requested outputs (if feasible)."""

        data = {}

        for eid, attrs in outputs.items():
            log_msg = {
                "id": f"{self.sid}.{eid}",
                "name": eid,
                "type": eid.split("-")[0],
                "sim_time": self.sim_time,
                "msg_type": "output",
            }
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = getattr(self.models[eid], attr)
                log_msg[attr] = getattr(self.models[eid], attr)

            LOG.info(json.dumps(log_msg))

        return data

    # def _create_combined_model(self, model_params):
    #     series = self.data[model_params["name"]]

    #     model = DataModel(
    #         data_p=series,
    #         data_q=None,
    #         data_step_size=900,
    #         scaling=model_params.get("scaling", 1.0),
    #         seed=self.rng.randint(self.seed_max),
    #         interpolate=self.interpolate,
    #         randomize_data=self.randomize_data,
    #         randomize_cos_phi=self.randomize_cos_phi,
    #     )

    #     return model

    # def _create_active_model(self, model_params):
    #     series = self.data[model_params["name"]]

    # def _create_land(self, model_params):
    #     idx = model_params.get("eidx", None)
    #     if idx is None:
    #         idx = self.lvland_ctr
    #         self.lvland_ctr = (self.lvland_ctr + 1) % self.num_lvlands
    #     else:
    #         idx = max(0, min(self.num_lvlands, idx))

    #     hh_per_lvl = INFO[f"Land{idx}"]["num_houses"] - 1
    #     fkey = f"Load{idx}p000"
    #     tkey = f"Load{idx}p{hh_per_lvl}"

    #     data_p = self.load_p.loc[:, fkey:tkey].sum(axis=1)
    #     data_q = None
    #     if self.load_q is not None:
    #         data_q = self.load_q.loc[:, fkey:tkey].sum(axis=1)

    #     model = DataModel(
    #         data_p=data_p,
    #         data_q=data_q,
    #         data_step_size=900,
    #         scaling=model_params.get("scaling", 1.0),
    #         seed=self.rng.randint(self.seed_max),
    #         interpolate=model_params.get("interpolate", self.interpolate),
    #         randomize_data=model_params.get(
    #             "randomize_data", self.randomize_data
    #         ),
    #         randomize_cos_phi=model_params.get(
    #             "randomize_cos_phi", self.randomize_cos_phi
    #         ),
    #     )
    #     return model

    # def _create_household_forecast(self, model_params):
    #     idx = model_params.get("eidx", None)
    #     if idx is None:
    #         idx = self.household_ctr
    #         self.household_ctr = (self.household_ctr + 1) % 
    # self.num_households
    #     else:
    #         idx = max(0, min(self.num_households, idx))

    #     col = self.load_p.columns[idx]
    #     data_q = None
    #     if self.load_q is not None:
    #         data_q = self.load_q[col]

    #     model = ForecastDataModel(
    #         data_p=self.load_p[col],
    #         data_q=data_q,
    #         data_step_size=900,
    #         scaling=model_params.get("scaling", 1.0),
    #         seed=self.rng.randint(self.seed_max),
    #         interpolate=model_params.get("interpolate", self.interpolate),
    #         randomize_data=model_params.get(
    #             "randomize_data", self.randomize_data
    #         ),
    #         randomize_cos_phi=model_params.get(
    #             "randomize_cos_phi", self.randomize_cos_phi
    #         ),
    #         forecast_horizon_hours=model_params.get(
    #             "forecast_horizon_hours", 1.0
    #         ),
    #     )

    #     return model

    # def _create_land_forecast(self, model_params):
    #     raise NotImplementedError()

    def get_data_info(self, eid=None):
        if eid is not None:
            return self.models[eid].p_mwh_per_a
        else:
            info = {
                key: {"p_mwh_per_a": model.p_mwh_per_a}
                for key, model in self.models.items()
            }
            # info["num_lands"] = self.num_models.get("Land", 0)
            # info["num_households"] = self.num_models.get("Household", 0)
            return info


if __name__ == "__main__":
    set_and_init_logger(0, "sndata-logfile", "midas-sndata.log", replace=True)
    LOG.info("Starting mosaik simulation...")
    mosaik_api_v3.start_simulation(PowerSeriesSimulator())
