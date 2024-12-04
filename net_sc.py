import requests
from bs4 import BeautifulSoup
import json

# 類別的 URL 列表
category_urls = [
    "https://www.net-fashion.net/category/2105",
    "https://www.net-fashion.net/category/2106",
    "https://www.net-fashion.net/category/2443",
    "https://www.net-fashion.net/category/2448",

]


# 儲存所有類別的商品資料
all_products = []

# 迭代每個類別的 URL
cnt=0
for category_url in category_urls:
    
    response = requests.get(category_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    max_pages = soup.find("a",class_="number_line_a")
     # 找到所有符合 class="number_line_a" 的 <a> 標籤
    max_pages = soup.find_all("a", class_="number_line_a")
    last_number = int(max_pages[-2].text.strip())
    print(last_number)
    for nowpage in range(0, last_number):
        if(nowpage==0):
            temp=""
        else:
            temp=str(nowpage)
        response = requests.get(category_url+"/"+temp, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"無法訪問 {category_url}，狀態碼：{response.status_code}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找到所有商品區塊，這些商品位於 <li> 標籤內
        product_items = soup.find_all("div",class_="main_con js-product-block")
        
        if not product_items:
            print(f"{category_url} 中沒有商品資料")
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
                cnt=cnt+1
                print(f"第{cnt}件 商品名稱: {name}, 價格: {price}, 圖片: {img_url}")
            except AttributeError:
                # 遇到無法找到資料的情況時跳過
                continue

# 儲存為 JSON 檔案
with open("net_products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)

print(f"所有商品資料已成功儲存至 'net_products.json'！")