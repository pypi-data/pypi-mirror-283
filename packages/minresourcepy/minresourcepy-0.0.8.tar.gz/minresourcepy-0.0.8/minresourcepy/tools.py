# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Import libraries
import pandas as pd
import numpy as np
import math
import transforms3d as t3d
import plotly.express as px
import pandas.io.formats.format as fmt
import matplotlib.pyplot as plt
import minresourcepy.auxiliaries as ax

def tongrade(df, begin, end, step, variable, acc):
    """
    TonXGrade chart lists creation function
    Params:
    :param df: dataset to be used (it can be a block model, drill holes, etc)
    :type df: DataFrame
    :param begin: Lower cut-off grade desired
    :type begin: float
    :param end: Upper cut-off grade desired
    :type end: float
    :param step: Cut-off increment
    :type step: float
    :param variable: Grade variable in the dataset (e.g. AU_fin, CU...)
    :type variable: string
    :param acc: Variable to be used to weight the grade (e.g. tonnage or volume)
    :type acc: string
    :return: The function will return four lists with the values accumulated by each cut-off, being these the cut-off, grade, tonnage, and proportion
    :rtype: list
    """
    cutoff = np.arange(begin, end, step)
    df['gacc'] = df[variable] * df[acc]
    grade = []
    ton = []
    prop = []

    for c in cutoff:
        df_ = df.loc[df[variable] >= c]
        if df_.empty:
            grade.append(np.nan)
            ton.append(0)
            prop.append(ton[len(ton) - 1])
        else:
            grade.append(df_['gacc'].sum() / df_[acc].sum())
            ton.append(df_[acc].sum())
            if len(prop) == 0:
                prop.append(1)
            else:
                prop.append(ton[len(ton) - 1] / ton[0])

    return cutoff, grade, ton, prop


def xyzrotate(df, xcol, ycol, zcol, xori, yori, zori, angle, rot):
    """
    Rotate/unrotate coordinates function
    Params:
    :param df: dataset to be used (it can be a block model, drill holes, etc)
    :type df: DataFrame
    :param xcol: name of the X coordinates column (e.g. 'XC')
    :type xcol: string
    :param ycol: name of the Y coordinates column (e.g. 'YC')
    :type ycol: string
    :param zcol: name of the Z coordinates column (e.g. 'ZC')
    :type zcol: string
    :param xori: X origin coordinate
    :type xori: float
    :param yori: Y origin coordinate
    :type yori: float
    :param zori: Z origin coordinate
    :type zori: float
    :param angle: rotation agle
    :type angle: float
    :param rot: method to be used (0: generate the unrotated coordinates from rotated file; 1: generate the rotated coordinates from unrotated file)
    :type rot: int
    :return: return the updated dataframe
    :rtype: DataFrame
    """

    if rot == 1:
        mat = t3d.euler.euler2mat(ai=np.radians(angle), aj=0, ak=0, axes='szxz')
        rotxyz = np.dot(np.array(df[[xcol, ycol, zcol]]), mat)
        rotxyz[:, 0] += xori
        rotxyz[:, 1] += yori
        rotxyz[:, 2] += zori

        df['XROT'] = rotxyz[:, 0]
        df['YROT'] = rotxyz[:, 1]
        df['ZROT'] = rotxyz[:, 2]

    if rot == 0:
        mat = t3d.euler.euler2mat(ai=np.radians(angle * (-1)), aj=0, ak=0, axes='szxz')
        rotxyz = df[[xcol, ycol, zcol]].copy()
        rotxyz.loc[:, xcol] -= xori
        rotxyz.loc[:, ycol] -= yori
        rotxyz.loc[:, zcol] -= zori

        new_xyz = np.dot(rotxyz, mat)
        df['XUROT'] = new_xyz[:, 0]
        df['YUROT'] = new_xyz[:, 1]
        df['ZUROT'] = new_xyz[:, 2]

    return df


