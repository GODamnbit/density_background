�ӿڲ��ԣ�
��Ŀ���к�ʹ��postman���ԣ�
1. ��¼���ԣ�POST  123.57.55.107:5000/login
	header��json����ֵ��user_id��password����longitude��latitude����timestamp��role
	��ex��user_id��2��password��123����longitude��103.980411��latitude��30.772793����timestamp��2020-04-12 15:55:12��role��0��
	ע���������˾�γ����չʾ�����������վ�㼰�ڵ�ͼ�ϵ�ͼƬ��ע������������չʾ���ҵ�¼�������˳���γ�ȹ̶�����ɫ��Ϊadmin��role=1����user��role=0��


����Աģ�飺POST  123.57.55.107:5000/admin
	header��json����ֵ��admin_id��admin_id��1��

	1��ɾ���û���Ϣ��
	��ֵ��delete_user��user_id
	��ex��delete_user��1��user_id��10��

	2���༭·����Ϣ��
	GET����չʾ·����Ϣ��
	��ֵ��edit_route��route_id
	��ex��edit_route��1��route_id��1��
	
	POST�����༭·����Ϣ��
	��ֵ��edit_route��route_id��route_name
	��ex��edit_route��1��route_id��1��route_name�������ߣ�
	
	3��ɾ��·����Ϣ��
	��ֵ��delete_route��route_name
	��ex��delete_route��1��route_name��2���ߣ�
	
	4�����·����Ϣ��
	��ֵ��add_route��route_name
	��ex��add_route��1��route_name��4���ߣ�
	
	5���༭վ����Ϣ��
	GET����չʾվ����Ϣ��
	��ֵ��edit_station��station_id
	��ex��edit_station��1��station_id��1��

	POST�����༭վ����Ϣ��
	��ֵ��edit_station��station_id����station_name��station_type��station_longitude��station_latitude�������ڿ���ѡ�Ķ�����γ�Ȳ�����Ķ�
	��ex��edit_station��1��station_id��1��station_name���츮�㳡վ��station_type��1��
	
	6��ɾ��վ����Ϣ��
	��ֵ��delete_station��station_name
	��ex��delete_station��1��station_name���츮�㳡վ��
	ע�����������ɾ��ģ�飬���ṩ�˲����ڵ�վ����������

	7�����վ�㣺
	��ֵ��add_station��station_name��station_type
	��ex��add_station��1��station_name���ɶ����츮�㳡վ��station_type��1��
	ע��վ����Խ��ϸԽ�ã����ں�̨��ȡվ�㾭γ��

	8���༭������Ϣ��
	GET����չʾ������Ϣ��
	��ֵ��edit_bus��bus_id
	��ex��edit_bus��1��bus_id��1��
	
	POST�����༭������Ϣ��
	��ֵ��edit_bus��bus_id����route_id��user_id��type_id��permit_passengers��start_date��belong_company�������ڿ���ѡ�Ķ�
	��ex��edit_bus��1��bus_id��1��route_id��1��user_id��1��type_id��1��permit_passengers��40��start_date��2020-01-01��belong_company���츮ͨ������˾��
	
	9��ɾ��������Ϣ��
	��ֵ��delete_bus��bus_id
	��ex��delete_bus��1��bus_id��1��

	10����ӹ�����Ϣ��
	��ֵ��add_bus��route_id��user_id��type_id��permit_passengers��start_date��belong_company
	��ex��add_bus��1��route_id��1��user_id��1��type_id��1��permit_passengers��40��start_date��2020-01-01��belong_company���츮ͨ������˾��
	


2. ע����ԣ�POST  123.57.55.107:5000/add
	header��json����ֵ��phone��user_name��(email)��password��(sex)��born_date
	��ex��phone��126��user_name��lala��password��w123��sex���У�born_date��1999-2-3��
	ps����������user_id�ֶΣ�����Ϊ�������û������Լ�ע�ᣬ�����ڲ�����Ϊ�գ�sex����/Ů��ע��ɹ��󽫷����û�ID

