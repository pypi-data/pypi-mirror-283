import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
if 'map' in dir(pd.DataFrame):
    pd.DataFrame.applymap = pd.DataFrame.map
import numpy as np
import os
import re
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import num2date
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, AutoLocator, FixedLocator, MaxNLocator,LinearLocator)
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from statsmodels.stats.stattools import durbin_watson
from scipy.optimize import nnls
from scipy.stats import ttest_rel, ttest_ind, sem, t


# from causal_impact.utility_functions import flatten_list, date_to_index, cols_to_listcol, squeeze_y_ax, squeeze_x_ax, squeeze_axes, p_to_stars

# install functions
def install_r_optimizer():
    utils = importr('utils')
    utils.chooseCRANmirror(ind=72)
    utils.install_packages('lsei')
    
def install_r_causal_impact():
    utils = importr('utils')
    utils.chooseCRANmirror(ind=72)
    utils.install_packages('CausalImpact')

def setup():
    # print('- Installing CNLS')
    # install_r_optimizer()
    print('- Installing Causal Impact')
    install_r_causal_impact()
    
def format_ci_data(data):
    if np.min([x in data.columns for x in ['dates','posa','kpi']]) == True:
        data['dates'] = data['dates'].apply(lambda x: pd.to_datetime(x).date())
        return data
    else:
        print('Error: dataframe must have minimum 3 columns called dates, posa, kpi\n====================================================================')

# general functions
def flatten_list(l):
    # flattens a list of lists to a single list
    # l : list of lists
    flattened_list = [item for sublist in l for item in sublist]
    return flattened_list

def date_to_index(index,date):
    # matches a date to its position in a DataFrame index
    # and returns the index of that position
    # index : DataFrame index
    # date : pandas TimeStamp
    date_idx = int(np.where(index==date)[0])
    return date_idx

def cols_to_listcol(df,cols):
    # convert a group of cols in a pandas dataframe into a single column containing
    # a list of the values in those columns
    # df : DataFrame : must contain columns in cols
    # cols : list of str : column names to convert to column of lists
    col = df[cols].applymap(lambda x: [x]).sum(axis=1)
    return col

def squeeze_y_ax(ax,fac):
    l = ax.get_ylim()
    v = fac * np.diff(l)
    ax.set_ylim([l[0]-v,l[1]+v])
    
def squeeze_x_ax(ax,fac):
    l = ax.get_ylim()
    v = fac * np.diff(l)
    ax.set_ylim([l[0]-v,l[1]+v])
    
def squeeze_axes(ax,fac):
    if isinstance(fac,float):
        fac = [fac]
    squeeze_x_ax(ax,fac)
    squeeze_y_ax(ax,fac)
    
    
def format_labels(labels):
    max_magnitude = np.min([12,np.max([np.log10(abs(x))  if x != 0 else 0 for x in labels])])

    if max_magnitude < 3:
        suffix = ''
        max_magnitude = 0
    elif max_magnitude < 6:
        suffix = 'K'
        max_magnitude = 3
    elif max_magnitude < 9:
        suffix = 'M'
        max_magnitude = 6
    elif max_magnitude < 12:
        suffix = 'B'
        max_magnitude = 9
    else:
        suffix = 'T'

    labels = [np.round(x/(10**max_magnitude),2) for x in labels]
    if np.min([int(str(x).split('.')[-1])==0 for x in labels]) == True:
        labels = ['{}{}'.format(int(np.round(x,0)),suffix) for x in labels]
    else:
        labels = ['{}{}'.format(np.round(x,2),suffix) for x in labels]
    return labels

def p_to_stars(p):
    stars_dict = {0.05:'***',0.1:'**',0.2:'*'}
    if p<=0.05:
        o = '***'
    elif (p>0.05) & (p<=0.1):
        o = '**'
    elif (p>0.1) & (p<=0.2):
        o = '*'
    else:
        o = 'ns'
    return o

def make_ci_results_table(ci_results,**kwargs):
    """
    User function to concatenate results from multiple Causal Impact tests into one table
    ...
    
    
    Arguments
    ----------
    [REQUIRED]
    ci_results : dict of DataFrames
        Dictionary where each value is a Causal Impact test results DataFrame output by
        ci.test_results
        
    [OPTIONAL]
    expts : list of str
        List containing the keys to the experiments that need analysing in ci_results
    round : Bool
        Flag to dictate whether KPI columns are rounded. Note that P-values and correlation
        coefficients will not be rounded
    """
    
    expts = kwargs.get('expts',ci_results.keys())
    round_flag = kwargs.get('round',True)
    
    col_swap_dict = {'Prediction':'Predicted KPI',
                     'Actual':'Actual KPI',
                     'Absolute Effect':'Incremental KPI',
                     'Relative Effect':'Impact %',
                     'p':'Significance',
                     'control_corr':'Control correlation'}


    results_table = pd.DataFrame([x for x in [ci_results[k].test_results.rename(columns=col_swap_dict).loc['Cumulative',col_swap_dict.values()].rename(k) for k in expts]])

    if round_flag:
        rounded_cols = ['Predicted KPI','Actual KPI','Incremental KPI','Impact %']
        results_table[rounded_cols] = results_table[rounded_cols].applymap(lambda x: int(round(x)))

    results_table['Test success'] = (results_table['Significance']<=0.2) & (results_table['Control correlation']>=0.80)
    results_table['stars'] = results_table['Significance'].apply(p_to_stars)
    results_table.loc[results_table['Test success']==False,'stars'] = ''
    
    return results_table

def remove_r_components(obj):
    try:
        delattr(obj.test,'model')
    except:
        pass
    
def combine_ci_results(ci_dict):
    results_list = []
    for kpi in ci_dict.keys():
        results_list.append(make_ci_results_table(ci_dict[kpi]).assign(kpi=kpi))
    all_results = pd.concat(iter(results_list),axis=0)
    cols = list(all_results.columns)
    cols.remove('kpi')
    all_results = all_results[['kpi']+cols]
    return all_results

def format_ci_outputs(ci_dict):
    results_list = []
    timeseries_list = []
    coef_list = []
    for kpi in ci_dict.keys():
        results_list.append(make_ci_results_table(ci_dict[kpi]).assign(kpi=kpi))
        for grouping in ci_dict[kpi].keys():
            remove_r_components(ci_dict[kpi][grouping])
            timeseries_list.append(ci_dict[kpi][grouping].timeseries.assign(kpi=kpi,grouping=grouping))
            coef_list.append(ci_dict[kpi][grouping].df_coef_optimal.assign(kpi=kpi,grouping=grouping))

    all_results = pd.concat(iter(results_list),axis=0)
    cols = list(all_results.columns)
    cols.remove('kpi')
    all_results = all_results[['kpi']+cols]
    all_timeseries = pd.concat(iter(timeseries_list),axis=0)
    all_coef = pd.concat(iter(coef_list),axis=0)
    return ci_dict,all_results,all_timeseries,all_coef

def save_ci_outputs(ci_dict,savename):
    savename = os.path.join('causal_impact_results',savename.replace('.csv',''))
    
    if os.path.isdir('causal_impact_results')==False:
        os.mkdir('causal_impact_results')
    
    ci_dict,all_results,all_timeseries,all_coef = format_ci_outputs(ci_dict)
    all_results.to_csv(savename+'_ci_results.csv')
    all_timeseries.to_csv(savename+'_ci_timeseries.csv')
    all_coef.to_csv(savename+'_ci_coefficients.csv')
    with open(savename+'_ci_test.pickle', 'wb') as handle:
        pickle.dump(ci_dict, handle)
        
def load_ci_results(ci_results_file):
    file = open(ci_results_file,'rb')
    return pickle.load(file)

