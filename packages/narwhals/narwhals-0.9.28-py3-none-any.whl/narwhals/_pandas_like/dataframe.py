from __future__ import annotations

import collections
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Literal
from typing import Sequence
from typing import overload

from narwhals._pandas_like.expr import PandasExpr
from narwhals._pandas_like.utils import create_native_series
from narwhals._pandas_like.utils import evaluate_into_exprs
from narwhals._pandas_like.utils import generate_unique_token
from narwhals._pandas_like.utils import horizontal_concat
from narwhals._pandas_like.utils import translate_dtype
from narwhals._pandas_like.utils import validate_dataframe_comparand
from narwhals._pandas_like.utils import validate_indices
from narwhals.dependencies import get_cudf
from narwhals.dependencies import get_modin
from narwhals.dependencies import get_numpy
from narwhals.dependencies import get_pandas
from narwhals.utils import flatten
from narwhals.utils import parse_version

if TYPE_CHECKING:
    from typing_extensions import Self

    from narwhals._pandas_like.group_by import PandasGroupBy
    from narwhals._pandas_like.namespace import PandasNamespace
    from narwhals._pandas_like.series import PandasSeries
    from narwhals._pandas_like.typing import IntoPandasExpr
    from narwhals.dtypes import DType


class PandasDataFrame:
    # --- not in the spec ---
    def __init__(
        self,
        dataframe: Any,
        *,
        implementation: str,
    ) -> None:
        self._validate_columns(dataframe.columns)
        self._dataframe = dataframe
        self._implementation = implementation

    def __narwhals_dataframe__(self) -> Self:
        return self

    def __narwhals_lazyframe__(self) -> Self:
        return self

    def __narwhals_namespace__(self) -> PandasNamespace:
        from narwhals._pandas_like.namespace import PandasNamespace

        return PandasNamespace(self._implementation)

    def __native_namespace__(self) -> Any:
        if self._implementation == "pandas":
            return get_pandas()
        if self._implementation == "modin":  # pragma: no cover
            return get_modin()
        if self._implementation == "cudf":  # pragma: no cover
            return get_cudf()
        msg = f"Expected pandas/modin/cudf, got: {type(self._implementation)}"  # pragma: no cover
        raise AssertionError(msg)

    def __len__(self) -> int:
        return len(self._dataframe)

    def _validate_columns(self, columns: Sequence[str]) -> None:
        if len(columns) != len(set(columns)):
            counter = collections.Counter(columns)
            for col, count in counter.items():
                if count > 1:
                    msg = f"Expected unique column names, got {col!r} {count} time(s)"
                    raise ValueError(
                        msg,
                    )
            raise AssertionError("Pls report bug")

    def _from_dataframe(self, df: Any) -> Self:
        return self.__class__(
            df,
            implementation=self._implementation,
        )

    @overload
    def __getitem__(self, item: str) -> PandasSeries: ...

    @overload
    def __getitem__(self, item: slice) -> PandasDataFrame: ...

    def __getitem__(self, item: str | slice) -> PandasSeries | PandasDataFrame:
        if isinstance(item, str):
            from narwhals._pandas_like.series import PandasSeries

            return PandasSeries(
                self._dataframe.loc[:, item],
                implementation=self._implementation,
            )

        elif isinstance(item, (slice, Sequence)):
            from narwhals._pandas_like.dataframe import PandasDataFrame

            return PandasDataFrame(
                self._dataframe.iloc[item], implementation=self._implementation
            )
        elif (
            (np := get_numpy()) is not None
            and isinstance(item, np.ndarray)
            and item.ndim == 1
        ):
            return self._from_dataframe(self._dataframe.iloc[item])

        else:  # pragma: no cover
            msg = f"Expected str or slice, got: {type(item)}"
            raise TypeError(msg)

    # --- properties ---
    @property
    def columns(self) -> list[str]:
        return self._dataframe.columns.tolist()  # type: ignore[no-any-return]

    def rows(
        self, *, named: bool = False
    ) -> list[tuple[Any, ...]] | list[dict[str, Any]]:
        if not named:
            return list(self._dataframe.itertuples(index=False, name=None))

        return self._dataframe.to_dict(orient="records")  # type: ignore[no-any-return]

    def iter_rows(
        self,
        *,
        named: bool = False,
        buffer_size: int = 512,
    ) -> Iterator[list[tuple[Any, ...]]] | Iterator[list[dict[str, Any]]]:
        """
        NOTE:
            The param ``buffer_size`` is only here for compatibility with the polars API
            and has no effect on the output.
        """
        if not named:
            yield from self._dataframe.itertuples(index=False, name=None)
        else:
            yield from (row._asdict() for row in self._dataframe.itertuples(index=False))

    @property
    def schema(self) -> dict[str, DType]:
        return {
            col: translate_dtype(self._dataframe.loc[:, col])
            for col in self._dataframe.columns
        }

    # --- reshape ---
    def select(
        self,
        *exprs: IntoPandasExpr,
        **named_exprs: IntoPandasExpr,
    ) -> Self:
        new_series = evaluate_into_exprs(self, *exprs, **named_exprs)
        if not new_series:
            # return empty dataframe, like Polars does
            return self._from_dataframe(self._dataframe.__class__())
        new_series = validate_indices(new_series)
        df = horizontal_concat(
            new_series,
            implementation=self._implementation,
        )
        return self._from_dataframe(df)

    def drop_nulls(self) -> Self:
        return self._from_dataframe(self._dataframe.dropna(axis=0))

    def with_row_index(self, name: str) -> Self:
        row_index = create_native_series(
            range(len(self._dataframe)),
            index=self._dataframe.index,
            implementation=self._implementation,
        ).alias(name)
        return self._from_dataframe(
            horizontal_concat(
                [row_index._series, self._dataframe], implementation=self._implementation
            )
        )

    def filter(
        self,
        *predicates: IntoPandasExpr | Iterable[IntoPandasExpr],
    ) -> Self:
        from narwhals._pandas_like.namespace import PandasNamespace

        plx = PandasNamespace(self._implementation)
        expr = plx.all_horizontal(*predicates)
        # Safety: all_horizontal's expression only returns a single column.
        mask = expr._call(self)[0]
        _mask = validate_dataframe_comparand(self._dataframe.index, mask)
        return self._from_dataframe(self._dataframe.loc[_mask])

    def with_columns(
        self,
        *exprs: IntoPandasExpr,
        **named_exprs: IntoPandasExpr,
    ) -> Self:
        index = self._dataframe.index
        new_columns = evaluate_into_exprs(self, *exprs, **named_exprs)
        # If the inputs are all Expressions which return full columns
        # (as opposed to scalars), we can use a fast path (concat, instead of assign).
        # We can't use the fastpath if any input is not an expression (e.g.
        # if it's a Series) because then we might be changing its flags.
        # See `test_memmap` for an example of where this is necessary.
        fast_path = (
            all(len(s) > 1 for s in new_columns)
            and all(isinstance(x, PandasExpr) for x in exprs)
            and all(isinstance(x, PandasExpr) for (_, x) in named_exprs.items())
        )

        if fast_path:
            new_column_name_to_new_column_map = {s.name: s for s in new_columns}
            to_concat = []
            # Make sure to preserve column order
            for name in self._dataframe.columns:
                if name in new_column_name_to_new_column_map:
                    to_concat.append(
                        validate_dataframe_comparand(
                            index, new_column_name_to_new_column_map.pop(name)
                        )
                    )
                else:
                    to_concat.append(self._dataframe.loc[:, name])
            to_concat.extend(
                validate_dataframe_comparand(index, new_column_name_to_new_column_map[s])
                for s in new_column_name_to_new_column_map
            )

            df = horizontal_concat(
                to_concat,
                implementation=self._implementation,
            )
        else:
            df = self._dataframe.assign(
                **{s.name: validate_dataframe_comparand(index, s) for s in new_columns}
            )
        return self._from_dataframe(df)

    def rename(self, mapping: dict[str, str]) -> Self:
        return self._from_dataframe(self._dataframe.rename(columns=mapping))

    def drop(self, *columns: str | Iterable[str]) -> Self:
        return self._from_dataframe(self._dataframe.drop(columns=list(flatten(columns))))

    # --- transform ---
    def sort(
        self,
        by: str | Iterable[str],
        *more_by: str,
        descending: bool | Sequence[bool] = False,
    ) -> Self:
        flat_keys = flatten([*flatten([by]), *more_by])
        df = self._dataframe
        if isinstance(descending, bool):
            ascending: bool | list[bool] = not descending
        else:
            ascending = [not d for d in descending]
        return self._from_dataframe(df.sort_values(flat_keys, ascending=ascending))

    # --- convert ---
    def collect(self) -> PandasDataFrame:
        return PandasDataFrame(
            self._dataframe,
            implementation=self._implementation,
        )

    # --- actions ---
    def group_by(self, *keys: str | Iterable[str]) -> PandasGroupBy:
        from narwhals._pandas_like.group_by import PandasGroupBy

        return PandasGroupBy(
            self,
            flatten(keys),
        )

    def join(
        self,
        other: Self,
        *,
        how: Literal["left", "inner", "outer", "cross", "anti"] = "inner",
        left_on: str | list[str] | None = None,
        right_on: str | list[str] | None = None,
    ) -> Self:
        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        if how == "cross":
            if self._implementation in {"modin", "cudf"} or (
                self._implementation == "pandas"
                and (pd := get_pandas()) is not None
                and parse_version(pd.__version__) < parse_version("1.4.0")
            ):
                key_token = generate_unique_token(
                    n_bytes=8, columns=[*self.columns, *other.columns]
                )

                return self._from_dataframe(
                    self._dataframe.assign(**{key_token: 0}).merge(
                        other._dataframe.assign(**{key_token: 0}),
                        how="inner",
                        left_on=key_token,
                        right_on=key_token,
                        suffixes=("", "_right"),
                    ),
                ).drop(key_token)
            else:
                return self._from_dataframe(
                    self._dataframe.merge(
                        other._dataframe,
                        how="cross",
                        suffixes=("", "_right"),
                    ),
                )

        if how == "anti":
            indicator_token = generate_unique_token(
                n_bytes=8, columns=[*self.columns, *other.columns]
            )

            other = (
                other._dataframe.loc[:, right_on]
                .rename(  # rename to avoid creating extra columns in join
                    columns=dict(zip(right_on, left_on))  # type: ignore[arg-type]
                )
                .drop_duplicates()
            )
            return self._from_dataframe(
                self._dataframe.merge(
                    other,
                    how="outer",
                    indicator=indicator_token,
                    left_on=left_on,
                    right_on=left_on,
                )
                .loc[lambda t: t[indicator_token] == "left_only"]
                .drop(columns=[indicator_token])
                .reset_index(drop=True)
            )

        return self._from_dataframe(
            self._dataframe.merge(
                other._dataframe,
                left_on=left_on,
                right_on=right_on,
                how=how,
                suffixes=("", "_right"),
            ),
        )

    # --- partial reduction ---

    def head(self, n: int) -> Self:
        return self._from_dataframe(self._dataframe.head(n))

    def tail(self, n: int) -> Self:
        return self._from_dataframe(self._dataframe.tail(n))

    def unique(self, subset: str | list[str]) -> Self:
        subset = flatten(subset)
        return self._from_dataframe(self._dataframe.drop_duplicates(subset=subset))

    # --- lazy-only ---
    def lazy(self) -> Self:
        return self

    @property
    def shape(self) -> tuple[int, int]:
        return self._dataframe.shape  # type: ignore[no-any-return]

    def to_dict(self, *, as_series: bool = False) -> dict[str, Any]:
        if as_series:
            # todo: should this return narwhals series?
            return {col: self._dataframe.loc[:, col] for col in self.columns}
        return self._dataframe.to_dict(orient="list")  # type: ignore[no-any-return]

    def to_numpy(self) -> Any:
        from narwhals._pandas_like.series import PANDAS_TO_NUMPY_DTYPE_MISSING

        # pandas return `object` dtype for nullable dtypes, so we cast each
        # Series to numpy and let numpy find a common dtype.
        # If there aren't any dtypes where `to_numpy()` is "broken" (i.e. it
        # returns Object) then we just call `to_numpy()` on the DataFrame.
        for dtype in self._dataframe.dtypes:
            if str(dtype) in PANDAS_TO_NUMPY_DTYPE_MISSING:
                import numpy as np

                return np.hstack([self[col].to_numpy()[:, None] for col in self.columns])
        return self._dataframe.to_numpy()

    def to_pandas(self) -> Any:
        if self._implementation == "pandas":
            return self._dataframe
        if self._implementation == "modin":  # pragma: no cover
            return self._dataframe._to_pandas()
        return self._dataframe.to_pandas()  # pragma: no cover

    def write_parquet(self, file: Any) -> Any:
        self._dataframe.to_parquet(file)

    # --- descriptive ---
    def is_duplicated(self: Self) -> PandasSeries:
        from narwhals._pandas_like.series import PandasSeries

        return PandasSeries(
            self._dataframe.duplicated(keep=False),
            implementation=self._implementation,
        )

    def is_empty(self: Self) -> bool:
        return self._dataframe.empty  # type: ignore[no-any-return]

    def is_unique(self: Self) -> PandasSeries:
        from narwhals._pandas_like.series import PandasSeries

        return PandasSeries(
            ~self._dataframe.duplicated(keep=False),
            implementation=self._implementation,
        )

    def null_count(self: Self) -> PandasDataFrame:
        return PandasDataFrame(
            self._dataframe.isnull().sum(axis=0).to_frame().transpose(),
            implementation=self._implementation,
        )

    def item(self: Self, row: int | None = None, column: int | str | None = None) -> Any:
        if row is None and column is None:
            if self.shape != (1, 1):
                msg = (
                    "can only call `.item()` if the dataframe is of shape (1, 1),"
                    " or if explicit row/col values are provided;"
                    f" frame has shape {self.shape!r}"
                )
                raise ValueError(msg)
            return self._dataframe.iat[0, 0]

        elif row is None or column is None:
            msg = "cannot call `.item()` with only one of `row` or `column`"
            raise ValueError(msg)

        _col = self.columns.index(column) if isinstance(column, str) else column
        return self._dataframe.iat[row, _col]

    def clone(self: Self) -> Self:
        return self._from_dataframe(self._dataframe.copy())
