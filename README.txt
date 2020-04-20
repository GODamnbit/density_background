接口测试：
项目运行后使用postman测试：
1. 登录测试：POST  123.57.55.107:5000/login
	header：json，键值对user_id、password、（longitude、latitude）、timestamp、role
	（ex：user_id：2，password：123，（longitude：103.980411、latitude：30.772793）、timestamp：2020-04-12 15:55:12、role：0）
	注：若输入了经纬度则展示“离我最近”站点及在地图上的图片标注，若否则不予以展示，且登录后若不退出则经纬度固定，角色分为admin（role=1）和user（role=0）


管理员模块：POST  123.57.55.107:5000/admin
	header：json，键值对admin_id（admin_id：1）

	1）删除用户信息：
	键值对delete_user、user_id
	（ex：delete_user：1，user_id：10）

	2）编辑路线信息：
	GET：（展示路线信息）
	键值对edit_route、route_id
	（ex：edit_route：1，route_id：1）
	
	POST：（编辑路线信息）
	键值对edit_route、route_id、route_name
	（ex：edit_route：1，route_id：1，route_name：二号线）
	
	3）删除路线信息：
	键值对delete_route、route_name
	（ex：delete_route：1，route_name：2号线）
	
	4）添加路线信息：
	键值对add_route、route_name
	（ex：add_route：1，route_name：4号线）
	
	5）编辑站点信息：
	GET：（展示站点信息）
	键值对edit_station、station_id
	（ex：edit_station：1，station_id：1）

	POST：（编辑站点信息）
	键值对edit_station、station_id、（station_name、station_type、station_longitude、station_latitude）括号内可任选改动，经纬度不建议改动
	（ex：edit_station：1，station_id：1，station_name：天府广场站，station_type：1）
	
	6）删除站点信息：
	键值对delete_station、station_name
	（ex：delete_station：1，station_name：天府广场站）
	注：不建议测试删除模块，故提供了不存在的站点名供测试

	7）添加站点：
	键值对add_station、station_name、station_type
	（ex：add_station：1，station_name：成都市天府广场站、station_type：1）
	注：站点名越详细越好，便于后台获取站点经纬度

	8）编辑公交信息：
	GET：（展示公交信息）
	键值对edit_bus、bus_id
	（ex：edit_bus：1，bus_id：1）
	
	POST：（编辑公交信息）
	键值对edit_bus、bus_id、（route_id、user_id、type_id、permit_passengers、start_date、belong_company）括号内可任选改动
	（ex：edit_bus：1，bus_id：1，route_id：1，user_id：1，type_id：1，permit_passengers：40，start_date：2020-01-01，belong_company：天府通公交公司）
	
	9）删除公交信息：
	键值对delete_bus、bus_id
	（ex：delete_bus：1，bus_id：1）

	10）添加公交信息：
	键值对add_bus、route_id、user_id、type_id、permit_passengers、start_date、belong_company
	（ex：add_bus：1，route_id：1，user_id：1，type_id：1，permit_passengers：40，start_date：2020-01-01，belong_company：天府通公交公司）
	


2. 注册测试：POST  123.57.55.107:5000/add
	header：json，键值对phone、user_name、(email)、password、(sex)、born_date
	（ex：phone：126，user_name：lala，password：w123，sex：男，born_date：1999-2-3）
	ps：切勿增加user_id字段，设置为自增长用户不能自己注册，括号内参数可为空，sex：男/女，注册成功后将返回用户ID

3.个人信息编辑模块：
	获取所有个人信息：
	GET  123.57.55.107:5000/edit
	header:json，键值对user_id
	(ex：user_id：2）
	
	编辑个人信息：
	POST  123.57.55.107:5000/edit
	header:json，键值对user_id+任意信息字段的编辑(phone,user_name, email, 		password,sex,head_img, address, born_date='1999-1-1', longitude=0, latitude=0, 		production)

4. 发布测试：
	1）地铁站台：
	  发布首页：GET  123.57.55.107:5000/station
	（此处我加了一个多选query_way：若为1，则是按站点名查询；2，则是按路线查询）

	按站点名查询：GET  123.57.55.107:5000/by_station_name
	header：json，键值对station_name、color（前端返回颜色“R”“G”“B”）
	（ex：station_name：春熙路，color：R）
	    
	按地铁路线查询：GET 123.57.55.107:5000/by_route_station
	header：json，键值对route_name、timestamp
	（ex：route_name：2号线&timestamp:2020-04-12 15:55:12）
	
	2）公交站台：
	发布首页：GET  123.57.55.107:5000/bus
	（此处我加了一个多选query_way：若为1，则是按站点名查询；2，则是按路线查询）

	按公交ID查询：GET  123.57.55.107:5000/by_bus_id
	header：json，键值对bus_id、color（前端返回颜色“R”“G”“B”）
	（ex：bus_id：1，color：R）
	    
	按公交路线查询：GET 123.57.55.107:5000/by_route_bus
	header：json，键值对route_name、timestamp
	（ex：route_name：2号线&timestamp:2020-04-13 11:10:47）

注：1.将返回该路线所有站点的密度信息density，前端自行设置阈值判定获取颜色“R”“	G”“B”（	以供站点查询使用）
      2.目前该路线（2号线）仅有三个站点（犀浦快铁站、春熙路、天河路），另外存在两个公交站点（	西华大学南大门站，西华大学西门站），切勿将公交站点放在地铁路线上以便后续开发
      3.由于识别数据不一定能及时，时间戳建议为2020-04-12 21:04:58


5. 数据分析模块：
	GET/POST  123.57.55.107:5000/vision
	header：json，键值对request_way、start_time、end_time、station_id
	1）某段时间内不同站台的人群数量统计直方图
	request_way：3，start_time：2020-04-06 00:00:00，end_time：2020-04-11 00:00:00
	返回：json的直方图HTML

	2）不同站台的人群数量随时间的变化情况折线图
	request_way：4，start_time：2020-04-06 00:00:00，end_time：2020-04-07 00:00:00
	返回：json的折线图HTML

	3）某号站台的人群数量随时间的变化情况折线图
	request_way：5，station_id：2，start_time：2020-04-06 00:00:00，end_time：2020-04-07 00:00:00
	返回：json的折线图HTML

	4）不同公交路线的人群数量随时间的变化情况折线图
	request_way：1，start_time：2020-04-13 10:46:00，end_time：2020-04-13 14:49:00
	返回：json的折线图HTML

	5）某路公交车上人群数量随时间的变化情况折线图
	request_way：2，start_time：2020-04-13 10:46:00，end_time：2020-04-13 14:49:00，bus_id：2
	返回：json的折线图HTML

	注：反馈时间较慢需等待