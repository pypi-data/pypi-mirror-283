#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, ValidationError
from sqlalchemy import Row, RowMapping, asc, desc, func, or_
from sqlalchemy import delete as sa_delete
from sqlalchemy import select as sa_select
from sqlalchemy import update as sa_update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.selectable import Select

from crudx.errors import (
    FilterExpressionError,
    JoinExpressionError,
    ModelColumnError,
    SelectExpressionError,
    SortExpressionError,
)
from crudx.helper import JoinArgs, extract_columns, get_primary_key

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SelectSchemaType = TypeVar("SelectSchemaType", bound=BaseModel)


class AsyncCRUD(Generic[ModelType]):
    """
    Base class for CRUD operations on a model.

    This class provides a set of methods for create, read, update,
    and delete operations on a given SQLAlchemy model,
    utilizing Pydantic schemas for data validation and serialization.

    Args:
        model: The SQLAlchemy model type.
    """

    _SUPPORTED_FILTERS = {
        """
        键(如 "gt", "lt", "gte" 等)代表过滤操作的名称,是比较操作的缩写
        值是一个 lambda 函数, 它接受一个列对象(column)作为参数, 并返回该列的一个比较方法,如:
        `lambda column: column.__gt__`:返回列对象的`__gt__`方法,该方法生成"greater than"比较的查询条件
        `lambda column: column.is_not`:返回列对象的`is_not`方法,用于生成"is not"条件的查询条件
        """
        "gt": lambda column: column.__gt__,
        "lt": lambda column: column.__lt__,
        "gte": lambda column: column.__ge__,
        "lte": lambda column: column.__le__,
        "ne": lambda column: column.__ne__,
        "is": lambda column: column.is_,
        "is_not": lambda column: column.is_not,
        "like": lambda column: column.like,
        "notlike": lambda column: column.notlike,
        "ilike": lambda column: column.ilike,
        "notilike": lambda column: column.notilike,
        "startswith": lambda column: column.startswith,
        "endswith": lambda column: column.endswith,
        "contains": lambda column: column.contains,
        "match": lambda column: column.match,
        "between": lambda column: column.between,
        "in": lambda column: column.in_,
        "not_in": lambda column: column.not_in,
    }

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.pk_name = get_primary_key(model)
        self.pk_column = getattr(model, self.pk_name)
        self.column_names = [col.key for col in model.__table__.columns]

    async def create(
        self, session: AsyncSession, object: CreateSchemaType, **kwargs: Any
    ) -> ModelType:
        """
        Create a new record in the database.

        Args:
            session: The SQLAlchemy async session.
            object: The Pydantic schema containing the data to be saved.
            kwargs: Other data to be save.

        Returns:
            The created database object.
        """
        if kwargs:
            instance = self.model(**object.model_dump(), **kwargs)
        else:
            instance = self.model(**object.model_dump())
        session.add(instance)
        return instance

    async def create_bulk(
        self, session: AsyncSession, objects: Iterable[CreateSchemaType]
    ) -> List[ModelType]:
        """
        Bulk create new record of a model in the database

        Args:
            session: The SQLAlchemy async session.
            objects: The Pydantic schema containing the data list to be saved.

        Returns:
            The created database object.
        """
        instance_list = [self.model(**obj.model_dump()) for obj in objects]
        session.add_all(instance_list)
        return instance_list


    async def build_select_statement(
        self,
        select_schema: Optional[SelectSchemaType] = None,
        sort_columns: Optional[Union[str, List[str]]] = None,
        sort_orders: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ) -> Select:
        """
        Constructs a SQL Alchemy `Select` statement with optional column selection,
        filtering, and sorting.

        Args:
            select_schema: Pydantic schema to determine which columns to include
                in the selection. If not provided, selects all columns of the model.
            sort_columns: A single column name or list of column names to sort the query results by.
                Must be used in conjunction with sort_orders.
            sort_orders: A single sort order ('asc' or 'desc') or a list of sort orders,
                corresponding to each column in sort_columns. If not specified,
                defaults to ascending order for all sort_columns.

        Returns:
            Selectable: An SQL Alchemy `Select` statement object
                that can be executed or further modified.

        Examples:
            Selecting specific columns with filtering and sorting:
            ```python
            stmt = await crud.build_select_statement(
                select_schema=UserReadSchema,
                sort_columns=["age", "username"],
                sort_orders=["asc", "desc"],
                age__gt=18,
            )
            ```

            Creating a statement to select all users without any filters:
            ```python
            stmt = await crud.build_select_statement()
            ```

            Selecting users with a specific role, ordered by name:
            ```python
            stmt = await crud.build_select_statement(
                select_schema=UserReadSchema,
                sort_columns="name",
                role="admin"
            )
            ```
        Note:
            This method does not execute the generated SQL statement.
            Use `session.execute(stmt)` to run the query and fetch results.
        """

        filters = self._parse_filters(self.model, **kwargs)
        if select_schema:
            to_select = extract_columns(self.model, select_schema)
            stmt = sa_select(*to_select).filter(*filters) # select columns
        else:
            stmt = sa_select(self.model).filter(*filters) # select model

        if sort_columns:
            stmt = self._apply_sorting(stmt, sort_columns, sort_orders)
        return stmt


    async def get_one(
        self,
        session: AsyncSession,
        select_schema: Optional[SelectSchemaType] = None,
        **kwargs: Any,
    ) -> Optional[Union[ModelType, SelectSchemaType]]:
        """
        Fetches a single record based on specified filters.
        This method allows for advanced filtering through comparison operators,
        enabling queries to be refined beyond simple equality checks.

        Args:
            session: The database session to use for the operation.
            select_schema: Optional Pydantic schema for selecting specific columns.
            **kwargs: Filters to apply to the query, using field names for direct matches
                or appending comparison operators for advanced queries.

        Returns:
            A sqlalchemy model or a Pydantic model instance of the fetched database row,
            or None if no match is found.

        Examples:
            Fetch a user by ID:
            ```python
            user = await crud.get_one(session, id=1)
            ```

            Fetch a user with an age greater than 30:
            ```python
            user = await crud.get_one(session, age__gt=30)
            ```

            Fetch a user with a registration date before Jan 1, 2020:
            ```python
            user = await crud.get_one(session, registration_date__lt=datetime(2020, 1, 1))
            ```

            Fetch a user not equal to a specific username:
            ```python
            user = await crud.get_one(session, username__ne='admin')
            ```
        """
        stmt = await self.build_select_statement(select_schema, **kwargs)
        query = await session.execute(stmt)
        if select_schema is None:
            return query.scalars().first()

        first_row = query.first()
        if first_row is None:
            return None

        dict_row = dict(first_row._mapping)
        return select_schema(**dict_row)


    async def get_list(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: Optional[int] = 20,
        select_schema: Optional[SelectSchemaType] = None,
        sort_columns: Optional[Union[str, List[str]]] = None,
        sort_orders: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> Optional[Sequence[Union[ModelType, SelectSchemaType]]]:
        """
        Fetches multiple records based on filters, supporting sorting, pagination.

        Args:
            session: The database session to use for the operation.
            select_schema: Optional Pydantic schema for selecting specific columns.
            offset: The offset (number of records to skip) for pagination.
            limit: Maximum number of records to fetch in one call.
                Use `None` for "no limit", fetching all matching rows.
            sort_columns: A single column name or a list of column names on which to apply sorting.
            sort_orders: A single sort order ('asc' or 'desc') or a list of sort orders
                corresponding to the columns in sort_columns. If not provided, defaults to 'asc' for each column.
            **kwargs: Filters to apply to the primary query,
                including advanced comparison operators for refined searching.

        Returns:
            A list containing sqlalchemy model or a Pydantic model instances
            of fetched records matching the filters.

        Raises:
            FilterExpressionError: If limit or offset is negative.

        Examples:
            Fetch the first 10 users:
            ```python
            users = await crud.get_list(db, 0, 10)
            ```

            Fetch next 10 users with sorted by username:
            ```python
            users = await crud.get_list(db, 10, 10, sort_columns="username", sort_orders="desc")
            ```

            Fetch 10 users older than 30, sorted by age in descending order:
            ```python
            users = await crud.get_list(
                db, offset=0, limit=10, sort_columns="age", sort_orders="desc", age__gt=30
            )
            ```

            Fetch 10 users with a registration date before Jan 1, 2020:
            ```python
            users = await crud.get_list(
                db, offset=0, limit=10, registration_date__lt=datetime(2020, 1, 1)
            )
            ```

            Fetch 10 users with a username other than 'admin',
            returning as model instances (ensure appropriate schema is passed):
            ```python
            users = await crud.get_list(
                db,
                offset=0,
                limit=10,
                select_schema=UserSchema,
                username__ne="admin",
            )
            ```

            Fetch users with filtering and multiple column sorting:
            ```python
            users = await crud.get_list(
                db,
                offset=0,
                limit=10,
                sort_columns=["username", "email"],
                sort_orders=["asc", "desc"],
                is_active=True,
            )
            ```
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise FilterExpressionError("Limit and offset must be non-negative.")

        stmt = await self.build_select_statement(
            select_schema=select_schema,
            sort_columns=sort_columns,
            sort_orders=sort_orders,
            **kwargs,
        )

        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        if not select_schema:
            return result.scalars().all()

        data = [dict(row) for row in result.mappings()]
        return [select_schema(**row) for row in data]


    async def get_joined(
        self,
        session: AsyncSession,
        joins: List[JoinArgs],
        select_schema: Optional[SelectSchemaType] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches a single record with one or multiple joins on other models.
        If 'joins' is not provided, the method attempts to automatically
        detect the join condition using foreign key relationships.
        For multiple joins, use 'joins' to specify each join configuration.

        Args:
            session: The database session to use for the operation.
            joins: A list of JoinArgs instances, each specifying a model to join with,
                join condition, optional prefix for column names, schema for selecting specific
                columns, and the type of join. This parameter enables support for multiple joins.
            select_schema: Pydantic schema for selecting specific columns from the primary model.
            **kwargs: Filters to apply to the query, using field names for direct matches
                or appending comparison operators for advanced queries.

        Returns:
            A dictionary representing the joined record, or None if no record matches the criteria.

        Examples:
            Fetching a single user and its associated department where user name is "user-dev":
            ```python
            crud = AsyncCRUD(User)
            joins: JoinArgs = [
                JoinArgs(
                    model=Dept,
                    join_on=Dept.id == User.dept_id,
                    join_type="left",
                    join_prefix="join_dept_"
                ),
            ]
            result = await crud.get_joined(session, joins, name="user-dev")
            ```
        """
        primary_select = extract_columns(self.model, select_schema)
        stmt: Select = sa_select(*primary_select).select_from(self.model)
        stmt = self._apply_joins(stmt, joins=joins)
        primary_filters = self._parse_filters(self.model, **kwargs)
        if primary_filters:
            stmt = stmt.filter(*primary_filters)
        query = await session.execute(stmt)
        result = query.first()
        return dict(result._mapping) if result is not None else None


    async def get_list_joined(
        self,
        session: AsyncSession,
        joins: List[JoinArgs],
        offset: int = 0,
        limit: Optional[int] = 20,
        select_schema: Optional[SelectSchemaType] = None,
        sort_columns: Optional[Union[str, List[str]]] = None,
        sort_orders: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch multiple records with a join on another model,
        allowing for pagination, optional sorting, and model conversion.

        Args:
            session: The database session to use for the operation.
            joins: A list of JoinArgs instances, each specifying a model to join with,
                join condition, optional prefix for column names, schema for selecting specific
                columns, and the type of join. This parameter enables support for multiple joins.
            offset: The offset (number of records to skip) for pagination.
            limit: Maximum number of records to fetch in one call.
                Use `None` for "no limit", fetching all matching rows.
            select_schema: Pydantic schema for selecting specific columns from the primary model.
            sort_columns: A single column name or a list of column names on which to apply sorting.
            sort_orders: A single sort order ('asc' or 'desc') or a list of sort orders
                corresponding to the columns in sort_columns. If not provided, defaults to 'asc' for each column.
            **kwargs: Filters to apply to the primary query,
                including advanced comparison operators for refined searching.

        Raises:
            FilterExpressionError: If limit or offset is negative.

        Returns:
            A list of dictionary containing the fetched rows.

        Examples:
            Fetching all the users and its associated department:
            ```python
            crud = AsyncCRUD(User)
            joins: JoinArgs = [
                JoinArgs(
                    model=Dept,
                    join_on=Dept.id == User.dept_id,
                    join_type="left",
                    join_prefix="join_dept_"
                ),
            ]
            result = await crud.get_list_joined(session, joins)
            ```
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise FilterExpressionError("Limit and offset must be non-negative.")

        primary_select = extract_columns(self.model, select_schema)
        stmt: Select = sa_select(*primary_select)
        stmt = self._apply_joins(stmt=stmt, joins=joins)
        primary_filters = self._parse_filters(self.model, **kwargs)
        if primary_filters:
            stmt = stmt.filter(*primary_filters)
        if sort_columns:
            stmt = self._apply_sorting(stmt, sort_columns, sort_orders)
        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        query = await session.execute(stmt)

        results: list[Dict[str, Any]] = []
        for row in query.mappings().all():
            row_dict = dict(row)
            results.append(row_dict)
        return results

    async def update(
        self,
        session: AsyncSession,
        object: Union[UpdateSchemaType, Dict[str, Any]],
        **kwargs
    ) -> int:
        """
        Updates an existing record or multiple records in the database based on specified filters.
        This method allows for precise targeting of records to update.

        Args:
            session: The database session to use for the operation.
            object: A Pydantic schema or dictionary containing the update data.
            **kwargs: Filters to identify the record(s) to update, 
                supporting advanced comparison operators for refined querying.

        Returns:
            row count to be updated.

        Examples:
            Update a user's email based on their ID:
            ```python
            update(session, {'email': 'new_email@example.com'}, id=1)
            ```

            Update users's status to 'inactive' where age is greater than 30:
            ```python
            update(session, {'status': 'inactive'}, age__gt=30)
            ```

            Update a user's username excluding specific user ID:
            ```python
            update(session, {'username': 'new_username'}, id__ne=1)
            ```
        """
        instance_data = (
            object if isinstance(object, dict) else object.model_dump(exclude_unset=True)
        )

        filters = self._parse_filters(self.model, **kwargs)
        update_stmt = sa_update(self.model).filter(*filters).values(instance_data)
        result = await session.execute(update_stmt)
        return result.rowcount  # type: ignore


    async def delete(self, session: AsyncSession, **kwargs) -> int:
        """
        Deletes a record or multiple records from the database based on specified filters.

        Args:
            session: The database session to use for the operation.
            **kwargs: Filters to identify the record(s) to delete,
                including advanced comparison operators for detailed querying.

        Returns:
            row count to be deleted.

        Raises:
            NoResultFound: If no record matches the filters.

        Examples:
            Delete the users based on their ID:
            ```python
            delete(session, id=1)
            ```

            Delete users older than 30 years:
            ```python
            delete(session, age__gt=30)
            ```

            Delete a user with a specific username:
            ```python
            delete(session, username='unique_username')
            ```
        """
        total_count = await self.count(session, **kwargs)
        if total_count == 0:
            raise NoResultFound("No record found to delete.")

        filters = self._parse_filters(self.model, **kwargs)
        delete_stmt = sa_delete(self.model).filter(*filters)
        result = await session.execute(delete_stmt)
        return result.rowcount  # type: ignore


    async def exists(self, session: AsyncSession, **kwargs: Any) -> bool:
        """
        Checks if any records exist that match the given filter conditions.

        Args:
            session: The database session to use for the operation.
            **kwargs: Filters to apply to the query, supporting both direct matches
                and advanced comparison operators for refined search criteria.

        Returns:
            True if at least one record matches the filter conditions, False otherwise.

        Examples:
            Fetch a user by ID exists:
            ```python
            exists = await crud.exists(session, id=1)
            ```

            Check if any user is older than 30:
            ```python
            exists = await crud.exists(session, age__gt=30)
            ```

            Check if any user registered before Jan 1, 2020:
            ```python
            exists = await crud.exists(session, registration_date__lt=datetime(2020, 1, 1))
            ```

            Check if a username other than 'admin' exists:
            ```python
            exists = await crud.exists(session, username__ne="admin")
            ```
        """
        filters = self._parse_filters(self.model, **kwargs)
        stmt = sa_select(self.model).filter(*filters).limit(1)

        result = await session.execute(stmt)
        return result.first() is not None

    async def count(
        self, session: AsyncSession, joins: Optional[List[JoinArgs]] = None, **kwargs: Any
    ) -> int:
        """
        Counts records that match specified filters.

        Args:
            session: The database session to use for the operation.
            joins: Optional configuration for applying joins in the count query.
            **kwargs: Filters to apply for the count, including field names for equality checks
                or with comparison operators for advanced queries.

        Returns:
            The total number of records matching the filter conditions.

        Examples:
            Count users by ID:
            ```python
            count = await crud.count(session, id=1)
            ```

            Count users older than 30:
            ```python
            count = await crud.count(session, age__gt=30)
            ```

            Count users with a username other than 'admin':
            ```python
            count = await crud.count(session, username__ne="admin")
            ```

            Count projects with at least one participant (many-to-many relationship):
            ```python
            joins = [
                JoinArgs(
                    model=ProjectsParticipantsAssociation,
                    join_on=Project.id == ProjectsParticipantsAssociation.project_id,
                    join_type="inner"
                ),
                JoinArgs(
                    model=Participant,
                    join_on=ProjectsParticipantsAssociation.participant_id == Participant.id,
                    join_type="inner"
                )
            ]
            count = await crud.count(session, joins=joins)
        """
        primary_filters = self._parse_filters(self.model, **kwargs)

        if joins is not None:
            joins_query = sa_select(self.pk_column)
            for join in joins:
                if join.join_type == "inner":
                    joins_query = joins_query.join(join.model, join.join_on)
                else: # left
                    joins_query = joins_query.outerjoin(join.model, join.join_on)

                if join.filters:
                    join_filters = self._parse_filters(join.model, **join.filters)
                    joins_query = joins_query.where(*join_filters)

            if primary_filters:
                joins_query = joins_query.where(*primary_filters)

            subquery = joins_query.subquery()
            count_query = sa_select(func.count()).select_from(subquery)
        else:
            count_query = sa_select(func.count()).select_from(self.model)
            if primary_filters:
                count_query = count_query.where(*primary_filters)

        total_count: Optional[int] = await session.scalar(count_query)
        if total_count is None:
            raise SelectExpressionError("Could not find the count.")

        return total_count

    def _get_sqlalchemy_filter(
        self, operator: str, value: Any
    ) -> Optional[Callable[[str], Callable]]:
        if operator in {"in", "not_in", "between"} and not isinstance(value, (tuple, list, set)):
                raise FilterExpressionError(f"<{operator}> filter must be tuple, list or set")
        return self._SUPPORTED_FILTERS.get(operator)  # return None if not found

    def _parse_filters(
        self, model: Optional[type[ModelType]] = None, **kwargs
    ) -> List[ColumnElement]:
        """
        :param kwargs: filters params

        :examples:
            _parse_filters(id__in=[1, 2])
            _parse_filters(id__not_in=[1, 2])
            _parse_filters(age__gt=18)
            _parse_filters(name__ne='James')
            _parse_filters(id__between=1)
            _parse_filters(id__in=1)
            _parse_filters(id__or={"gt": 1, "lt": 5})
            _parse_filters(date__lt=datetime(2020, 1, 1))

        """
        model = model or self.model
        filters = []

        for key, value in kwargs.items():
            if "__" in key:
                field_name, op = key.rsplit("__", 1)  # 从结尾位置开始切一次
                column = getattr(model, field_name, None)
                if column is None:
                    raise ModelColumnError(f"Invalid filter column: {field_name}")

                if op == "or":
                    or_filters = []
                    for or_key, or_value in value.items():
                        sqlalchemy_filter = self._get_sqlalchemy_filter(or_key, value)
                        if sqlalchemy_filter:
                            or_filters.append(sqlalchemy_filter(column)(or_value))

                    filters.append(or_(*or_filters))
                else:
                    sqlalchemy_filter = self._get_sqlalchemy_filter(op, value)
                    if sqlalchemy_filter:
                        filters.append(sqlalchemy_filter(column)(value))
            else:
                column = getattr(model, key, None)
                if column is not None:
                    filters.append(column == value)

        return filters

    def _apply_sorting(  # noqa: C901
        self,
        stmt: Select,
        sort_columns: Union[str, List[str]],
        sort_orders: Optional[Union[str, List[str]]] = None,
    ) -> Select:
        """
        Apply sorting to a SQLAlchemy query based on specified column names and sort orders.

        Args:
            stmt: The SQLAlchemy Select statement to which sorting will be applied.
            sort_columns: A single column name or a list of column names on which to apply sorting.
            sort_orders: A single sort order ('asc' or 'desc') or a list of sort orders corresponding
                to the columns in sort_columns. If not provided, defaults to 'asc' for each column.

        Raises:
            SortExpressionError: Raised if sort orders are provided without corresponding sort columns,
                or if an invalid sort order is provided (not 'asc' or 'desc').
            ModelColumnError: Raised if an invalid column name is provided that does not exist in the model.

        Returns:
            The modified Select statement with sorting applied.

        Examples:
            Applying ascending sort on a single column:
            >>> stmt = _apply_sorting(stmt, "name")

            Applying descending sort on a single column:
            >>> stmt = _apply_sorting(stmt, "age", "desc")

            Applying mixed sort orders on multiple columns:
            >>> stmt = _apply_sorting(stmt, ["name", "age"], ["asc", "desc"])

            Applying ascending sort on multiple columns:
            >>> stmt = _apply_sorting(stmt, ["name", "age"])

        Note:
            This method modifies the passed Select statement in-place by applying the order_by clause
            based on the provided column names and sort orders.
        """
        if sort_orders and not sort_columns:
            raise SortExpressionError("Sort orders provided without corresponding sort columns.")

        if sort_columns is None:
            return stmt

        if not isinstance(sort_columns, list):
            sort_columns = [sort_columns]

        if sort_orders:
            if not isinstance(sort_orders, list):
                sort_orders = [sort_orders] * len(sort_columns)
            if len(sort_columns) != len(sort_orders):
                raise SortExpressionError(
                    "The length of sort_columns and sort_orders must match."
                )

            for _, order in enumerate(sort_orders):
                if order not in ["asc", "desc"]:
                    raise SortExpressionError(
                        f"Invalid sort order: {order}. Only 'asc' or 'desc' are allowed."
                    )

        # 默认是 'asc'
        validated_sort_orders = sort_orders if sort_orders else ["asc"] * len(sort_columns)

        for idx, column_name in enumerate(sort_columns):
            column = getattr(self.model, column_name, None)
            if column is None:
                raise ModelColumnError(f"Invalid sort column name: {column_name}")

            order = validated_sort_orders[idx]
            stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

        return stmt

    def _apply_joins(
        self,
        stmt: Select,
        joins: List[JoinArgs],
    ):
        """
        Applies joins to the given SQL statement based on a list of JoinArgs objects.

        Args:
            stmt: The initial SQL statement.
            joins: Configurations for all joins.

        Returns:
            Select: The modified SQL statement with joins applied.
        """
        for join in joins:
            join_select = extract_columns(join.model, join.select_columns, join.join_prefix)
            joined_filters = self._parse_filters(model=join.model, **(join.filters or {}))

            if join.join_type == "left":
                stmt = stmt.outerjoin(join.model, join.join_on).add_columns(*join_select)
            elif join.join_type == "inner":
                stmt = stmt.join(join.model, join.join_on).add_columns(*join_select)
            else:  # pragma: no cover
                raise ValueError(f"Unsupported join type: {join.join_type}.")
            if joined_filters:
                stmt = stmt.filter(*joined_filters)

        return stmt
