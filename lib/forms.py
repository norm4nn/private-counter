from nc_py_api.ex_app import SettingsForm, SettingsField, SettingsFieldType

SETTINGS_FORM = SettingsForm(
    id="private_counter",
    section_type="admin",
    section_id="declarative_settings",
    title="Private Counter Settings",
    description="These settings are used to configure the private counter app.",
    fields=[
        SettingsField(
            id="scan_path",
            title="Scan Path",
            description="Path to scan for counter images",
            type=SettingsFieldType.TEXT,
            default="/"
        ),
        SettingsField(
            id="output_path",
            title="CSV Output Path",
            description="Path to the output CSV file, in which results will be saved",
            type=SettingsFieldType.TEXT,
            default="/output.csv",
        ),
        SettingsField(
            id="scan_interval",
            title="Scan Interval",
            description="Interval in minutes to scan for new images",
            type=SettingsFieldType.NUMBER,
            default=5
        ),
        SettingsField(
            id="enabled",
            title="Enabled",
            description="Enable or disable images scanning",
            type=SettingsFieldType.CHECKBOX,
            default=True
        )
    ],
)
