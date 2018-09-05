import requests
import lxml
import lxml.html
import pandas as pd

def get_data(stocks, years, jidus):
    header = None
    data = []
    for stock in stocks:
        for year in years:
            for jidu in jidus:
                url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%d.phtml?year=%d&jidu=%d" % (stock, year, jidu)
                print("download %s" % url)
                resp = requests.get(url)
                doc = lxml.html.document_fromstring(resp.content.decode('gbk'))
                trs = doc.xpath('//*[@id="FundHoldSharesTable"]//tr')
                i = 0
                for tr in trs[1:]:
                    tds = tr.xpath(".//td")
                    if i == 0:
                        row = ["股票代码"]
                    else:
                        row = ["%s" % stock]
                    for td in tds:
                        text = lxml.etree.tounicode(td, method='text').strip()
                        row.append(text)
                    if i == 0:
                        header = row
                    else:
                        data.append(row)
                    i += 1
    df = pd.DataFrame(data=data, columns=header)
    filename = "result.csv"
    print("saving to %s" % filename)
    df.to_csv(filename, index=False)
    return df

if __name__ == "__main__":
    stocks = [601006, 601007]
    years = [2017, 2018]
    jidus = [1, 2, 3, 4]
    get_data(stocks, years, jidus)
