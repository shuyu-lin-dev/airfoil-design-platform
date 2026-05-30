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
        aerodynamics/
        structure/
        weights/          (非源码：.pt / .onnx 权重文件)
      optimization/
        algorithms/
      artifacts/
      config/
      lib/
```

## 目录职责

- `api/`：FastAPI 路由，只做请求响应、参数转换、错误码映射和调用 service。
- `contracts/`：Pydantic 数据契约，请求模型、响应模型、字段单位和校验。
- `core/`：翼型、气动、强度、优化的纯领域编排逻辑，只依赖 `models/` 和 `optimization/` 的抽象接口，不感知具体实现。
- `services/`：业务工作流编排。
- `models/`：预测模型适配层——抽象接口（`base.py`）+ 工厂注册（`factory.py`）+ 可替换实现（`aerodynamics/`、`structure/`）。权重文件放在 `models/weights/`（非 Python 源码）。
- `optimization/`：优化算法适配层——抽象接口（`base.py`）+ 工厂注册（`factory.py`）+ 可替换算法（`algorithms/`）。
- `artifacts/`：HDF5 与 STEP artifact 代码。
- `config/`：默认值和路径配置。
- `lib/`：通用基础工具，只放脱离翼型业务也有意义的代码。

## 依赖方向

推荐依赖方向：

```text
api -> services -> core
api -> contracts
services -> contracts
services -> models / optimization / artifacts
core -> models (抽象接口) / optimization (抽象接口) / config
lib -> 不依赖业务层
```

约束：

- `contracts` 是 API 数据契约，不是机器学习模型层。
- `models` 是预测模型适配层，包含抽象接口和可替换实现，不是 Pydantic contract。
- `api` 不写业务逻辑。
- `services` 不依赖 FastAPI 路由对象。
- `lib` 不 import `services` 或 `api`。
- `core/` 只 import `models/` 和 `optimization/` 的抽象接口（`base.py`），不直接依赖具体实现类。具体实现通过工厂注册后按配置创建。
- 默认机翼平面参数、默认蒙皮材料、默认内部结构材料、重力加速度、artifact 根目录和 stub 模式统一来自 `config/settings.py`。
