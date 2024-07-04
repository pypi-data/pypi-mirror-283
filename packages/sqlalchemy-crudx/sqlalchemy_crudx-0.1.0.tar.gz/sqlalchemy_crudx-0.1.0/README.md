# sqlalchemy-crudx

基于 SQLAlChemy2 模型的异步 CRUD 操作

## 下载

```shell
pip install sqlalchemy-crudx
```

## TODO

- [ ] ...

## Use

以下仅为简易示例

```python
from sqlalchemy.orm import declarative_base
from crudx import AsyncCRUD

Base = declarative_base()

class User(Base):
    # your sqlalchemy model
    pass


class CRUDUser(AsyncCRUD[User]):
    # your controller service
    pass


# singleton
user_dao = CRUDUser(User)
```

## 互动

[github](https://github.com/maxisioux)
[gitee](https://gitee.com/codemaxi)

## 赞助

如果此项目能够帮助到你，你可以赞助作者一些咖啡豆表示鼓励：[:coffee: Sponsor :coffee:](https://github.com/maxisioux)