#### SUB-CLASSES   
class Params:
    """
    Sub-class used to format and arrange all parameters necessary for matching, testing
    and plotting
    ...
    
    
    Attributes
    ----------
    [REQUIRED]
    baseline_period : list of pandas timestamps
        2 timestamps defining the beginning and end date of the baseline period respectively.
        If the optional inputs train_period and control_period are not defined, then the
        baseline period will be used as the train_period (to fit the synthetic control) and the 
        control period (for the causal impact test)
    test_period : list of pandas timestamps
        2 timestamps defining the beginning and end of the campaign test period respectively
    
    [OPTIONAL]
    train_period : list of pandas timestamps
        2 timestamps defininf the beginning and end of the period used to generate the synthetic
        control timeseries (NB this MUST NOT include any of the test period). If not set, then
        this defauls to the baseline_period
    control_period : list of pandas timestamps
        2 timestamps defining the beginning and end of the control period used for the causal
        impact test. If not set, then this defaults to the baseline period
    post_period : list of pandas timestamps
        2 timestamps defining the beginning and end date of the post-test period respectively.
        If not set, then this defaults to the next consecutive date after the end of the test
        period until the maximum date in the data
    forced_control_posa : list of str
        Forces the list of posa that will be considered by the matching procedure
    exclude : list of str
        List of control posa to exclude from any analysis
    nseasons : int
        Number of timestamps within a seasonal trend, e.g. if timestamps are days then for a
        weekly trend set nseasons = 7 and season_duration = 1
    season_duration : int
        how long each element (nseason) of a seasonal trend lasts. So if timestamps are days
        and the seasonal trend is defined across days, then set the season_duration = 1
    plot : bool
        Flag dictating whether to plot causal impact test result outputs
    report : bool
        Flag dictating whether to print the results of the matching and testing phases
    figsize : list of int
        [X,Y] pixel dimensions of the causal impact test figure
    plot_style : list of str
        Any combination of ['kpi','point-wise','cumulative'] which correspond to the 3 styles
        of plot output by the causal impact test. 'kpi' = the overlay of the test and synthetic
        control posa timeseries (+/- 95% CI), 'point-wise' = (time)point-wise differences between
        test and control timeseries in the test period, 'cumulative' = cumulative difference
        between the test and control timeseries in the test period
    format_x : bool
        Flag dictating whether to re-format the x-axis in causal impact test plots so as to 
        only include the 1st and 15th of each month
    format_y : bool
        Flag dictating whether to re-format the y-axis in causal impact test plots so that all
        1000 --> K (e.g. 150,000 --> 150K)
    face_color : str or list of float
        Defines the color of 95% CI shading in all plots
    line_color : str or list of float
        Defines the color of the synthetic timeseries line in all plots
    """
    
    # period = baseline ([misc +] control + train [+ misc]) -> test -> post
    def __init__(self,data,baseline_period,test_period,test_posa,control_posa,**kwargs):
        
        # timing info
        test_posa = list(test_posa)
        control_posa = list(control_posa)
        
        self.baseline_period = baseline_period
        self.train_period = kwargs.get('train_period',baseline_period) # matching train period
        self.validation_period = kwargs.get('validation_period',[])
        self.control_period = kwargs.get('control_period',baseline_period) # causal impact baseline
        self.test_period = test_period # causal impact test
        max_date = data['dates'].apply(lambda x: pd.to_datetime(x).date()).max()
        self.post_period = kwargs.get('post_period',[np.min([max_date,np.max(test_period)+relativedelta(days=1)]),max_date])
        self.test_type = (kwargs.get('test_type','causal impact')).lower()
        
        # input and format all posa info
        self._data_posa = self._standardise_posa(list(data['posa'].unique()))
        self._test_posa0 = self._standardise_posa(test_posa)
        self._control_posa0 = self._standardise_posa(control_posa)
        self.exclude = self._standardise_posa(kwargs.get('exclude',[]))
        self.forced_control_posa = self._standardise_posa(kwargs.get('forced_control_posa',[]))
        self._test_posa0 = self._standardise_posa_list_format(self._test_posa0)
        self._control_posa0 = self._standardise_posa_list_format(self._control_posa0)
        self.exclude = self._standardise_posa_list_format(self.exclude)
        self.forced_control_posa = self._standardise_posa_list_format(self.forced_control_posa)
        if len(self.forced_control_posa)>0:
            print('- WARNING: using forced controls - ' + ', '.join(self.forced_control_posa))
            self._control_posa0 = self.forced_control_posa
        self._check_posa() # adds test_posa and control_posa attributes
        #self.control_posa_optimal = []
        
        # model params
        self.nseasons = kwargs.get('nseasons',1)
        self.season_duration = kwargs.get('season_duration',1)
        self.validated = self.validation_period != []
        
        # plot params
        self.plot = kwargs.get('plot',True)
        self.report = kwargs.get('report',True)
        if self.test_type=='causal impact':
            self.figsize = kwargs.get('figsize',[8,10])
        else: 
            self.figsize = kwargs.get('figsize',[8,5])
        self.plot_style = kwargs.get('plot_style',['kpi','point-wise','cumulative'])
        self.format_x = kwargs.get('format_x',True)
        self.format_y = kwargs.get('format_y',True)
        self.face_color = kwargs.get('face_color',[0.4,0.6,0.8])
        self.line_color = kwargs.get('line_color',[0,0,0])
        
    def _standardise_posa_list_format(self,posa_list):
        if isinstance(posa_list,str):
            posa_list = [posa_list]
        elif isinstance(posa_list,np.ndarray):
            posa_list = list(posa_list)
        return posa_list

    def _standardise_posa(self,s):
        if isinstance(s,str):
            s = s.strip()
            s = s.lower()
            s = re.sub('[ ]{0,}-[ ]{0,}',' ',s)
        elif isinstance(s,list):
            s = [self._standardise_posa(x) for x in s]
        elif isinstance(s,dict):
            s = dict(zip(s.keys(),self._standardise_posa([s[key] for key in s.keys()])))
        return s

    def _check_posa(self):
        self.test_posa = list(np.unique(self._test_posa0))
        self.control_posa = list(np.unique([x for x in self._control_posa0 if x in self._data_posa and x not in self.test_posa and x not in self.exclude]))
        if len(set(self.forced_control_posa).intersection(set(self.exclude)))>0:
            print('>>>> WARNING: forced control posa are present in your exclude list. These have been excluded, but check this is desired behaviour')
            
               