3.������Ϣ�༭ģ�飺
	��ȡ���и�����Ϣ��
	GET  123.57.55.107:5000/edit
	header:json����ֵ��user_id
	(ex��user_id��2��
	
	�༭������Ϣ��
	POST  123.57.55.107:5000/edit
	header:json����ֵ��user_id+������Ϣ�ֶεı༭(phone,user_name, email, 		password,sex,head_img, address, born_date='1999-1-1', longitude=0, latitude=0, 		production)

4. �������ԣ�
	1������վ̨��
	  ������ҳ��GET  123.57.55.107:5000/station
	���˴��Ҽ���һ����ѡquery_way����Ϊ1�����ǰ�վ������ѯ��2�����ǰ�·�߲�ѯ��

	��վ������ѯ��GET  123.57.55.107:5000/by_station_name
	header��json����ֵ��station_name��color��ǰ�˷�����ɫ��R����G����B����
	��ex��station_name������·��color��R��
	    
	������·�߲�ѯ��GET 123.57.55.107:5000/by_route_station
	header��json����ֵ��route_name��timestamp
	��ex��route_name��2����&timestamp:2020-04-12 15:55:12��
	
	2������վ̨��
	������ҳ��GET  123.57.55.107:5000/bus
	���˴��Ҽ���һ����ѡquery_way����Ϊ1�����ǰ�վ������ѯ��2�����ǰ�·�߲�ѯ��

	������ID��ѯ��GET  123.57.55.107:5000/by_bus_id
	header��json����ֵ��bus_id��color��ǰ�˷�����ɫ��R����G����B����
	��ex��bus_id��1��color��R��
	    
	������·�߲�ѯ��GET 123.57.55.107:5000/by_route_bus
	header��json����ֵ��route_name��timestamp
	��ex��route_name��2����&timestamp:2020-04-13 11:10:47��

ע��1.�����ظ�·������վ����ܶ���Ϣdensity��ǰ������������ֵ�ж���ȡ��ɫ��R����	G����B����	�Թ�վ���ѯʹ�ã�
      2.Ŀǰ��·�ߣ�2���ߣ���������վ�㣨Ϭ�ֿ���վ������·�����·�������������������վ�㣨	������ѧ�ϴ���վ��������ѧ����վ�������𽫹���վ����ڵ���·�����Ա��������
      3.����ʶ�����ݲ�һ���ܼ�ʱ��ʱ�������Ϊ2020-04-12 21:04:58


5. ���ݷ���ģ�飺
	GET/POST  123.57.55.107:5000/vision
	header��json����ֵ��request_way��start_time��end_time��station_id
	1��ĳ��ʱ���ڲ�ͬվ̨����Ⱥ����ͳ��ֱ��ͼ
	request_way��3��start_time��2020-04-06 00:00:00��end_time��2020-04-11 00:00:00
	���أ�json��ֱ��ͼHTML

	2����ͬվ̨����Ⱥ������ʱ��ı仯�������ͼ
	request_way��4��start_time��2020-04-06 00:00:00��end_time��2020-04-07 00:00:00
	���أ�json������ͼHTML

	3��ĳ��վ̨����Ⱥ������ʱ��ı仯�������ͼ
	request_way��5��station_id��2��start_time��2020-04-06 00:00:00��end_time��2020-04-07 00:00:00
	���أ�json������ͼHTML

	4����ͬ����·�ߵ���Ⱥ������ʱ��ı仯�������ͼ
	request_way��1��start_time��2020-04-13 10:46:00��end_time��2020-04-13 14:49:00
	���أ�json������ͼHTML

	5��ĳ·����������Ⱥ������ʱ��ı仯�������ͼ
	request_way��2��start_time��2020-04-13 10:46:00��end_time��2020-04-13 14:49:00��bus_id��2
	���أ�json������ͼHTML

	ע������ʱ�������ȴ