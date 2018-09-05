import requests
import lxml
import lxml.html
import pandas as pd

def get_data(stock):
    years = [2017, 2018]
    jidus = [1, 2, 3, 4]
    header = None
    data = []
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
    filename = "%d.csv" % stock
    print("saving to %s" % filename)
    df.to_csv(filename, index=False)
    return df

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <stock_id>" % sys.argv[0])
        sys.exit(1)
    stock = int(sys.argv[1])
    get_data(stock)
    #get_data(601006)
