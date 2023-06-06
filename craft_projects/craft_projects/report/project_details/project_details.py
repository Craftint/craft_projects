# Copyright (c) 2023, Dany and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			'label':_('Name'),
			'fieldname':'name',
			'fieldtype':'Link',
			'options':'Task'
		},
		{
			'label':_('Status'),
			'fieldname': 'status',
			'fieldtype':'Select',
			'options': [
				'Open',
				'Assigned',
				'Pending Documents - External',
				'Pending Documents - Internal',
				'Working',
				'Pending Review',
				'Overdue',
				'Completed',
				'Cancelled',
				'Template'
				]
		},
		{
			'label':_('Actual Start Date'),
			'fieldtype':'Date',
			'fieldname': 'actual_start_date',
			'width':100
		},
		{
			'label':_('Actual End Date'),
			'fieldtype':'Date',
			'fieldname': 'completed_on',
			'width':100
		},
		{
			'label':_('Expected Start Date'),
			'fieldname':'exp_start_date',
			'fieldtype':'Date',
			'width':100
		},
		{
			'label':_('Expected End Date'),
			'fieldname':'exp_end_date',
			'fieldtype':'Date',
			'width':100
		},
		{
			'label':'Duration',
			'fieldname':'actual_duration',
			'fieldtype':'Float'
		},
		{
			'label':'Task Name',
			'fieldname':'subject',
			'fieldtype':'Data'
		},
		{
			'label':_('Employee'),
			'fieldname':'employee',
			'fieldtype':'Link',
			'options':'Employee'
		},
		{
			'label':_('Employee Name'),
			'fieldname':'employee_name',
			'fieldtype':'Data',
		},
		{
			'label':_('Assignee'),
			'fieldname':'teams_involved',
			'fieldtype':'Data',
		},
		{
			'label':'Project',
			'fieldname':'project',
			'fieldtype':'Link',
			'options':'Project'
		},
		{
			'label':'Type',
			'fieldname':'type',
			'fieldtype':'Link',
			'options':'Task Type',
		},
		{
			'label':'Task Description',
			'fieldname': 'description',
			'fieldtype':'Text Editor'
		},
		{
			'label':'Is Milestone',
			'fieldname':'is_milestone',
			'fieldtype':'Check'
		}
	]


	if filters.show_priorities:
		columns.append({'label':'Priority','fieldname':'priority','fieldtype':'Select','options':['Low','Medium','High','Urgent']})


	return columns

def get_data(filters):
	fields = []
	columns = get_columns(filters)

	for field in columns:
		fields.append(field["fieldname"])

	# Get Data
	if filters.get('show_priorities'):
		del filters['show_priorities']
	tasks = frappe.db.get_list("Task", filters=filters, fields=fields)

	# Sort by actual date
	try:
		data = sorted(tasks, key=lambda d:d["actual_start_date"])
	except:
		data = tasks

	type_weight = get_task_type_dict(data)

	# Get details
	project_manager = ""
	project_title = ""
	company = "Craft Interactive"
	if filters.get("project"):
		project_title = frappe.db.get_value("Project", filters.get("project"), "project_name")
		project_manager = frappe.db.get_value("Project", filters.get("project"), "project_owner_name")
		company = frappe.db.get_value("Project", filters.get("project"), "company")

	date = frappe.utils.nowdate()

	data.append({"project_title":project_title,"company":company, "project_manager": project_manager, "date":date, "type_weight":type_weight})

	return data

def get_task_type_dict(data):
	types = []
	type_weight = []

	for row in data:
		types.append(row["type"])
	
	types = list(set(types))

	for type in types:
		type_weight.append({"type": type, "weight": frappe.db.get_value("Task Type", type, "weight")})
		
	if type_weight:
		type_weight = sorted(type_weight, key=lambda d:d["weight"])

	return type_weight
	