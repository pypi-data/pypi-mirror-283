#-----------------------------------------------------------------------------
# Copyright (c) Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import io
import os
from contextlib import contextmanager
from os.path import abspath, expanduser, splitext
from tempfile import mkstemp
from typing import (
    TYPE_CHECKING,
    Any,
    Iterator,
    cast,
)

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

# Bokeh imports
from ..core.types import PathLike
from ..document import Document
from ..embed import file_html
from ..resources import INLINE, Resources
from ..themes import Theme
from ..util.warnings import warn
from .state import State, curstate
from .util import default_filename

if TYPE_CHECKING:
    from PIL import Image

    from ..models.plots import Plot
    from ..models.ui import UIElement

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'export_png',
    'export_svg',
    'export_svgs',
    'get_layout_html',
    'get_screenshot_as_png',
    'get_svgs',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def export_png(obj: UIElement | Document, *, filename: PathLike | None = None, width: int | None = None,
        height: int | None = None, scale_factor: float = 1, webdriver: WebDriver | None = None,
        timeout: int = 5, state: State | None = None) -> str:
    ''' Export the ``UIElement`` object or document as a PNG.

    If the filename is not given, it is derived from the script name (e.g.
    ``/foo/myplot.py`` will create ``/foo/myplot.png``)

    Args:
        obj (UIElement or Document) : a Layout (Row/Column), Plot or Widget
            object or Document to export.

        filename (PathLike, e.g. str, Path, optional) : filename to save document under (default: None)
            If None, infer from the filename.

        width (int) : the desired width of the exported layout obj only if
            it's a Plot instance. Otherwise the width kwarg is ignored.

        height (int) : the desired height of the exported layout obj only if
            it's a Plot instance. Otherwise the height kwarg is ignored.

        scale_factor (float, optional) : A factor to scale the output PNG by,
            providing a higher resolution while maintaining element relative
            scales.

        webdriver (selenium.webdriver) : a selenium webdriver instance to use
            to export the image.

        timeout (int) : the maximum amount of time (in seconds) to wait for
            Bokeh to initialize (default: 5) (Added in 1.1.1).

        state (State, optional) :
            A :class:`State` object. If None, then the current default
            implicit state is used. (default: None).

    Returns:
        filename (str) : the filename where the static file is saved.

    If you would like to access an Image object directly, rather than save a
    file to disk, use the lower-level :func:`~bokeh.io.export.get_screenshot_as_png`
    function.

    .. warning::
        Responsive sizing_modes may generate layouts with unexpected size and
        aspect ratios. It is recommended to use the default ``fixed`` sizing mode.

    '''
    image = get_screenshot_as_png(obj, width=width, height=height, scale_factor=scale_factor, driver=webdriver,
                                  timeout=timeout, state=state)

    if filename is None:
        filename = default_filename("png")

    if image.width == 0 or image.height == 0:
        raise ValueError("unable to save an empty image")

    filename = os.fspath(filename) # XXX: Image.save() doesn't fully support PathLike
    image.save(filename)

    return abspath(expanduser(filename))

def export_svg(obj: UIElement | Document, *, filename: PathLike | None = None, width: int | None = None,
        height: int | None = None, webdriver: WebDriver | None = None, timeout: int = 5, state: State | None = None) -> list[str]:
    ''' Export a layout as SVG file or a document as a set of SVG files.

    If the filename is not given, it is derived from the script name
    (e.g. ``/foo/myplot.py`` will create ``/foo/myplot.svg``)

    Args:
        obj (UIElement object) : a Layout (Row/Column), Plot or Widget object to display

        filename (PathLike, e.g. str, Path, optional) : filename to save document under (default: None)
            If None, infer from the filename.

        width (int) : the desired width of the exported layout obj only if
            it's a Plot instance. Otherwise the width kwarg is ignored.

        height (int) : the desired height of the exported layout obj only if
            it's a Plot instance. Otherwise the height kwarg is ignored.

        webdriver (selenium.webdriver) : a selenium webdriver instance to use
            to export the image.

        timeout (int) : the maximum amount of time (in seconds) to wait for
            Bokeh to initialize (default: 5)

        state (State, optional) :
            A :class:`State` object. If None, then the current default
            implicit state is used. (default: None).

    Returns:
        filenames (list(str)) : the list of filenames where the SVGs files are saved.

    .. warning::
        Responsive sizing_modes may generate layouts with unexpected size and
        aspect ratios. It is recommended to use the default ``fixed`` sizing mode.

    '''
    svgs = get_svg(obj, width=width, height=height, driver=webdriver, timeout=timeout, state=state)
    return _write_collection(svgs, filename, "svg")

