from tools.base import ToolDef, resolve_tools


def test_tool_override_logic():

    Tools = [
        ToolDef(tool_name="web_search"),
        ToolDef(tool_name="calculator"),
        ToolDef(tool_name="wiki_search"),
    ]

    overrides = {"web_search": ToolDef(tool_name="web_search", kwargs={"test_kwarg": "test string"})}

    resolve_tools(Tools, overrides)

    assert Tools[0].tool_name == "web_search"
    assert Tools[0].kwargs == {"test_kwarg": "test string"}

    assert Tools[1].tool_name == "calculator"
    assert not Tools[1].kwargs

    assert Tools[2].tool_name == "wiki_search"
    assert not Tools[2].kwargs
