import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64


def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')

    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))

    # Tenure Months to grouping categories
    def grouping_tenure(telco):
        if telco["tenure_months"] <= 12:
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] < 24):
            return "1-2 Year"
        elif (telco["tenure_months"] < 24) & (telco["tenure_months"] <= 48):
            return "2-4 Year"
        elif (telco["tenure_months"] <= 48) & (telco["tenure_months"] < 60):
            return "4-5 Year"
        else:
            return "> 5 Year"

    telco["tenure_group"] = telco.apply(
        lambda telco: grouping_tenure(telco), axis=1)

    # # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(
        telco["tenure_group"], categories=tenure_group, ordered=True)

    return(telco)


def table_churn(data):
    table = pd.crosstab(
        data['churn_label'],
        columns='percent',
        normalize=True)*100
    return(table)


def plot_phone(data):

    # ---- Phone Service Customer
    phone_serv = pd.crosstab(
        data['phone_service'],
        columns=data['churn_label'],
        normalize='index'
    )

    ax = phone_serv.plot(kind='barh', color=[
                         '#53a4b1', '#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_internet(data):

    # ---- Internet Service Customer
    internet_serv = pd.crosstab(
        data['internet_service'],
        columns=data['churn_label'],
        normalize=True
    )
    # Plot Configuration
    ax2 = internet_serv.plot(
        kind='barh', color=['#53a4b1', '#c34454'], figsize=(8, 6))

    ax2.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_tenure_churn(data):

    # ---- Churn Rate by Tenure Group
    tenure_pd = pd.crosstab(data['tenure_group'],
                            data['churn_label'], normalize=True)
    ax3 = tenure_pd.plot(kind='bar', color=[
                         '#53a4b1', '#c34454'], figsize=(8, 6))


    # Plot Configuration
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation=360)
    plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)
    plt.title('Churn Rate by Tenure Group')
    # Plot Configuration
    # ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    # plt.axes().get_xaxis().set_label_text('')
    # plt.xticks(rotation=360)
    # plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)
    # plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure
    avg_tenure = pd.crosstab(
        data['tenure_months'], data['churn_label'], values=data['cltv'], aggfunc="mean")

    ax = avg_tenure.plot(color=['#333333', '#b3b3b3'],
                         figsize=(8, 6), style='.--')


    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.xticks(rotation=360)
    plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)
    plt.title('Average Lifetime Value by Tenure')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation=360)
    plt.legend(['Retain', 'Churn'], fancybox=True, shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)


def plot_top_ten(data):

    # ---- Average Lifetime Value by Tenure
    top10 = data.groupby('city').churn_label.count().sort_values(ascending=False).head(10).index.to_list()

    top10_data = data[data['city'].isin(top10)]

    _df = pd.crosstab(
        index=top10_data['city'],
        columns=top10_data['churn_label'],
        normalize='index'
    )*100

    axTop = _df.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (10,6))


    axTop.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'], fancybox=True,shadow=True, bbox_to_anchor=(1, 1))
    plt.axes().get_yaxis().set_label_text('City')
    plt.title('Top 10 churn city')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)
