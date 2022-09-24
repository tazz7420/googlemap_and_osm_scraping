from random import randint
import overpass_turbo_spider as ots
import google_map_spider as gms
import osmnx as ox
import networkx as nx
import json, folium


class RandomChoise():
# overpass 環域分析(餐廳)位置擷取
    def __init__(self, qDis, lon, lat):
        self.restaurant_list = json.loads(ots.restaurant_buffer(qDis, lat, lon))
        for idx, obj in enumerate(self.restaurant_list):
                if obj['name'] == 'unknown':
                    self.restaurant_list.pop(idx)
        self.lon = lon
        self.lat = lat
        self.qDis = qDis

    def print_list(self):
        for i in range(len(self.restaurant_list)):
            print(f'編號: {i+1}, 餐廳名稱: {self.restaurant_list[i]["name"]}')


    def del_restauant(self):
        del_val = input('想要刪除的餐廳編號:\n')
        try:
            for idx, obj in enumerate(self.restaurant_list):
                if obj['id'] == int(del_val):
                    self.restaurant_list.pop(idx)

        except:
            print('無此餐廳編號')

    def go(self):
        first_one = self.restaurant_list[0]['id']
        last_one = self.restaurant_list[-1]['id']

        self.random_one = randint(first_one, last_one)-1
        print(f"抽中的餐廳是: {self.restaurant_list[self.random_one]['name']}")

    def draw_route(self):
        # folium畫地圖 取得地圖中心位置
        fmap = folium.Map(location=[self.restaurant_list[self.random_one]['lat']/2 + self.lat/2, self.restaurant_list[self.random_one]['lon']/2 + self.lon/2], zoom_start=17)
        # 加入地點的圖徽
        fmap.add_child(folium.Marker(location=[self.lat, self.lon],popup='現在位置',icon=folium.Icon(icon='paper-plane', # Icon類型
                                            color='green', # Marker顏色
                                            prefix='fa'))) # 使用Font Awesome Icons
        fmap.add_child(folium.Marker(location=[self.restaurant_list[self.random_one]['lat'], self.restaurant_list[self.random_one]['lon']],popup=self.restaurant_list[self.random_one]['name']))

        # osmnx透過中心點抓路網
        G = ox.graph_from_point((self.lat,self.lon), self.qDis*2, network_type='walk')

        # 以下註解為抓路名的方式
        #G = ox.graph_from_point((lat,lon), qDis*2, network_type='drive')
        #near_road = ox.nearest_edges(G, X=lon, Y=lat, return_dist=True)
        #print(near_road[0])
        #print(G[near_road[0][0]][near_road[0][1]][0]['name'])

        # 抓起點最近節點
        origin = ox.distance.nearest_nodes(G, X=self.lon,Y=self.lat)
        # 抓終點最近節點
        destination = ox.distance.nearest_nodes(G, X=self.restaurant_list[self.random_one]['lon'], Y=self.restaurant_list[self.random_one]['lat'])
        # 取得最短路徑
        route = nx.shortest_path(G, origin, destination)

        # 取得最短路徑
        points = []
        point = [self.lat,self.lon]
        points.append(point)
        for n in route:
            point = [G._node[n]['y'],G._node[n]['x']]
            points.append(point)

        # 終點
        point = [self.restaurant_list[self.random_one]['lat'],self.restaurant_list[self.random_one]['lon']]
        points.append(point)

        # 繪製
        fmap.add_child(folium.PolyLine(locations=points, weight=8)) # 線條寬度
        fmap.save('map.html')



if __name__ == '__main__':   
    qString = input('請輸入地點或坐標:\n')
    qDis = int(input('請輸入搜尋距離:\n'))

    # google map抓坐標
    lon, lat = gms.get_current_location(qString)

    rc = RandomChoise(qDis, lon, lat)
    act = 'start'

    while act != 'go':
        print('')
        print('')
        print('-----操作指令-----')
        print('print: 看附近搜尋到的餐廳')
        print('  del: 刪除不想餐與抽選的餐廳')
        print('   go: 開始抽選 繪製路線')
        print('')
        print('')

        act = input('輸入指令: ')
        if act == 'print':
            rc.print_list()
        elif act == 'del':
            rc.del_restauant()
            rc.print_list()
        elif act == 'go':
            rc.go()
            rc.draw_route()