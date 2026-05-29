# Airfoil Design Platform Backend

翼型气动与强度智能设计平台后端 MVP。

## 目标

构建 FastAPI 后端 MVP，用占位算法打通翼型生成、气动预测、强度预测、优化设计和 artifact 存储的数据流，为后续真实模型、前端可视化和智能体调度打基础。

## 非目标（第一版不做）

- 前端页面、可视化渲染
- 真实神经网络模型、遗传算法
- LangGraph 智能体、DeepSeek API
- 用户登录权限、数据库、对象存储、文件上传

## 快速开始

```bash
cd backend
pip install -e ".[dev]"
# 如需 CAD 功能：
pip install -e ".[dev,cad]"
uvicorn airfoil_platform.main:app --reload
```

## 运行测试

```bash
cd backend && pytest
```

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/geometry/airfoil-2d` | 二维翼型生成（12 CST 参数 → 200 点） |
| POST | `/geometry/wing-3d` | 三维机翼结构 STEP 生成 |
| POST | `/aerodynamics/predict` | 气动预测（升阻比 + Cp 分布 + HDF5 场数据） |
| POST | `/structure/predict` | 强度预测（max_stress + weight） |
| POST | `/optimization/aerodynamic` | 单一气动优化 |
| POST | `/optimization/structural` | 单一强度优化 |
| POST | `/optimization/coupled` | 气动强度耦合优化 |
| POST | `/teaching/airfoil-from-control-points` | 教学翼型生成 |
| POST | `/teaching/cst-from-airfoil` | 教学 CST 参数反推 |
| GET | `/artifacts/{id}` | Artifact 元信息查询 |
| GET | `/artifacts/{id}/download` | Artifact 文件下载 |

## 字段单位

| 字段 | 单位 |
|------|------|
| cst_params | 无量纲（12 个：前 6 上表面，后 6 下表面） |
| mach | 无量纲 |
| angle_of_attack | degree |
| span, chord | m |
| rear_spar_web_thickness, rib_thickness, rib_spacing | m |
| elastic_modulus | Pa |
| material_density | kg/m^3 |
| max_stress | Pa |
| weight | N |
| lift_drag_ratio | 无量纲（二维翼型升阻比） |
| fitness | 1/N（lift_drag_ratio / weight） |

## 目录结构

```
backend/
  src/airfoil_platform/
    main.py              # FastAPI 应用入口
    api/                 # 路由层（只做请求响应）
    contracts/           # Pydantic 数据契约
    core/                # 纯领域逻辑
    services/            # 业务编排
    models/              # 模型适配层（stub）
    optimization/        # 优化算法（stub）
    artifacts/           # HDF5/STEP 存储
    serialization/       # MessagePack/numpy 编解码
    config/              # 默认值和路径配置
    lib/                 # 通用基础工具
  tests/                 # pytest 测试
  runtime_artifacts/     # HDF5/STEP 运行时输出（gitignore）
```

## Artifact 策略

- `artifact_id` = SHA-256(规范化 JSON 输入) 前 12 字符，天然幂等
- HDF5 field data: `runtime_artifacts/aerodynamic/<id>.h5` + `.json` sidecar
- STEP geometry: `runtime_artifacts/geometry/<id>.step` + `.json` sidecar
- 同步写入、异步语义（保留 pending/ready/failed 状态契约）
- 查询：`GET /artifacts/{id}` 读取 sidecar
- 下载：`GET /artifacts/{id}/download` 返回文件

## 坐标系

- x = 弦向
- y = 厚度方向
- z = 展向

## 所有响应均含

- `is_stub: true`
- `model_version: "stub-v0"`
