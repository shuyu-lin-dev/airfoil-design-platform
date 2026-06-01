# Airfoil Design Platform Backend

翼型气动与强度智能设计平台后端 MVP (v0.2.0)。

## 目标

- 翼型 2D 生成（CST 参数 → 200 点轮廓）
- 气动预测（CST + 工况 → 升阻比、Cp 分布、HDF5 场数据）
- 强度预测（翼型 + 结构参数 → 最大应力、重量）
- 三维机翼结构几何（CST + 平面 + 结构 → STEP 装配）
- 气动/结构/耦合优化
- 教学接口（控制点翼型生成、CST 反推）
- Artifact 存储（HDF5 场数据 + STEP 结构几何）

## 快速开始

```bash
cd backend
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,cad]"
```

## 启动开发服务器

```bash
uvicorn airfoil_platform.main:app --reload
```

## 运行测试

```bash
pytest
pytest tests/test_geometry_api.py
```

## 字段单位

| 字段 | 单位 |
|------|------|
| 长度 | m |
| 角度 | degree |
| 压力/应力 | Pa |
| 重量 | N |
| 密度 | kg/m³ |
| 速度 | m/s |
| 比例 | 小数 |

## 架构边界

- `api/` 不写业务逻辑
- `core/` 不依赖具体实现类
- `artifacts/` 不依赖业务层

## Artifact 策略

- 压力场/速度场 → HDF5，不通过 JSON 返回
- 结构几何 → STEP，不返回点云
- 查询 `GET /artifacts/{id}`，下载 `GET /artifacts/{id}/download`
- `runtime_artifacts/` 由 `.gitignore` 忽略
