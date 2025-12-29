# gui/actions/run_pipeline.py

def run_pipeline_action(controller, ui_refs):
    """
    Reads UI state, executes pipeline, updates chart.
    """

    api_info = ui_refs["api_selector"].get_value()
    if not api_info:
        print("No API / ticker selected")
        return

    fetch_config = ui_refs["fetch_config"].get_value()
    indicators = ui_refs["indicators"].get_value()
    strategies = ui_refs["strategies"].get_value()

    for ind in indicators:
        controller.strategy_manager._indicator_manager.add(ind)

    for strat in strategies:
        controller.strategy_manager.add(strat)

    df = controller.run_pipeline(
        api_info=api_info,
        fetch_config=fetch_config,
        indicators=indicators,
        strategies=strategies,
    )

    ui_refs["chart"].set_data(df)
