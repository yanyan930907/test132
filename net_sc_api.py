from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 類別的 URL 列表
category_urls = [
    "https://www.net-fashion.net/category/2105",
    "https://www.net-fashion.net/category/2106",
    "https://www.net-fashion.net/category/2443",
    "https://www.net-fashion.net/category/2448",
]

@app.route('/scrape_products', methods=['GET'])
def scrape_products():
    all_products = []
    cnt = 0
    
    # 迭代每個類別的 URL
    for category_url in category_urls:
        response = requests.get(category_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 取得最大頁數
        max_pages = soup.find_all("a", class_="number_line_a")
        if max_pages:
            last_number = int(max_pages[-2].text.strip())
        else:
            last_number = 1
        
        for nowpage in range(0, last_number):
            temp = "" if nowpage == 0 else str(nowpage)
            response = requests.get(f"{category_url}/{temp}", headers={"User-Agent": "Mozilla/5.0"})
            
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 找到所有商品區塊
            product_items = soup.find_all("div", class_="main_con js-product-block")
            
            if not product_items:
                continue
            
            # 解析每個商品資料
            for item in product_items:
                try:
                    # 商品名稱
                    name = item.find("div", class_="main_name").find("a").text.strip()
                    
                    # 商品價格
                    price = item.find("span", class_="price_orginal").text.strip()
                    
                    # 商品圖片 URL
                    img_url = item.find("img", class_="js-product-img")["src"]
                    
                    # 儲存商品資料
                    all_products.append({
                        "name": name,
                        "price": price,
                        "image": img_url
                    })
                    cnt += 1
                except AttributeError:
                    continue
    
    return jsonify(all_products)


if __name__ == '__main__':
    app.run(debug=True)