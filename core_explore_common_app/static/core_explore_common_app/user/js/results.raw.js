var getDataSourcesHTMLUrl = "{% url 'core_explore_common_data_sources_html' %}";
var dataSortingFields = "{{data.data_sorting_fields}}";
var displayPersistentQueryButton = '{{display_persistent_query_button}}';
var defaultDataSortingFields = '{{data.default_data_sorting_fields}}';
var defaultDateToggleValue = '{{data.default_date_toggle_value}}'
var editRecordUrl = "{% url 'core_dashboard_edit_record' %}";
var openXMLRecordUrl = "{% url 'core_main_app_xml_text_editor_view' %}";
var openJSONRecordUrl = "{% url 'core_main_app_json_text_editor_view' %}";