class Match:
    """
    Sub-class wrapping the constrained, non-negative least squares
    regression algorithm used by EG's EGGX to find the weighting of optimal
    control posa that results in a weighted sum timeseries that best matches
    the test posa (a synthetic control)
    ...
    
    
    Attributes
    ----------
    data : DataFrame
        Input data which should have timepoints as rows and posa as columns.
        Test and control posa should be described in relevant fields of the
        params object
    params : Params object
        Contains all params necessary for the matching procedure
    X : DataFrame
        Contains standardised control posa timeseries (all have been divided
        by their own mean)
    y : DataFrame
        Contains the standardised test posa timeseries (divided by its own 
        mean)
    df_coef: DataFrame
        Contains the posa and associated weighting coefficients just for all
        posa (including those with 0 weighting)
    df_coef_optimal : DataFrame
        Contains the posa and associated weighting coefficients just for those
        with non-zero weighting
    prc_correspondence : float
        Correlation coefficient calculated between the test posa and synthetic
        control posa during the train period (e.g. before the test occurs)
    timeseries: DataFrame]
        Test posa timeseries (sum of all test posa timeseries) and synthetic
        control timeseries (weighted sum of all control posa, weighted by the
        coefficients returned during the matching procedure)
    control_posa_optimal : list of str
        List of control posa that have >0 coefficient weighting in generating
        the synthetic control timeseries
    
    Methods
    -------
    run()

    """
    
    def __init__(self,data,params):
        self.data = data
        self.params = params
        self.params.train_start_date = np.min(self.params.train_period)
        self.params.train_end_date = np.max(self.params.train_period)
        if len(self.params.validation_period) != 0:
            self.params.validation_start_date = np.min(self.params.validation_period)
            self.params.validation_end_date = np.max(self.params.validation_period)
        else:
            self.params.validation_start_date = []
            self.params.validation_end_date = []
        self.params.control_start_date = np.min(self.params.control_period)
        self.params.control_end_date = np.max(self.params.control_period)
        
    def get_control_stats(self,data,**kwargs):
        period_start = kwargs.get('period_start',data.index.min())
        period_end = kwargs.get('period_end',data.index.max())
        d = data.loc[period_start:period_end,:]
        r2 = d[['test_timeseries','control_timeseries']].corr().values[0][1]
        dw = durbin_watson((d['test_timeseries']-d['control_timeseries']).values)
        return r2, dw

    def fit(self):
        # fit coefs on train period, validate on validation period, then make timeseries from 
        # time periods (control = train + validation period)
        control_start_date = self.params.control_start_date
        control_end_date = self.params.control_end_date        
        train_start_date = self.params.train_start_date
        train_end_date = self.params.train_end_date
        validation_start_date = self.params.validation_start_date
        validation_end_date = self.params.validation_end_date
        
        # data and params
        data0 = self.data       
        data_train = self.data.loc[train_start_date:train_end_date,:]
        data_control = self.data.loc[control_start_date:control_end_date,:]
        test_posa = self.params.test_posa
        control_posa = self.params.control_posa
        report = self.params.report
        plot = self.params.plot
        
        # fit CNLS to train period get coefs
        X,y = self._data_to_ols_vars(data_train,test_posa,control_posa)
        X = self._preprocess_data(X)
        y = self._preprocess_data(y)
        c = self._cnls_solve(X,y)
        df_coef = pd.DataFrame(data={'regions':control_posa,'coefficients':c}).set_index('regions')
        df_coef = df_coef.sort_values(by='coefficients',ascending=False)
        df_coef_optimal = df_coef.loc[df_coef['coefficients']>0,:]
        control_posa_optimal = list(df_coef_optimal.index)
        
        # make & assess train & validation control timeseries
        train_timeseries = self._make_timeseries(data0,test_posa,control_posa,c,start_train_date=train_start_date,end_train_date=train_end_date)  
        train_prc_correspondence, train_dw = self.get_control_stats(train_timeseries,period_start=train_start_date,period_end=train_end_date)
        if self.params.validated:
            validation_prc_correspondence, validation_dw = self.get_control_stats(train_timeseries,period_start=validation_start_date,period_end=validation_end_date)
        else:
            validation_prc_correspondence = []
            validation_dw = []
   
        # make & assess final control timeseries (i.e. use whole control period)
        timeseries = self._make_timeseries(data0,test_posa,control_posa,c,start_train_date=train_start_date,end_train_date=train_end_date)
        control_prc_correspondence, control_dw = self.get_control_stats(timeseries,period_start=train_start_date,period_end=train_end_date)
        
        # assign to match object
        self.X = X
        self.y = y
        self._coef = c
        self.df_coef = df_coef
        self.df_coef_optimal = df_coef_optimal
        self.control_posa_optimal = control_posa_optimal
        self.timeseries = timeseries
        # train period
        self.train_prc_correspondence = train_prc_correspondence
        self.train_dw = train_dw
        self.train_timeseries = train_timeseries
        # validation period
        self.validation_prc_correspondence = validation_prc_correspondence
        self.validation_dw = validation_dw
        # train + validation period
        self.prc_correspondence = control_prc_correspondence
        self.dw = control_dw
        
        if report:
            self.report()
            
        if plot:
            self.plot()
            
    def plot(self,**kwargs):
        self._plot_test_control_diff(**kwargs)
      
    def report(self,optimal=True):
        string = '- Test vs. Control % correspondence = {}% (train = {}%; val = {}%); DW = {} (train = {}; val = {})'
        prc = [self.prc_correspondence,self.train_prc_correspondence,self.validation_prc_correspondence]
        dw = [self.dw, self.train_dw, self.validation_dw]
        print(string.format(*[str(int(np.round(x*100))) if type(x) != list else '' for x in prc] + [str(np.round(x,1)) if type(x) != list else '' for x in dw]))
        if optimal:
            display(self.df_coef_optimal)
        else:
            display(self.df_coef)
    
    def _data_to_ols_vars(self,data,test_posa,control_posa):
        X = data[control_posa]
        y = data[test_posa].sum(axis=1).to_frame()
        return X,y
        
    def _preprocess_data(self,data,**kwargs):
        fillna = kwargs.get('fillna',0)
        baseline_start = kwargs.get('baseline_start',data.index.min())
        baseline_end = kwargs.get('baseline_end',data.index.max())
        data = (data / data.loc[baseline_start:baseline_end,:].mean(axis=0,skipna=True)).fillna(fillna)
        return data
        
    def _cnls_solve(self,X,y):       
        X = X.values
        y = y.values.reshape((-1,1)).ravel()
        c = nnls(X,y,maxiter=1000)[0]
        c = c/c.sum()
        return c
        
    def _make_timeseries(self,data,test_posa,control_posa,control_weights,**kwargs):
        # get test group mean in baseline

        # optional arguments:
        # 'start_train_date' = start date of period to fit model (only data >= this will be used)
        # 'end_train_date' = end date of period to fit model (only data <= this will be used)

        # get training period of data
        start_date = kwargs.get('start_train_date',data.index.min())
        end_date = kwargs.get('end_train_date',data.index.max())

        # compute scaled synthetic control (relative values)
        X,_ = self._data_to_ols_vars(data,test_posa,control_posa)
        X = self._preprocess_data(X,baseline_start=start_date,baseline_stop=end_date)
        sc = np.dot(X,control_weights.reshape(-1,1)).ravel()

        # scale synthetic control by test_baseline_mean
        # to offset back to absolute values
        test_baseline_mean = data.loc[start_date:end_date,test_posa].sum(axis=1).mean(axis=0)
        synthetic_control_ts = sc * test_baseline_mean    
        test_ts = data[test_posa].sum(axis=1)

        df_test_control = test_ts.to_frame().rename(columns={0:'test_timeseries'}).assign(control_timeseries=synthetic_control_ts)
        return df_test_control
    
    def _format_kpi_axis(self,*args):
        if len(args)==0:
            ax = plt.gca()
        else:
            ax = args[0]
            
        #ax.yaxis.set_major_locator(MaxNLocator(3))
        # ax.yaxis.set_major_locator(LinearLocator(numticks=3))
        # ticks_loc = ax.get_yticks().tolist()
        # ax.yaxis.set_major_locator(FixedLocator(ticks_loc))
            
        def format_label(label):
            f = '{:,.2f}'.format(label/1000)
            f = f.split('.')
            if int(f[1])>0:
                f[1] = ''.join([x for x in f[1] if x!='0'])
                f = '.'.join(f) + 'K'
            else:
                f = f[0] + 'K'
            return f
    
        if np.max(ax.get_yticks()) > 100:
            ylabels = format_labels(list(ax.get_yticks()))
            # ax.set_yticklabels(ylabels)
            ax.set_yticks(ax.get_yticks(),labels=ylabels)
        
    def _format_control_test_plot(self,ax_list,colors):
        [self._format_kpi_axis(x) for x in ax_list]
        ax_list[0].xaxis.set_major_locator(AutoLocator())
        ax_list[0].xaxis.set_minor_locator(AutoMinorLocator())
        ax_list[0].set_xticklabels('',minor=True)
        [x.tick_params(axis='y', colors=y) for x,y in zip(ax_list,colors)]
        [x.spines['top'].set_alpha(0) for x in ax_list]
        [[x.spines[y].set_alpha(0) for x in ax_list] for y in ['left','right']]
        for x in ax_list:
            squeeze_y_ax(x,0.35)
            
    def _plot_test_control_diff(self,**kwargs):
        figsize=kwargs.get('figsize',[8,5])
        
        plt.figure(figsize=figsize)
        ax1 = plt.subplot(2,2,1)
        ax2 = plt.subplot(2,2,3)
        ax3 = plt.subplot(2,4,7)
        axs = [ax1, ax2, ax3]
        
        data = self.timeseries.loc[:self.params.control_end_date,:]
        d = data[['control_timeseries','test_timeseries']].diff(axis=1)['test_timeseries'].rename('diff').to_frame()
        d = d.assign(positive=d['diff']>0)

        h = data.plot(ax=axs[1],color=[[0.4,0.4,1],[0.7,0.7,0.7]],legend=False)
        h.legend(fontsize='x-small',ncol=2,loc='lower center')
        d['diff'].plot(kind='bar',color=d.positive.map({False: [0.7,0.7,0.7], True: [0.4,0.4,1]}),ax=axs[0])
        
        axs[0].set_ylabel('Test - Control')
        axs[1].set_ylabel('KPI')

        xl1 = axs[1].get_xlim()
        xl2 = axs[0].get_xlim()
        
        # plot periods
        [axs[1].axvline(x,linestyle='--',color=[0.6,0.6,0.6],linewidth=2) for x in self.params.train_period]
        if self.params.validated:
            [axs[1].axvline(x,linestyle='--',color=[1,0.6,0.6],linewidth=2) for x in self.params.validation_period]
            
        axs[1].set_xlim([xl1[0]-1,xl1[1]+1])
        axs[0].set_xlim([xl2[0]-0.5,xl2[1]+0.5])
                
        axs[1].tick_params(axis='x', labelrotation = 90)

        axs[0].axhline(color=[0.7,0.7,0.7])
        [axs[0].spines[y].set_alpha(0) for y in ['top','bottom','right']]
        [axs[1].spines[y].set_alpha(0) for y in ['top','right']]
        axs[0].set_xticks([])
        axs[0].set_xlabel('')
        axs[1].set_xlabel('Dates')

        axs[1].yaxis.set_major_locator(AutoLocator())
        ticks_loc = axs[1].get_yticks().tolist()
        squeeze_y_ax(axs[1],0.35)
        axs[1].yaxis.set_ticks(ticks_loc)

