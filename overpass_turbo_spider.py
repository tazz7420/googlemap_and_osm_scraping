import requests as req
import json, google_map_spider



def restaurant_buffer(dis, lat, lon):
    stores = []
    counter = 1
    # GIS環域資料抓取網址
    url = f"https://overpass-api.de/api/interpreter"
    distance = dis
    #dataForm = f'data=%5Bout%3A+json%5D%5Btimeout%3A+25%5D%3B%0A%0A(%0Anode%5B%22amenity%22+%3D+%22restaurant%22%5D(around%3A+{distance}%2C+{lat}%2C+{lon})%3B%0Anode%5B%22amenity%22+%3D+%22fast_food%22%5D(around%3A+{distance}%2C+{lat}%2C+{lon})%3B%0A)%3B%0A%0Aout+body%3B%0A%3E%3B%0Aout+skel+qt%3B'
    # POST封包內容
    dataForm = f'''data=[out:json][timeout:25];
        (
            # 節點node 線段way
            # 關鍵字索引[xxx = ???]
            # 環域分析 距離 緯度 經度
            node["amenity" = "restaurant"](around: {distance}, {lat}, {lon});
            node["amenity" = "fast_food"](around: {distance}, {lat}, {lon});
        );
        out body;>;out skel qt;
        '''
    res = req.post(url, data = dataForm)
    data = json.loads(res.text)
    for element in data['elements']:
        try:
            stores.append({
                'id': counter,
                'name': element['tags']['name'],
                'lat': element['lat'],
                'lon': element['lon']
            })
        except:
            try:
                stores.append({
                    'id': counter,
                    'name': element['tags']['name:en'],
                    'lat': element['lat'],
                    'lon': element['lon']
                })
            except:
                stores.append({
                    'id': counter,
                    'name': 'unknown',
                    'lat': element['lat'],
                    'lon': element['lon']
                })
        counter = counter + 1
    return json.dumps(stores, ensure_ascii=False)

# 測試
if __name__ == '__main__':
    # 透過google map抓經緯度
    lon, lat = google_map_spider.get_current_location('資展國際')
    restaurant_list = restaurant_buffer(200, lat, lon)
    print(restaurant_list)
