var getDataSourcesHTMLUrl = "{% url 'core_explore_common_data_sources_html' %}";
var data_sorting_fields = "{{data.data_sorting_fields}}".trim().split(',');
var displayLastModificationDate = '{{data.display_last_modification_date}}'
var data_permissions_url = "{% url 'core_main_app_rest_data_permissions' %}"
var editRecordUrl = "{% url 'core_dashboard_edit_record' %}";