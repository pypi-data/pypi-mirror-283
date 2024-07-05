# Part of TAP-Producer.
# See LICENSE.txt in the project root for details.
"""Test Anything Protocol tools."""
from __future__ import annotations

import os
import sys
import warnings
from collections import Counter
from contextlib import ContextDecorator
from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Generator
from typing import NoReturn
from typing import TextIO

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

OK = 'ok'
NOT_OK = 'not_ok'
SKIP = 'skip'
PLAN = 'plan'


def _warn_format(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: str | None = None,
) -> str:
    """Test Anything Protocol formatted warnings."""
    return f'# {category.__name__}\n'  # pragma: no cover


def _warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    line: TextIO | None = None,
    stacklevel: int = 1,
) -> None:
    """emit a TAP formatted warning."""
    sys.stdout.write(f'not ok {message}\n')  # pragma: no cover
    sys.stderr.write(  # pragma: no cover
        warnings.formatwarning(message, category, filename, lineno),
    )


class TAP(ContextDecorator):
    """Test Anything Protocol warnings for TAP Producer APIs with a simple decorator.

    Redirects warning messages to stdout with the diagnostic printed to stderr.

    All TAP API calls reference the same thread context.

    .. note::
        Subtests are not implemented.

    .. note::
        Not known to be thread-safe.
    """

    _formatwarning = staticmethod(warnings.formatwarning)
    _showwarning = staticmethod(warnings.showwarning)
    _count = Counter(ok=0, not_ok=0, skip=0, plan=0)

    @classmethod
    def end(cls: type[Self], skip_reason: str = '') -> NoReturn:
        """End a TAP diagnostic.

        :param skip_reason: A skip reason, optional, defaults to ''.
        :type skip_reason: str, optional
        :return: Exits the diagnostic.
        :rtype: NoReturn
        """
        skip_count = cls.skip_count()
        if skip_reason != '' and skip_count == 0:
            TAP.diagnostic('unnecessary argument "skip_reason" to TAP.end')
        if cls._count[PLAN] < 1:
            TAP.plan(count=None, skip_reason=skip_reason, skip_count=skip_count)
        exit(0)

    @staticmethod
    def diagnostic(*message: str) -> None:
        r"""Print a diagnostic message.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """
        formatted = ' - '.join(message).strip()
        sys.stderr.write(f'# {formatted}\n')

    @staticmethod
    def bail_out(*message: str) -> NoReturn:
        r"""Print a bail out message and exit.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        """
        print('Bail out!', *message, file=sys.stderr)
        sys.exit(1)

    @classmethod
    def skip_count(
        cls: type[Self],
    ) -> int:
        """Get the current skip count.

        :return: skip count
        :rtype: int
        """
        try:
            skip_count = cls._count.pop(SKIP)
        except KeyError:  # pragma: no cover
            TAP.diagnostic('Possible thread violation by TAP producer.')
            skip_count = 0
        return skip_count

    @classmethod
    def plan(  # noqa: C901
        cls: type[Self],
        count: int | None = None,
        skip_reason: str = '',
        skip_count: int | None = None,
    ) -> None:
        """Print a TAP test plan.

        :param count: planned test count, defaults to None
        :type count: int | None, optional
        :param skip_reason: diagnostic to print, defaults to ''
        :type skip_reason: str, optional
        :param skip_count: number of tests skipped, defaults to None
        :type skip_count: int | None, optional
        """
        count = cls._count.total() if count is None else count
        if skip_count is None:
            skip_count = cls.skip_count()
        if skip_reason != '' and skip_count == 0:
            TAP.diagnostic('unnecessary argument "skip_reason" to TAP.plan')
        if cls._count[PLAN] < 1:
            cls._count[PLAN] += 1
            match [count, skip_reason, skip_count]:
                case [n, r, s] if r == '' and s > 0:  # type: ignore
                    TAP.diagnostic('items skipped', str(s))
                    sys.stdout.write(f'1..{n}\n')
                case [n, r, s] if r != '' and s > 0:  # type: ignore
                    TAP.diagnostic('items skipped', str(s))
                    sys.stdout.write(f'1..{n} # SKIP {r}\n')
                case [n, r, s] if r == '' and s == 0:
                    sys.stdout.write(f'1..{n}\n')
                case _:  # pragma: no cover
                    TAP.bail_out('TAP.plan failed due to invalid arguments.')
        else:
            TAP.diagnostic('TAP.plan called more than once during session.')

    @staticmethod
    @contextmanager
    def suppress() -> Generator[None, Any, None]:  # pragma: defer to python
        """Suppress output from TAP Producers.

        Suppresses the following output to stderr:

        * ``warnings.warn``
        * ``TAP.bail_out``
        * ``TAP.diagnostic``

        and ALL output to stdout.

        .. note::
            Does not suppress Python exceptions.
        """
        warnings.simplefilter('ignore')
        null = Path(os.devnull).open('w')
        with redirect_stdout(null):
            with redirect_stderr(null):
                yield
        null.close()
        warnings.resetwarnings()

    @staticmethod
    @contextmanager
    def strict() -> Generator[None, Any, None]:  # pragma: defer to OZI
        """Transform any ``warn()`` or ``TAP.not_ok()`` calls into Python errors.

        .. note::
            Implies non-TAP output.
        """
        warnings.simplefilter('error', category=RuntimeWarning, append=True)
        yield
        warnings.resetwarnings()

    @classmethod
    def ok(cls: type[Self], *message: str, skip: bool = False) -> None:
        r"""Mark a test result as successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """
        cls._count[OK] += 1
        cls._count[SKIP] += 1 if skip else 0
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip()
        sys.stdout.write(
            f'ok {cls._count.total() - cls._count[SKIP]} {directive} {formatted}\n',
        )

    @classmethod
    def not_ok(cls: type[Self], *message: str, skip: bool = False) -> None:
        r"""Mark a test result as :strong:`not` successful.

        :param \*message: messages to print to TAP output
        :type \*message: tuple[str]
        :param skip: mark the test as skipped, defaults to False
        :type skip: bool, optional
        """
        cls._count[NOT_OK] += 1
        cls._count[SKIP] += 1 if skip else 0
        directive = '-' if not skip else '# SKIP'
        formatted = ' - '.join(message).strip()
        warnings.formatwarning = _warn_format
        warnings.showwarning = _warn  # type: ignore
        warnings.warn(
            f'{cls._count.total() - cls._count[SKIP]} {directive} {formatted}',
            RuntimeWarning,
            stacklevel=2,
        )
        warnings.formatwarning = cls._formatwarning  # pragma: no cover
        warnings.showwarning = cls._showwarning  # pragma: no cover
