u"""
Created on 2016-9-5

@author: cheng.li
"""

import pandas as pd
import numpy as np
from FactorModel.schedule import Scheduler
from FactorModel.portcalc import PortCalc
from FactorModel.ermodel import ERModelTrainer


class PerfAttribute(object):

    def __init__(self):
        self.p_table = pd.DataFrame()
        self.report = pd.DataFrame()

    def analysis(self,
                 er_trainer: ERModelTrainer,
                 schedule: Scheduler,
                 port_calc: PortCalc,
                 data: pd.DataFrame) -> None:
        all_apply_dates = sorted(data.index.unique())
        all_calculate_dates = sorted(data.calcDate.unique())
        factor_names = er_trainer.factor_names
        self.report = pd.DataFrame(columns=['calcDate', 'total'] + list(factor_names))
        for calc_date, apply_date in zip(all_calculate_dates, all_apply_dates):
            print(calc_date, apply_date)

            if self.p_table.empty and not schedule.is_rebalance(apply_date):
                continue

            this_data = data.loc[apply_date, :]
            codes = this_data.code
            returns = this_data['nextReturn1day'].values
            today_holding = this_data['todayHolding'].values.copy()
            evolved_bm = this_data['evolvedBMWeight'].values

            if not schedule.is_rebalance(apply_date):
                evolved_new_table = pd.DataFrame(np.zeros((len(codes), len(factor_names)), dtype=float),
                                                 index=codes,
                                                 columns=factor_names)
                evolved_new_table[factor_names] = self.p_table[factor_names]
                evolved_new_table.fillna(0, inplace=True)
                cashes = 1. - evolved_new_table.sum()
                evolved_new_table = evolved_new_table.multiply(1. + returns, axis=0)
                evolved_new_table /= cashes + evolved_new_table.sum()
                p_matrix = evolved_new_table.values
                total_pnl = np.dot(today_holding - evolved_bm, returns)
                today_holding.shape = -1, 1
                factor_pnl = returns @ (today_holding - p_matrix)
                self.p_table = evolved_new_table
                self.report.loc[apply_date] = [calc_date, total_pnl] + list(factor_pnl)
            else:
                evolved_preholding = this_data['evolvedPreHolding'].values
                pre_holding = pd.DataFrame(evolved_preholding, index=codes, columns=['todayHolding'])
                factor_values = this_data[factor_names]

                er_model = er_trainer.fetch_model(apply_date)['model']

                p_matrix = np.zeros((len(codes), len(factor_names)), dtype=float)
                for i, factor in enumerate(factor_names):
                    tb_copy = factor_values.copy(deep=True)
                    tb_copy[factor] = 0.
                    er = er_model.calculate_er(tb_copy)
                    er_table = pd.DataFrame(er, index=codes, columns=['er'])
                    res = port_calc.trade(er_table, pre_holding)
                    p_matrix[:, i] = res['todayHolding'].values

                total_pnl = np.dot(today_holding - evolved_bm, returns)
                today_holding.shape = -1, 1
                factor_pnl = returns @ (today_holding - p_matrix)
                self.p_table = pd.DataFrame(p_matrix, index=codes, columns=factor_names)
                self.report.loc[apply_date] = [calc_date, total_pnl] + list(factor_pnl)

    def plot(self):
        self.report[self.report.columns[1:]].cumsum().plot()


class PerfAttribute2(object):

    def __init__(self):
        self.p_table = pd.DataFrame()
        self.report = pd.DataFrame()

    def analysis(self,
                 er_trainer: ERModelTrainer,
                 schedule: Scheduler,
                 port_calc: PortCalc,
                 data: pd.DataFrame) -> None:
        all_apply_dates = sorted(data.index.unique())
        all_calculate_dates = sorted(data.calcDate.unique())
        factor_names = er_trainer.factor_names
        self.report = pd.DataFrame(columns=['calcDate', 'total'] + list(factor_names))
        for calc_date, apply_date in zip(all_calculate_dates, all_apply_dates):
            print(calc_date, apply_date)

            if self.p_table.empty and not schedule.is_rebalance(apply_date):
                continue

            this_data = data.loc[apply_date, :]
            codes = this_data.code
            returns = this_data['nextReturn1day'].values
            today_holding = this_data['todayHolding'].values.copy()
            evolved_bm = this_data['evolvedBMWeight'].values

            if not schedule.is_rebalance(apply_date):
                evolved_new_table = pd.DataFrame(np.zeros((len(codes), len(factor_names)), dtype=float),
                                                 index=codes,
                                                 columns=factor_names)
                evolved_new_table[factor_names] = self.p_table[factor_names]
                evolved_new_table.fillna(0, inplace=True)
                cashes = 1. - evolved_new_table.sum()
                evolved_new_table = evolved_new_table.multiply(1. + returns, axis=0)
                evolved_new_table /= cashes + evolved_new_table.sum()
                p_matrix = evolved_new_table.values
                total_pnl = np.dot(today_holding - evolved_bm, returns)
                evolved_bm.shape = -1, 1
                factor_pnl = returns @ (p_matrix - evolved_bm)
                self.p_table = evolved_new_table
                self.report.loc[apply_date] = [calc_date, total_pnl] + list(factor_pnl)
            else:
                evolved_preholding = this_data['evolvedPreHolding'].values
                pre_holding = pd.DataFrame(evolved_preholding, index=codes, columns=['todayHolding'])
                factor_values = this_data[factor_names]

                er_model = er_trainer.fetch_model(apply_date)['model']

                p_matrix = np.zeros((len(codes), len(factor_names)), dtype=float)
                for i, factor in enumerate(factor_names):
                    tb_copy = factor_values.copy(deep=True)
                    tb_copy.loc[:, :] = 0.
                    tb_copy[factor] = factor_values[factor]
                    er = er_model.calculate_er(tb_copy)
                    er_table = pd.DataFrame(er, index=codes, columns=['er'])
                    res = port_calc.trade(er_table, pre_holding)
                    p_matrix[:, i] = res['todayHolding'].values

                total_pnl = np.dot(today_holding - evolved_bm, returns)
                evolved_bm.shape = -1, 1
                factor_pnl = returns @ (p_matrix - evolved_bm)
                self.p_table = pd.DataFrame(p_matrix, index=codes, columns=factor_names)
                self.report.loc[apply_date] = [calc_date, total_pnl] + list(factor_pnl)

    def plot(self):
        self.report[self.report.columns[1:]].cumsum().plot()
