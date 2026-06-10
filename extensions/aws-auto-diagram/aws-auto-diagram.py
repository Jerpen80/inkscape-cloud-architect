import inkex
from pathlib import Path

from ica_utils.config import load_config
from ica_utils.engine import RenderDoc


class aws_auto_diagram(inkex.EffectExtension):
    """Inkscape extension entry point.

    This is a thin wrapper: the actual rendering lives in ``ica_utils.engine``
    so the same implementation can run headless (via ``engine.render()``) and
    from inside Inkscape. ``effect()`` binds a ``RenderDoc`` to the live
    ``self.svg`` and delegates.
    """

    def add_arguments(self, pars):
        pars.add_argument("--theme", type=str, default="light")
        pars.add_argument("--layout_mode", type=str, default="spaced")
        pars.add_argument("--account_name", type=str, default="")
        pars.add_argument("--data_dir", type=str, default="")
        pars.add_argument("--region", type=str, default="eu-west-1")

    def effect(self):
        extension_dir = str(Path(__file__).parent)
        config = load_config(extension_dir)
        doc = RenderDoc(self.svg, config=config, options=self.options)
        doc.render()


if __name__ == '__main__':
    aws_auto_diagram().run()
