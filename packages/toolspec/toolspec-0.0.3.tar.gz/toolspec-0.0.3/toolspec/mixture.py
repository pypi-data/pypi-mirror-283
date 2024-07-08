# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from tqdm import tqdm
import pandas as pd
import numpy as np

class Concurrent:
    def __init__(self, n_pro, func, *args):
        self.counter = 0
        self.n_pro = n_pro
        self.q_in = Queue(maxsize=-1)
        self.q_out = Queue(maxsize=-1)
        self.p_list = []
        for i in range(self.n_pro):
            p = Process(func, args=(self.q_in, self.q_out, *args))
            self.p_list.append(p)
            p.start()
        self.check()
    def check(self):
        if sum([0 if p.is_alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise RuntimeError('Child Process Exception!')
        return True
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=10)
                self.counter -= 1
                return output
            except:
                continue
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= self.n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()

def feature_processing(data, var_list, lbound, ubound, fill_else=np.nan, decimal=3):
    def limit(x):
        return x if x >= lbound and x <= ubound else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in tqdm(list(target_region.keys())):
        region = target_region[target]
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(region).index, target] = fill_else


def calc_ks_auc(data, var_list, target_list, bins=None, weight=None, partition=None, ascending=None):
    def subtask(q_in, q_out, data, target_list, index_list, bins, weight, partition, ascending):
        while 1:
            try:
                var = q_in.get(timeout=10)
            except:
                continue
            data['value'] = data[var].astype('float').fillna(0)
            if bins:
                data['value'] = np.qcut(data['value'], bins, include_lowest=True).astype('str')
            else:
                data['value'] = data['value'].round(3)
            if partition:
                grouped = data.groupby(by=partition+['value'],as_index=False)[index_list].sum()
                grouped = grouped.merge(grouped.groupby(by=partition,as_index=False)[index_list].sum(), how='inner', on=partition, suffixes=('','_Total'))
                for target in target_list:
                    grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped.groupby(by=partition)[['Bad_%s' % target,'Good_%s' % target]].cumsum()
                    grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['CumBad_%s_Total' % target]
                    grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['CumGood_%s_Total' % target]
                    grouped['PctCumBadLst_%s'] = grouped.groupby(by=partition)['PctCumBad_%s' % target].shift(1).fillna(0)
                    grouped['PctCumGoodLst_%s'] = grouped.groupby(by=partition)['PctCumGood_%s' % target].shift(1).fillna(0)
                    grouped['ks_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                    grouped['auc_%s' % target] = (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) * (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) / 2
            else:
                grouped = data.groupby(by='value',as_index=False)[index_list].sum()
                for target in target_list:
                    grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped[['Bad_%s' % target,'Good_%s' % target]].cumsum()
                    grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['CumBad_%s' % target].max()
                    grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['CumGood_%s' % target].max()
                    grouped['PctCumBadLst_%s'] = grouped['PctCumBad_%s' % target].shift(1).fillna(0)
                    grouped['PctCumGoodLst_%s'] = grouped['PctCumGood_%s' % target].shift(1).fillna(0)
                    grouped['ks_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                    grouped['auc_%s' % target] = (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) * (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) / 2
            columns = partition + target_list + ['ks','auc']
            result = pd.DataFrame(columns=columns)
            for target in target_list:
                grouped['ks'] = grouped['ks_%s' % target]
                grouped['auc'] = grouped['auc_%s' % target]
                result = result.append(grouped[columns],ignore_index=True)
            result['var'] = var
            q_out.put(result)
    if partition and type(partition) == str:
        partition = [partition]
    index_list = []
    for target in target_list:
        index_list += ['Bad_%s' % target,'Good_%s' % target]
        if weight:
            data['Bad_%s' % target] = (data[target] == 1) * data[weight]
            data['Good_%s' % target] = (data[target] == 0) * data[weight]
        else:
            data['Bad_%s' % target] = (data[target] == 1) * 1
            data['Good_%s' % target] = (data[target] == 0) * 1
    con = Concurrent(n_pro, subtask, data, target_list, index_list)
    con.put(var_list)
    result = pd.DataFrame()
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output,ignore_index=True)
    con.exit()
    return result


def rules_mining_single(data, var_list, target_list, min_cnt=100, min_pct=0.05, weight=None, ascending=False, reverse=False):
    index_list = []
    for target in target_list:
        index_list += ['Bad_%s' % target,'Good_%s' % target,'Total_%s' % target]
        if weight:
            data['Bad_%s' % target] = (data[target] == 1) * data[weight]
            data['Good_%s' % target] = (data[target] == 0) * data[weight]
        else:
            data['Bad_%s' % target] = (data[target] == 1) * 1
            data['Good_%s' % target] = (data[target] == 0) * 1
        data['Total_%s' % target] = data['Bad_%s' % target] + data['Good_%s' % target]
    for var in var_list:
        data['value'] = data[var].astype('float').round(3)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        for target in target_list:
            grouped[]
    return

def calc_ks_auc_old(data, var_list, target_list, weight=None, partition=None, ascending=None):
    if partition:
        if type(partition) != list:
            partition = [partition]
    index_list = []
    for target in target_list:
        data['Bad_%s' % target] = (data[target] - data[target].min()) / (data[target].max() - data[target].min())
        data['Good_%s' % target] = (data[target].max() - data[target]) / (data[target].max() - data[target].min())
        if weight:
            data['Bad_%s' % target] = data['Bad_%s' % target] * data[weight]
            data['Good_%s' % target] = data['Good_%s' % target] * data[weight]
        index_list += ['%s_%s' % (index,target) for index in ['Bad','Good']]
    perf_tbl = pd.DataFrame()
    for var in var_list:
        if partition:
            grouped = data.groupby(by=partition+[var],as_index=False)[index_list].sum()
            grouped.sort_values(by=partition+[var],ascending=False,inplace=True)
            result = data.groupby(by=partition,as_index=False)[var].count()
            for target in target_list:
                grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped[['Bad_%s' % target,'Good_%s' % target]].groupby(by=partition).cumsum()
                grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
                grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
                grouped[['PctCumBadLst_%s' % target,'PctCumGoodLst_%s' % target]] = grouped[['PctCumBad_%s' % target,'PctCumGood_%s' % target]].groupby(by=partition).shift(1).fillna(0)
                grouped['+KS_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                grouped['-KS_%s' % target] = - grouped['+KS_%s' % target]
                grouped['+AUC_%s' % target] = (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) * (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) / 2
                grouped['-AUC_%s' % target] = grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target] - grouped['+AUC_%s' % target]
                result = result.merge(grouped.groupby(by=partition,as_index=False)[['+KS_%s' % target,'-KS_%s' % target]].max(), how='left', on=partition)
                result = result.merge(grouped.groupby(by=partition,as_index=False)[['+AUC_%s' % target,'-AUC_%s' % target]].sum(), how='left', on=partition)
                if ascending == True:
                    result['KS_%s' % target] = result['+KS_%s' % target]
                    result['AUC_%s' % target] = result['+AUC_%s' % target]
                elif ascending == False:
                    result['KS_%s' % target] = result['-KS_%s' % target]
                    result['AUC_%s' % target] = result['-AUC_%s' % target]
                else:
                    result['KS_%s' % target] = result[['+KS_%s' % target,'-KS_%s' % target]].apply(max,axis=1)
                    result['AUC_%s' % target] = result[['+AUC_%s' % target,'-AUC_%s' % target]].apply(max,axis=1)
            result['var'] = var
            result = result[['var']+partition+['KS_%s' % target for target in target_list]+['AUC_%s' % target for target in target_list]]
        else:
            grouped = data.groupby(by=var,as_index=False)[index_list].sum()
            grouped.sort_values(by=var,ascending=False,inplace=True)
            result = [var]
            columns = ['var']
            for target in target_list:
                grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped[['Bad_%s' % target,'Good_%s' % target]].cumsum()
                grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
                grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
                grouped[['PctCumBadLst_%s' % target,'PctCumGoodLst_%s' % target]] = grouped[['PctCumBad_%s' % target,'PctCumGood_%s' % target]].shift(1).fillna(0)
                grouped['+KS_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                grouped['-KS_%s' % target] = - grouped['+KS_%s' % target]
                grouped['+AUC_%s' % target] = (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) * (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) / 2
                grouped['-AUC_%s' % target] = grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target] - grouped['+AUC_%s' % target]
                if ascending == True:
                    result.append(grouped['+KS_%s' % target].max())
                    result.append(grouped['+AUC_%s' % target].sum())
                elif ascending == False:
                    result.append(grouped['-KS_%s' % target].max())
                    result.append(grouped['-AUC_%s' % target].sum())
                else:
                    result.append(grouped[['+KS_%s' % target,'-KS_%s' % target]].max().max())
                    result.append(grouped[['+AUC_%s' % target,'-AUC_%s' % target]].sum().max())
                columns += ['KS_%s' % target,'AUC_%s' % target]
            result = pd.DataFrame(columns=columns, data=[result])
        perf_tbl = perf_tbl.append(result,ignore_index=True)
    return perf_tbl

def cutoff_single(data, var_list, target_list, weight=None):
    index_list = []
    for target in target_list:
        data['Cnt_%s' % target] = 1 * (data[target] >= 0)
        if weight:
            data['Total_%s' % target] = data[weight] * (data[target] >= 0)
            data['Bad_%s' % target] = data[weight] * (data[target] == 1)
        else:
            data['Total_%s' % target] = 1 * (data[target] >= 0)
            data['Bad_%s' % target] = 1 * (data[target] == 1)
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['%s_%s' % (index,target) for index in ['Cnt','Total','Bad','Good']]
    for var in var_list:
        grouped = data.groupby(by=var,as_index=False)[index_list].sum()
        grouped['cutoff'] = (grouped[var] + grouped[var].shift(-1)) / 2
        grouped[['Cum%s' % index for index in index_list]] = grouped[index_list].cumsum()
        for target in target_list:
            grouped['PctCumCnt_%s' % target] = grouped['CumCnt_%s' % target] / grouped['Cnt_%s' % target].sum()
            grouped['PctCumTotal_%s' % target] = grouped['CumTotal_%s' % target] / grouped['Total_%s' % target].sum()
            grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
            grouped['Cnt_a_%s' % target] = grouped['CumCnt_%s' % target]
            grouped['Cnt_b_%s' % target] = grouped['CumCnt_%s' % target].max() - grouped['CumCnt_%s' % target]
            grouped['PctCnt_a_%s' % target] = grouped['PctCumCnt_%s' % target]
            grouped['PctCnt_b_%s' % target] = grouped['PctCumCnt_%s' % target].max() - grouped['PctCumCnt_%s' % target]
            grouped['PctTotal_a_%s' % target] = grouped['PctCumTotal_%s' % target]
            grouped['PctTotal_b_%s' % target] = grouped['PctCumTotal_%s' % target].max() - grouped['PctCumTotal_%s' % target]
            grouped['Badrate_a_%s' % target] = grouped['CumBad_%s' % target] / grouped['CumTotal_%s' % target]
            grouped['Badrate_b_%s' % target] = (grouped['CumBad_%s' % target].max()-grouped['CumBad_%s' % target]) / (grouped['CumTotal_%s' % target].max()-grouped['CumTotal_%s' % target])
            grouped['Entropy_a_%s' % target] = - grouped['Badrate_a_%s' % target] * np.log(grouped['Badrate_a_%s' % target]) - (1-grouped['Badrate_a_%s' % target]) * np.log(1-grouped['Badrate_a_%s' % target])
            grouped['Entropy_b_%s' % target] = - grouped['Badrate_b_%s' % target] * np.log(grouped['Badrate_b_%s' % target]) - (1-grouped['Badrate_b_%s' % target]) * np.log(1-grouped['Badrate_b_%s' % target])
            grouped['EntropyNew_%s' % target] = grouped['Entropy_a_%s' % target] * grouped['PctTotal_a_%s' % target] + grouped['Entropy_b_%s' % target] * grouped['PctTotal_b_%s' % target]
            grouped['BadrateAll_%s' % target] = grouped['CumBad_%s' % target].max() / grouped['CumTotal_%s' % target].max()
            grouped['EntropyOld_%s' % target] = - grouped['BadrateAll_%s' % target] * np.log(grouped['BadrateAll_%s' % target]) - (1-grouped['BadrateAll_%s' % target]) * np.log(1-grouped['BadrateAll_%s' % target])
            grouped['Gain_%s' % target] = grouped['EntropyOld_%s' % target] - grouped['EntropyNew_%s' % target]
        grouped['Gain'] = grouped[['Gain_%s' % target for target in target_list]].apply(max,axis=1)
        grouped.sort_values(by='Gain',ascending=False,inplace=True)
        cutoff = grouped.iloc[0]
    return cutoff

def woebin(data, var_list, target, cnt_min=100, pct_min=0.05, gain_min=0.001, index='Entropy', ascending=None):
    bin_tbl = pd.DataFrame(columns=['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV'])
    for var in var_list:
        grouped = data.groupby(by=var,as_index=False)[target].agg({'Total':'count','Bad':'sum'})
        grouped['cutoff'] = (grouped[var] + grouped[var].shift(-1)) / 2
        grouped.eval('Good = Total - Bad',inplace=True)
        grouped[['CumTotal','CumBad','CumGood']] = grouped[['Total','Bad','Good']].cumsum()
        grouped['PctCumTotal'] = grouped['CumTotal'] / grouped['Total'].sum()
        grouped['PctCumBad'] = grouped['CumBad'] / grouped['Bad'].sum()
        grouped['PctCumGood'] = grouped['CumGood'] / grouped['Good'].sum()
        grouped[['CumTotalLst','CumBadLst','CumGoodLst']] = grouped[['CumTotal','CumBad','CumGood']].shift(1).fillna(0)
        grouped[['PctCumTotalLst','PctCumBadLst','PctCumGoodLst']] = grouped[['PctCumTotal','PctCumBad','PctCumGood']].shift(1).fillna(0)
        intervals = []
        badrates = [grouped['Bad'].sum()/grouped['Total'].sum()]
        index = 0
        while index <= len(intervals):
            lbound = -np.inf if index == 0 else intervals[index-1]
            ubound = np.inf if index == len(intervals) else intervals[index]
            tmp = grouped[(grouped[var] >= lbound) & (grouped[var] <= ubound)].copy()
            tmp['Total_a'] = tmp['CumTotal'] - tmp['CumTotalLst'].min()
            tmp['Total_b'] = tmp['CumTotal'].max() - tmp['CumTotal']
            tmp['PctTotal_a'] = tmp['PctCumTotal'] - tmp['PctCumTotalLst'].min()
            tmp['PctTotal_b'] = tmp['PctCumTotal'].max() - tmp['PctCumTotal']
            tmp['PctBad_a'] = tmp['PctCumBad'] - tmp['PctCumBadLst'].min()
            tmp['PctBad_b'] = tmp['PctCumBad'].max() - tmp['PctCumBad']
            tmp['PctGood_a'] = tmp['PctCumGood'] - tmp['PctCumGoodLst'].min()
            tmp['PctGood_b'] = tmp['PctCumGood'].max() - tmp['PctCumGood']
            tmp['Badrate_a'] = (tmp['CumBad']-tmp['CumBadLst'].min()) / (tmp['CumTotal']-tmp['CumTotalLst'].min())
            tmp['Badrate_b'] = (tmp['CumBad'].max()-tmp['CumBad']) / (tmp['CumTotal'].max()-tmp['CumTotal'])
            tmp['Entropy_a'] = - tmp['Badrate_a'] * np.log(tmp['Badrate_a']) - (1-tmp['Badrate_a']) * np.log(1-tmp['Badrate_a'])
            tmp['Entropy_b'] = - tmp['Badrate_b'] * np.log(tmp['Badrate_b']) - (1-tmp['Badrate_b']) * np.log(1-tmp['Badrate_b'])
            tmp['EntropyNew'] = tmp['Entropy_a'] * tmp['PctTotal_a'] + tmp['Entropy_b'] * tmp['PctTotal_b']
            tmp['BadrateAll'] = (tmp['CumBad'].max()-tmp['CumBadLst'].min()) / (tmp['CumTotal'].max()-tmp['CumTotalLst'].min())
            tmp['EntropyOld'] = - tmp['BadrateAll'] * np.log(tmp['BadrateAll']) - (1-tmp['BadrateAll']) * np.log(1-tmp['BadrateAll'])
            tmp['GainEnt'] = tmp['EntropyOld'] - tmp['EntropyNew']
            tmp['IV_Old'] = (tmp['PctCumBad'].max()-tmp['PctCumBadLst'].min()-tmp['PctCumGood'].max()+tmp['PctCumGoodLst'].min()) * np.log((tmp['PctCumBad'].max()-tmp['PctCumBadLst'].min())/(tmp['PctCumGood'].max()-tmp['PctCumGoodLst'].min()))
            tmp['IV_New'] = (tmp['PctBad_a']-tmp['PctGood_a']) * np.log(tmp['PctBad_a']/tmp['PctGood_a']) + (tmp['PctBad_b']-tmp['PctGood_b']) * np.log(tmp['PctBad_b']/tmp['PctGood_b'])
            tmp['GainIV'] = tmp['IV_Old'] - tmp['IV_All']
            tmp['Gain'] = tmp['GainEnt'] * (index == 'Entropy') + tmp['GainIV'] * (index == 'IV')
            tmp = tmp[(tmp['Total_a'] > cnt_min) & (tmp['Total_b'] > cnt_min)]
            tmp = tmp[(tmp['PctTotal_a'] > pct_min) & (tmp['PctTotal_b'] > pct_min)]
            tmp = tmp[(tmp['Gain'] > gain_min) & (tmp['Gain'] < np.inf)]
            if ascending == True:
                tmp = tmp[tmp['Badrate_a'] < tmp['Badrate_b']]
                if index > 0:
                    tmp = tmp[tmp['Badrate_a'] > badrates[index-1]]
                if index < len(intervals):
                    tmp = tmp[tmp['Badrate_b'] < badrates[index+1]]
            elif ascending == False:
                tmp = tmp[tmp['Badrate_a'] > tmp['Badrate_b']]
                if index > 0:
                    tmp = tmp[tmp['Badrate_a'] < badrates[index-1]]
                if index < len(intervals):
                    tmp = tmp[tmp['Badrate_b'] > badrates[index+1]]
            if not tmp.empty:
                cutoff = tmp.sort_values(by='Gain',ascending=False).iloc[0]
                intervals.insert(index,cutoff['cutoff'])
                badrates[index] = cutoff['Badrate_b']
                badrates.insert(index,cutoff['Badrate_a'])
            else:
                index += 1
        intervals.insert(0,-np.inf)
        intervals.append(np.inf)
        grouped['bucket'] = np.cut(grouped[var],intervals,include_lowest=True)
        grouped = grouped.groupby(by='bucket',as_index=False)[['Total','Bad','Good']].sum()
        grouped['PctTotal'] = grouped['Total'] / grouped['Total'].sum()
        grouped['Badrate'] = grouped['Bad'] / grouped['Total']
        grouped['WOE'] = np.log((grouped['Bad']/grouped['Bad'].sum())/(grouped['Good']/grouped['Good'].sum()))
        grouped['IV'] = (grouped['Bad']/grouped['Bad'].sum()-grouped['Good']/grouped['Good'].sum()) * grouped['WOE']
        grouped['var'] = var
        grouped['bin'] = grouped.index + 1
        grouped['bucket'] = grouped['bucket'].apply(lambda x : str(x).strip().replace('inf]','inf)'))
        grouped['lbound'] = grouped['bucket'].apply(lambda x : str(x).split(',')[0].replace('(','').replace('[',''))
        grouped['ubound'] = grouped['bucket'].apply(lambda x : str(x).split(',')[1].replace(')','').replace(']',''))
        bin_tbl = bin_tbl.append(grouped[['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV']])
    iv_tbl = bin_tbl.groupby(by='var',as_index=False)['IV'].agg({'bins':'count','IV':'sum'}).sort_values(by='IV',ascending=False).reset_index().rename(columns={'index':'id'})
    bin_tbl = bin_tbl.merge(iv_tbl[['var','id']], how='left', on='var').sort_values(by=['id','bin']).drop(columns='id').reset_index(drop=True)
    return iv_tbl, bin_tbl

def raw2woe(data, var_list, bin_tbl):
    woe_data = data[var_list].copy()
    for var in var_list:
        bin_tmp = bin_tbl[bin_tbl['var'] == var].copy()
        if not bin_tmp.empty:
            woe_data[var] = 0
            for i in range(bin_tmp.shape[0]):
                value = bin_tmp.iloc[i]
                woe_data[var] = woe_data[var] + value['WOE'] * (data[var] > float(value['lbound'])) * (data[var] <= float(value['ubound']))
    return woe_data

def createcard(res, bin_tbl, point0=660, odds0=1/15, pdo=15, reverse=False):
    B = pdo / np.log(2) * (-1 if reverse == True else 1)
    A = point0 + B * np.log(odds0)
    bp = A + B * res.params[0]
    scoring_table = bin_tbl.merge(pd.DataFrame(columns=['coef'],data=res.params).reset_index().rename(columns={'index':'var'}), how='inner', on='var')
    scoring_table['score_org'] = - scoring_table['WOE'] * scoring_table['coef'] * B
    grouped = scoring_table.groupby(by='var',as_index=False)['score'].min()
    bp_amort = (bp + grouped['score'].sum()) / grouped['score'].count()
    scoring_table = scoring_table.merge(grouped.rename(columns={'score':'score_min'}), how='left', on='var')
    scoring_table['score'] = (scoring_table['score_org'] - scoring_table['score_min'] + bp_amort).apply(int)
    return scoring_table


#######################################################################################################################################################################################

from multiprocessing import Process, Queue
from tqdm import tqdm
import pandas as pd
import numpy as np


class Concurrent:
    def __init__(self, n_pro, func, args*):
        self.n_pro = n_pro
        self.q_in = Queue(maxsize=-1)
        self.q_out = Queue(maxsize=-1)
        self.counter = 0
        self.p_list = []
        for i in range(self.n_pro):
            p = Process(func, q_in, q_out, args*, daemon=True)
            self.p_list.append(p)
            p.start()
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=1)
                self.counter -= 1
                return output
            except:
                continue
    def check(self):
        if sum([0 if p.alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise('RuntimeError')
        return True
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()


def single_cutting(data, var, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, target_weight={}, method='sum', ascending=None):
    target_min_list = list(target_min_dict.keys())
    target_max_list = list(target_max_dict.keys())
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    index_list = ['cnt']
    data['cnt'] = (data[cnt_field] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in target_weight.keys():
            data['cnt_%s' % target] = (data[target] >= 0) * taget_weight[target] 
            data['sum_%s' % target] = (data[target] >= 0) * taget_weight[target] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    data['value'] = data.eval(var)
    grouped = data.groupby(by='value',as_index=False)[index_list].sum()
    ascending_list = [ascending] if ascending else [True, False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value',ascending=ascending)
        temp['cutoff'] = (temp['value'] + temp['value'].shift(-1)) / 2
        temp[index_list] = temp[index_list].cumsum()
        for target in target_list:
            temp['avg_%s' % target] = temp['sum_%s' % target] / temp['cnt_%s' % target]
            temp['gap_%s' % target] = 0
        for target in target_min_list:
            temp['gap_%s' % target] += (temp['avg_%s' % target] - target_min_dict[target]) * (temp['avg_%s' % target] > target_min_dict[target])
        for target in target_max_list:
            temp['gap_%s' % target] += (target_max_dict[target] - temp['avg_%s' % target]) * (temp['avg_%s' % target] < target_max_dict[target])
        for target in target_list:
            temp['gap_%s' % target] = temp['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
        temp['gap'] = temp[['gap_%s' % target for target in target_list]].apply(method, axis=1)
        temp['direction'] = '<' if ascending == True else '>'
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicate(subset='direction',keep='first')
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var'] = var
    return cutoff


def double_cutting(data, var1, var2, cnt_filed, cnt_req, target_min_dict={}, target_max_dict={}, target_weight={}, method='sum', ascending=None, pct_single=0):
    target_min_list = list(target_min_dict.keys())
    target_max_list = list(target_max_dict.keys())
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    index_list = ['cnt']
    data['cnt'] = (data[cnt_field] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in target_weight.keys():
            data['cnt_%s' % target] = (data[target] >= 0) * target_weight[target]
            data['sum_%s' % target] = (data[target] >= 0) * target_weight[target] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    data['value1'] = data.eval(var1)
    data['value2'] = data.eval(var2)
    mesh = pd.merge(data[['cnt','value1']].drop_duplicates(), data[['cnt','value2']].drop_duplicates(), how='inner', on=['cnt'])[['value1','value2']]
    grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value1',ascending=ascending[0])
        temp['cutoff1'] = (temp['value1'] + temp.groupby(by='value2')['value1'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value2')[index_list].cumsum()
        temp = temp.sort_values(by='value2',ascending=ascending[1])
        temp['cutoff2'] = (temp['value2'] + temp.groupby(by='value1')['value2'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value1')[index_list].cumsum()
        for target in target_list:
            temp['avg_%s' % target] = temp['sum_%s' % target] / temp['cnt_%s' % target]
            temp['gap_%s' % target] = 0
        for target in target_min_list:
            temp['gap_%s' % target] += (temp['avg_%s' % target] - target_min_dict[target]) * (temp['avg_%s' % target] > target_min_dict[target])
        for target in target_max_list:
            temp['gap_%s' % target] += (target_max_dict[target] - temp['avg_%s' % target]) * (temp['avg_%s' % target] < target_max_dict[target])
        for target in target_list:
            temp['gap_%s' % target] = temp['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
        temp['gap'] = temp[['gap_%s' % target for target in target_list]].apply(method, axis=1)
        temp['direction1'] = '<' if ascending[0] == True else '>'
        temp['direction2'] = '<' if ascending[1] == True else '>'
        result = result.append(temp,ignore_index=True)
    result = result.merge(grouped.groupby(by='value1',as_index=False)['cnt'].sum(), how='inner', on='value1', suffixes=('','_1'))
    result = result.merge(grouped.groupby(by='value2',as_index=False)['cnt'].sum(), how='inner', on='value2', suffixes=('','_2'))
    result['pct_1'] = (result['cnt_2'] - result['cnt']) / (grouped['cnt'].sum() - result['cnt'])
    result['pct_2'] = (result['cnt_1'] - result['cnt']) / (grouped['cnt'].sum() - result['cnt'])
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset=['direction1','direction2','value1'],keep='first')
    result = result[(result['pct_1'] >= pct_single) & (result['pct_2'] >= pct_single)]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var1'] = var1
    cutoff['var2'] = var2
    return cutoff


def cross_cutting(data, var_list, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, target_weight={}, method='sum', ascending=None, pct_single=0, min_gain=0, var_min=5, var_max=10, n_pro=30):
    def subtask(q_in, q_out, data, var_cutoff, cnt_field, cnt_req, cnt_tol, target_min_dict, target_max_dict, target_weight, method, ascending, pct_single, var_min, var_max):
        while 1:
            try:
                input = q_in.get(timeout=1)
            except:
                continue
            data['flag'] = 1
            for var in var_cutoff.keys():
                if var not in input:
                    direciton, cutoff = var_cutoff[var]
                    data['flag'] = data['flag'] * ((data[var] < cutoff) if direction == '<' else (data[var] > cutoff))
            if len(input) == 1:
                var = input[0]
                cutoff = single_cutting(data.query('flag == 1'), var, cnt_field, cnt_req, target_min_dict= target_min_dict, target_max_dict=target_max_dict, target_weight=target_weight, method=method, ascending=ascending)
            else:
                var1, var2 = input[0], input[1]
                cutoff = double_cutting(data.query('flag == 1'), var1, var2, cnt_field, cnt_req, target_min_dict= target_min_dict, target_max_dict=target_max_dict, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single)
            var_num = len(set(list(var_cutoff.keys()+input)))
            cutoff['gap_adj'] = cutoff['gap'] + 10 * (cutoff['cnt'] - cnt_req) / cnt_tol + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            q_out.put(cutoff)
    var_cutoff = {}
    def calculate(input_list):
        con = Concurrent(n_pro, subtask, data, var_cutoff, cnt_field, cnt_req, cnt_tol, target_min_dict, target_max_dict, target_weight, method, ascending, pct_single, var_min, var_max)
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        con.exit()
        return result
    gap_min = np.inf
    while 1:
        if len(var_cutoff) == 0:
            input_list = [(var,) for var in var_list]
        else:
            input_list = []
            var_list_1 = list(var_cutoff.keys())
            for i,var1 in enumerate(var_list_1):
                input_list += [(var1,var2) for j,var2 in enumerate(var_list_1) if j > i]
                input_list += [(var1,var2) for var2 in var_list if var2 not in var_list_1]
        result = calculate(input_list)
        if not result.empty:
            opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
            if opt['gap_adj'] > gap_min-min_gain:
                break
            gap_min = opt['gap_adj']
            if 'var' in opt.index:
                var_cutoff[opt['var']] = (opt['direction'],opt['cutoff'])
            else:
                var_cutoff[opt['var1']] = (opt['direction1'],opt['cutoff1'])
                var_cutoff[opt['var2']] = (opt['direction2'],opt['cutoff2'])
        else:
            break
    result = []
    for var in var_cutoff.keys():
        data['cnt1'] = data['cnt']
        for i in var_cutoff.keys():
            if i != var:
                direction, cutoff = var_cutoff[i]
                data['cnt1'] = data['cnt1'] * ((data[i] < cutoff) if direction == '<' else (data[i] > cutoff))
        direction, cutoff = var_cutoff[var]
        data['cnt2'] = data['cnt'] * (data[var] < cutoff) if direction == '<' else (data[var] > cutoff)
        pct_self = (data['cnt'].sum() - data['cnt2'].sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        pct_gain = (data['cnt1'].sum() - data.eval('cnt1*cnt2').sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        result.append([var,direction,cutoff,pct_self,pct_gain])
    var_cutoff = pd.DataFrame(columns=['var','direction','cutoff','pct_self','pct_gain'], data=result).sort_values(by='pct_gain',ascending=False).reset_index(drop=True)
    return var_cutoff


def cross_grouping(data, var_list, cnt_field, tab_conf, method='sum', ascending=False, pct_single=0, min_gain=0, var_min=5, var_max=10, reverse=False, n_pro=30):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse == True:
        index_list = [column for column if tab_copy.columns if 'min_' in column or 'max_' in colum]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = ['cnt']
    data['cnt'] = (data[cnt_field] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in target_weight.keys():
            data['cnt_%s' % target] = (data[target] >= 0) * target_weight[target]
            data['sum_%s' % target] = (data[target] >= 0) * target_weight[target] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    cnt_tol = data['cnt'].sum()
    data_choice = data.copy()
    result = pd.DataFrame()
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        var_cutoff = cross_cutting(data_choice, var_list, cnt_field, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single, min_gain=min_gain, var_min=var_min, var_max=var_max, n_pro=n_pro)
        data_choice['flag'] = 1
        for var in var_cutoff.keys():
            direction, cutoff = var_cutoff[var]
            data_choice['flag'] = data_choice['flag'] * ((data_choice[var] < cutoff) if direction == '<' else (data_choice[var] > cutoff))
        if reverse == True:
            data_choice = data_choice.query('flag == 1')
        else:
            data_choice = data_choice.query('flag == 0')
        result = result.append(var_cutoff,ignore_index=True)
    cross_tab = pd.pivot_table(result, index='id', columns='var', values='cutoff')
    if reverse == True:
        cross_tab.sort_index(ascending=False,inplace=True)
        cross_tab = cross_tab.cummin() if ascending == True else cross_tab.cummax()
    cross_tab['region'] = cross_tab.apply(lambda x : ' and '.join(['%s %s %f' % (column,'<' if ascending == True else '>',x[column]) for column in cross_tab.columns if x[colum] > 0]))
    cross_tab = cross_tab.reset_index().sort_values(by='id',ascending=True)
    data['id'] = 0
    for i in range(cross_tab.shape[0]):
        value = cross_tab.iloc[i]
        data.loc[(data['id'] == 0) & (data.index.isin(data.query(value['region']).index)), 'id'] = value['id']
    grouped = data.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    result = tab_conf.merge(cross_tab, how='left', on='id').merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return result


def merge_cutting(data, var_list, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, target_weight={}, method='sum', ascending=None, min_gain=0, var_min=5, var_max=10, max_weight=1, step_list=[], n_pro=30):
    def subtask(q_in, q_out, data, var_list, cnt_field, cnt_req):
        while 1:
            try:
                var_weight = q_in.get(timeout=1)
            except:
                continue
            formula = ' + '.join(['%s * %f' % (var_list[i],weight) for i,weight in enumerate(var_weight) if weight > 0])
            data['value'] = data.eval(formula).round(3)
            cutoff = single_cutting(data, 'value', cnt_field, cnt_req)
            var_num = len([1 for weight in var_weight if weight > 0])
            gap_add = sum([(weight-max_weight) for weight in var_weight if weight > max_weight])
            cutoff['gap_adj'] = cutoff['gap'] + 10 * gap_add + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            cutoff[var_list] = var_weight
            q_out.put(cutoff[['gap_adj']+var_list])
    con = Concurrent(n_pro, subtask, data)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    input_list = [[(1 if i == var else 0) for i in var_list] for var in var_list]
    result_all = calculate(input_list)
    opt = result_all.sort_values(by='gap_adj',ascending=True).iloc[0]
    var_weight_best = list(opt[var_list])
    gap_min = opt['gap_adj']
    for step in step_list:
        while 1:
            var_sub_1 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > max_weight]
            var_sub_2 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight >= step]
            var_sub = var_sub_1 if len(var_sub_1) > 0 else var_sub_2
            var_add = [var_list[i] for i,weight in enumerate(var_weight_best) if round(weight+step) <= max_weight]
            var_weight_cand = []
            for var1 in var_sub:
                for var2 in var_add:
                    if var1 != var2:
                        var_weight = var_weight_best.copy()
                        var_weight[var_list.index(var1)] = round(var_weight[var_list.index(var1)]-step)
                        var_weight[var_list.index(var2)] = round(var_weight[var_list.index(var2)]+step)
                        var_weight_cand.append(var_weight)
            var_weight_cand = list(pd.concat([result_all.eval('flag=1'), pd.DataFrame(columns=var_list, data=var_weight_list).eval('flag=0')], axis=0).drop_duplicates(subset=var_list,keep='first').query('flag=0')[var_list])
            var_weight_cand = [list(var_weight) for var_weight in var_weight_cand]
            result = calculate(var_weight_cand)
            result_all = result_all.append(result,ignore_index=True)
            if not result.empty:
                opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
                if opt['gap_adj'] > gap_min-min_gain:
                    break
                gap_min = opt['gap_adj']
                var_weight_best = list(opt[var_list])
    con.exit()
    var_choice = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > 0]
    var_weight = [weight for weight in var_weight_best if weight > 0]
    return var_choice, var_weight


def grid_cutting(data, var_couple, q_list, cnt_field, cnt_req, target_min_dict={}, target_max_dict={}, target_weight={}, method='sum', ascending=False, min_gain=0):
    target_min_list = list(target_min_dict.keys())
    target_max_list = list(target_max_dict.keys())
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    index_list = ['cnt']
    data['cnt'] = 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in target_weight.keys():
            data['cnt_%s' % target] = (data[target] >= 0) * target_weight[target]
            data['sum_%s' % target] = (data[target] >= 0) * target_weight[target] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = np.qcut(data[var_x], q_list, duplicates='drop')
    data['bin_y'] = np.qcut(data[var_y], q_list, duplicates='drop')
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['flag'] = 0
    choice = {}
    for index in index_list:
        choice[index] = 0
    border = []
    gap_min = np.inf
    while 1:
        if len(border) > 0:
            point_cand = []
            for i,j in enumerate(border):
                if i == 0 and j < len(var_y):
                    point_cand.append((i+1,j+1))
                elif i > 0 and j < border[i-1]:
                    point_cand.append((i+1,j+1))
            else:
                if i < len(bin_x) - 1:
                    point_cand.append((i+2,1))
        else:
            point_cand = [(1,1)]
        cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
        if cand.empty:
            break
        for index in index_list:
            cand[index] += choice[index]
        for target in target_list:
            cand['avg_%s' % target] = cand['sum_%s' % target] / cand['cnt_%s' % target]
            cand['gap_%s' % target] = 0
        for target in target_min_list:
            cand['gap_%s' % target] += (cand['avg_%s' % target] - target_min_dict[target]) * (cand['avg_%s' % target] > target_min_dict[target])
        for target in target_max_list:
            cand['gap_%s' % target] += (target_max_dict[target] - cand['avg_%s' % target]) * (cand['avg_%s' % target] < target_max_dict[target])
        for target in target_list:
            cand['gap_%s' % target] = cand['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
        cand['gap'] = cand[['gap_%s' % target for target in target_list]].apply(method,axis=1)
        opt = cand.sort_values(by='gap',ascending=True).iloc[0]
        if min_gain >= 0 and opt['gap'] > gap_min-min_gain:
            break
        point_x = bin_x.index(opt['bin_x']) + 1
        point_y = bin_y.index(opt['bin_y']) + 1
        if point_x <= len(border):
            border[point_x-1] = point_y
        else:
            border.append(point_y)
        for index in index_list:
            choice[index] = opt[index]
        mesh.loc[(opt['bin_x'],opt['bin_y']), 'flag'] = 1
        if min_gain < 0 and opt['cnt'] >= cnt_req:
            break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='flag')
    return cross_tab


def grid_grouping(data, var_couple, cnt_field, tab_conf, target_weight={}, method='sum', ascending=False, min_gain=0):
    target_min_list = [column.replace('min_','') for column if tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column if tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False)
    index_list = ['cnt']
    data['cnt'] = (data[cnt_field] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in target_weight.keys():
            data['cnt_%s' % target] = (data[target] >= 0) * target_weight[target]
            data['sum_%s' % target] = (data[target] >= 0) * target_weight[target] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    cnt_tol = data['cnt'].sum()
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = np.qcut(data[var_x], q_list, duplicates='drop')
    data['bin_y'] = np.qcut(data[var_y], q_list, duplicates='drop')
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['id'] = 0
    border = []
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        id = value['id']
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        choice = {}
        for index in index_list:
            choice[index] = 0
        gap_min = np.inf
        while 1:
            if len(border) > 0:
                point_cand = []
                for i,j in enumerate(border):
                    if i == 0 and j < len(bin_y):
                        point_cand.append((i+1,j+1))
                    elif i > 0 and j < border[i-1]:
                        point_cand.append((i+1,j+1))
                else:
                    if i < len(bin_x) - 1:
                        point_cand.append((i+2,1))
            else:
                point_cand = [(1,1)]
            if len(point_cand) == 0:
                break
            cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
            for index in index_list:
                cand[index] += choice[index]
            for target in target_list:
                cand['avg_%s' % target] = cand['sum_%s' % target] / cand['cnt_%s' % target]
                cand['gap_%s' % target] = 0
            for target in target_min_list:
                cand['gap_%s' % target] += (cand['avg_%s' % target] - target_min_dict[target]) * (cand['avg_%s' % target] > target_min_dict[target])
            for target in target_max_list:
                cand['gap_%s' % target] += (target_max_dict[target] - cand['avg_%s' % target]) * (cand['avg_%s' % target] < target_max_dict[target])
            for target in target_list:
                cand['gap_%s' % target] = cand['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
            cand['gap'] = cand[['gap_%s' % target for target in target_list]].apply(method,axis=1)
            opt = cand.sort_values(by='gap',ascending=True).iloc[0]
            if min_gain >= 0 and opt['gap'] > gap_min-min_gain:
                break
            point_x = bin_x.index(opt['bin_x']) + 1
            point_y = bin_y.index(opt['bin_y']) + 1
            if point_x <= len(border):
                border[point_x-1] = point_y
            else:
                border.append(point_y)
            for index in index_list:
                choice[index] = opt[index]
            mesh.loc[(opt['bin_x'],opt['bin_y']), 'id'] = id
            if min_gain < 0 and opt['cnt'] >= cnt_req:
                break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='id')
    grouped = mesh.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    grouped = tab_conf.merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return cross_tab, grouped


def attr_single_cutting(data1, data2, var, target, prefix=None, ascending=None):
    data = pd.concat([data1.eval('src = 1'), data2.eval('src = 2')], axis=0)
    index_list = ['cnt_1','cnt_2','sum_1','sum_2']
    data['cnt_1'] = (data['src'] == 1) * (data[target] >= 0) * 1
    data['cnt_2'] = (data['src'] == 2) * (data[target] >= 0) * 1
    data['sum_1'] = (data['src'] == 1) * (data[target] >= 0) * data[target]
    data['sum_2'] = (data['src'] == 2) * (data[target] >= 0) * data[target]
    avg_tol_1 = data['sum_1'].sum() / data['cnt_1'].sum()
    avg_tol_2 = data['sum_2'].sum() / data['cnt_2'].sum()
    gap_tol =  avg_tol_1 - avg_tol_2
    ascending_list = [ascending] if ascending else [True,False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        data['value'] = data.eval(var)
        if prefix:
            data.loc[~data.index.isin(data.query(prefix).index),'value'] = np.nan
        data.fillna(data['value'].max() if ascending == True else data['value'].min(),inplace=True)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        grouped.sort_values(by='value',ascending=ascending)
        grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
        grouped[index_list] = grouped[index_list].cumsum()
        grouped['pct_cnt_1'] = grouped['cnt_1'] / grouped['cnt_1'].max()
        grouped['pct_cnt_2'] = grouped['cnt_2'] / grouped['cnt_2'].max()
        grouped['pct_sum_1'] = grouped['sum_1'] / grouped['sum_1'].max()
        grouped['pct_sum_2'] = grouped['sum_2'] / grouped['sum_2'].max()
        grouped['avg_tgt_1'] = grouped['sum_1'] / grouped['cnt_1']
        grouped['avg_tgt_2'] = grouped['sum_2'] / grouped['cnt_2']
        grouped['pct_gap'] = (grouped['avg_tgt_1'] * grouped['pct_cnt_1'] - grouped['avg_tgt_2'] * grouped['pct_cnt_2']) / gap_tol
        grouped['diff'] = grouped['pct_gap'] - grouped['pct_cnt_2']
        grouped['direction'] = '<' if ascending == True else '>'
        grouped['var'] = var
        result = result.append(grouped,ignore_index=True)
    columns = ['diff','var','direction','cutoff','pct_gap','gap_tol','avg_tol_1','avg_tol_2','pct_cnt_1','pct_cnt_2','pct_sum_1','pct_sum_2','avg_tgt_1','avg_tgt_2']
    cutoff = result[columns].sort_values(by='diff',ascending=False).iloc[:1]
    return cutoff



def attr_double_cutting(data1, data2, var1, var2, target, prefix=None, ascending=None):
    data = pd.concat([data1.eval('src = 1'), data2.eval('src = 2')], axis=0)
    index_list = ['cnt_1','cnt_2','sum_1','sum_2']
    data['cnt_1'] = (data['src'] == 1) * (data[target] >= 0) * 1
    data['cnt_2'] = (data['src'] == 2) * (data[target] >= 0) * 1
    data['sum_1'] = (data['src'] == 1) * (data[target] >= 0) * data[target]
    data['sum_2'] = (data['src'] == 2) * (data[target] >= 0) * data[target]
    avg_tol_1 = data['sum_1'].sum() / data['cnt_1'].sum()
    avg_tol_2 = data['sum_2'].sum() / data['cnt_2'].sum()
    gap_tol =  avg_tol_1 - avg_tol_2
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        data['value1'] = data.eval(var1)
        data['value2'] = data.eval(var2)
        if prefix:
            data.loc[~data.index.isin(data.query(prefix).index),'value'] = np.nan
        data['value1'].fillna(data['value1'].max() if ascending[0] == True else data['value1'].min(),inplace=True)
        data['value2'].fillna(data['value2'].max() if ascending[1] == True else data['value2'].min(),inplace=True)
        data['flag'] = 1
        mesh = pd.merge(data[['flag','value1']].drop_duplicates(), data[['flag','value2']].drop_duplicates(), how='inner', on='flag')[['value1','value2']]
        grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
        grouped.sort_values(by='value1',ascending=ascending[0])
        grouped['cutoff1'] = (grouped['value1'] + grouped.groupby(by='value2')['value1'].shift(-1)) / 2
        grouped[index_list] = grouped.groupby(by='value2')[index_list].cumsum()
        grouped.sort_values(by='value2',ascending=ascending[1])
        grouped['cutoff2'] = (grouped['value2'] + grouped.groupby(by='value1')['value2'].shift(-1)) / 2
        grouped[index_list] = grouped.groupby(by='value1')[index_list].cumsum()
        grouped['pct_cnt_1'] = grouped['cnt_1'] / grouped['cnt_1'].max()
        grouped['pct_cnt_2'] = grouped['cnt_2'] / grouped['cnt_2'].max()
        grouped['pct_sum_1'] = grouped['sum_1'] / grouped['sum_1'].max()
        grouped['pct_sum_2'] = grouped['sum_2'] / grouped['sum_2'].max()
        grouped['avg_tgt_1'] = grouped['sum_1'] / grouped['cnt_1']
        grouped['avg_tgt_2'] = grouped['sum_2'] / grouped['cnt_2']
        grouped['pct_gap'] = (grouped['avg_tgt_1'] * grouped['pct_cnt_1'] - grouped['avg_tgt_2'] * grouped['pct_cnt_2']) / gap_tol
        grouped['diff'] = grouped['pct_gap'] - grouped['pct_cnt_2']
        grouped['direction1'] = '<' if ascending[0] == True else '>'
        grouped['direction2'] = '<' if ascending[1] == True else '>'
        grouped['var1'] = var1
        grouped['var2'] = var2
        result = result.append(grouped,ignore_index=True)
    columns = ['diff','var1','direction1','cutoff1','var2','direction2','cutoff2','pct_gap','gap_tol','avg_tol_1','avg_tol_2','pct_cnt_1','pct_cnt_2','pct_sum_1','pct_sum_2','avg_tgt_1','avg_tgt_2']
    cutoff = result[columns].sort_values(by='diff',ascending=False).iloc[:1]
    return cutoff



def rules_mining_single(data, var_list, target_list, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False):
    index_list = []
    for target in target_list:
        index_list += ['Total_%s' % target, 'Bad_%s' % target, 'Good_%s' % target]
        if weight:
            data['Total_%s' % target] = (data[target] >= 0) * data[weight]
            data['Bad_%s' % target] = (data[target] >= 0) * data[weight] * data[target]
        else:
            data['Total_%s' % target] = (data[target] >= 0) * 1
            data['Bad_%s' % target] = (data[target] >= 0) * data[target]
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
    columns = ['iv','var','direction','cutoff']
    for target in target_list:
        columns += ['%s_%s' % (index,target) for index in ['+Total','+PctTotal','+Badrate','-Total','-PctTotal','-Badrate']]
    result = pd.DataFrame(columns=columns)
    for var in var_list:
        data['value'] = data.eval(var)
        grouped = data.groupby(by='value',as_index=False)[index_list].sum()
        grouped.sort_values(by='value',ascending=True)
        grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
        grouped[['%s_1' % index for index in index_list]] = grouped[index_list].cumsum()
        for index in index_list:
            grouped['%s_2' % index] = grouped[index].sum() - grouped['%s_1' % index]
        for target in target_list:
            grouped['PctTotal_%s_1' % target] = grouped['Total_%s_1' % target] / grouped['Total_%s' % target].sum()
            grouped['PctTotal_%s_2' % target] = grouped['Total_%s_2' % target] / grouped['Total_%s' % target].sum()
            grouped['PctBad_%s_1' % target] = grouped['Bad_%s_1' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctBad_%s_2' % target] = grouped['Bad_%s_2' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctGood_%s_1' % target] = grouped['Good_%s_1' % target] / grouped['Good_%s' % target].sum()
            grouped['PctGood_%s_2' % target] = grouped['Good_%s_2' % target] / grouped['Good_%s' % target].sum()
            grouped['Badrate_%s_1' % target] = grouped['Bad_%s_1' % target] / grouped['Total_%s_1' % target]
            grouped['Badrate_%s_2' % target] = grouped['Bad_%s_2' % target] / grouped['Total_%s_2' % target]
            grouped['iv_%s_1' % target] = (grouped['PctBad_%s_1' % target] - grouped['PctGood_%s_1' % target]) * np.log(grouped['PctBad_%s_1' % target] / grouped['PctGood_%s_1' % target])
            grouped['iv_%s_2' % target] = (grouped['PctBad_%s_2' % target] - grouped['PctGood_%s_2' % target]) * np.log(grouped['PctBad_%s_2' % target] / grouped['PctGood_%s_2' % target])
            grouped['iv_%s' % target] = grouped['iv_%s_1' % target] + grouped['iv_%s_2' % target]
        grouped['iv'] = grouped[['iv_%s' % target for target in target_list]].apply(max,axis=1)
        grouped = grouped[(grouped['iv'] > 0) & (grouped['iv'] < np.inf)]
        for target in target_list:
            if ascending == True:
                grouped = grouped[grouped['Badrate_%s_1' % target] < grouped['Badrate_%s_2' % target]]
            else:
                grouped = grouped[grouped['Badrate_%s_1' % target] > grouped['Badrate_%s_2' % target]]
        grouped['direction'] = '<' if ascending == reverse else '>'
        for target in target_list:
            grouped['+Total_%s' % target] = grouped['Total_%s_1' % target] * (grouped['direction'] == '<') + grouped['Total_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-Total_%s' % target] = grouped['Total_%s_1' % target] * (grouped['direction'] == '>') + grouped['Total_%s_2' % target] * (grouped['direction'] == '<')
            grouped['+PctTotal_%s' % target] = grouped['PctTotal_%s_1' % target] * (grouped['direction'] == '<') + grouped['PctTotal_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-PctTotal_%s' % target] = grouped['PctTotal_%s_1' % target] * (grouped['direction'] == '>') + grouped['PctTotal_%s_2' % target] * (grouped['direction'] == '<')
            grouped['+Badrate_%s' % target] = grouped['Badrate_%s_1' % target] * (grouped['direction'] == '<') + grouped['Badrate_%s_2' % target] * (grouped['direction'] == '>')
            grouped['-Badrate_%s' % target] = grouped['Badrate_%s_1' % target] * (grouped['direction'] == '>') + grouped['Badrate_%s_2' % target] * (grouped['direction'] == '<')
            grouped = grouped[(grouped['+Total_%s' % target] >= cnt_min) & (grouped['+PctTotal_%s' % target] >= pct_min)]
        if not grouped.empty:
            opt = grouped.sort_values(by='iv',ascending=False).iloc[0]
            opt['var'] = var
            result = result.append(opt,ignore_index=True)
    result = result.sort_values(by='iv',ascending=False).reset_index(drop=True)[columns]
    return result


def rules_mining_deep(data, var_list, target_list, benchmark, target_lift, initial_point=[], max_depth=3, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False, n_pro=30):
    def subtask(q_in, q_out, data, var_list):
        while 1:
            try:
                wher_str = q_in.get(timeout=1)
            except:
                continue
            result = rules_mining_single(data.query(wher_str) if where_str else data, var_list, target_list, cnt_min=100, pct_min=0.05, weight=None, ascending=False, reverse=False)
            for i,target in enumerate(target_list):
                result['lift_%s' % target] = result['Badrate_%s' % target] / benchmark[i]
            result['lift'] = result[['lift_%s' % target]].apply(np.mean,axis=1)
            result['flag'] = (result['lift'] <= target_lift) * (reverse == True) + (result['lift'] >= target_lift) * (reverse == False)
            result['rule'] = result['var'] + result['direction'] + result['cutoff'].astype('str')
            q_out.put(result)
    con = Concurrent(n_pro, subtask, data)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    initial_point = [None] if len(initial_point) == 0 else initial_point
    detail = pd.DataFrame()
    for point in initial_point:
        input_list = [point]
        depth = 0
        result = pd.DataFrame()
        while depth < max_depth and len(input_list) > 0:
            depth += 1
            con.put(input_list)
            output = calculate(input_list)
            choice = output.query('flag == 1')
            result = result.append(choice,ignore_index=True)
            input_list = list(output['rule'])
        detail = detail.append(result,ignore_index=True)
    con.exit()
    rule_set = list(detail['rule'])
    return rule_set, detail


def rules_filter(data_oot, data_app, rule_set, target_list, benchmark, target_lift, cnt_oot_min=100, pct_oot_min=0.05, cnt_app_min=100, weight=None, reverse=False, mode='risk', n_pro=30):
    def subtask(q_in, q_out, data_oot, data_app):
        while 1:
            try:
                rule = q_in.get(timeout=1)
            except:
                continue
            hit_oot = data_oot.query(rule)[index_list].sum()
            cnt_app_hit = data_app.query(rule).shape[0]
            if min([hit_oot['+Total_%s' % target] for target in target_list]) >= cnt_oot_min and min([hit_oot['+PctTotal_%s' % target] for target in target_list]) >= pct_oot_min and cnt_app_hit >= cnt_app_min:
                lift = np.mean([hit_oot['+Badrate_%s' % target]/benchmark[i] for i,target in enumerate(target_lift)])
                lift = (1 / lift) if reverse == True else lift
                if lift > 1:
                    if mode == 'pct':
                        lift = cnt_app_hit / cnt_app_min
                else:
                    lift = 0
            else:
                lift = 0
            q_out.put([rule,lift])
    oot_remain = data_oot.copy()
    app_remain = data_app.copy()
    rule_choice = []
    rule_remain = rule_set.copy()
    while len(rule_remain) > 0:
        con = Concurrent(n_pro, subtask, oot_remain, app_remain)
        con.put(rule_remain)
        result = []
        for i in tqdm(rule_remain):
            output = con.get()
            result.append(output)
        con.exit()
        result = pd.DataFrame(columns=['rule','lift'], data=result)
        opt = result.sort_values(by='lift',ascending=False).iloc[0]
        if opt['lift'] <= 1:
            break
        rule = opt['rule']
        oot_remain = oot_remain.loc[~oot_remain.index.isin(oot_remain.query(rule).index)]
        app_remain = app_remain.loc[~app_remain.index.isin(app_remain.query(rule).index)]
        rule_choice.append(rule)
        rule_remain = list(result.query('lift > 1')['rule'])
    return rule_choice