#         axs[1].xaxis.set_major_locator(MultipleLocator(7))
#         axs[1].xaxis.set_ticklabels('',minor=True)
#         axs[1].xaxis.set_minor_locator(AutoMinorLocator())

#         tl = axs[1].xaxis.get_ticklabels(minor=False)
#         axs[1].xaxis.set_ticklabels([num2date(x.get_position()[0]).date() for x in tl])

#         myFmt = mdates.DateFormatter("%d %b '%y")
#         axs[1].xaxis.set_major_formatter(myFmt)

        yl = axs[0].get_yticks()
        max_val = np.max(np.abs(yl))
        axs[0].set_ylim([-max_val,max_val])
        axs[0].set_yticks(yl[1:-1])
        
        [self._format_kpi_axis(a) for a in axs]
        
        sns.kdeplot(d['diff'].values,fill=True,color=[0.4,0.4,1])
        plt.axvline(color=[0.7,0.7,0.7])
        xl = axs[2].get_xlim()
        max_val = np.max(np.abs(xl))
        axs[2].set_xlim([-max_val,max_val])
        [axs[2].spines[y].set_alpha(0) for y in ['left','top','right']]
        axs[2].set_yticks([])
        axs[2].set_ylabel('')
        axs[2].set_xlabel('Test - Control')
        
        plt.tight_layout()          
        plt.show()
        
    def plot_controls_on_test(self,**kwargs):
        #data = self.data.loc[:self.params.test_period[0]-pd.Timedelta(days=1),:]
        data = self.data.copy()
        test_posa = self.params.test_posa
        scale = kwargs.get('scale',False)
        if kwargs.get('optimal',True):
            control_posa = self.control_posa_optimal
        else:
            control_posa = self.params.control_posa
        figsize = kwargs.get('figsize',[10,3])
        lims = kwargs.get('ylims',[0.5,1.5])
        
        test = data[test_posa].sum(axis=1).rename('test').to_frame()
        controls = data[control_posa]
        dat = pd.concat((test,controls),axis=1) 
        dat.index = [pd.to_datetime(x).date() for x in dat.index]
        if scale:
            dat = self._preprocess_data(dat,baseline_end=self.params.test_period[0]-pd.Timedelta(days=1))
        
        dat.loc[self.params.test_period[0]:self.params.test_period[1],:] = np.nan
        cols = dat.columns
        test_agg_col = cols[0]
        control_regions = cols[1:]

        n_plots = len(control_posa)
        n_cols = 3
        n_rows = int(np.ceil(n_plots/n_cols))
        figsize[1] = figsize[1]*n_rows
        n_grid = n_rows + n_cols
        
        cols = ['#1f77b4','#ff7f0e']
        fig, axs = plt.subplots(n_rows,n_cols,figsize=figsize)
        axs = axs.flatten()
        for i,a in enumerate(axs):
            if i<n_plots:
                this_comparison = [control_regions[i],test_agg_col]
                if scale:
                    dat.loc[:,this_comparison].plot(ax=a)
                    a.set_ylim(lims)
                else:
                    twin_ax = a.twinx()
                    ax_list = [a,twin_ax]
                    l1 = dat.loc[:,this_comparison[0]].plot(ax=a,color=cols[0])
                    l2 = dat.loc[:,this_comparison[1]].plot(ax=twin_ax,color=cols[1])
                    a.legend(loc='upper center',fontsize='x-small')
                    twin_ax.legend(loc='lower center',fontsize='x-small')
                    self._format_control_test_plot(ax_list,cols)                           
                a.set_xlabel('')
            else:
                [a.spines[y].set_alpha(0) for y in ['left','top','right','bottom']]
                a.set_xticks([])
                a.set_yticks([])
            a.tick_params(axis='x', labelrotation = 90)

        plt.tight_layout()
        plt.show()
    