def export_svgs(obj: UIElement | Document, *, filename: str | None = None, width: int | None = None,
        height: int | None = None, webdriver: WebDriver | None = None, timeout: int = 5, state: State | None = None) -> list[str]:
    ''' Export the SVG-enabled plots within a layout. Each plot will result
    in a distinct SVG file.

    If the filename is not given, it is derived from the script name
    (e.g. ``/foo/myplot.py`` will create ``/foo/myplot.svg``)

    Args:
        obj (UIElement object) : a Layout (Row/Column), Plot or Widget object to display

        filename (str, optional) : filename to save document under (default: None)
            If None, infer from the filename.

        width (int) : the desired width of the exported layout obj only if
            it's a Plot instance. Otherwise the width kwarg is ignored.

        height (int) : the desired height of the exported layout obj only if
            it's a Plot instance. Otherwise the height kwarg is ignored.

        webdriver (selenium.webdriver) : a selenium webdriver instance to use
            to export the image.

        timeout (int) : the maximum amount of time (in seconds) to wait for
            Bokeh to initialize (default: 5) (Added in 1.1.1).

        state (State, optional) :
            A :class:`State` object. If None, then the current default
            implicit state is used. (default: None).

    Returns:
        filenames (list(str)) : the list of filenames where the SVGs files are saved.

    .. warning::
        Responsive sizing_modes may generate layouts with unexpected size and
        aspect ratios. It is recommended to use the default ``fixed`` sizing mode.

    '''
    svgs = get_svgs(obj, width=width, height=height, driver=webdriver, timeout=timeout, state=state)

    if len(svgs) == 0:
        log.warning("No SVG Plots were found.")
        return []

    return _write_collection(svgs, filename, "svg")

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

def get_screenshot_as_png(obj: UIElement | Document, *, driver: WebDriver | None = None, timeout: int = 5,
        resources: Resources = INLINE, width: int | None = None, height: int | None = None,
        scale_factor: float = 1, state: State | None = None) -> Image.Image:
    ''' Get a screenshot of a ``UIElement`` object.

    Args:
        obj (UIElement or Document) : a Layout (Row/Column), Plot or Widget
            object or Document to export.

        driver (selenium.webdriver) : a selenium webdriver instance to use
            to export the image.

        timeout (int) : the maximum amount of time to wait for initialization.
            It will be used as a timeout for loading Bokeh, then when waiting for
            the layout to be rendered.

        scale_factor (float, optional) : A factor to scale the output PNG by,
            providing a higher resolution while maintaining element relative
            scales.

        state (State, optional) :
            A :class:`State` object. If None, then the current default
            implicit state is used. (default: None).

    Returns:
        image (PIL.Image.Image) : a pillow image loaded from PNG.

    .. warning::
        Responsive sizing_modes may generate layouts with unexpected size and
        aspect ratios. It is recommended to use the default ``fixed`` sizing mode.

    '''
    from .webdriver import (
        get_web_driver_device_pixel_ratio,
        scale_factor_less_than_web_driver_device_pixel_ratio,
        webdriver_control,
    )

    with _tmp_html() as tmp:
        theme = (state or curstate()).document.theme
        html = get_layout_html(obj, resources=resources, width=width, height=height, theme=theme)
        with open(tmp.path, mode="w", encoding="utf-8") as file:
            file.write(html)

        if driver is not None:
            web_driver = driver
            if not scale_factor_less_than_web_driver_device_pixel_ratio(scale_factor, web_driver):
                device_pixel_ratio = get_web_driver_device_pixel_ratio(web_driver)
                raise ValueError(f'Expected the web driver to have a device pixel ratio greater than {scale_factor}. '
                                 f'Was given a web driver with a device pixel ratio of {device_pixel_ratio}.')
        else:
            web_driver = webdriver_control.get(scale_factor=scale_factor)
        web_driver.maximize_window()
        web_driver.get(f"file://{tmp.path}")
        wait_until_render_complete(web_driver, timeout)
        [width, height, dpr] = _maximize_viewport(web_driver)
        png = web_driver.get_screenshot_as_png()

    from PIL import Image
    return (Image.open(io.BytesIO(png))
                 .convert("RGBA")
                 .crop((0, 0, width*dpr, height*dpr))
                 .resize((int(width*scale_factor), int(height*scale_factor))))

