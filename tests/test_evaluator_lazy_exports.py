import sys


def test_calc_evaluator_exports_do_not_load_unrelated_metric_stacks():
    from desktop_env.evaluators import metrics

    assert "desktop_env.evaluators.metrics.docs" not in sys.modules
    assert "desktop_env.evaluators.metrics.vlc" not in sys.modules

    assert metrics.compare_table.__module__ == "desktop_env.evaluators.metrics.table"
    assert "desktop_env.evaluators.metrics.docs" not in sys.modules
    assert "desktop_env.evaluators.metrics.vlc" not in sys.modules


def test_file_getters_load_without_chrome_getters():
    from desktop_env.evaluators import getters

    assert getters.get_cloud_file.__module__ == "desktop_env.evaluators.getters.file"
    assert getters.get_vm_file.__module__ == "desktop_env.evaluators.getters.file"
    assert "desktop_env.evaluators.getters.chrome" not in sys.modules
