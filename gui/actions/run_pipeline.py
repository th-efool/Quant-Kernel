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
    indicator = ui_refs["indicator_selector"].get_value()
    strategy = ui_refs["strategy_selector"].get_value()

    df = controller.run_pipeline(
        api_info=api_info,
        fetch_config=fetch_config,
        indicator=indicator,
        strategy=strategy,
    )

    ui_refs["chart"].set_data(df)
