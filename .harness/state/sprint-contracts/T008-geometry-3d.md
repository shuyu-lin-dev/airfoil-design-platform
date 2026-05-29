# 冲刺合同：T008 Geometry 3D API

## 范围

- 扩展 `api/geometry.py` 添加 `POST /geometry/wing-3d` 路由。
- 扩展 `core/geometry.py` 实现 CadQuery 三维机翼结构 STEP 生成。
- 扩展 `services/geometry_service.py` 编排三维生成 + artifact 存储。
- 扩展 `tests/test_geometry_api.py` 添加 wing-3d 测试。
- 坐标系统：x=弦向, y=厚度方向, z=展向。
- 矩形直半翼假设：右半翼，z∈[0, span/2]，恒定弦长。

## 验证标准

- POST /geometry/wing-3d 接收 CST参数 + wing_planform + structure_design。
- 返回 geometry_artifact (format=step, role=structural_step)。
- STEP 文件和 JSON sidecar 存在。
- STEP 可被 CadQuery 回读，组件非空。
- 外包盒符合 chord 和 span/2，翼肋数量符合 rib_spacing 推导规则。
- 不返回 1000 个三维点云。

## 排除项

- 不实现前端或可视化。
- 不连接真实数据库。
- 不生成气动外形 STEP artifact。

## 观测信号

- 日志：第一版不要求结构化日志。
- 任务轨迹：`tasks/tasks.yaml` T008.evidence 和 PROGRESS.md 的最近验证。

## 失败反馈格式

- WHAT：哪条命令或测试失败。
- WHY：从错误消息判断的直接原因。
- FIX：下一步应修改的文件或配置。
