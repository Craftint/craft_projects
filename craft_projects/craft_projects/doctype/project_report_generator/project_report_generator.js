// Copyright (c) 2023, Craftinteractive and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Report Generator', {
	refresh: function(frm){
		frm.add_custom_button(__('Generate'), function(){
			get_task_details(frm)
		})
	},
	project: function(frm){
		frm.clear_table("project_tasks")
		frm.refresh_fields("project_tasks")
	}
});

var get_task_details = function(frm){
	console.log("Heree")
	frappe.call({
		method: "get_task_details",
		args: {
			document: frm.doc.name,
			project: frm.doc.project
		},
		callback: function(r){
			frm.clear_table("project_tasks")
			if(r.data.length){
				$.each(r.data, (k, task)=>{
					let child = frm.add_child("project_tasks", task)
					child.display_order = child.idx
				})
			}
			frm.refresh_fields("project_tasks")
			frm.save()
		}
	})
}