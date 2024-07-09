from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuButton, PluginMenuItem

from netbox_swupdate.utils import link_adapter

repository_buttons = [
    PluginMenuButton(
        title="Add",
        link=link_adapter("repository_add"),
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
    ),
]

menu_items = (
    PluginMenuItem(
        link=link_adapter("repository_list"),
        link_text="Repository",
        buttons=repository_buttons,
    ),
)
