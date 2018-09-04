import requests
import lxml
import lxml.html
import pandas as pd

def get_data(stock, year, jidu):
    #url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2018&jidu=1"
    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%d.phtml?year=%d&jidu=%d" % (stock, year, jidu)
    resp = requests.get(url)
    doc = lxml.html.document_fromstring(resp.content.decode('gbk'))
    trs = doc.xpath('//*[@id="FundHoldSharesTable"]//tr')
    i = 0
    header = None
    data = []
    for tr in trs[1:]:
        tds = tr.xpath(".//td")
        row = []
        for td in tds:
            text = lxml.etree.tounicode(td, method='text').strip()
            row.append(text)
        if i == 0:
            header = row
        else:
            data.append(row)
        i += 1
    df = pd.DataFrame(data=data, columns=header)
    df.to_csv("%d_%d_%d.csv" % (stock, year, jidu), index=False)
    return df

if __name__ == "__main__":
    get_data(601006, 2018, 1)