def pplotp(df, variable, log=True, xunit='g/t', weight=''):
    """
    Generate dynamic probability plots to assist with the outlier definition.
    :param df: dataset to be used (drill hole or samples file)
    :type df: DataFrame
    :param variable: Grade variable in the dataset (e.g. AU_fin, CU...)
    :type variable: String
    :param log: True: X axis will be displayed in lognormal; False: X axis will be displayed as it is
    :type log: Text
    :param xunit: Unit of the variable to be displayed (e.g. g/t, %, ppm...)
    :type xunit: String
    :param weight: Weight variable for the probability plot
    :type weight: <Optional> String
    """
    if weight:
        df1 = df[[variable, weight]].copy()
        df1.dropna(subset=variable, inplace=True)
        df1.sort_values(by=variable, inplace=True)
        df1[weight] = 1
        dfuw = ax.weights_cdf(df1, weight)
        dfuw['Type'] = 'Raw'

        df2 = df[[variable, weight]].copy()
        df2.dropna(subset=variable, inplace=True)
        df2.sort_values(by=variable, inplace=True)
        dfw = ax.weights_cdf(df2, weight)
        dfw['Type'] = 'Weighted'

        dfmerged = pd.concat([dfuw, dfw])

        fig = px.ecdf(dfmerged, x=variable, y=weight, markers=True, lines=False, facet_col='Type',
                      log_x=log, symbol_sequence=['cross-thin'],
                      labels={variable: variable + ' (' + xunit + ')'})
        fig.update_traces(marker=dict(size=5, line=dict(width=1, color='green')))
        fig.update_layout(plot_bgcolor='white', width=1000, height=500)
        fig.update_layout(yaxis={"title": "Probability"})
        fig.update_layout(title='<b>' + variable + ' Probability Plot</b>', title_x=0.5, font_color='black')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            minor=dict(ticks="inside", ticklen=3, showgrid=True),
            tickmode='linear')
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey')
        fig.show()

    else:
        fig = px.ecdf(df, x=variable, markers=True, lines=False,
                      log_x=log, symbol_sequence=['cross-thin'],
                      labels={variable: variable + ' (' + xunit + ')'})
        fig.update_traces(marker=dict(size=5, line=dict(width=1, color='green')))
        fig.update_layout(plot_bgcolor='white', width=600, height=500)
        fig.update_layout(yaxis={"title": "Probability"})
        fig.update_layout(title='<b>' + variable + ' Probability Plot</b>', title_x=0.5, font_color='black')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            minor=dict(ticks="inside", ticklen=3, showgrid=True),
            tickmode='linear')
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey')
        fig.show()


def describew(df, weight, var=None, percentiles=None, include=None, exclude=None, missing=False):
    """
    Generate the same output of .describe(), but considering a weight variable. It was designed originally to deal
    with drill holes and samples, on the exploratory data analysis procedures.
    :param df: dataset to be used (it can be a block model, drill holes, etc)
    :type df: DataFrame
    :param weight: wight variable to be used for the statistics
    :type weight: float
    :param var: optional field to be used to specify the variables that you want the statistics. If not specified,
    all numeric variables will be in the result. E.g. ['au_ppm', 'cu_ppm']
    :type var: float
    :param percentiles: optional field to be used to specify the quantiles that you want the statistics. If not
    specified, Q25, Q50, and Q75 will be in the result.  E.g. [0.10, 0.20, 0.90]
    :type percentiles: list
    :param missing: optional field to be used when the user wants the missing data for each variable
    :type missing: True
    :return: return the statistic table weighted by a variable
    :rtype: table
    """
    Variables, Count, Nanno, WMean, STD, variances, Minimum, Maximum, = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )

    exclude = [] if exclude is None else exclude
    if weight in df.columns:
        w = df[weight]
        if weight not in exclude:
            exclude.append(weight)
    else:
        w = weight

    if var is None:
        var = list(df.select_dtypes(include='number').columns)
        var.remove(weight)

    if percentiles is None:
        percentiles = [0.25, 0.5, 0.75]
    percentiles = dict(zip(fmt.format_percentiles(percentiles), percentiles))
    Q = {p: [] for p in percentiles}

    for i, v in enumerate(var):
        # Filtering out NaN
        Nanno.append(df[v].isna().sum())
        df_ = pd.DataFrame(list(zip(w, df[v])), columns=[weight, v])
        df_.dropna(inplace=True)

        # Count, weighted mean, std, minimum and maximum determination
        Variables.append(var[i])
        Count.append(len(df_[v]))
        wavrg = np.average(df_[v], weights=df_[weight])
        WMean.append(wavrg)
        Minimum.append(df_[v].min())
        Maximum.append(df_[v].max())

        # Variance and STD determination
        v1 = df_[weight].sum()
        v1exp2 = v1 ** 2
        v2 = (df_[weight] ** 2).sum()
        numerator = (((df_[v] - wavrg) ** 2) * df_[weight]).sum()
        variance = v1 / (v1exp2 - v2) * numerator
        variances.append(variance)
        STD.append(math.sqrt(variance))

        # Quantiles determination
        values_sort = df_.sort_values(by=v)

        # assert np.sum(weight_sort) != 0.0, "The sum of the weights must not equal zero"
        weights = np.array(values_sort[weight])
        sumweights = np.sum(weights)
        offset = (weights[0] / sumweights) / 2.0
        probs = np.cumsum(weights) / sumweights - offset
        for percentile_name, percentile in percentiles.items():
            Q[percentile_name].append(np.interp(x=percentile, xp=probs, fp=values_sort[v]))

    # Tabulating the results
    result = pd.DataFrame({"": Variables,
                           "count": Count,
                           "wmean": WMean,
                           "variance": variances,
                           "std": STD,
                           "min": Minimum,
                           **Q,
                           "max": Maximum,
                           "weight": weight,
                           }
                          )

    if missing:
        result['Missing values'] = Nanno

    result.set_index("", inplace=True)
    return result.transpose()


