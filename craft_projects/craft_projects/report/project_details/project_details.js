// Copyright (c) 2023, Dany and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Details"] = {
	"filters": [
		{
			'label':__('Project'),
			'fieldname':'project',
			'fieldtype':'Link',
			'options':'Project',
			'reqd':'1'
		},
		{
			'label':'Is Milestone',
			'fieldname':'is_milestone',
			'fieldtype':'Check'
		},
		{
			'label':'Show Priorities',
			'fieldname':'show_priorities',
			'fieldtype':'Check'
		}
	]
};
