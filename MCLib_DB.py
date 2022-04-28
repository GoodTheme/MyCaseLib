#coding=utf-8
import sqlite3
import os
from shutil import copyfile
from datetime import datetime, timedelta

class DataBase(object):
	def __init__(self, PATH, DB_NAME, DB_PATH):
		self.PATH = PATH
		self.DB_NAME = DB_NAME
		self.DB_PATH = DB_PATH
		if not os.path.exists(self.DB_PATH):
			self.init()

	# 基本
	def trans(self, s):
		if not s:
			return ''
		trans = ''
		for t in str(s):
			trans = trans + t if t != "'" else trans + "''"
		return trans

	def execute(self, s):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		s = self.trans(s)

		try:
			cursor.execute(s)
		finally:
			results = cursor.fetchall()
			cursor.close()
			conn.commit()
			conn.close()
			return results 

	def add_column(self, table_name, column_name, column_type):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, column_name, column_type = map(trans, [table_name, column_name, column_type])

		try:
			cursor.execute(f"alter table {table_name} add column {column_name} {column_type}")
		finally:
			cursor.close()
			conn.commit()
			conn.close()

	def delete_column(self, table_name, column_name):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, column_name = map(self.trans, [table_name, column_name])

		try:
			cursor.execute(f"alter table {table_name} drop column {column_name}")
		finally:
			cursor.close()
			conn.commit()
			conn.close()

	def insert(self, table_name, column_name, value):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, column_name, value = map(self.trans, [table_name, column_name, value])

		cursor.execute(f"insert into {table_name} ({column_name}) values ('{value}')")
		cursor.close()

		conn.commit()
		conn.close()

	def delete(self, table_name, column_name, value):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, column_name, value = map(self.trans, [table_name, column_name, value])

		try:
			cursor.execute(f"delete from {table_name} where {column_name} = '{value}'")
		finally:
			cursor.close()
			conn.commit()
			conn.close()

	def delete_multi_condition(self, table_name, condition):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name = self.trans(table_name)

		try:
			cursor.execute(f"delete from {table_name} where {condition}")
		finally:
			cursor.close()
			conn.commit()
			conn.close()

	def update_latest(self, table_name, column_name, value):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, column_name, value = map(self.trans, [table_name, column_name, value])

		cursor.execute(f"select max(id) from {table_name}")
		p_id=cursor.fetchone()[0]

		try:
			cursor.execute(f"update {table_name} set {column_name} = '{value}' where id = '{p_id}'")
		except:
			print("更新数据出错", table_name, column_name, value)
		finally:
			cursor.close()
			conn.commit()
			conn.close()

	## update的条件均在前面
	def update(self, table_name, p_column, p_value, column_name, value):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
		table_name, p_column, p_value, column_name, value = map(self.trans,
			[table_name, p_column, p_value, column_name, value])

		cursor.execute(f"update {table_name} set {column_name} = '{value}'"\
			f"where {p_column} = '{p_value}'")
		cursor.close()
		
		conn.commit()
		conn.close()

	def update_multi_condition(self, table_name, condition, column_name, value):
		conn = sqlite3.connect(self.DB_PATH)
		cursor = conn.cursor()
	
		cursor.execute(f"update {table_name} set {column_name} = '{value}' where {condition}")
		cursor.close()

		conn.commit()
		conn.close()

	def select(self, table_name, column, c_col = None, c_value = None, c_cp = '='):
		if c_col and not c_value:
			print('select wrong!!')
			return
		conn = sqlite3.connect(self.DB_PATH)
		table_name, column, c_col, c_value = map(self.trans, [table_name, column, c_col, c_value])
		
		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d

		conn.row_factory = dict_factory
		cursor = conn.cursor()
		if c_col:
			cursor.execute(f"select {column} from {table_name} where {c_col} {c_cp} '{c_value}'")
		else:
			cursor.execute(f"select {column} from {table_name}")
		values = cursor.fetchall()
		cursor.close()

		conn.close()
		return values

	def select_by_order(self, table_name, column, value, flag = None):
		order = '' if flag == None else 'desc'
		table_name, column, value = map(self.trans, [table_name, column, value])

		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d
		
		conn = sqlite3.connect(self.DB_PATH)
		conn.row_factory = dict_factory

		cursor = conn.cursor()
		cursor.execute(f"select {column} from {table_name} order by {value}  {order}" )
		values = cursor.fetchall()
		cursor.close()

		conn.close()
		return values

	def select_all(self, table_name, column_name = None, value = None):
		if column_name and value:
			return self.select(table_name, "*", column_name, value)
		else:
			return self.select(table_name, "*")

	def select_multi_condition(self, table_name, column, condition):
		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d

		conn = sqlite3.connect(self.DB_PATH)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		cursor.execute(f"select {column} from {table_name} where {condition}")
		values = cursor.fetchall()
		cursor.close()
		conn.close()
		return values

	def count_rows(self, table_name, column_name = None, value = None):
		if column_name and value:
			return self.select(table_name, "count(*) num", column_name, value)[0]['num']
		else:
			return self.select(table_name, "count(*) num")[0]['num']

	def swap(self, table_name, column_name, id1, id2):
		t1 = self.select_all(table_name, 'id', id1)
		t2 = self.select_all(table_name, 'id', id2)
		self.update(table_name, 'id', id1, column_name, t2[0][column_name])
		self.update(table_name, 'id', id2, column_name, t1[0][column_name])

	def get_id_unique(self, table_name, column_name, value):
		s = self.select_all(table_name, column_name, value)
		return s[0]['id']

	def get_id_latest(self, table_name):
		s = self.select(table_name, 'max(id) maxid')
		return s[0]['maxid']

	# 案件类型
	def new_type(self, type_name):
		self.insert('type_list', 'type_name', type_name)
			
	def delete_type(self, type_name):
		for s in self.select_all('case_list', 'case_type', type_name):
			self.delete_case(s['case_name'])	
		for s in self.select_all('case_type', 'type_name', type_name):
			self.delete_type_item(type_name, s['item'])
		self.delete('type_list', 'type_name', type_name)

	def add_type_item(self, type_name, item_name, item_form):
		for s in self.select_all('case_type', 'type_name', type_name):
			if s['item'] == item_name:
				return False
		try:
			self.insert('case_type', 'type_name', type_name)
		except:
			return False
		else:
			self.update_latest('case_type', 'item', item_name)
			self.update_latest('case_type', 'item_form', item_form)
		return True

	def delete_type_item(self, type_name, item_name):
		for s in self.select_all('case_list', 'case_type', type_name):
			case_name = s['case_name']
			self.delete_multi_condition('case_info', f"case_name = '{self.trans(case_name)}' and item = '{self.trans(item_name)}'")
		
		self.delete_multi_condition('case_type', f"type_name = '{self.trans(type_name)}' and item = '{self.trans(item_name)}'")

	# 项目
	def new_project(self, project_name, project_num = None, file_path = None):
		try:
			self.insert('project_list', 'project_name', project_name)
		except:
			pass
		else:
			self.update_latest('project_list', 'label', '1')
			if project_num:
				self.update_latest('project_list', 'project_num', project_num)
			if file_path:
				self.update_latest('project_list', 'file_path', file_path)

	def delete_project(self, project_name):
		for s in self.select_all('case_list', 'project_name', project_name):
			self.delete_case(s['case_name'])	
		self.delete('project_list', 'project_name', project_name)

	def rename_project(self, project_name, new_name):
		self.update('project_list', 'project_name', project_name, 'project_name', new_name)
		for s in self.select_all('case_list', 'project_name', project_name):
			self.update(s['case_name'], 'item', 'project_name', 'value', new_name)
		self.update('case_list', 'project_name', project_name, 'project_name', new_name)

	# 案件
	def change_project(self, case_name, project_name, new_project):
		self.update('case_list', 'case_name', case_name, 'project_name', new_project)

	def new_case(self, project_name, case_name, case_type):
		try:
			self.insert('case_list', 'project_name', project_name)
		except:
			pass
		else:
			self.update_latest('case_list', 'case_name', case_name)
			self.update_latest('case_list', 'case_type', case_type)

	def rename_case(self, project_name, case_name, new_name):
		try:
			self.update('case_list', 'case_name', case_name, 'case_name', new_name)
		except:
			pass
		else:
			self.update('case_info', 'case_name', case_name, 'case_name', new_name)
			self.update('todo_list', 'case_name', case_name, 'case_name', new_name)
			self.update('event', 'case_name', case_name, 'case_name', new_name)

	def delete_case(self, case_name):
		self.delete('case_list', 'case_name', case_name)
		self.delete('case_info', 'case_name', case_name)
		self.delete('todo_list', 'case_name', case_name)
		self.delete('event_list', 'case_name', case_name)

	def insert_value(self, case_name, item_name, item_form, *value):
		self.insert('case_info', 'case_name', case_name)
		self.update_latest('case_info', 'item', item_name)
		self.update_latest('case_info', 'value_form', item_form)
		if item_form == 'text':
			self.update_latest('case_info', 'value', value[0])
		elif item_form == 'contact' or item_form == 'party':
			self.update_latest('case_info', 'value', value[0])
			self.update_latest('case_info', 'value2', value[1])

	# 当事人和联系人
	def new_party_contact_class(self, which_type, class_name, fisrt_item):
		self.insert(f"{which_type}_class", 'class', class_name)
		self.update_latest(f"{which_type}_class", 'item', fisrt_item)
		
	def new_party_contact_item(self, which_type, which_class, item_name):
		if item_name in [p['item'] for p in self.select(f"{which_type}_class", 'item', 'class', which_class)]:
			return False
		else:
			self.insert(f"{which_type}_class", 'class', which_class)
			self.update_latest(f"{which_type}_class", 'item', item_name)
			return True

	def new_person(self, which_type, which_class, name):
		self.insert(f"{which_type}_list", 'class', which_class)
		self.update_latest(f"{which_type}_list", 'name', name)

		items = self.select(f"{which_type}_class", 'item', 'class', which_class)
		pid = self.get_id_latest(f"{which_type}_list")

		self.insert(f"{which_type}_info", f"{which_type}_id", pid)
		self.update_latest(f"{which_type}_info", 'class', which_class)
		self.update_latest(f"{which_type}_info", 'item', items[0]['item'])
		self.update_latest(f"{which_type}_info", 'value', name)
		for s in items[1:]:
			self.insert(f"{which_type}_info", f"{which_type}_id", pid)
			self.update_latest(f"{which_type}_info", 'class', which_class)
			self.update_latest(f"{which_type}_info", 'item', s['item'])

	def delete_party_contact_class(self, which_type, which_class):
		for s in self.select(f"{which_type}_list", 'id', 'class', which_class):
			self.delete_person(which_type, s['id'])
		self.delete(f"{which_type}_class", 'class', which_class)
		self.delete(f"{which_type}_list", 'class', which_class)
		self.delete(f"{which_type}_info", 'class', which_class)

	def delete_party_contact_item(self, which_type, which_class, which_item):
		self.delete_multi_condition(f"{which_type}_class", f"class = '{self.trans(which_class)}' "\
			f"and item = '{self.trans(which_item)}'")
		self.delete_multi_condition(f"{which_type}_info", f"class = '{self.trans(which_class)}' "\
			f"and item = '{self.trans(which_item)}'")

	def delete_person(self, which_type, pid):
		self.delete(f"{which_type}_list", 'id', pid)
		self.delete(f"{which_type}_info", f"{which_type}_id", pid)
		self.delete_multi_condition('case_info', f"case_name = '{self.trans(case_name)}' and"\
				f" value_form = '{which_type}' and value2 = '{pid}'")

	# 数据库文件
	def delete_DB(self):
		if os.path.exists(self.DB_PATH):
			os.remove(self.DB_PATH)

	def init(self):
		self.delete_DB()
		example_path = os.path.join(os.path.abspath('.'), 'example')
		if os.path.exists(example_path):
			copyfile(example_path, self.DB_PATH)

	# 生成讯息
	def generate_project_info_html(self, project):
		color = self.select('profile', 'value')[2: 3][0]
		s = '''
			<head>
			<style>
			h3 {
				text-align: center;
				background-color: %s;
				font-size: x-large;
				letter-spacing: 4px;
				margin-bottom: 6px;
			}
			p {
				text-align: center;
				font-size: 13px;
				margin-top: 4px;
				margin-bottom: 4px;
			}
			</style>
			</head>
			<body>
		''' % (color['value'])
		s = s + f"<h3>{project}</h3>"
		project_info = self.select_all('project_list', 'project_name', project)
		if project_info and project_info[0]['project_num']:
			s = s + f"<p>项目号：{project_info[0]['project_num']}</p>"
		self.labels = ('特殊', '进行中', '搁置', '已结', '其他')
		s = s + f"<p>当前状态：{self.labels[int(project_info[0]['label'])]}</p>"
		s = s + "</body>"
		return s

	def generate_case_info_html(self, case):
		color1, color2 = self.select('profile', 'value')[3: 5]
		project = self.select('case_list', 'project_name', 'case_name', case)[0]['project_name']
		case_type = self.select('case_list', 'case_type', 'case_name', case)[0]['case_type']
		type_item = self.select_all('case_type', 'type_name', case_type)
			
		s = '''
			<head>
			<style>
			h3 {
				text-align: center;
				background-color: %s;
				font-size: x-large;
				margin-bottom: 0px;
				letter-spacing: 2px;
			}
			h4 {
				text-align: center;
				font-size: medium;
				margin-top: 3px;
				margin-bottom: 6px;
			}
			table {
				margin-top: 3px;
				border-collapse: collapse;
			}
			td {
				font-size: 13px;
				padding: 5px;
				border-style: solid;
				margin-top: 8px;
				margin-bottom: 8px;
				border: 1px solid #ddd;
				text-align: left;
			}
			.left {
				text-indent: 8px;
			}
			.right {
				text-indent: 2px;
			}
			.mid {
				background-color: %s;
			}
			</style>
			</head>
			<body>
		''' % (color1['value'], color2['value'])
		s = s + f"<h3>{case}</h3>"
		s = s + f"<h4>{project}</h4>"

		s = s + "<table width = '100%'>"
		s = s + "<tr><td class = 'mid' colspan = '2'> 基本信息 </td></tr>"
		for i in [x for x in type_item if x['item_form'] == 'text']:
			this_item = i['item']
			items = self.select_multi_condition('case_info', "id, value_form, value, value2",
				f"case_name = '{self.trans(case)}' and item = '{self.trans(this_item)}'")
			if items:
				value_form = items[0]['value_form']
				for k in items:
					s = s + f"<tr> <td class = 'left' width = '30%'> {this_item} </td>"\
						f"<td class = 'right' width = '70%'> {k['value']} </td> </tr>"
		for i in [x for x in type_item if (x['item_form'] == 'party' or x['item_form'] == 'contact')]:
			this_item = i['item']
			items = self.select_multi_condition('case_info', "id, value_form, value, value2",
				f"case_name = '{self.trans(case)}' and item = '{self.trans(this_item)}'")
			if items:
				value_form = items[0]['value_form']
				s = s + f"<tr><td class = 'mid' colspan = '2'> {this_item} </td></tr>"
				for k in items:
					name = self.select(f"{value_form}_info", 'value', f"{value_form}_id", k['value2'])[0]['value']
					s = s + f"<tr> <td class = 'left'> {k['value']} </td>"\
					f"<td class ='right'> {name} </td></tr>"
		s = s + "<table> </body>"
		return s

	def generate_report_html(self):
		color1, color2, color3 = self.select('profile', 'value')[5: 8]
		s = '''
			<head>
			<style>
			h1 {
				text-align: center;
				background-color: %s;
				font-size: x-large;
				margin-bottom: 2px;
			}
			p {
				text-align: center;
				font-size: medium;
				margin-top: 2px;
				margin-bottom: 2px;
			}
			h3 {
				text-align: center;
				background-color: %s;
				font-size: medium;
				margin-top: 2px;
			}
			table {
				border-collapse: collapse;
			}
			td {
				background-color: %s;
				border: 1px solid #ddd;
				padding: 6px;
			}
			td.left {
				border-style: none dotted none none;
			}
			td.right {
				border-style: none none none dotted;
			}
			td.mid {
				border-style: none dotted none dotted;
			}
			</style>
			</head>
			<body>
		''' % (color1['value'], color2['value'], color3['value'])

		def date_to_string(d):
			return f"{d.strftime('%Y')}年{d.strftime('%m')}月{d.strftime('%d')}日"

		def if_blank(s):
			return s if s else ' '

		weekday = ['星期' + d for d in ('日', '一', '二', '三', '四', '五', '六')]
		today_year = f"{datetime.now().strftime('%Y')}年"
		today_month = f"{datetime.now().strftime('%m')}月"
		today_day = f"{datetime.now().strftime('%d')}日"
		today_week = weekday[int(datetime.now().strftime('%w'))]
		s = s + "<h1>今日简报</h1>"
		s = s + f"<p>{today_year}{today_month}{today_day}  {today_week}</p>"

		s = s + "<h3>今日待办</h3>"
		s = s + "<table>"
		today = datetime.now().strftime('%Y-%m-%d')
		todos = sorted(self.select('todo_list', 'case_name, date, things'), 
			key = lambda x: (x['date']))
		for todo in todos:
			if todo['date'] ==  today:
				s = s + f"<tr> <td class = 'left' width = '30%'>{todo['case_name']}</td> "\
				f"<td class = 'right' width = '70%'>{if_blank(todo['things'])}</td> </tr>"
			elif todo['date'] > today:
				break
		s = s + "</table> <br>"

		s = s + "<h3>十五日内</h3>"
		s = s + "<table>"
		after_15 = (datetime.now() + timedelta(days = 15)).strftime('%Y-%m-%d')
		for todo in todos:
			if todo['date'] > today and todo['date'] < after_15:
				todo_date = datetime.strptime(todo['date'], '%Y-%m-%d')
				s = s + f"<tr> <td class = 'left' width = '25%'>{date_to_string(todo_date)}</td> "\
				f"<td class = 'mid' width = '25%'>{if_blank(todo['case_name'])}</td> "\
				f"<td class = 'right' width = '50%'>{todo['things']}</td> </tr>"
		s =s + "</table> </body>"
		return s
	
	def generate_mail_address(self, pid):
		infos = [[x['item'], x['value']] for x in self.select('contact_info', 'item, value', 'contact_id', pid)]
		s = ''
		for t in infos:
			if t[0] == '邮寄地址' or t[0] == '联系地址':
				if t[1]:
					s = s + t[1]
				else:
					s = s + "（缺少邮寄或联系地址）"
				break 
		s = s + f" {infos[0][1]}（收） "
		for t in infos:
			if t[0] == '联系电话':
				if t[1]:
					s = s + t[1]
				else:
					s = s + "（缺少联系电话）" 
				break
		return s

	def generate_party_info(self, pid):
		infos = [[x['item'], x['value']] for x in self.select('party_info', 'item, value', 'party_id', pid)]
		s = infos[0][1] + '\n'
		for t in infos:
			if t[0] in ('身份证号', '法定代表人', '地址', '注册地址', '居住地址', '联系电话'):
				if t[1]:
					s = s + f"{t[0]}：{t[1]}\n"
				else:
					s = s + f"{t[0]}：\n"
		return s

	def generate_case_info(self, case, abbr):
		case_info = self.select_all('case_info', 'case_name', case)
		project = self.select('case_list', 'project_name', 'case_name', case)[0]['project_name']
		case_type = self.select('case_list', 'case_type', 'case_name', case)[0]['case_type']
		type_item = self.select_all('case_type', 'type_name', case_type)
		
		s = ''
		last_status = ''
		flag = False
		flag_2 = False
		for i in [x for x in type_item if (x['item_form'] == 'party')]:
			this_item = i['item']
			items = self.select_multi_condition('case_info', "id, value_form, value, value2",
				f"case_name = '{self.trans(case)}' and item = '{self.trans(this_item)}'")
			if items:
				for k in items:
					status = k['value']
					infos = self.select(f"party_info", 'item, value', f"party_id", k['value2'])
					name = infos[0]['value']
					if status != last_status and not flag:
						s = s + status + name
						flag = True
						last_status = status
					elif status != last_status:
						if not flag_2:
							s = s + f"与{status}{name}"
							flag_2 = True
						else:
							s = s + f"，{status}{name}"
						last_status = status
					elif status == status:
						s = s + f"、{name}"
					if abbr:
						abbreviation = [x['value'] for x in infos if x['item'] == '简称'] + [[]][0]
						if abbreviation:
							s = s + f"(以下简称“{abbreviation[0]}”)"

		if '仲裁协议' in [x['item'] for x in type_item]:
			contract = [x['value'] for x in case_info if x['item'] == '仲裁协议'] + [[]][0]
			if contract:
				s = s + f"之间因{contract[0]}所引起的争议仲裁案"
				if abbr:
					abbreviation = [x['value'] for x in case_info if x['item'] == '仲裁协议简称'] + [[]][0]
					if abbreviation:
						s = s + f"(以下简称“{abbreviation[0]}”)"
		elif '案由' in [x['item'] for x in type_item]:
			cause = [x['value'] for x in case_info if (x['item'] == '案由')] + [[]][0]
			if cause:
				grade = [x['value'] for x in case_info if (x['item'] == '审级')] + [[]][0]
				if grade and grade != "一审":
					s = s + f"之间的{cause[0]}{grade[0]}案件"
				else:
					s = s + f"之间的{cause[0]}案件"					

		num = [x['value'] for x in case_info if (x['item'] == '案号')] + [[]][0]
		if num:
			s = s + f"[案号：{num[0]}]"

		return s