def get_svg(obj: UIElement | Document, *, driver: WebDriver | None = None, timeout: int = 5,
        resources: Resources = INLINE, width: int | None = None, height: int | None = None, state: State | None = None) -> list[str]:
    from .webdriver import webdriver_control

    with _tmp_html() as tmp:
        theme = (state or curstate()).document.theme
        html = get_layout_html(obj, resources=resources, width=width, height=height, theme=theme)
        with open(tmp.path, mode="w", encoding="utf-8") as file:
            file.write(html)

        web_driver = driver if driver is not None else webdriver_control.get()
        web_driver.get(f"file://{tmp.path}")
        wait_until_render_complete(web_driver, timeout)
        svgs = cast(list[str], web_driver.execute_script(_SVG_SCRIPT))

    return svgs

def get_svgs(obj: UIElement | Document, *, driver: WebDriver | None = None, timeout: int = 5,
        resources: Resources = INLINE, width: int | None = None, height: int | None = None, state: State | None = None) -> list[str]:
    from .webdriver import webdriver_control

    with _tmp_html() as tmp:
        theme = (state or curstate()).document.theme
        html = get_layout_html(obj, resources=resources, width=width, height=height, theme=theme)
        with open(tmp.path, mode="w", encoding="utf-8") as file:
            file.write(html)

        web_driver = driver if driver is not None else webdriver_control.get()
        web_driver.get(f"file://{tmp.path}")
        wait_until_render_complete(web_driver, timeout)
        svgs = cast(list[str], web_driver.execute_script(_SVGS_SCRIPT))

    return svgs

def get_layout_html(obj: UIElement | Document, *, resources: Resources = INLINE,
        width: int | None = None, height: int | None = None, theme: Theme | None = None) -> str:
    '''

    '''
    template = r"""\
    {% block preamble %}
    <style>
        html, body {
            box-sizing: border-box;
            width: 100%;
            height: 100%;
            margin: 0;
            border: 0;
            padding: 0;
            overflow: hidden;
        }
    </style>
    {% endblock %}
    """

    def html() -> str:
        return file_html(
            obj,
            resources=resources,
            title="",
            template=template,
            theme=theme,
            suppress_callback_warning=True,
            _always_new=True,
        )

    if width is not None or height is not None:
        # Defer this import, it is expensive
        from ..models.plots import Plot
        if not isinstance(obj, Plot):
            warn("Export method called with width or height argument on a non-Plot model. The size values will be ignored.")
        else:
            with _resized(obj, width, height):
                return html()

    return html()

def wait_until_render_complete(driver: WebDriver, timeout: int) -> None:
    '''

    '''
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.wait import WebDriverWait

    def is_bokeh_loaded(driver: WebDriver) -> bool:
        return cast(bool, driver.execute_script('''
            return typeof Bokeh !== "undefined" && Bokeh.documents != null && Bokeh.documents.length != 0
        '''))

    try:
        WebDriverWait(driver, timeout, poll_frequency=0.1).until(is_bokeh_loaded)
    except TimeoutException as e:
        _log_console(driver)
        raise RuntimeError('Bokeh was not loaded in time. Something may have gone wrong.') from e

    driver.execute_script(_WAIT_SCRIPT)

    def is_bokeh_render_complete(driver: WebDriver) -> bool:
        return cast(bool, driver.execute_script('return window._bokeh_render_complete;'))

    try:
        WebDriverWait(driver, timeout, poll_frequency=0.1).until(is_bokeh_render_complete)
    except TimeoutException:
        log.warning("The webdriver raised a TimeoutException while waiting for "
                    "a 'bokeh:idle' event to signify that the layout has rendered. "
                    "Something may have gone wrong.")
    finally:
        _log_console(driver)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

@contextmanager
def _resized(obj: Plot, width: int | None, height: int | None) -> Iterator[None]:
    old_width = obj.width
    old_height = obj.height

    if width is not None:
        obj.width = width
    if height is not None:
        obj.height = height

    yield

    obj.width = old_width
    obj.height = old_height

