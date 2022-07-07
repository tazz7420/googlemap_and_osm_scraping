from random import randint
import overpass_turbo_spider as ots
import google_map_spider as gms
import osmnx as ox
import networkx as nx
import json, folium

qString = input('請輸入地點或坐標:\n')
qDis = int(input('請輸入搜尋距離:\n'))

# google map抓坐標
lon, lat = gms.get_current_location(qString)

# overpass 環域分析(餐廳)位置擷取
restaurant_list = json.loads(ots.restaurant_buffer(qDis, lat, lon))

first_one = restaurant_list[0]['id']
last_one = restaurant_list[-1]['id']

# 隨機選擇餐廳
random_one = randint(first_one, last_one)
print(restaurant_list[random_one]['name'])

# folium畫地圖 取得地圖中心位置
fmap = folium.Map(location=[restaurant_list[random_one]['lat']/2 + lat/2, restaurant_list[random_one]['lon']/2 + lon/2], zoom_start=17)
# 加入地點的圖徽
fmap.add_child(folium.Marker(location=[lat, lon],popup='現在位置',icon=folium.Icon(icon='paper-plane', # Icon類型
                                    color='green', # Marker顏色
                                    prefix='fa'))) # 使用Font Awesome Icons
fmap.add_child(folium.Marker(location=[restaurant_list[random_one]['lat'], restaurant_list[random_one]['lon']],popup=restaurant_list[random_one]['name']))

# osmnx透過中心點抓路網
G = ox.graph_from_point((lat,lon), qDis*2, network_type='walk')

# 以下註解為抓路名的方式
#G = ox.graph_from_point((lat,lon), qDis*2, network_type='drive')
#near_road = ox.nearest_edges(G, X=lon, Y=lat, return_dist=True)
#print(near_road[0])
#print(G[near_road[0][0]][near_road[0][1]][0]['name'])

# 抓起點最近節點
origin = ox.distance.nearest_nodes(G, X=lon,Y=lat)
# 抓終點最近節點
destination = ox.distance.nearest_nodes(G, X=restaurant_list[random_one]['lon'], Y=restaurant_list[random_one]['lat'])
# 取得最短路徑
route = nx.shortest_path(G, origin, destination)
print(route)

# 取得最短路徑
points = []
point = [lat,lon]
points.append(point)
for n in route:
    print(G._node[n])
    point = [G._node[n]['y'],G._node[n]['x']]
    points.append(point)

# 終點
point = [restaurant_list[random_one]['lat'],restaurant_list[random_one]['lon']]
points.append(point)

# 繪製
fmap.add_child(folium.PolyLine(locations=points, weight=8)) # 線條寬度
fmap.save('map.html')
