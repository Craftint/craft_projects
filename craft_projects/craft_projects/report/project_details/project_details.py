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
			'fieldname':'expected_time',
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
			'label':'Assignee',
			'fieldname':'employee_name',
			'fieldtype':'Data',
		},
		{
			'label':'Project',
			'fieldname':'project',
			'fieldtype':'Link',
			'options':'Project'
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
	data = frappe.db.get_list("Task", filters=filters, fields=fields)

	project_manager = ""
	
	if filters.get("project"):
		project_manager = frappe.db.get_value("Project", filters.get("project"), "project_owner_name")

	date = frappe.utils.nowdate()

	data.append({"company":"Craft Interactive", "project_manager": project_manager, "date":date})

	return data