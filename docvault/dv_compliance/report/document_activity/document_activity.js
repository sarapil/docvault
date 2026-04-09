// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// License: MIT

frappe.query_reports["Document Activity"] = {
	filters: [
		{
			fieldname: "category",
			label: __("Category"),
			fieldtype: "Link",
			options: "DV Category",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nActive\nArchived\nExpired",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
	],
};
