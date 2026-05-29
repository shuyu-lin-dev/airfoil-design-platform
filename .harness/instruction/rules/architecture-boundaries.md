# 架构边界规则

本文定义后端 MVP 的目录职责和依赖边界。

## 目标目录

```text
backend/
  README.md
  pyproject.toml
  tests/
  runtime_artifacts/
  src/
    airfoil_platform/
      main.py
      api/
      contracts/
      core/
      services/
      models/
      optimization/
      artifacts/
      serialization/
      config/
      lib/
```

## 目录职责

- `api/`：FastAPI 路由，只做请求响应、参数转换、错误码映射和调用 service。
- `contracts/`：Pydantic 数据契约，请求模型、响应模型、字段单位和校验。
- `core/`：翼型、气动、强度、优化的纯领域逻辑。
- `services/`：业务工作流编排。
- `models/`：机器学习模型适配层，第一版为 stub。
- `optimization/`：遗传算法、目标函数和停止条件，第一版为 stub。
- `artifacts/`：HDF5 与 STEP artifact 代码。
- `serialization/`：MessagePack / numpy bytes 编解码边界。
- `config/`：默认值和路径配置。
- `lib/`：通用基础工具，只放脱离翼型业务也有意义的代码。

## 依赖方向

推荐依赖方向：

```text
api -> services -> core
api -> contracts
services -> contracts
services -> models / optimization / artifacts
core -> config 或纯输入
lib -> 不依赖业务层
```

约束：

- `contracts` 是 API 数据契约，不是机器学习模型层。
- `models` 是机器学习模型适配层，不是 Pydantic contract。
- `api` 不写业务逻辑。
- `services` 不依赖 FastAPI 路由对象。
- `lib` 不 import `services` 或 `api`。
- 默认机翼平面参数、默认蒙皮材料、默认内部结构材料、重力加速度、artifact 根目录和 stub 模式统一来自 `config/settings.py`。