class Test:
    """
    Sub-class containing the causal impact test. NB this wraps around the R
    causal impact function and incorporates methods to port python variables to R format
    and back again to pass between the languages
    
    http://google.github.io/CausalImpact/CausalImpact.html
    ...
    
    
    Attributes
    ----------
    params : Params object
    data : DataFrame
        Contains data output by causal impact test
    model : R package
        Handle to Google's R Causal Impact package. NB python variables must be re-formatted
        before they can be passed to this function
    model_output : DataFrame
        Contains the timeseries used/returned by the causal impact test. These include the test
        posa timeseries, synthetic control timeseries, the point-wise (pw) difference between them
        and the cumulative difference between them. 95% CI for each timeseries are also included
    report : str
        Formatted text report output by the causal impact test describing the results and their
        implications
    results : DataFrame
        Contains the numerical outputs of the causal impact test for both the average and cumulative
        difference between test and control timeseries. By default we report cumulative values

    Methods
    -------
    run()
        Runs causal impact test
    print_results()
        Prints the results of the causal impact test, including formatted report of the
        implications
    """
    
    def __init__(self,data,params):
        self.data = data
        self.set_params(params)
        self._init_test()
        
    def set_params(self,params):
        defaults = {'nseasons':1,'season_duration':1,'report':True,'control_period':[],'test_period':[],'test_type':[]}
        params = params.__dict__
        if hasattr(self,'params')==False:
            self.params = {}
        for key in defaults.keys():
                self.params[key] = params.get(key,self.params.get(key,defaults[key]))
        
    def _init_test(self):
        self.model = importr('CausalImpact')
        
    def _format_tt_output(self,tt_output):
        if tt_output[1]<0.01:
            v = '.2e'
        else:
            v = '.2f'
        return 't = %.2f, p = %' + v
    
    def _prc_difference(self,a,b):
        return 100 * ((b-a)/a)


    def _mean_confidence_interval(self, data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se, sd = np.mean(a), sem(a), np.std(a)
        h = se * t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h, sd

        
    def run(self):
        data = self.data
        test_type = self.params['test_type']
        control_period = self.params['control_period']
        test_period = self.params['test_period']
        nseasons = self.params['nseasons']
        season_duration = self.params['season_duration']
        report = self.params['report']
        
        if test_type == 'causal impact':
            with localconverter(ro.default_converter + pandas2ri.converter):
                r_from_pd_df = ro.conversion.py2rpy(data.reset_index(drop=True))

            r_control_period = ro.IntVector([date_to_index(data.index,x)+1 for x in control_period])
            r_test_period = ro.IntVector([date_to_index(data.index,x)+1 for x in test_period])
            mdl_args = ro.ListVector({'nseasons':nseasons, 'season.duration':season_duration})

            o = self.model.CausalImpact(r_from_pd_df, r_control_period, r_test_period, mdl_args)
            ci_data = pd.DataFrame(data=np.array(o[0])[:,[0,2,3,4,8,9,10,11,12,13]],index=data.index,columns=['test','control_pred',
                                                                                            'control_pred_lower',
                                                                                            'control_pred_upper',
                                                                                            'control_pred_pw',
                                                                                            'control_pred_lower_pw',
                                                                                            'control_pred_upper_pw',
                                                                                            'control_pred_cumulative',
                                                                                            'control_pred_lower_cumulative',
                                                                                            'control_pred_upper_cumulative'])

            self.model_output = ci_data
            self._format_r_causal_impact_results(pd.DataFrame(o[1]))
            self.report = str(o[2])
            self._r_mdl_output = o
            if report:
                self.model.PrintSummary(o)
                self.model.PrintReport(o)
                
        elif test_type == 't-test':
            test_d = data.loc[test_period[0]:test_period[1],:]
            control_d = data.loc[control_period[0]:control_period[1],:]
            diffs = test_d[['control_timeseries','test_timeseries']].diff(axis=1).values[:,1]

            baseline_tt = ttest_rel(control_d['test_timeseries'],control_d['control_timeseries'])
            treatment_tt = ttest_rel(test_d['test_timeseries'],test_d['control_timeseries'])
            bl_treat_tt = ttest_ind(test_d['test_timeseries']-test_d['control_timeseries'],control_d['test_timeseries']-control_d['control_timeseries'])

            test_diff_abs, test_ci_abs_l, test_ci_abs_u, test_sd_abs = self._mean_confidence_interval(diffs)
            test_diff_rel, test_ci_rel_l, test_ci_rel_u = [self._prc_difference(test_d['control_timeseries'].mean(),test_d['control_timeseries'].mean()+x)\
                                                           for x in [test_diff_abs,test_ci_abs_l,test_ci_abs_u]]

            test_cumulative = test_d.sum(axis=0)
            cumul_test_diff_abs,\
            cumul_test_ci_abs_l,\
            cumul_test_ci_abs_u = [test_cumulative[['control_timeseries','test_timeseries']].diff().values[1]*x \
                                    for x in [1]+[x/test_diff_abs for x in [test_ci_abs_l,test_ci_abs_u]]]

            v_cumul = [test_cumulative['test_timeseries'],np.nan,np.nan,np.nan,\
                       test_cumulative['control_timeseries'],np.nan,np.nan,np.nan,\
                       cumul_test_diff_abs, cumul_test_ci_abs_l, cumul_test_ci_abs_u, np.nan, \
                       test_diff_rel, test_ci_rel_l, test_ci_rel_u, \
                       np.nan,np.nan,np.nan]

            avg = {**dict(zip(['Actual','actual_ci_lower','actual_ci_upper','Actual (s.d.)'],self._mean_confidence_interval(test_d['test_timeseries']))), \
            **dict(zip(['Prediction','prediction_ci_lower','prediction_ci_upper','Prediction (s.d.)'],self._mean_confidence_interval(test_d['control_timeseries']))), \
            **dict(zip(['Absolute Effect','abs_effect_ci_lower','abs_effect_ci_upper','Absolute Effect (s.d.)'],[test_diff_abs, test_ci_abs_l, test_ci_abs_u, test_sd_abs])), \
            **dict(zip(['Relative Effect','rel_effect_ci_lower','rel_effect_ci_upper'],[test_diff_rel, test_ci_rel_l, test_ci_rel_u])), \
            **dict(zip(['t-stat','p','alpha'],list(treatment_tt) + [0.95]))}

            agg = dict(zip(list(avg.keys()),v_cumul))

            results = pd.DataFrame(dict(zip(['Average','Cumulative'],[avg,agg]))).T
            model_output = results.copy()

            results['Prediction 95% CI'] = cols_to_listcol(results,['prediction_ci_lower','prediction_ci_upper'])
            results['Absolute Effect 95% CI'] = cols_to_listcol(results,['abs_effect_ci_lower','abs_effect_ci_upper'])
            results['Relative Effect 95% CI'] = cols_to_listcol(results,['rel_effect_ci_lower','rel_effect_ci_upper'])

            column_names = results.columns

            results = results.drop(columns=[x for x in column_names if 'ci' in x])
            col_order = ['Actual','Prediction','Prediction (s.d.)','Prediction 95% CI',
                         'Absolute Effect','Absolute Effect (s.d.)','Absolute Effect 95% CI',
                        'Relative Effect','Relative Effect 95% CI',
                         't-stat','alpha','p']
            results = results[col_order]
            
            self.results = results
            self.model_output = model_output
            
            if report:
                print('Test vs. Control (treatment):       ' + self._format_tt_output(treatment_tt) % treatment_tt)
                print('Test vs. Control (baseline):        ' + self._format_tt_output(baseline_tt) % baseline_tt)
                print('Treatment delta vs. Baseline delta: ' + self._format_tt_output(bl_treat_tt) % bl_treat_tt)
                display(self.results)
                
            
    def _format_r_causal_impact_results(self,results):
        results = results.T.assign(Analysis=['Average','Cumulative']).set_index('Analysis',drop=True)
        column_names = ['Actual','Prediction','prediction_ci_lower','prediction_ci_upper','Prediction (s.d.)',
                        'Absolute Effect','abs_effect_ci_lower','abs_effect_ci_upper','Absolute Effect (s.d.)',
                        'Relative Effect','rel_effect_ci_lower','rel_effect_ci_upper','Relative Effect (s.d.)',
                        'alpha','p']

        results = results.rename(columns=dict(zip(results.columns,column_names)))
        relative_cols = [x for x in column_names if ('Relative' in x) or ('rel_' in x)]
        results[relative_cols] = results[relative_cols].applymap(lambda x: x*100)

        results['Prediction 95% CI'] = cols_to_listcol(results,['prediction_ci_lower','prediction_ci_upper'])
        results['Absolute Effect 95% CI'] = cols_to_listcol(results,['abs_effect_ci_lower','abs_effect_ci_upper'])
        results['Relative Effect 95% CI'] = cols_to_listcol(results,['rel_effect_ci_lower','rel_effect_ci_upper'])

        results = results.drop(columns=[x for x in column_names if 'ci' in x])
        col_order = ['Actual','Prediction','Prediction (s.d.)','Prediction 95% CI',
                     'Absolute Effect','Absolute Effect (s.d.)','Absolute Effect 95% CI',
                    'Relative Effect','Relative Effect (s.d.)','Relative Effect 95% CI',
                     'alpha','p']
        results = results[col_order]
        results = results.applymap(lambda x: np.round(x,2))
        self.results = results
        
    def print_results(self):
        if self.params['test_type']=='causal_impact':
            if all(hasattr(self,attr) for attr in ['_r_mdl_output']):
                self.model.PrintSummary(self._r_mdl_output)
                self.model.PrintReport(self._r_mdl_output)
        else:
            try:
                self.model.PrintSummary(self._r_mdl_output)
                self.model.PrintReport(self._r_mdl_output)
            except:
                display(self.results)
    
    
class Plot:
    """
    Sub-class used containing all causal impact plotting infrastructure
    ...
    
    
    Attributes
    ----------
    params : Params object
    data : DataFrame
        Contains data output by causal impact test
    fig: figure handle
        Handles of causal impact test figure
    ax: list of axes handles
        Handles of all axes in causal impact test figure
    test_period_handles: list of lists, each containing line handles
        Handles for the visualisation of the test period in all axes
    
    
    Methods
    -------
    make_ci_summary_plots()
        Makes summary plots for causal impact test. See method for input/output 
        definitions
    """
    
    def __init__(self,data,params,timeseries):
        self.data = data
        self.params = params
        self.timeseries = timeseries
    
    def _plot_series_ci(self,data, **kwargs):
        x = kwargs.get('x','index')
        linestyle = kwargs.get('linestyle','-')
        linecolor = kwargs.get('linecolor','k')
        facecolor = kwargs.get('facecolor','grey')
        interpolate = kwargs.get('interpolate',True)
        alpha = kwargs.get('alpha',0.25)
        ax = kwargs.get('ax',plt.gca())
        y = kwargs.get('y',data.columns[0])
        lower = kwargs.get('lower',data.columns[1])
        upper = kwargs.get('upper',data.columns[2])

        if x=='index':
            x = data.index
        else:
            x = data[x]

        data[y].plot(ax=ax,linestyle=linestyle,color=linecolor)
        ax.fill_between(x,
            data[lower],
            data[upper],
            facecolor=facecolor,
            interpolate=interpolate,
            alpha=alpha
        )
        return ax

    def _plot_test_period(self,test_period,**kwargs):
        ax = kwargs.get('ax',plt.gca())
        linestyle = kwargs.get('linestyle','--')
        color = kwargs.get('color',[0.6,0.6,0.6])
        linewidth = 2
        h = [ax.axvline(x,linestyle=linestyle,color=color,linewidth=linewidth) for x in test_period]
        return h

    def _format_date_axis(self,ax):
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        first_of_months = [x for x in ax.get_xticks() if num2date(x).day in [1,15]]
        ax.set_xticks(first_of_months)
        myFmt = mdates.DateFormatter('%b %d')
        ax.xaxis.set_major_formatter(myFmt)
        plt.autoscale(enable=True, axis='x', tight=True)
        ax.xaxis.set_tick_params(labelsize='x-large')
        ax.yaxis.set_tick_params(labelsize='x-large')
        ax.xaxis.label.set_size('x-large')
        ax.yaxis.label.set_size('x-large')

    def _format_kpi_axis(self,*args):
        if len(args)==0:
            ax = plt.gca()
        else:
            ax = args[0]
            
        def format_label(label):
            f = '{:,.2f}'.format(label/1000)
            f = f.split('.')
            if int(f[1])>0:
                f[1] = ''.join([x for x in f[1] if x!='0'])
                f = '.'.join(f) + 'K'
            else:
                f = f[0] + 'K'
            return f
    
        if np.max(ax.get_yticks()) > 100:
            ylabels = format_labels(list(ax.get_yticks()))
            ax.set_yticks(ax.get_yticks(),labels=ylabels)
            # ax.set_yticklabels(ylabels)

    def make_ci_summary_plots(self,**kwargs):
        """
        Args
        ----
          figsize: list of ints
              [X,Y] pixel size of figure
          plot_style: list of str
              can contain any combination of 'kpi', 'point-wise' and 'cumulative'
          format_x: bool
              flags whether to reformat dates to just have 1st and 15th of each month
          format_y: bool
              flags whether to reformat 1000s to K in y-axis
          face_color: str or list of ints
              defines the shading colour of the 95% CI band of the control posa timeseries
          line_color: str or list of ints
              defines the line of the control posa timeseries
              
        Returns
        ---
            fig
                figure handle
            ax
                axes handles
            test_period_handles
                handle to test_period visualisation lines
        """
        
        data = self.data
        test_period = self.params.test_period
        
        param_dict = self.params.__dict__
        figsize = kwargs.get('figsize',param_dict.get('figsize'))
        plot_style = kwargs.get('plot_style',param_dict.get('plot_style'))
        format_x = kwargs.get('format_x',param_dict.get('format_x'))
        format_y = kwargs.get('format_y',param_dict.get('format_y'))
        fc = kwargs.get('face_color',param_dict.get('face_color'))
        lc = kwargs.get('line_color',param_dict.get('line_color'))

        fig,ax = plt.subplots(len(plot_style),1, figsize=figsize)


        if isinstance(ax,np.ndarray)==False:
            ax = np.array(ax).reshape(1,)
        data.index = [pd.to_datetime(x) for x in data.index]
        ax_idx = 0
        if 'kpi' in plot_style:
            self._plot_series_ci(data,y='control_pred',lower='control_pred_lower',upper='control_pred_upper', linestyle='--', facecolor=fc, linecolor=lc, ax=ax[ax_idx])
            data['test'].plot(ax=ax[ax_idx],color=[1,0,0],linewidth=2)
            ax[ax_idx].set_ylabel('KPI')
            ax_idx+=1
        if 'point-wise' in plot_style:
            self._plot_series_ci(data,y='control_pred_pw',lower='control_pred_lower_pw',upper='control_pred_upper_pw', linestyle='--', facecolor=fc, linecolor=lc, ax=ax[ax_idx])
            ax[ax_idx].axhline(0,color=[0.8,0.8,0.8],linestyle='-')
            ax[ax_idx].set_ylabel('Point-wise difference')
            ax_idx+=1
        if 'cumulative' in plot_style:
            self._plot_series_ci(data,y='control_pred_cumulative',lower='control_pred_lower_cumulative',upper='control_pred_upper_cumulative', facecolor=fc, linecolor=lc, linestyle='--', ax=ax[ax_idx])
            ax[ax_idx].axhline(0,color=[0.8,0.8,0.8],linestyle='-')
            ax[ax_idx].set_ylabel('Cumulative change')

        test_period_handles = [self._plot_test_period(test_period,ax=a) for a in ax]
        [a.set_xlabel('Dates') for a in ax]
        [a.grid(True, linestyle='-') for a in ax]
        # if format_x:
        #     [self._format_date_axis(a) for a in ax]
        lims = [data.index.min(),data.index.max()]
        [a.set_xlim(lims) for a in ax]

        plt.tight_layout()
        if format_y:
            [self._format_kpi_axis(a) for a in ax]
            
        self.fig = fig
        self.ax = ax
        self.test_period_handles = test_period_handles
        plt.show()
        return fig, ax
    
    def make_tt_summary_plots(self, **kwargs):  
        data = self.timeseries
        test_period = self.params.test_period
        train_period = self.params.train_period
        
        param_dict = self.params.__dict__
        figsize = kwargs.get('figsize',param_dict.get('figsize'))
        plot_style = kwargs.get('plot_style',param_dict.get('plot_style'))
        format_x = kwargs.get('format_x',param_dict.get('format_x'))
        format_y = kwargs.get('format_y',param_dict.get('format_y'))
        fc = kwargs.get('face_color',param_dict.get('face_color'))
        lc = kwargs.get('line_color',param_dict.get('line_color'))      
        
        fig = plt.figure(figsize=figsize)
        ax1 = plt.subplot(2,2,1)
        ax2 = plt.subplot(3,2,4)
        ax3 = plt.subplot(2,2,3)
        axs = [ax1, ax2, ax3]

        d = data[['control_timeseries','test_timeseries']].diff(axis=1)['test_timeseries'].rename('diff').to_frame()
        test_d = data.loc[test_period[0]:test_period[1],:]
        control_d = data.loc[train_period[0]:train_period[1],:]
        d = d.assign(positive=d['diff']>0)

        # point-wise
        d['diff'].plot(kind='bar',color=d.positive.map({False: [0.7,0.7,0.7], True: [1,0.6,0.6]}),ax=axs[0])
        axs[0].axhline(color=[0.7,0.7,0.7])
        axs[0].set_xticks([])
        axs[0].get_xaxis().set_visible(False)

        # distributions
        sns.kdeplot(control_d.assign(diff=control_d['test_timeseries']-control_d['control_timeseries'])['diff'].values,fill=True,color=[0.6,0.6,0.6],ax=axs[1])
        sns.kdeplot(test_d.assign(diff=test_d['test_timeseries']-test_d['control_timeseries'])['diff'].values,fill=True,color=[1,0.6,0.6],ax=axs[1])
        axs[1].axvline(color=[0.7,0.7,0.7])
        axs[1].set_xlim(np.asarray([-1,1]) * np.max([np.abs(x) for x in axs[1].get_xlim()]))
        [axs[1].spines[y].set_alpha(0) for y in ['left','top','right']]
        axs[1].set_yticks([])
        axs[1].set_ylabel('')
        axs[1].set_xlabel('Test - Control')

        # cumulative
        cumsum = d['diff'].cumsum().to_frame()
        cumsum = cumsum.assign(positive=cumsum['diff']>0)
        cumsum['diff'].plot(color=[0.7,0.7,0.7],ax=axs[2])
        cumsum.loc[cumsum['positive']==True,'diff'].plot(color=[1,0.6,0.6],ax=axs[2])
        axs[2].axhline(color=[0.7,0.7,0.7])
        axs[2].set_xticks(axs[2].get_xticks(), axs[2].get_xticklabels(), rotation=45, ha='right')

        test_period_handles = self._plot_test_period(test_period,ax=axs[2])
        offset = [-0.5,0.5]
        [axs[0].axvline(x=np.argmax([x==p for x in d.index])+i,linestyle='--',color=[0.6,0.6,0.6],linewidth=2) for p,i in zip(test_period,offset)]
        
        for i,ax in enumerate(axs):
            if i != 1:
                if np.max(ax.get_yticks()) > 100:
                    ylabels = format_labels(list(ax.get_yticks()))
                    ax.set_yticks(ax.get_yticks(),labels=ylabels)
            else:
                if np.max(ax.get_xticks()) > 100:
                    xlabels = format_labels(list(ax.get_xticks()))
                    ax.set_xticks(ax.get_xticks(),labels=xlabels)
        
        plt.tight_layout()          
        plt.show()
        return fig,axs
        

##### MAIN CLASS
class CausalImpact(Params,Match,Test,Plot):
    """
    User-facing master class used to package synthetic control generation, causal impact test and plotting
    
    Synthetic control generation:
        Uses EG's EGGX R package's methodology (constrained, non-negative least squares regression) to
        generate a single synthetic control timeseries from a set of potential control posa timeseries
        by combining them as a weighted sum, where the weights are non-negative and sum to 1
    Causal impact test: 
        Uses Google's R Causal Impact package (http://google.github.io/CausalImpact/CausalImpact.html)
        to calculate the difference between test and control posa in the test period, accounting for
        temporal fluctuations in the input data
    Plotting:
        Plots the data used for the Causal Impact test in various different ways to allow the user to
        confirm/report results
    ...


    Attributes
    ----------
    params : Params object
        Object containing all the parameters for matching, testing and plotting
    match : Match object
        Object used to find optimal control posa and calculate appropriate coefficient weightings
        to use to combine them into a single control posa timeseries. This uses constrainted, non-
        negative least squares regression to find regression coefficients that allow control posa
        to be combined into a single timeseries that best reflects the test posa timeseries.
        Coefficients must sum to 1. See documentation above for relevant attributes and methods
    test : Test object
        Object used to run the causal impact test using the test and control timeseries calculated
        in the match step above. This fits confidence intervals to the control posa timeseries and
        returns a report detailing the results of the test. See documentation above for relevant
        attributes and methods
    plot : Plot object
        Object used to contain all plotting infrastructure used to visualise the output of the
        causal impact test. See documentation above for relevant attributes and methods
    test_posa : list
        List of test posa. This has been standardised and cleaned (i.e. de-duped)
    control_posa_optimal : list
        List of optimal control posa as found by matching algorithm. This has been standardised
        and will be subject to the list of excluded posa (exclude) and any foced_control_posa
    df_coef_optimal : DataFrame
        DataFrame containing the optimal control posa along with their weighting coefficient used
        when constructing the synthetic control
    timeseries : DataFrame
        DataFrame containing the test (sum across test posa) and synthetic control timeseries
        (weighted sum of optimal control posa)
    test_results : DataFrame
        Contains all results from the causal impact test. These are defined for both the average
        and cumulative differences between test and control. Reports tend to use the cumulative
        difference
    model_output : DataFrame
        Contains the timeseries used/returned by the causal impact test:
        - test : test posa timeseries (sum across test posa)
        - control_pred : control posa timeseries (weighted sum across control posa)
        - control_pred_lower : lower bound of 95% CI of above
        - control_pred_upper : upper bound of 95% CI of above
        - control_pred_pw : (time)point-wise difference between test and control timeseries
        - control_pred_lower_pw : lower bound of 95% CI of above
        - control_pred_upper_pw : upper bound of 95% CI of above
        - control_pred_cumulative : cumulative difference between test and control timeseries
        - control_pred_lower_cumulative : lower bound of 95% CI of above
        - control_pred_upper_cumulative : upper bound of 95% CI of above


    Methods
    -------
    run()
        Runs the full match and test routine, first finding best control posa for the test posa
        timeseries, creating a synthetic control, then running the causal impact test compating
        test and control timeseries
    match_posa()
        Posa matching: finds optimal combination of control timeseries that best correlates with
        test timeseries in the baseline/training period. This will later be used as the control
        in the causalimpact test 
    run_test()
        Causal impact test: runs the causal impact test comparing the test timeseries to the 
        synthetic control timeseries generated by match_posa() method
    print_match(optimal=True)
        Outputs the % correspondence between the test and synthetic control timeseries (just the
        correlation) and the optimal control posa along with their weighting coefficients. the
        "optimal" flag dictates whether just posa with non-zero coefficients are reported 
        (default=True)
    plot_results(plot=True,plot_style=['kpi','point-wise','cumulative'])
        Plots the results of the causal impact test (comparing test and control). 3 possible
        plots will be output: (1) kpi (this is the overlay of the test timeseries on the
        synthetic control timeseries +/- 95% CI); (2) point-wise (this is the difference between
        test and control at each timepoint +/- 95% CI); (3) cumulative (the cumulative difference
        between test and control during test period. Any combination of these plots can be output
    print_results()
        Prints out a formatted version of the causal impact test result values with a verbose
        report of the implications
    summary(optimal=True)
        Calls the 3 main output methods: print_match(), plot_results() and print_results() to
        give the user all possible info from the matching and test procedure
    set_params(**kwargs)
        Reset any parameters for the matching, testing and plotting process by using key value pairs.
        This will force a reset of the object so any matching and testing will have to be re-done
    """
    
    
    # period assumptions:
    # - baseline period = period before test period. Assumption is that all of this 
    #                     is used to do test/control matching, unless a subset of time is defined by:
    # ---- train period = period within the baseline on which test/control matching 
    #                     occurs (nb if not defined, assume whole baseline is used)
    # - test period = promo period to where test posa compared to control posa
    # - post period = any time after test period (e.g. to assess pull-forward)
    
    def __init__(self,data,baseline_period,test_period,test_posa,control_posa,**kwargs):
        data['dates'] = data['dates'].apply(lambda x: pd.to_datetime(x).date())
        self._reset(data,baseline_period,test_period,test_posa,control_posa,**kwargs)
    
    def _reset(self,data,baseline_period,test_period,test_posa,control_posa,**kwargs):
        self.params = Params(data,baseline_period,test_period,test_posa,control_posa,**kwargs)
        self.match = None
        self.test = None
        self.plot = None
        
        # initialise empty attributes
        self.test_posa = None
        self.control_posa_optimal = None
        self.df_coef_optimal = None
        self.timeseries = None
        self.test_results = None
        self.model_output = None
        
        self._data0 = data
        self._process_input_data()
        
    def _process_input_data(self):
        self.data = self._data0.copy()
        self.data = self.data[['dates','posa','kpi']]
        self.data = self.data.assign(dates=self.data['dates'].apply(lambda x: pd.to_datetime(x).date()))
        self.data = self.data.applymap(self.params._standardise_posa)
        self._filter_data() 
        self._pivot_data()
             
    def _filter_data(self):
        test_posa = self.params.test_posa
        control_posa = self.params.control_posa
        period_start = np.min(self.params.baseline_period)
        period_end = np.max(self.params.post_period)
        flag = (self.data['posa'].isin(test_posa + control_posa)) & (self.data['dates']>=period_start) & (self.data['dates']<=period_end)
        self.data = self.data.loc[flag,:]
    
    def _pivot_data(self):
        self.data = self.data.fillna('|')
        # pivot and replace missing data with 0
        self.data = self.data.pivot_table(values='kpi',index='dates',columns='posa')
        self.data = self.data.fillna(0)
        # reinsert pre-pivot nans where identifier exists
        self.data[self.data=='|'] = np.nan
        
    def run(self):
        self.match_posa()
        self.run_test()
        self.plot_results(plot=self.params.plot)
        
    def match_posa(self):
        self.match = Match(self.data,self.params)
        self.match.fit()
        self.test_posa = self.params.test_posa
        self.control_posa_optimal = self.match.control_posa_optimal
        self.df_coef_optimal = self.match.df_coef_optimal
        self.timeseries = self.match.timeseries
        # re-initialise test if new match called
        self.test = Test(self.match.timeseries,self.params)   
        
    def run_test(self):
        if self.match!=None:
            self.test = Test(self.match.timeseries,self.params)
            self.test.run()
            self.test_results = self.test.results
            self.model_output = self.test.model_output
            self.test_results = self.test_results.assign(control_corr=self.match.prc_correspondence)
        else:
            print('- You must create a synthetic control via the .match_posa() method before running a test')
                
    def print_match(self,optimal=True):
        if self.match!=None:
            self.match.report(optimal=optimal)
        else:
            print('- You must match test and control posa before printing the match')
    
    def plot_results(self,plot=True,**kwargs):
        self.plot = Plot(self.test.model_output,self.params,self.timeseries)
        if plot:
            if self.params.test_type == 'causal impact':
                fig, ax = self.plot.make_ci_summary_plots(**kwargs)
            else:
                fig, ax = self.plot.make_tt_summary_plots(**kwargs)
            return fig, ax
            
    def print_results(self):
        if hasattr(self.test,'results'):
            self.test.print_results()
        else:
            print('- You must run a test before printing results')
        
    def summary(self,**kwargs):
        if (self.match!=None) and (self.test!=None):
            optimal = kwargs.get('optimal',True)
            self.print_match(optimal=optimal)
            self.plot_results()
            self.print_results()
        else:
            print('- You must match test and control posa, then run a test, before printing a summary')
            
    def set_params(self,**kwargs):
        """
        Resets object parameters once it has been instantiated. Note that this will force a reinitialisation
        of the object (i.e. any match and test data will be reset to None)
        
        Potential parameters:
        ---------------------
        baseline_period : list of pandas timestamps
            2 timestamps defining the beginning and end date of the baseline period respectively.
            If the optional inputs train_period and control_period are not defined, then the
            baseline period will be used as the train_period (to fit the synthetic control) and the 
            control period (for the causal impact test)
        test_period : list of pandas timestamps
            2 timestamps defining the beginning and end of the campaign test period respectively
        train_period : list of pandas timestamps
            2 timestamps defininf the beginning and end of the period used to generate the synthetic
            control timeseries (NB this MUST NOT include any of the test period). If not set, then
            this defauls to the baseline_period
        control_period : list of pandas timestamps
            2 timestamps defining the beginning and end of the control period used for the causal
            impact test. If not set, then this defaults to the baseline period
        post_period : list of pandas timestamps
            2 timestamps defining the beginning and end date of the post-test period respectively.
            If not set, then this defaults to the next consecutive date after the end of the test
            period until the maximum date in the data
        forced_control_posa : list of str
            Forces the list of posa that will be considered by the matching procedure
        exclude : list of str
            List of control posa to exclude from any analysis
        nseasons : int
            Number of timestamps within a seasonal trend, e.g. if timestamps are days then for a
            weekly trend set nseasons = 7 and season_duration = 1
        season_duration : int
            how long each element (nseason) of a seasonal trend lasts. So if timestamps are days
            and the seasonal trend is defined across days, then set the season_duration = 1
        plot : bool
            Flag dictating whether to plot causal impact test result outputs
        report : bool
            Flag dictating whether to print the results of the matching and testing phases
        figsize : list of int
            [X,Y] pixel dimensions of the causal impact test figure
        plot_style : list of str
            Any combination of ['kpi','point-wise','cumulative'] which correspond to the 3 styles
            of plot output by the causal impact test. 'kpi' = the overlay of the test and synthetic
            control posa timeseries (+/- 95% CI), 'point-wise' = (time)point-wise differences between
            test and control timeseries in the test period, 'cumulative' = cumulative difference
            between the test and control timeseries in the test period
        format_x : bool
            Flag dictating whether to re-format the x-axis in causal impact test plots so as to 
            only include the 1st and 15th of each month
        format_y : bool
            Flag dictating whether to re-format the y-axis in causal impact test plots so that all
            1000 --> K (e.g. 150,000 --> 150K)
        face_color : str or list of float
            Defines the color of 95% CI shading in all plots
        line_color : str or list of float
            Defines the color of the synthetic timeseries line in all plots
        """
        
        replaced = 0
        for key in kwargs.keys():
            if hasattr(self.params,key):
                replaced+=1
                self.params.__dict__[key] = kwargs[key]
        if replaced>0:
            self._reset(self._data0,
                        self.params.baseline_period,
                        self.params.test_period,
                        self.params.test_posa,
                        self.params.control_posa,
                        control_period=self.params.control_period,
                        train_period=self.params.train_period,
                        validation_period=self.params.validation_period,
                        post_period=self.params.post_period,
                        exclude=self.params.exclude,
                        forced_control_posa=self.params.forced_control_posa,
                        nseasons=self.params.nseasons,
                        season_duration=self.params.season_duration,
                        plot=self.params.plot,
                        report=self.params.report,
                        figsize=self.params.figsize,
                        plot_style=self.params.plot_style,
                        format_x=self.params.format_x,
                        format_y=self.params.format_y,
                        face_color=self.params.face_color,
                        line_color=self.params.line_color,
                        test_type=self.params.test_type)
        