def _write_collection(items: list[str], filename: PathLike | None, ext: str) -> list[str]:
    if filename is None:
        filename = default_filename(ext)
    filename = os.fspath(filename)

    filenames: list[str] = []

    def _indexed(name: str, i: int) -> str:
        basename, ext = splitext(name)
        return f"{basename}_{i}{ext}"

    for i, item in enumerate(items):
        fname = filename if i == 0 else _indexed(filename, i)

        with open(fname, mode="w", encoding="utf-8") as f:
            f.write(item)

        filenames.append(fname)

    return filenames

def _log_console(driver: WebDriver) -> None:
    levels = {'WARNING', 'ERROR', 'SEVERE'}
    try:
        logs = driver.get_log('browser')
    except Exception:
        return
    messages = [ log.get("message") for log in logs if log.get('level') in levels ]
    if len(messages) > 0:
        log.warning("There were browser warnings and/or errors that may have affected your export")
        for message in messages:
            log.warning(message)

def _maximize_viewport(web_driver: WebDriver) -> tuple[int, int, int]:
    calculate_viewport_size = """\
        const root_view = Bokeh.index.roots[0]
        const {width, height} = root_view.el.getBoundingClientRect()
        return [Math.round(width), Math.round(height), window.devicePixelRatio]
    """
    viewport_size: tuple[int, int, int] = web_driver.execute_script(calculate_viewport_size)
    calculate_window_size = """\
        const [width, height, dpr] = arguments
        return [
            // XXX: outer{Width,Height} can be 0 in headless mode under certain window managers
            Math.round(Math.max(0, window.outerWidth - window.innerWidth) + width*dpr),
            Math.round(Math.max(0, window.outerHeight - window.innerHeight) + height*dpr),
        ]
    """
    [width, height] = web_driver.execute_script(calculate_window_size, *viewport_size)
    eps = 100 # XXX: can't set window size exactly in certain window managers, crop it to size later
    web_driver.set_window_size(width + eps, height + eps)
    return viewport_size

# TODO: consider UIElement like Pane
_SVGS_SCRIPT = """
const {LayoutDOMView} = Bokeh.require("models/layouts/layout_dom")
const {PlotView} = Bokeh.require("models/plots/plot")

function* collect_svgs(views) {
  for (const view of views) {
    if (view instanceof LayoutDOMView) {
      yield* collect_svgs(view.child_views.values())
    }
    if (view instanceof PlotView && view.model.output_backend == "svg") {
      const {ctx} = view.canvas_view.compose()
      yield ctx.get_serialized_svg(true)
    }
  }
}

return [...collect_svgs(Bokeh.index)]
"""

_SVG_SCRIPT = """\
function* export_svgs(views) {
  for (const view of views) {
    // TODO: use to_blob() API in future
    const {ctx} = view.export("svg")
    yield ctx.get_serialized_svg(true)
  }
}

return [...export_svgs(Bokeh.index)]
"""

_WAIT_SCRIPT = """
// add private window prop to check that render is complete
window._bokeh_render_complete = false;
function done() {
  window._bokeh_render_complete = true;
}

const doc = Bokeh.documents[0];

if (doc.is_idle)
  done();
else
  doc.idle.connect(done);
"""


class _TempFile:
    _closed: bool = False

    fd: int
    path: str

    def __init__(self, *, prefix: str = "tmp", suffix: str = "") -> None:
        # XXX: selenium has issues with /tmp directory (or equivalent), so try using the
        # current directory first, if writable, and otherwise fall back to the system
        # default tmp directory.
        try:
            self.fd, self.path = mkstemp(prefix=prefix, suffix=suffix, dir=os.getcwd())
        except OSError:
            self.fd, self.path = mkstemp(prefix=prefix, suffix=suffix)

    def __enter__(self) -> _TempFile:
        return self

    def __exit__(self, exc: Any, value: Any, tb: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        if self._closed:
            return

        try:
            os.close(self.fd)
        except OSError:
            pass

        try:
            os.unlink(self.path)
        except OSError:
            pass

        self._closed = True

def _tmp_html() -> _TempFile:
    return _TempFile(prefix="bokeh", suffix=".html")

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