def dist_reschart(df, bins, xdist, yvar, clas, position=None, output=0):
    """
    Resource classification X Sample distance chart
    @param df: dataset to be used (block model file)
    @type df: DataFrame
    @param bins: number of bins to be displayed in the chart
    @type bins: int64
    @param xdist: distance variable to be used (e.g. 'MinD', 'MinAvgD' etc)
    @type xdist: float
    @param yvar: Mineral Resource classification variable (e.g. 'CLASS', 'rec_class')
    @type yvar: int64 or text
    @param clas: Resource classification values (e.g. ['MEAS', 'IND', 'INF'], [1, 2, 3] etc)
    @type clas: list
    @param position: optional field to display the statistics of the xdist variable. E.g. [20, 3]
    @type position: list
    @param output: 0: displays the chart; 1: returns the lists with the values for the chart creation
    @type output: int64
    """
    df = df.sort_values(by=[xdist])

    # calculate and create a list with the probability values for each value
    prob = 100 / len(df[xdist])
    df['Prob'] = prob

    # generate the X values for the chart
    xintervals = math.ceil(df[xdist].max())  # calculate the number of intervals
    xbin = df[xdist].max() / bins  # calculate the size of each bin
    begin = xbin  # beginning of X axis
    x = []
    while begin < xintervals:
        x.append(begin)
        begin = begin + xbin

    # generate the Y lists for the chart
    MEAS = []
    IND = []
    INF = []
    i = 0
    while i < len(x):
        if i == 0:
            l = df.loc[(df[xdist] > i) & (df[xdist] < x[0])]
            MEAS.append(l['Prob'].loc[l[yvar] == clas[0]].sum())
            IND.append(l['Prob'].loc[l[yvar] == clas[1]].sum())
            INF.append(l['Prob'].loc[l[yvar] == clas[2]].sum())
            i = i + 1
        else:
            l = df.loc[(df[xdist] > x[i - 1]) & (df[xdist] < x[i])]
            MEAS.append(l['Prob'].loc[l[yvar] == clas[0]].sum())
            IND.append(l['Prob'].loc[l[yvar] == clas[1]].sum())
            INF.append(l['Prob'].loc[l[yvar] == clas[2]].sum())
            i = i + 1

    if output == 0:
        # chart generation
        v = df[xdist]
        barw = math.ceil(v.max() / bins)

        string_info = f'Distance (m)\n\nMean: {v.mean():.2f}\nStd. dev.: {v.std():.2f}\nMinimum: {v.min():.2f}\nMaximum: {v.max():.2f}\nn: {v.count()}'

        plt.figure(figsize=(7, 5))
        plt.bar(x, MEAS, color='r', edgecolor='black', width=barw)
        plt.bar(x, IND, bottom=MEAS, color='g', edgecolor='black', width=barw)
        plt.bar(x, INF, bottom=[MEAS[j] + IND[j] for j in range(len(MEAS))], color='b', edgecolor='black', width=barw)
        plt.xlabel("Distance (m)")
        plt.ylabel("Frequency (%)")
        plt.legend(["Measured", "Indicated", "Inferred"])
        plt.title("Distance Histogram")
        if position:
            plt.text(position[0], position[1], string_info, fontsize=12)
        plt.xlim([0, xintervals + 2])
        plt.show()
    else:
        return MEAS, IND, INF


def topcutstat(df, variable, weight=None, tc=False):
    """
    This tool that provides the statistics of a variable (including the metal loss and number of capped samples)
    given a list of capping values.
    @param df: dataset to be used (saples or composites file)
    @type df: DataFrame
    @param variable: variable from the dataset for the statistics
    @type variable: int or float
    @param weight: optional variable in case the results are weighted by a variable
    @type weight: int or float
    @param tc: top-cut(s) to be used in the statistics (e.g. tc= [0.1, 0.2, 0.3, 1, 5, 10])
    @type tc: int or float
    @return: return the statistic table (similiar of the describe() one).
    @rtype: table
    """
    smp_cut = [0]
    pct_cut = [0]
    mloss = [0]
    nanvalues = []

    if weight == None:
        df['N/A'] = 1
        weight = 'N/A'
    else:
        # Check if 'weight' column contains only numeric values
        if not ax.is_numeric_column(df, weight):
            raise ValueError("Weight values should be numeric.")

    result = pd.DataFrame()
    result[variable] = describew(df, weight, var=[variable])

    # Filtering out NaN
    nanvalues.append(df[variable].isna().sum())
    df.dropna(subset=[variable], inplace=True)

    if tc:
        for t in tc:
            if not isinstance(t, (int, float)):
                raise ValueError("Top cut values should be numeric.")

            filtered_values = df.where(df[variable] < t, t)
            result[f'TopCut_{t}'] = describew(filtered_values, weight, var=[variable])
            mloss.append((result['TopCut_' + str(t)]['wmean'] / result[variable]['wmean'] - 1) * 100)

            cutcount = df[df[variable] > t][variable].count()
            smp_cut.append(cutcount)
            pct_cut.append(cutcount / result['TopCut_' + str(t)]['count'] * 100)

    result.loc[len(result)] = mloss
    result.loc[len(result)] = smp_cut
    result.loc[len(result)] = pct_cut
    result.rename(index={10: 'Metal loss (%)', 11: 'Samples capped', 12: '% Samples capped'}, inplace=True)

    return result